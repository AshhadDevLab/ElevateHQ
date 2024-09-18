from django.http import HttpResponse
from django.shortcuts import render
import pathlib
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from visits.models import PageVisit

LOGIN = settings.LOGIN_URL

this_dir = pathlib.Path(__file__).resolve().parent

def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.first_name)
    return about_view(request, *args, **kwargs)

def about_view(request, *args, **kwargs):
    qs = PageVisit.objects.all()
    page_qs = PageVisit.objects.filter(path= request.path)
    try:
        percent = (page_qs.count() * 100.0) / qs.count()
    except:
        percent = 0
    my_title = "My Page"
    html_template = "home.html"
    my_context =  {
        "page_title": my_title,
        "page_visit_count": page_qs.count(),
        "percent": percent,
        "total_visit_count": qs.count(),
    }
    PageVisit.objects.create(path=request.path)
    return render(request, html_template, my_context)

VALID_CODE = "abc123"

def pw_protected_view(request, *args, **kwargs):
    is_allowed = False
    if request.method == "POST":
        user_pw_sent = request.session["protected_page_allowed"]
        if user_pw_sent == VALID_CODE:
            is_allowed = True
            request.session["protected_page_allowed"] = is_allowed
            
    if is_allowed:
        return render(request, "protected/view.html", {})
    return render(request, "protected/entry.html", {})

@login_required(login_url=LOGIN)
def user_only_view(request, *args, **kwargs):
    return render(request, "protected/yser-only.html", {})

@staff_member_required(login_url=LOGIN)
def staff_only_view(request, *args, **kwargs):
    return render(request, "protected/user-only.html", {})