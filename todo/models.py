from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    task_date = models.DateField(default=timezone.now)  # ✅ NEW
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
