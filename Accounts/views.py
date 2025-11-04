from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from TASKAPP.models import Task, Event
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from .forms import MemberSignupForm
from django.contrib import messages

User = get_user_model()

# --- Authentication Views ---
def member_login(request):
    """Handles member login using AuthenticationForm."""
    if request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:member_dashboard'))  # ✅ namespaced

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse_lazy('accounts:member_dashboard'))  # ✅ namespaced
    else:
        form = AuthenticationForm()
        
    return render(request, 'member/login.html', {'form': form, 'title': 'Member Login'})


def member_signup(request):
    """Handles member sign up using MemberSignupForm."""
    if request.user.is_authenticated:
        return redirect(reverse_lazy('accounts:member_dashboard'))  # ✅ namespaced
        
    if request.method == 'POST':
        form = MemberSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse_lazy('accounts:member_dashboard'))  # ✅ namespaced
    else:
        form = MemberSignupForm()
        
    return render(request, 'member/signup.html', {'form': form, 'title': 'Member Sign Up'})


@login_required
def member_dashboard(request):
    """Displays the main dashboard for a logged-in member."""
    try:
        tasks_count = Task.objects.filter(assigned_to=request.user, is_completed=False).count()
        seven_days_out = datetime.now() + timedelta(days=7)
        upcoming_events = Event.objects.filter(date__lte=seven_days_out).order_by('date')[:5]
        events_count = Event.objects.filter(date__lte=seven_days_out).count()

        context = {
            'tasks_count': tasks_count,
            'upcoming_events': upcoming_events,
            'events_count': events_count,
            'user': request.user
        }
    except Exception as e:
        print(f"Error fetching dashboard data: {e}")
        context = {'tasks_count': 0, 'upcoming_events': [], 'events_count': 0, 'user': request.user}
        
    return render(request, 'member/dashboard.html', context)


def member_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')  # ✅ already correct


def admin_panel_login(request):
    """Renders the dedicated admin panel login page template."""
    return render(request, 'admin_panel/login.html', {'title': 'Admin Login'})
