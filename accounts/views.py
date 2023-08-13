from django.shortcuts import redirect, render

# Create your views here.
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid user')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'you are now logged out')

        return redirect('index')


def register(request):
    if request.method == 'POST':
        # get valeu from the user
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if password is match or not
        if password == password2:
            # check for username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'user already existed')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error('request', 'That email is being used')
                    return redirect('register')
                else:
                    # looks good
                    user = User.objects.create_user(
                        username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                    # login after register
                    # auth.login(request, user)
                    # messages.success(request, 'you are login')
                    # return redirect('index')
                    user.save()
                    messages.success(
                        request, 'you are now registerd and can log in')

                    return redirect('login')
        else:
            messages.error(request, 'NOt matched password')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    user = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)

    context = {
        'data': user
    }

    return render(request, 'accounts/dashboard.html', context)
