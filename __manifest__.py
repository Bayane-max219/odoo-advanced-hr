{
    'name': 'Advanced HR — Skills Matrix & Performance',
    'version': '17.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Employee skills matrix, performance review cycles, training plans and career path management',
    'description': """
Advanced HR — Skills Matrix & Performance Reviews
==================================================
Extends Odoo 17 HR with a professional skills management framework used in enterprise HR departments.

Key Features:
- Skills Framework: define skill categories, skills, and 5-level proficiency scale
- Employee Skills Matrix: visual grid of team skills vs proficiency
- Performance Review Cycles: 360° reviews with self-assessment, manager review, peer review
- Training Plans: link skill gaps to training actions with deadline and budget
- Career Paths: define progression tracks with required skill thresholds
- Skills Gap Analysis: compare employee profile to job position requirements
- QWeb PDF: individual skills report and team matrix report
    """,
    'author': 'Bayane Miguel Singcol',
    'website': 'https://github.com/Bayane-max219/odoo-advanced-hr',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
        'hr_skills',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/skill_level_data.xml',
        'data/review_cron.xml',
        'views/skill_views.xml',
        'views/employee_skill_views.xml',
        'views/performance_review_views.xml',
        'views/training_plan_views.xml',
        'views/hr_employee_views.xml',
        'reports/skills_report.xml',
        'reports/skills_report_template.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': False,
}
