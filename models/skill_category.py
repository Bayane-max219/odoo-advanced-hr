from odoo import fields, models


class HrSkillCategory(models.Model):
    _inherit = 'hr.skill.type'

    description = fields.Text(translate=True)
    color = fields.Integer(string='Color Index', default=0)
    icon = fields.Char(
        string='Icon Class',
        help='Font Awesome icon class, e.g. fa-code',
        default='fa-star',
    )
    skill_count = fields.Integer(compute='_compute_skill_count')

    def _compute_skill_count(self):
        for category in self:
            category.skill_count = len(category.skill_ids)
