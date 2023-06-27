from django.shortcuts import render


def base(request):
    return render(request, 'includes/project_creation.html')
