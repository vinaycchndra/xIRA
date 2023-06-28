from .forms import ProjectCreationForm


def create_project_form(request):
    form = ProjectCreationForm()
    context = {
        'project_creation_form': form
    }
    return context
