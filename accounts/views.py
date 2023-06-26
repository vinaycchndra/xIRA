from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required



def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name   =  form.cleaned_data['first_name']
            last_name    =  form.cleaned_data['last_name']
            email        =  form.cleaned_data['email']
            phone_number =  form.cleaned_data['phone_number']
            password     =  form.cleaned_data['password']
            username     = email.split('@')[0]
            user         = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                                       email=email, username=username,password=password, )
            user.phone_number = phone_number
            user.save()

            # Create User Profile for registering user
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # User Activation code
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message      =  render_to_string('accounts/account_verification_mail.html', {
                'user': user,
                'domain': current_site,
                'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)

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


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')
