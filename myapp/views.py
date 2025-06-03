from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout
from django.views.decorators.cache import never_cache

# View accessible without login (like home page)
@csrf_exempt
def index(request):
    return render(request, 'index.html')

# Registration should NOT require login
@csrf_exempt
@never_cache
def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Username already registered')
            return redirect('registration')
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=fname, last_name=lname)
            user.save()
            try:
                group = Group.objects.get(name='customer')
                user.groups.add(group)
            except Group.DoesNotExist:
                group = Group.objects.create(name='customer')
                user.groups.add(group)

            messages.success(request, 'Account created successfully')
            return redirect('registration')

    return render(request, 'registration.html')

# Login should NOT require login, but needs never_cache
@csrf_exempt
@never_cache
def login(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request, username=uname, password=password)
        print("USER : ", user)
        if user is not None:
            auth_login(request, user)
            if user.groups.filter(name='customer').exists():
                return render(request, 'home.html', {'user': user, 'group': 'customer'})
            elif user.groups.filter(name='admin').exists():
                return render(request, 'admin_home.html', {'user': user, 'group': 'admin'})
            else:
                return render(request, 'home.html', {'user': user, 'group': 'other'})
        else:
            messages.error(request, 'Username or password incorrect')
    return render(request, 'login.html')

# Views that require login and prevent cache
@login_required(login_url='login')
@never_cache
def admin_view_customer(request):
    user_det = User.objects.all().exclude(username='admin').order_by('-date_joined')
    return render(request, 'admin_view_customer.html', {'user_det': user_det})

@login_required(login_url='login')
@never_cache
def logout_user(request):
    logout(request)              # Django logout
    request.session.flush()      # Clear session
    messages.success(request, "Logged out successfully.")
    return redirect('login')     # Redirect to login page


@login_required(login_url='login')
@never_cache
def user_view_profile(request):
    user_pro = User.objects.get(username=request.user)
    return render(request, 'user_view_profile.html', {'user_pro': user_pro, 'edit': False})


@login_required(login_url='login')
@never_cache
@csrf_exempt
def edit_profile(request, id):
    user_pro = User.objects.get(id=id)

    if request.method == "POST":
        user_pro.first_name = request.POST["first_name"]
        user_pro.last_name = request.POST["last_name"]
        user_pro.email = request.POST["email"]
        user_pro.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user_view_profile')

    return render(request, 'user_view_profile.html', {'user_pro': user_pro, 'edit': True})