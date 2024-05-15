from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.conf import settings
import uuid
from django.utils import timezone
from django.contrib.auth.models import User


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_updated', blank=True, null=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_deleted', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        abstract = True



class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
class UserProfile(AbstractUser):
    name = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
    

class Project(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


    def calculate_progress(self):
        tasks = self.task_set.all()
        total_tasks = tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = tasks.filter(status='COMPLETED').count()
        progress = (completed_tasks / total_tasks) * 100
        return progress

class Task(BaseModel):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    descriptions = models.TextField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    def __str__(self):
        return self.title

# Resolve the clashes in reverse accessor names for the User model related fields
User._meta.get_field('groups').remote_field.related_name = 'user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions'
