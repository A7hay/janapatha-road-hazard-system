from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.views.decorators.http import require_POST
from accounts.models import Profile
from.models import Complaint,ComplaintUpdate
from .forms import (ComplaintForm,ComplaintUpdateForm,AssignComplaintForm)



def send_notification(subject, message, email):
    if email:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=True
        )
        
@login_required
def complaint_create(request):

    try:
        if request.user.profile.role!='resident':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    if request.method=='POST':
        form=ComplaintForm(request.POST,request.FILES)
        if form.is_valid():
          complaint=form.save(commit=False)
          complaint.resident=request.user
          complaint.save()   

          ComplaintUpdate.objects.create(
              complaint=complaint,
              updated_by=request.user,
              status='pending',
              remarks='Complaint submitted successfully'
          )

          admin=User.objects.filter(is_superuser=True).first()

          if admin and admin.email:
              subject=  'New Complaint Submitted - JANAPATHA'    
              message = f"""
A new complaint has been submitted.

Tracking Number: {complaint.tracking_number}
Title: {complaint.title}
Category: {complaint.get_category_display()}
Location: {complaint.location}
Resident: {request.user.username}

Please log in to the admin dashboard
to review and assign this complaint.
"""
              send_notification(subject,message,admin.email)
        messages.success(request,'Complaint submitted successfully')
        return redirect('resident_dashboard')
    else:
        form=ComplaintForm()
    return render(request,'complaints/complaint_create.html',{'form':form})

@login_required
def complaint_detail(request,pk):
    complaint=get_object_or_404(Complaint,pk=pk)
    allowed=False
    if request.user.is_superuser:
        allowed=True
    elif complaint.resident==request.user:
        allowed=True
    else:
        try:
            profile=request.user.profile
            if(
                profile.role=='staff'
                and profile.department==complaint.department
            ):
                allowed=True
        except Profile.DoesNotExist:
            pass
        if not allowed:
            messages.error(request,'You not have the permission to view this complaint')
            return redirect('home')
    updates=complaint.updates.all().order_by('-created_at')
    return render(request,'complaints/complaint_detail.html',{'complaint':complaint,'updates':updates})    

@login_required
def assign_complaint(request, pk):

    if not request.user.is_superuser:
        return redirect('home')

    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':

        form = AssignComplaintForm(request.POST, instance=complaint)

        if form.is_valid():

            old_department = complaint.department

            complaint = form.save(commit=False)

        
            if old_department != complaint.department:
                complaint.assigned_staff = None

            
            if complaint.department:
                complaint.status = 'assigned'
            else:
                complaint.status = 'pending'

            
            complaint.save()
            ComplaintUpdate.objects.create(
                            complaint=complaint,
                            updated_by=request.user,
                            status=complaint.status,
                            remarks=complaint.admin_remarks or 'Complaint assigned to department.'
                        )
            if complaint.department:

                department_email = complaint.department.email


                if department_email:

                  subject = 'New Complaint Assigned - JANAPATHA'

                  message = f"""
Hello {complaint.department.name} Department,

A new road complaint has been assigned to your department.

Tracking Number: {complaint.tracking_number}
Title: {complaint.title}
Category: {complaint.get_category_display()}
Location: {complaint.location}

Description:
{complaint.description}

Please log in to JANAPATHA and take the necessary action.

Thank you,
JANAPATHA Administration
"""
              
                
                send_notification(
            subject,
            message,
            department_email
          )
               
            
 
        messages.success(
                request,
                'Complaint assigned successfully.'
            )

        return redirect('admin_dashboard')

    else:
        form = AssignComplaintForm(instance=complaint)

    return render(
        request,
        'complaints/assign_complaint.html',
        {
            'form': form,
            'complaint': complaint
        }
    )

@login_required
@require_POST
def take_complaint(request,pk):
    try:
        profile=request.user.profile
        if profile.role!='staff' or not profile.department:
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')
    with transaction.atomic():
        complaint=get_object_or_404(
            Complaint.objects.select_for_update(),
            pk=pk,
            department=profile.department
            
        )
        if complaint.assigned_staff is None:
            complaint.assigned_staff=request.user
            complaint.status='in_progress'
            complaint.save()

            ComplaintUpdate.objects.create(
                complaint=complaint,
                updated_by=request.user,
                status='in_progress',
                remarks='Work taken by'+ request.user.username
            )
            messages.success(request,'You have successfully taken this complaint')
        else:
            messages.warning(request,'This complaint has already been taken by' + complaint.assigned_staff.username)
    return redirect('staff_dashboard')


@login_required
def staff_update_complaint(request, pk):

    try:
        profile = request.user.profile

        if profile.role != 'staff':
            return redirect('home')

    except Profile.DoesNotExist:
        return redirect('home')

    complaint = get_object_or_404(
        Complaint,
        pk=pk,
        department=profile.department,
        assigned_staff=request.user
    )

    if request.method == 'POST':

        form = ComplaintUpdateForm(request.POST, request.FILES)

        if form.is_valid():

            update = form.save(commit=False)

            update.complaint = complaint
            update.updated_by = request.user

        
            update.save()

            
            complaint.status = update.status
            complaint.save()

        
            subject = 'Complaint Progress Updated - JANAPATHA'

            message = f"""
Hello {complaint.resident.first_name},

Your complaint has been updated.

Tracking Number: {complaint.tracking_number}
Title: {complaint.title}
Status: {complaint.get_status_display()}

Staff Remarks:
{update.remarks}

Thank you,
JANAPATHA Team
"""

            send_notification(
                subject,
                message,
                complaint.resident.email
            )

            messages.success(
                request,
                'Complaint status updated successfully.'
            )

            return redirect('staff_dashboard')

    else:
        form = ComplaintUpdateForm()

    return render(
        request,
        'complaints/staff_update.html',
        {
            'form': form,
            'complaint': complaint
        }
    )
  




