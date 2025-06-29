from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import SMTPConfig
from dashboard.decorators import admin_required
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email, ValidationError
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from dashboard.utils import test_smtp_connection
from dashboard.views.generic import BaseDelete

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
@csrf_exempt
def test_connection(request):
    if request.method == 'POST':
        host = request.POST.get('host', '').strip()
        port = int(request.POST.get('port', '').strip())
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        use_tls = request.POST.get('use_tls', 'false').lower() == 'true'
        print(host, port, username, password, use_tls)

        success, error = test_smtp_connection(host, port, username, password, use_tls)
        
        if success:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': error}, status=400)

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
