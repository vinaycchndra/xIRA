from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, work_email, password=None):
        if not work_email:
            raise ValueError('User must have an email address')

        user = self.model(
            work_email = self.normalize_email(work_email),
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, work_email, password=None):
        user = self.create_user(
            work_email = self.normalize_email(work_email),
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


choices = (
    ('Frontend Developer', 'Frontend Developer'),
    ('Backend Developer', 'Backend Developer'),
    ('UX Engineer', 'UX Engineer'),
    ('UX Engineer', 'UX Engineer'),
    ('Data Scientist', 'Data Scientist'),
    ('Data Engineer', 'Data Engineer'),
)


class Account(AbstractBaseUser):
    first_name           = models.CharField(max_length=50)
    last_name            = models.CharField(max_length=50)
    work_email           = models.EmailField(max_length=100, unique=True)
    contact_number       = models.CharField(max_length=50)
    work_profile         = models.CharField(max_length=30, choices=choices)


    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'work_email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    def is_project_manager(self):
        try:
            temp = ProjectManager.objects.get(project_manager__id=self.id)
            is_manager = True
        except ProjectManager.DoesNotExist:
            is_manager = False
        return is_manager


choices_1 = (
    ('Web_Development', 'Web Application'),
    ('Software_Development', 'Software Packages'),
    ('Machine Learning Project', 'Data Science Project'),
)


class ProjectManager(models.Model):
    project_manager = models.OneToOneField(Account, on_delete=models.CASCADE)
    domain          = models.CharField(max_length=40, choices=choices_1)

    def __str__(self):
        return self.project_manager.first_name

