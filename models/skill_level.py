from odoo import fields, models


class HrSkillLevel(models.Model):
    _inherit = 'hr.skill.level'

    description = fields.Text(translate=True)
    behaviors = fields.Text(
        string='Observable Behaviors',
        translate=True,
        help='Describe observable behaviors expected at this proficiency level.',
    )
