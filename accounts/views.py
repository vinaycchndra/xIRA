from django.shortcuts import render, redirect
from django.contrib import messages, auth


def login(request):
    if request.method == 'POST':
        work_email = request.POST['work_email']
        password = request.POST['password']
        user = auth.authenticate(work_email=work_email, password=password)
        print(user, work_email, password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are Successfully Logged-In')
            return redirect('login')
        else:
            messages.error(request, 'Credentials are not valid !!!')
            return redirect('login')

    return render(request, 'login.html')
