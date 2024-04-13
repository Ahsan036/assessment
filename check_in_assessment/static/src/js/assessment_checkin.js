odoo.define('check_in_assessment.inherit_my_attendance', function (require) {
    "use strict";

    const MyAttendances = require('hr_attendance.my_attendances');
    const session = require('web.session');

    MyAttendances.include({
        // Using event delegation for dynamically added select elements
        events: _.extend({}, MyAttendances.prototype.events, {
            'change select[id="projectSelect"]': '_onChangeProjectSelect',
        }),

        _onChangeProjectSelect: function (ev) {
            // Caching jQuery objects to reduce repeated DOM lookups
            const $projectSelect = this.$("#projectSelect");
            if ($projectSelect.length) {
                const $projectIDSelect = this.$("select[name='project_id']");
                const projectID = $projectIDSelect.val();
                console.log("Selected Project ID:", projectID);
                // Ensure `this.projects` is properly set up and contains `project_task_ids`
                if (!this.projects || !this.projects.project_task_ids) {
                    console.error("Project tasks data is missing or not properly initialized.");
                    return;  // Exit if data is not correctly initialized
                }

                let selectHtml = `<select class="col-7" name="project_task_id" id="projectTaskSelect">
                                    <option selected="selected" value=""></option>`;

                const tasks = this.projects.project_task_ids.filter(task => task.project_id == projectID);
                console.log("Filtered Tasks:", tasks);

                tasks.forEach(task => {
                    selectHtml += `<option value="${task.id}">${task.name}</option>`;
                });
                selectHtml += "</select>";
                this.$("#projectTaskSelect").replaceWith(selectHtml);

                // Handling the case where no tasks are associated with the selected project
                if (!tasks.length) {
                    console.warn("No tasks found for the selected project:", projectID);
                    this.$("#projectTaskSelect").html('<option value="">No tasks available</option>');
                }
            }
        },


        willStart: function () {
            return this._super.apply(this, arguments).then(() => {
                return this._fetchProjectData();
            });
        },

        // Encapsulating repetitive RPC calls into a method for reuse and better structure
        _fetchProjectData: function() {
            const self = this;
            return self._rpc({
                model: 'hr.employee',
                method: 'get_attendance_projects',
                args: [[['user_id', '=', self.getSession().uid]]],
                context: session.user_context,
            }).then(p => {
                self.projects = p;
            }).catch(error => {
                console.error("Failed to load projects:", error);
                self.displayNotification({
                    title: "Project Load Error",
                    message: "Could not load project data. Please try again.",
                    type: 'danger',
                    sticky: true,
                });
            });
        },

        update_attendance: function () {
            const self = this;
            const $projectIDSelect = this.$("select[name='project_id']");
            const project_id = $projectIDSelect.val();
            const project_task_id = this.$("select[name='project_task_id']").val();
            const description = this.$("textarea[id='attend_description']").val().trim();

            if (!project_id || !project_task_id || !description) {
                this.displayNotification({
                    title: "Validation Error",
                    message: "All fields (Project, Task, Description) must be filled.",
                    type: 'danger',
                    sticky: true,
                });
                return; // Stop execution if validation fails
            }

            const context = _.extend({}, session.user_context, {
                'project_id': project_id,
                'project_task_id': project_task_id,
                'attend_description': description,
            });

            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: context,
            }).then(result => {
                if (result.action) {
                    self.do_action(result.action);
                } else if (result.warning) {
                    self.displayNotification({
                        title: "Attendance Warning",
                        message: result.warning,
                        type: 'warning',
                        sticky: true,
                    });
                }
            }).catch(error => {
                console.error("Failed to update attendance:", error);
                self.displayNotification({
                    title: "Attendance Update Error",
                    message: "Failed to update attendance. Please check your data or try again.",
                    type: 'danger',
                    sticky: true,
                });
            });
        },
    });

    return MyAttendances;
});
