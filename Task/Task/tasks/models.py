from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Employee(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField()

    def __str__(self):
        return self.name


class TaskStatus(models.TextChoices):
    PENDING = 'P', 'Pending'
    IN_PROGRESS = 'I', 'In Progress'
    COMPLETED = 'C', 'Completed'


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=1,
        choices=TaskStatus.choices,
        default=TaskStatus.PENDING
    )
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    class Meta:
        ordering = ['due_date', 'title']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def days_left(self):
        """Return integer days left until due_date (can be negative if overdue)."""
        today = timezone.localdate()
        return (self.due_date - today).days
    days_left.short_description = "Days Left"

    def clean(self):
        """Custom validation logic."""
        errors = {}

        if self.assigned_to and self.status == TaskStatus.PENDING:
            qs = Task.objects.filter(
                assigned_to=self.assigned_to,
                status=TaskStatus.PENDING
            )
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            if qs.count() >= 5:
                errors['assigned_to'] = "This employee already has 5 pending tasks."

        if self.due_date and self.due_date < timezone.localdate():
            errors['due_date'] = "Due date cannot be in the past."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
       
        self.full_clean()
        super().save(*args, **kwargs)
