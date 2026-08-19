from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import Group

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            lib_group, created = Group.objects.get_or_create(name='Site Members')
            user.groups.add(lib_group)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(f"/accounts/login/?next={next_url}")
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})