from django.contrib import admin
from .models import Department, Complaint, ComplaintUpdate

admin.site.register(Department)
admin.site.register(Complaint)
admin.site.register(ComplaintUpdate)