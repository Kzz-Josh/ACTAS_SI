from django.shortcuts import render


def login_page(request):
    return render(request, "login.html")


def dashboard(request):
    # Simple template-based dashboard; API calls are done via fetch on the client.
    return render(request, "dashboard.html")
