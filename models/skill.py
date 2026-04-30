from odoo import fields, models


class HrSkill(models.Model):
    _inherit = 'hr.skill'

    description = fields.Text(translate=True)
    is_technical = fields.Boolean(
        string='Technical Skill',
        help='Differentiates hard skills from soft skills.',
    )
    career_path_ids = fields.Many2many(
        'hr.career.path',
        'career_path_skill_rel',
        'skill_id', 'career_path_id',
        string='Required In Career Paths',
    )
