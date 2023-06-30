from django.shortcuts import render


def manage_ticket(request, project_id):

    return render(request, 'tasks.html')
