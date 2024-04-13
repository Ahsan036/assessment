# -*- coding: utf-8 -*-
from odoo import api, fields, models

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    # Fields linking attendances to specific projects and tasks with proper documentation
    project_id = fields.Many2one(
        'project.project', string="Project", required=True,
        help="Links each attendance to a specific project."
    )
    project_task_id = fields.Many2one(
        'project.task', string="Task", required=True,
        domain="[('project_id','!=',False), ('project_id','=',project_id), ('is_closed','=',False)]",
        help="Links each attendance to a specific task within a project. Only tasks that are not closed and are linked to a project are selectable."
    )
    description = fields.Text(
        string="Descriptions", required=True,
        help="Descriptive text for the attendance record."
    )

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Computed fields that fetch data related to the most recent attendance record
    attendance_project_id = fields.Many2one('project.project', compute='_compute_attendance_project',
                                            string="Attendance Project", help="Project associated with the last attendance.")
    attendance_project_task_id = fields.Many2one('project.task', compute='_compute_attendance_project',
                                                 string="Attendance Project Task", help="Task associated with the last attendance.")
    attendance_description = fields.Text(compute='_compute_attendance_project',
                                         string="Attendance Descriptions", help="Description associated with the last attendance.")

    @api.depends('last_attendance_id')
    def _compute_attendance_project(self):
        # Efficient method to update computed fields based on last attendance
        for employee in self:
            att = employee.last_attendance_id.sudo()
            if att and not att.check_out:
                employee.update({
                    'attendance_project_id': att.project_id.id,
                    'attendance_project_task_id': att.project_task_id.id,
                    'attendance_description': att.description
                })
            else:
                employee.update({
                    'attendance_project_id': False,
                    'attendance_project_task_id': False,
                    'attendance_description': False
                })

    @api.model
    def get_attendance_projects(self, domain):
        # Efficient fetching of project and task data for frontend use
        project_domain = [('task_ids', '!=', False)]
        projects = self.env['project.project'].search(project_domain)
        tasks = self.env['project.task'].search_read(
            [('project_id', 'in', projects.ids), ('is_closed', '=', False)]
        )
        emp_id = self.search(domain, limit=1)
        return {
            'project_ids': [{'id': proj['id'], 'name': proj['display_name']} for proj in projects],
            'project_task_ids': [{'id': task['id'], 'name': task['display_name'], 'project_id': task['project_id'][0]} for task in tasks],
            'current_project_id': {'id': emp_id.attendance_project_id.id, 'name': emp_id.attendance_project_id.display_name} if emp_id.attendance_project_id else False,
            'current_project_task_id': {'id': emp_id.attendance_project_task_id.id, 'name': emp_id.attendance_project_task_id.display_name} if emp_id.attendance_project_task_id else False,
            'current_description': emp_id.attendance_description or False,
        }

    def _attendance_action_change(self):
        res = super(HrEmployee, self)._attendance_action_change()
        # Safely get context values with default fallbacks
        project_id = self.env.context.get('project_id', False)
        project_task_id = self.env.context.get('project_task_id', False)
        attend_description = self.env.context.get('attend_description', False)

        # Proceed to update the record if it exists
        if res:
            res.write({
                'project_id': int(project_id) if project_id else False,
                'project_task_id': int(project_task_id) if project_task_id else False,
                'description': attend_description or False
            })
        return res

