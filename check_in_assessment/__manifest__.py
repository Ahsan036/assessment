{
    'name': 'Check-In Assessment Customization',
    'version': '1.0',
    'summary': 'Customize Check-In Process',
    'description': "Add custom fields of Project, Task associated with the project and description while user is"
                   " check in / check out using Odoo attendance application",
    'sequence': 10,
    'depends': ['hr_attendance', 'project'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'check_in_assessment/static/src/js/**/*',
        ],
        'web.assets_qweb': [
            'check_in_assessment/static/src/xml/**/*',
        ],
    },

    'installable': True,
    'application': False,
    'auto_install': False,
}
