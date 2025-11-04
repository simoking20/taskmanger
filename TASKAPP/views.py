from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task, Event
from .forms import TaskForm, EventForm # Import the new forms

# Custom test to check for staff/admin status
def is_task_admin(user):
    """Checks if the user has staff or superuser privileges."""
    return user.is_staff or user.is_superuser

# Function to check if a user is the creator or an admin for a specific object
def is_creator_or_admin(user, obj):
    """Checks if the user is the object's creator or a superuser/staff member."""
    return user == obj.created_by or is_task_admin(user)


# --- Admin View (Already FBV) ---

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(is_completed=True).count()
    upcoming_events_count = Event.objects.count()

    tasks = Task.objects.all().select_related('assigned_to')

    return render(request, "taskapp/admin_dashboard.html", {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "upcoming_events_count": upcoming_events_count,
        "tasks": tasks
    })
# =========================================================================
# --- TASK VIEWS (Function-Based CRUD) ---
# =========================================================================

@login_required
def task_list(request):
    """
    Displays a list of all general tasks. (ListView equivalent)
    """
    tasks = Task.objects.all().order_by('-created_at')
    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)

@login_required
def my_tasks(request):
    """
    Displays tasks specifically assigned to the current user. (ListView equivalent with filter)
    """
    my_tasks = Task.objects.filter(assigned_to=request.user).order_by('-due_date')
    context = {'my_tasks': my_tasks}
    return render(request, 'tasks/my_tasks.html', context)

@login_required
def task_detail(request, pk):
    """
    Displays the detail view for a single task. (DetailView equivalent)
    """
    task = get_object_or_404(Task, pk=pk)
    context = {'task': task}
    return render(request, 'tasks/task_detail.html', context)

@login_required
def create_task(request):
    """
    Handles the form for creating a new task. (CreateView equivalent)
    """
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user  # Set the created_by field automatically
            task.save()
            return redirect(reverse('task_list'))
    else:
        form = TaskForm()
        
    context = {'form': form}
    return render(request, 'tasks/create_task.html', context)

@login_required
def update_task(request, pk):
    """
    Handles updating an existing task. (UpdateView equivalent)
    Requires the user to be the task creator or admin.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if not is_creator_or_admin(request.user, task):
        # Redirect if user does not have permissions
        return redirect(reverse('task_detail', kwargs={'pk': pk})) 
        
    if request.method == 'POST':
        # Use request.FILES to handle potential file uploads
        form = TaskForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('tasks:task_detail', kwargs={'pk': pk}))
    else:
        form = TaskForm(instance=task)
        
    context = {'form': form, 'task': task}
    # Re-using create_task.html as it acts as a generic form template
    return render(request, 'tasks/create_task.html', context) 

@login_required
def delete_task(request, pk):
    """
    Handles deleting a task. (DeleteView equivalent)
    Requires the user to be the task creator or admin.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if not is_creator_or_admin(request.user, task):
        # Redirect if user does not have permissions
        return redirect(reverse('tasks:task_detail', kwargs={'pk': pk})) 

    if request.method == 'POST':
        task.delete()
        return redirect(reverse('task:task_list'))
        
    context = {'task': task}
    # Renders the confirmation template
    return render(request, 'tasks/task_confirm_delete.html', context) 


# =========================================================================
# --- EVENT VIEWS (Function-Based ) ---
# =========================================================================
@login_required
def event_list(request):
    """Displays a list of all scheduled events. (ListView equivalent)"""
    events = Event.objects.all().order_by('-date')
    context = {'events': events}
    return render(request, 'tasks/event_list.html', context)

@login_required
def event_detail(request, pk):
    """Displays the detail view for a single event. (DetailView equivalent)"""
    event = get_object_or_404(Event, pk=pk)
    context = {'event': event}
    return render(request, 'tasks/event_detail.html', context)

@login_required
def create_event(request):
    """Handles the form for creating a new event. (CreateView equivalent)"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect(reverse('tasks:event_list'))
    else:
        form = EventForm()
        
    context = {'form': form}
    return render(request, 'tasks/event_form.html', context)

@login_required
def update_event(request, pk):
    """Handles updating an existing event. (UpdateView equivalent)"""
    event = get_object_or_404(Event, pk=pk)
    
    if not is_creator_or_admin(request.user, event):
        return redirect(reverse('tasks:event_detail', kwargs={'pk': pk}))

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect(reverse('tasks:event_detail', kwargs={'pk': pk}))
    else:
        form = EventForm(instance=event)

    context = {'form': form, 'event': event}
    return render(request, 'tasks/event_form.html', context)

@login_required
def delete_event(request, pk):
    """Handles deleting an event. (DeleteView equivalent)"""
    event = get_object_or_404(Event, pk=pk)
    
    if not is_creator_or_admin(request.user, event):
        return redirect(reverse('task:event_detail', kwargs={'pk': pk}))

    if request.method == 'POST':
        event.delete()
        return redirect(reverse('tasks:event_list'))

    context = {'event': event}
    return render(request, 'tasks/event_confirm_delete.html', context)
