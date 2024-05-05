from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from users.forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, JsonResponse



def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print(request, "Registration successful.")
            return redirect("/swagger/")
        print(request, "Unsuccessful registration. Invalid information.")
        print(form)
    form = NewUserForm()
    return render(request=request, template_name="users/registration.html", context={"register_form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(username)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                print(request, f"You are now logged in as {username}.")
                print(request.GET.get('next'))
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(request.GET.get('next'))
                return HttpResponseRedirect("/swagger/")
            else:
                print(request, "Invalid username or password.")
        else:
            print(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form": form})

def logout_user(request):
    logout(request)
    print(request, "You have successfully logged out.")
    return redirect("/swagger/")

@csrf_exempt
def get_user_info(request):
    print(request.user)
    if request.user.is_authenticated:
        user = {"id": request.user.id, "email": request.user.email, "last_name": request.user.last_name,
                "first_name": request.user.first_name}
        return JsonResponse(user)
    else:
        return JsonResponse({"error": "You are not auth"})
