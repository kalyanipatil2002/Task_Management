// $(document).ready(function() {
//     // Function to fetch projects and tasks from the server
//     function fetchProjectsAndTasks() {
//         // Make AJAX request to fetch projects
//         $.ajax({
//             type: 'GET',
//             url: '/api/projects', // Replace with your endpoint to fetch projects
//             success: function(projects) {
//                 // Update project list
//                 $('#project-list').empty();
//                 projects.forEach(function(project) {
//                     $('#project-list').append('<div>' + project.name + '</div>');
//                 });
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error fetching projects:', error);
//             }
//         });

//         // Make AJAX request to fetch tasks
//         $.ajax({
//             type: 'GET',
//             url: '/api/tasks', // Replace with your endpoint to fetch tasks
//             success: function(tasks) {
//                 // Update task list
//                 $('#task-list').empty();
//                 tasks.forEach(function(task) {
//                     $('#task-list').append('<div>' + task.name + '</div>');
//                 });
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error fetching tasks:', error);
//             }
//         });
//     }

//     // Call fetchProjectsAndTasks initially to populate the lists
//     fetchProjectsAndTasks();

//     // Event listener for submitting add project form
//     $('#add-project-form').submit(function(event) {
//         event.preventDefault();
//         var projectName = $('#project-name').val();

//         // Make AJAX request to add project
//         $.ajax({
//             type: 'POST',
//             url: 'get_projects', // Replace with your endpoint to add project
//             data: { name: projectName },
//             success: function(response) {
//                 // Fetch projects and tasks again to update the lists
//                 fetchProjectsAndTasks();
//                 $('#project-name').val(''); // Clear input field
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error adding project:', error);
//             }
//         });
//     });

//     // Event listener for submitting add task form
//     $('#add-task-form').submit(function(event) {
//         event.preventDefault();
//         var taskName = $('#task-name').val();
//         var projectId = $('#project-select').val();

//         // Make AJAX request to add task
//         $.ajax({
//             type: 'POST',
//             url: 'get_tasks', // Replace with your endpoint to add task
//             data: {
//                 name: taskName,
//                 project_id: projectId
//             },
//             success: function(response) {
//                 // Fetch projects and tasks again to update the lists
//                 fetchProjectsAndTasks();
//                 $('#task-name').val(''); // Clear input field
//             },
//             error: function(xhr, status, error) {
//                 console.error('Error adding task:', error);
//             }
//         });
//     });
// });
$(document).ready(function() {
    // Toggle task form visibility
    $('#add-task-btn').click(function() {
        $('#task-form-container').toggle();
    });

    // AJAX to submit task form
    $('#task-form').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: window.location.href,
            data: $(this).serialize(),
            success: function(response) {
                if (response.status === 'success') {
                    // Append new task to task list
                    $('.list-group').append('<li class="list-group-item">' + response.task.title + ' - ' + response.task.status + '<span class="float-right">' + response.task.deadline + '</span></li>');
                    // Reset form
                    $('#task-form')[0].reset();
                    // Hide form
                    $('#task-form-container').hide();
                }
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ': ' + xhr.responseText);
            }
        });
    });
});
