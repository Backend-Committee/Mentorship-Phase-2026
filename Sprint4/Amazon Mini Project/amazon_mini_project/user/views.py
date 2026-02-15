from django.http import HttpResponse


def test(request):
    context = {
        "title": "About Page",
        "description": "This is a simple Django view example.",
    }
    return HttpResponse("This is users page!")
