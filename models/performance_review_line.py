from odoo import fields, models

SCORE_SELECTION = [
    ('1', '1 — Below Expectations'),
    ('2', '2 — Partially Meets'),
    ('3', '3 — Meets Expectations'),
    ('4', '4 — Exceeds Expectations'),
    ('5', '5 — Outstanding'),
]


class PerformanceReviewLine(models.Model):
    _name = 'hr.performance.review.line'
    _description = 'Review Line'
    _order = 'sequence, id'

    review_id = fields.Many2one(
        'hr.performance.review', required=True, ondelete='cascade'
    )
    sequence = fields.Integer(default=10)
    name = fields.Char(string='Competency / Objective', required=True, translate=True)
    skill_id = fields.Many2one('hr.skill', string='Related Skill')
    current_level_id = fields.Many2one('hr.skill.level', string='Current Level')
    new_level_id = fields.Many2one('hr.skill.level', string='Level After Review')
    self_score = fields.Selection(SCORE_SELECTION, string='Self Rating')
    manager_score = fields.Selection(SCORE_SELECTION, string='Manager Rating')
    self_comment = fields.Text(string='Employee Comment')
    manager_comment = fields.Text(string='Manager Comment')
    weight = fields.Float(default=1.0, string='Weight')
