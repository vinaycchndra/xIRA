from django.shortcuts import render


def create_ticket(request, project_id):

    return render(request, 'create_task.html')
