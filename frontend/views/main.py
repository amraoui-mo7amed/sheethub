from .generic import *

def index(request):
    """
    Render the index page.
    """

    return render(request, 'frontend/index.html')