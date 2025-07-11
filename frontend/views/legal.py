from .generic import *

def terms(request):
    """
    Render the terms and conditions page.
    """
    return render(request, 'frontend/terms.html')
