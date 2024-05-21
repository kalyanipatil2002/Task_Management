from django.utils import timezone
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from projects.models import Project, Task, User, UserProfile, Role
from sweetify import sweetify
from projects.forms import ProjectForm, TaskForm, CreateUserForm, RoleForm, RoleAssignmentForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date
# @staff_member_required()


def dashboardView(request):
    return render(request, 'dashboard.html', locals())


def indexView(request):
    if request.user.is_authenticated:
        print("dddd")
        return redirect('task_list')
    else:
        print("iikii")
        return redirect('login_view')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page after successful login
            if request.user.is_superuser:
                return redirect('project_list')
            else:
                return redirect('task_list')
        else:
            # Handle invalid login credentials
            return render(request, 'registration/login.html', {'error_message': 'Invalid username or password'})
    else:
        # Render the login form
        return render(request, 'registration/login.html')


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_at = timezone.now()
            # task.created_by = request.user

            task.save()
            sweetify.success(
                request, "The User has been successfully created.")
            return redirect('list_users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CreateUserForm()

    return render(request, 'project/user/create_user.html', locals())


@login_required
def list_users(request):
    users = UserProfile.objects.all()
    users = UserProfile.objects.filter(is_deleted=False)
    return render(request, 'project/user/list_users.html', {'users': users})
#


@login_required
def update_user(request, pk):
    user = UserProfile.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateUserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.updated_at = timezone.now()
            user.save()
            sweetify.success(
                request, "The User has been successfully updated.")
            return redirect('list_users')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}")
    else:
        form = CreateUserForm(instance=user)
    return render(request, 'project/user/update_user.html', {'form': form})

@login_required
def view_profile(request, pk):
    user = UserProfile.objects.get(pk=pk)
    return render(request, 'project/user/view_profile.html', {'user': user})
# # delete #
@login_required
def delete_user(request, pk):
    user = UserProfile.objects.get(pk=pk)
    if request.method == 'POST':
        user.is_deleted = True
        user.deleted_at = timezone.now()
        # project.deleted_by = request.user
        user.save()
        sweetify.success(request, "The project has been successfully deleted.")
        return redirect('list_users')  # Redirect to the project list view
    return JsonResponse({'status': False, 'error': 'Project Not Found '})


@login_required
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('role_list')  # Redirect to role list page
    else:
        form = RoleForm()
    return render(request, 'project/role/create_role.html', {'form': form})


@login_required
def role_list(request):
    role = Role.objects.all()
    role = Role.objects.filter(is_deleted=False)
    return render(request, 'project/role/list_role.html', {'role': role})


@login_required
def update_role(request, pk):
    role = Role.objects.get(pk=pk)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save(commit=False)
            role.updated_at = timezone.now()
            role.save()
            sweetify.success(
                request, "The User has been successfully updated.")
            return redirect('role_list')
    else:
        form = RoleForm(instance=role)
    return render(request, 'project/role/update_role.html', {'form': form})


@login_required
def delete_role(request, pk):
    role = Role.objects.get(pk=pk)
    if request.method == 'POST':
        role.is_deleted = True
        role.deleted_at = timezone.now()

        role.save()
        sweetify.success(request, "The role has been successfully deleted.")
        return redirect('role_list')  # Redirect to the project list view
    return JsonResponse({'status': False, 'error': 'Project Not Found '})


@login_required
def user_role_assignment(request, user_id):
    user = UserProfile.objects.get(id=user_id)
    if request.method == 'POST':
        form = RoleAssignmentForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('list_users')  
    else:
        form = RoleAssignmentForm(instance=user)
    return render(request, 'project/user/user_role_assignment.html', {'form': form})


@login_required
def create_Project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_at = timezone.now()
            # project.created_by = request.user

            project.save()
            sweetify.success(
                request, "The card make has been successfully added.")
            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'project/create_project.html', {'form': form})


@login_required
def project_list(request):
    projects = Project.objects.filter(is_deleted=False).order_by('created_at')
    return render(request, 'project/list_project.html', {'projects': projects})


@login_required
def get_projects(request):
    projects = Project.objects.all()
    projects = Project.objects.filter(is_deleted=False).order_by('created_at')
    project_list = [{'id': project.id, 'name': project.name}
                    for project in projects]
    return JsonResponse({'projects': project_list})

# # update #


@login_required
def update_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project.updated_at = timezone.now()
            # project.updated_by = request.user
            # instance.save()
            form.save()
            sweetify.success(
                request, "The card make has been successfully updated.")
            return redirect('project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/update_project.html', {'form': form})


# # delete #
@login_required
def delete_project(request, pk):
    project = Project.objects.get(pk=pk)
    if request.method == 'POST':
        project.is_deleted = True
        project.deleted_at = timezone.now()

        project.save()
        sweetify.success(request, "The project has been successfully deleted.")
        return redirect('project_list')  # Redirect to the project list view
    return JsonResponse({'status': False, 'error': 'Project Not Found '})

def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    tasks = project.tasks.all()

    context = {
        'project': project,
        'tasks': tasks
    }
    return render(request, 'project/project_detail.html', context)
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_at = timezone.now()

            assigned_to_id = request.POST.get('assigned_to')
            if assigned_to_id:
                task.assigned_to_id = assigned_to_id
            task.save()
            sweetify.success(request, "The Task has been successfully added.")
            return redirect('task_list')
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            return render(request, 'project/task/create_task.html', {'form': form})
    else:
        form = TaskForm()

    return render(request, 'project/task/create_task.html', {'form': form})


@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.filter(is_deleted=False)
    else:
        tasks = Task.objects.filter(is_deleted=False, assigned_to=request.user)

    # Filter tasks by status
    status_filter = request.GET.get('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    # Filter tasks by deadline
    deadline_filter = request.GET.get('deadline')
    if deadline_filter:
        tasks = tasks.filter(deadline=deadline_filter)

    return render(request, 'project/task/list_task.html', locals())


@login_required
def update_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.updated_at = timezone.now()
            assigned_to_id = request.POST.get('assigned_to')
            if assigned_to_id:
                task.assigned_to_id = assigned_to_id
            deadline_datetime=form.cleaned_data.get('deadline')
            deadline_date=deadline_datetime.date()

            current_date=date.today()
            if deadline_date< current_date:
                return  render(request,'project/task/update_task.html',{'form':form,'alert_message':"deadline cannot set past date"})
            
            else:
                task.save()

                form.save()
                sweetify.success(
                    request, "The task has been successfully updated.")
                return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'project/task/update_task.html', {'form': form})


# # delete #
@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        task.is_deleted = True
        task.deleted_at = timezone.now()
        # project.deleted_by = request.user
        task.save()
        sweetify.success(request, "The task has been successfully deleted.")
        return redirect('task_list')

    return JsonResponse({'status': False, 'error': 'Project Not Found '})


@login_required
def add_task(request):
    print("kkkkkkkkkkkkkkkkkkkkk")
    if request.method == 'POST':
        print("qqqqqqqqqqqqqqqqqqqqqq")
        # Extract task details from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        # Assuming project_id is passed in the form data
        project_id = request.POST.get('project_id')

        # Create the task
        task = Task.objects.create(
            title=title,
            description=description,
            deadline=deadline,
            project_id=project_id
        )

        # Return a JSON response with the task details
        return JsonResponse({
            'title': task.title,
            'description': task.description,
            # Format the deadline as needed
            'deadline': task.deadline.strftime('%Y-%m-%d %H:%M:%S')
        })
    else:
        # Handle GET requests gracefully
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)
