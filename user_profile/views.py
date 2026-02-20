from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserEditForm


# Create your views here.


def index(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated.')
            return redirect(reverse('user_profile:index'))
        else:
            return render(request, 'user_profile/index.html', { "form": form })

    form = UserEditForm()

    if request.user and request.user.is_authenticated:
        form = UserEditForm(instance=request.user)

    context = {
        "form": form
    }
    return render(request, 'user_profile/index.html', context)
