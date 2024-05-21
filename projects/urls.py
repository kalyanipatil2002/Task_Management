from django.urls import path



from projects.views import *
urlpatterns = [

    

    path('', login_view, name='login_view'),
    path('dashboard', dashboardView, name='dashboard'),
    path('create-Project', create_Project, name='create_Project'),
    path('projects', project_list, name='project_list'),
    path('get_projects', get_projects, name='get_projects'),
    path('update-project/<uuid:pk>', update_project, name='update_project'),
    path('delete-project/<uuid:pk>', delete_project, name='delete_project'),
    path('project_detail/<uuid:pk>', project_detail, name='project_detail'),


    path('create-task', create_task, name='create_task'),
    path('tasks', task_list, name='task_list'),
    path('update-task/<uuid:pk>', update_task, name='update_task'),
    path('delete-task/<uuid:pk>', delete_task, name='delete_task'),

    path('create-user', create_user, name='create_user'),
    path('users', list_users, name='list_users'),
    # path('update-user/<uuid:pk>', update_user, name='update_user'),
    path('update-user/<int:pk>/', update_user, name='update_user'),
    path('view_profile/<int:pk>/', view_profile, name='view_profile'),
    path('delete-user/<int:pk>/', delete_user, name='delete_user'),
    path('create-role/', create_role, name='create_role'),
    path('role_list/', role_list, name='role_list'),
    path('update-role/<int:pk>/', update_role, name='update_role'),
    path('delete_role/<int:pk>/', delete_role, name='delete_role'),
    path('user_role_assignment/<int:user_id>/', user_role_assignment, name='user_role_assignment'),
    path('add_task/', add_task, name='add_task'),

    # path('delete-user/<uuid:pk>', delete_user, name='delete_user'),
]