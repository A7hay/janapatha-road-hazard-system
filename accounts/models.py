from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = [
        ('resident', 'Resident'),
        ('staff', 'Department Staff'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='resident'
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    department = models.ForeignKey(
        'complaints.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members'
    )

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.role == 'staff' and not self.department:
            raise ValidationError(
                {'department': 'Department is required for staff.'}
            )

        if self.role == 'resident' and self.department:
            raise ValidationError(
                {'department': 'Residents cannot belong to a department.'}
            )

    def __str__(self):
        return f'{self.user.username} - {self.role}'

