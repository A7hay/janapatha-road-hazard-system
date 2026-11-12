from django.db import models
from django.contrib.auth.models import User
import uuid


class Department(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    email = models.EmailField()

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Complaint(models.Model):

    CATEGORY_CHOICES = [
        ('pothole', 'Pothole'),
        ('road_damage', 'Road Damage'),
        ('waterlogging', 'Waterlogging'),
        ('streetlight', 'Streetlight Problem'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    tracking_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )

    resident = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='complaints'
    )

    title = models.CharField(max_length=150)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    location = models.CharField(max_length=255)

    description = models.TextField()

    photo = models.ImageField(
        upload_to='complaints/',
        blank=True,
        null=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='complaints'
    )

    assigned_staff = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_complaints'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    admin_remarks = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.tracking_number:
            self.tracking_number = (
                'JAN' + uuid.uuid4().hex[:10].upper()
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.tracking_number


class ComplaintUpdate(models.Model):

    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='updates'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=Complaint.STATUS_CHOICES
    )

    remarks = models.TextField()

    evidence_photo = models.ImageField(
        upload_to='repair_evidence/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return (
            f'{self.complaint.tracking_number} - {self.status}'
        )