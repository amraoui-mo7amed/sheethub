from frontend.models import Contact
from .generic import *
from mailjet import MailJet
from dashboard.models import contactReply
from django.urls import reverse, reverse_lazy
from dashboard.decorators import admin_required
from django.utils.translation import gettext_lazy as _

mailjet = MailJet()

@admin_required
def List(request):
    context = {
        'contacts': Contact.objects.all()
    }
    return render(request, 'contacts/list.html', context=context)

@admin_required
def details(request, pk):
    comtext = {
        'contact' : Contact.objects.get(pk=pk)
    }
    return render(request, 'contacts/details.html', context=comtext)

@admin_required
def Reply(request,contact_pk):
    contact = Contact.objects.get(pk=contact_pk)
    if request.method == 'POST':
        subject = _("Sheethub Support Team")
        message = request.POST.get('message')
        errors = []
    if not subject or not message:
        errors.append(_("All fields are required"))
    
    if errors:
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=400)
    
    try:
        contactReply.objects.create(
            contact = contact,
            message = message,
        )
        success, is_sent = mailjet.sendMessage(
            templateID=7151620,
            subject=subject,
            recipiant_email=contact.email,
            recipiant_name=contact.name,
            variabels={
                'text': message
            },
            type="support"
        )
        print(success)
        return JsonResponse({
            'success': True,
            'message': _('Message sent successfully, please reload the page'),
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
    
    
    