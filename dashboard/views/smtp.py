from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import SMTPConfig
from dashboard.decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email, ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from dashboard.utils import test_smtp_connection
from dashboard.views.generic import BaseDelete
from mailjet import MailJet
from django.contrib.auth import get_user_model

UserModel = get_user_model()

mailjet = MailJet()

@login_required
@admin_required
@csrf_exempt
@require_http_methods(['POST'])
def update_smtp_config(request):
    if request.method == "POST":
        errors = []
        # Required fields
        host = request.POST.get('host', '').strip()
        port = request.POST.get('port', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        from_email = request.POST.get('email', '').strip()
        use_tls = request.POST.get('use_tls', 'false').lower() == 'true'
        
        # Validate host
        if not host:
            errors.append(_('SMTP host is required'))
        elif len(host) > 255:
            errors.append(_('SMTP host is too long (max 255 characters)'))
        
        # Validate port
        try:
            port = int(port) if port else None
            if port is None:
                errors.append(_('Port is required'))
            elif not (1 <= port <= 65535):
                errors.append(_('Port must be between 1 and 65535'))
        except ValueError:
            errors.append(_('Port must be a valid number'))
        
        # Validate username
        if not username:
            errors.append(_('Username is required'))
        elif len(username) > 255:
            errors.append(_('Username is too long (max 255 characters)'))
        
        # Validate password
        if not password:
            errors.append(_('Password is required'))
        
        # Validate email
        if not from_email:
            errors.append(_('Email is required'))
        else:
            try:
                validate_email(from_email)
            except ValidationError:
                errors.append(_('Enter a valid email address'))
        
        # If there are validation errors, return them
        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)
        
        try:
            # Create new SMTP configuration
            smtp_config = SMTPConfig.objects.create(
                host=host,
                port=port,
                username=username,
                password=password,
                from_email=from_email,
                use_tls=use_tls,
                is_active=True  # Auto-activate new configurations
            )
                
            return JsonResponse({
                'success': True,
                'message': _('SMTP configuration created successfully'),
                'redirect_url': reverse_lazy('dash:smtp_config')  
            }, status=201)  # 201 Created status code
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': [str(e)]
            }, status=500)

@login_required
@admin_required
@require_http_methods(["POST"])
def test_connection(request):
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(
            {'success': False, 'error': 'Invalid request'}, 
            status=400
        )
    
    try:
        host = request.POST.get('host', '').strip()
        port_str = request.POST.get('port', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        use_tls = request.POST.get('use_tls', 'false').lower() == 'true'
        print(host, port_str, username, password, use_tls)

        success, error = test_smtp_connection(host, int(port_str), username, password, use_tls)
        
        if success:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': str(error) if error else 'Connection failed'}, status=400)
            
    except Exception as e:
        import traceback
        print(f"Error testing SMTP connection: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse(
            {'success': False, 'error': 'An unexpected error occurred'}, 
            status=500
        )

@login_required
@admin_required
def SMTPConfigDetails(request):
    try:
        smtp_servers = SMTPConfig.objects.all().order_by('-id')
    except SMTPConfig.DoesNotExist:
        smtp_servers = None
    context = {
        'smtp_servers': smtp_servers 
    }

    return render(request, 'smtp/config.html', context=context)




@admin_required
def Delete(request, pk):
    return BaseDelete(request,SMTPConfig,pk)



@require_POST
@admin_required
def send_mail(request):
    """
    send_to_all = False  ->  send to the single e-mail in the modal
    send_to_all = True   ->  send to every Contact e-mail
    Returns JSON: {success: bool, errors: list[str]}
    """
    subject      = request.POST.get('subject', '').strip()
    message      = request.POST.get('message', '').strip()
    send_to_all  = request.POST.get('send_to_all') == 'on'   # checkbox

    errors = []
    if not subject:
        errors.append(_('Subject is required.'))
    if not message:
        errors.append(_('Message body is required.'))
    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # decide recipient list
    if send_to_all:
        recipients = list(UserModel.objects.values_list('email', flat=True).distinct())
        if not recipients:
            return JsonResponse({'success': False, 'errors': [_("No contacts to send to.")]}, status=400)
    else:
        to = request.POST.get('to', '').strip()
        if not to:
            return JsonResponse({'success': False, 'errors': ['Recipient e-mail is missing.']}, status=400)
        recipients = [to]

    # bulk send – collect failures
    failed = []

    for email in recipients:
        ok, info = mailjet.sendMessage(
            templateID=7151620,               # plain-text fallback
            subject=subject,
            recipiant_email=email,
            recipiant_name=email,       # fallback
            variabels={'text': message},
            type='noreply'
        )
        if not ok:
            failed.append(f'{email}: {info}')

    if failed:
        return JsonResponse({'success': False, 'errors': failed}, status=400)
    return JsonResponse({'success': True, 'message': _('Email sent successfully')})