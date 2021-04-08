from django.db import models


class ToDoTask(models.Model):
    content = models.CharField(max_length=255)
    complete = models.BooleanField(default=False)
    rating = models.IntegerField(default=1)
    priority = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.pk} todo task'
