from .generic import *
from dashboard.models import Feedback
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from dashboard.decorators import role_required
from django.utils.translation import gettext as _


@login_required
@role_required('admin')
def feedback_list(request):
    """
    View to list all feedback entries.
    """
    feedbacks = Feedback.objects.all().order_by('-created_at')

    return render(request, 'feedback/list.html', {'feedbacks': feedbacks})

@login_required
@role_required('seller')
def create(request):
    """
    View to create a new feedback entry.
    """
    if request.method == 'POST':
        feedbackType = request.POST.get('feedbackType')
        feedbackMessage = request.POST.get('feedbackMessage')

        errors = []
        if not feedbackType:
            errors.append(_('Feedback type is required.'))
        if not feedbackMessage:
            errors.append(_('Feedback message is required.'))

        if feedbackType not in ['bug', 'feature', 'general']:
            errors.append(_('Invalid feedback type.'))

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            feedback = Feedback.objects.create(
                user=request.user,
                type=feedbackType,
                message=feedbackMessage
            )
            feedback.save()
            return JsonResponse({'success': True, 'message': _('Feedback submitted successfully.')})


    else:
        return JsonResponse({'error': [_('Invalid request method. Use POST to submit feedback.')]}, status=405)