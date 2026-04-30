from odoo import fields, models


class HrTrainingPlan(models.Model):
    """
    Links a skill gap to a concrete training action with budget and timeline.
    Auto-created when a skill with target_level > current_level is added.
    """
    _name = 'hr.training.plan'
    _description = 'Training Plan'
    _inherit = ['mail.thread']
    _order = 'deadline'

    employee_id = fields.Many2one('hr.employee', required=True, index=True)
    skill_id = fields.Many2one('hr.skill', required=True)
    current_level_id = fields.Many2one('hr.skill.level', string='Current Level')
    target_level_id = fields.Many2one('hr.skill.level', string='Target Level')
    state = fields.Selection([
        ('draft', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)
    training_type = fields.Selection([
        ('internal', 'Internal Training'),
        ('external', 'External Course'),
        ('e_learning', 'E-Learning'),
        ('coaching', 'Coaching / Mentoring'),
        ('conference', 'Conference'),
    ], default='external')
    provider = fields.Char(string='Training Provider')
    cost = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id,
    )
    deadline = fields.Date(string='Completion Deadline')
    completion_date = fields.Date(string='Actual Completion Date')
    notes = fields.Text()
    department_id = fields.Many2one(related='employee_id.department_id', store=True)

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_complete(self):
        for rec in self:
            rec.write({
                'state': 'completed',
                'completion_date': fields.Date.today(),
            })
            # Automatically update the employee skill level
            skill = self.env['hr.employee.skill'].search([
                ('employee_id', '=', rec.employee_id.id),
                ('skill_id', '=', rec.skill_id.id),
            ], limit=1)
            if skill and rec.target_level_id:
                skill.write({'skill_level_id': rec.target_level_id.id})
