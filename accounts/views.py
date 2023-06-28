from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import RegistrationForm


def register(request):
    form = RegistrationForm()
    context = {
        'form': form
    }
    if request.method == 'POST':
        form_request = RegistrationForm(request.POST)
        if form_request.is_valid():
            first_name   =  form_request.cleaned_data['first_name']
            last_name    =  form_request.cleaned_data['last_name']
            work_email        =  form_request.cleaned_data['work_email']
            contact_number =  form_request.cleaned_data['contact_number']
            password     =  form_request.cleaned_data['password']
            user         = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                                       work_email=work_email, password=password, )
            user.contact_number = contact_number
            user.is_active = True
            user.save()
            messages.success(request, 'Successfully Registered Kindly Login!')
            return redirect('login')
        else:

            context['form'] = form_request
            messages.error(request, 'Could not register')

    return render(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        work_email = request.POST['work_email']
        password = request.POST['password']
        user = auth.authenticate(work_email=work_email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are Successfully Logged-In')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credentials are not valid !!!')
            return redirect('login')
    return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')
