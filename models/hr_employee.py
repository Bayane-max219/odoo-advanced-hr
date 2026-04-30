from odoo import api, fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    performance_review_ids = fields.One2many(
        'hr.performance.review', 'employee_id', string='Performance Reviews'
    )
    performance_review_count = fields.Integer(
        compute='_compute_performance_review_count'
    )
    training_plan_ids = fields.One2many(
        'hr.training.plan', 'employee_id', string='Training Plans'
    )
    training_plan_count = fields.Integer(
        compute='_compute_training_plan_count'
    )
    skills_gap_count = fields.Integer(
        compute='_compute_skills_gap_count',
        string='Skill Gaps',
        help='Number of skills where current level < target level.',
    )
    last_review_date = fields.Date(
        compute='_compute_last_review_date',
        store=True,
        string='Last Review',
    )
    overall_performance_score = fields.Float(
        compute='_compute_overall_performance_score',
        store=True,
        digits=(3, 1),
        string='Performance Score',
    )

    @api.depends('performance_review_ids')
    def _compute_performance_review_count(self):
        for emp in self:
            emp.performance_review_count = len(emp.performance_review_ids)

    def _compute_training_plan_count(self):
        for emp in self:
            emp.training_plan_count = len(emp.training_plan_ids.filtered(
                lambda t: t.state in ('draft', 'in_progress')
            ))

    def _compute_skills_gap_count(self):
        for emp in self:
            emp.skills_gap_count = len(emp.employee_skill_ids.filtered(
                lambda s: s.target_level_id
                and s.skill_level_id.level_progress < s.target_level_id.level_progress
            ))

    @api.depends('performance_review_ids.state', 'performance_review_ids.date_start')
    def _compute_last_review_date(self):
        for emp in self:
            completed = emp.performance_review_ids.filtered(
                lambda r: r.state == 'completed'
            )
            emp.last_review_date = max(completed.mapped('date_start')) if completed else False

    @api.depends('performance_review_ids.average_score', 'performance_review_ids.state')
    def _compute_overall_performance_score(self):
        for emp in self:
            completed = emp.performance_review_ids.filtered(
                lambda r: r.state == 'completed' and r.average_score
            )
            if completed:
                emp.overall_performance_score = sum(r.average_score for r in completed) / len(completed)
            else:
                emp.overall_performance_score = 0.0

    def action_view_performance_reviews(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Performance Reviews',
            'res_model': 'hr.performance.review',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }

    def action_view_training_plans(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Training Plans',
            'res_model': 'hr.training.plan',
            'view_mode': 'list,form',
            'domain': [('employee_id', '=', self.id)],
            'context': {'default_employee_id': self.id},
        }
