from django.shortcuts import render


def home(request):
    return render(request, "pages/index.html")


def impressum(request):
    return render(request, "pages/impressum.html")


def datenschutz(request):
    return render(request, "pages/datenschutz.html")
