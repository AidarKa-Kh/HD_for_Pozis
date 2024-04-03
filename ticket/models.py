import uuid
from django.db import models
from users.models import User


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='media/knowledge_base/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'База знаний'

    def __str__(self):
        return self.title


class Department(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name


class DepartmentMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Пользователи отделов'

    def __str__(self):
        return f"{self.user.username} - {self.department.name}"


class Ticket(models.Model):
    status_choices = (
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Rejected', 'Rejected'),
        ('Blocked', 'Blocked'),
    )
    ticket_number = models.UUIDField(default=uuid.uuid4)
    media = models.FileField(upload_to='media/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    date_created = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(null=True, blank=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    ticket_status = models.CharField(max_length=15, choices=status_choices)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Заявки пользователей'

    def __str__(self):
        return self.title

