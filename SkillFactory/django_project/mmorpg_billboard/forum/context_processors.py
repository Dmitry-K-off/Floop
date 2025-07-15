"""
Context processor function to provide a list of all categories to templates.
"""

from.models import Category

def categories(request):
    return {
        'categories': Category.objects.all()
    }
