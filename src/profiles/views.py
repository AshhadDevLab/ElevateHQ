from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User = get_user_model()

def profile_list_view(request, *args, **kwargs):
    context = {
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request, "profiles/list.html", context)
    

# Create your views here.
@login_required
def profile_view(request,username = None ,*args, **kwargs):
    user = request.user
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = profile_user_obj == user
    return HttpResponse(f"<h1>Hello {username} - {profile_user_obj.id} - {user.id} - {is_me}</h1>")