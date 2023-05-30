from django.shortcuts import render


def index_page(request):
    context = {}
    return render(request, "index.html", context)


def page_not_found_view(request, exception):
    return render(request, 'error404.html', status=404)
