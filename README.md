# assessment
Technical Survey Assessment Apexive
# Inheriting HR Attendance Table and HR Employee Table
I have inherited the hr.attendance table and added custom field for Project, Task and Description on that table to record
I have also inherited the hr.employee table and add the computed fields for project, project_task_id and description to compute the Project, project_task_id and description from last attendance record.
I have added a function for efficient fetching of project and task data for frontend use in hr.employee table
I have override the _attendance_action_change function to write the project, project_task_id and description in hr.employee table
# Javascript code 
I have used an event delegation for dynamically showing task based on selected project
Upon rendering the JS file I have used encapsulated _fetchProjectData function with error handling in order to encapsulating repetitive RPC calls into a method for reuse and better structure
I have override the update_attendance function in order to add project, project_task_id and description and also added a validation that these fields must be filled before check in or check out of an employee with error handling.
