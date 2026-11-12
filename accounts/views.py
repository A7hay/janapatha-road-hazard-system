
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ResidentRegisterForm, StaffRegisterForm
from .models import Profile

from complaints.models import Complaint, Department


def home(request):
    return render(request, 'home.html')




def register(request):

    if request.method == 'POST':
        form = ResidentRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Profile.objects.create(user=user, role='resident')

            login(request, user)

            return redirect('resident_dashboard')

    else:
        form = ResidentRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def add_staff(request):

    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Staff registered successfully.')

            return redirect('staff_login')

    else:
        form = StaffRegisterForm()

    return render(request, 'accounts/add_staff.html', {'form': form})



def resident_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            try:
                if not user.is_superuser and user.profile.role == 'resident':

                    login(request, user)

                    return redirect('resident_dashboard')

            except Profile.DoesNotExist:
                pass

        messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/resident_login.html')



def admin_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_superuser:

            login(request, user)

            return redirect('admin_dashboard')

        messages.error(request, 'Invalid administrator credentials.')

    return render(request, 'accounts/admin_login.html')


def staff_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            try:
                if user.profile.role == 'staff':

                    login(request, user)

                    return redirect('staff_dashboard')

            except Profile.DoesNotExist:
                pass

        messages.error(request, 'Invalid staff credentials.')

    return render(request, 'accounts/staff_login.html')



@login_required
def resident_dashboard(request):

    if request.user.is_superuser:
        return redirect('home')

    try:
        if request.user.profile.role != 'resident':
            return redirect('home')
    except Profile.DoesNotExist:
        return redirect('home')

    complaints = Complaint.objects.filter(
        resident=request.user
    ).order_by('-created_at')

    context = {
        'complaints': complaints,
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='pending').count(),
        'in_progress_complaints': complaints.filter(status='in_progress').count(),
        'completed_complaints': complaints.filter(status='completed').count(),
    }

    return render(request, 'accounts/resident_dashboard.html', context)


@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return redirect('home')

    complaints = Complaint.objects.all().order_by('-created_at')
    departments = Department.objects.all()

    context = {
        'complaints': complaints,
        'departments': departments,
        'total_complaints': complaints.count(),
        'pending_complaints': complaints.filter(status='pending').count(),
        'assigned_complaints': complaints.filter(status='assigned').count(),
        'in_progress_complaints': complaints.filter(status='in_progress').count(),
        'completed_complaints': complaints.filter(status='completed').count(),
    }

    return render(request, 'accounts/admin_dashboard.html', context)


@login_required
def staff_dashboard(request):

    try:
        profile = request.user.profile

        if profile.role != 'staff':
            return redirect('home')

    except Profile.DoesNotExist:
        return redirect('home')

    complaints = Complaint.objects.filter(
        department=profile.department
    ).order_by('-created_at')

    context = {
        'complaints': complaints,
        'total_complaints': complaints.count(),
        'available_complaints': complaints.filter(assigned_staff__isnull=True).count(),
        'my_complaints': complaints.filter(assigned_staff=request.user).count(),
        'in_progress_complaints': complaints.filter(status='in_progress').count(),
        'completed_complaints': complaints.filter(status='completed').count(),
    }

    return render(request, 'accounts/staff_dashboard.html', context)



@login_required
def user_logout(request):

    logout(request)

    return redirect('home')
