from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class PerformanceReview(models.Model):
    """
    Annual/semi-annual performance review cycle.
    Supports self-assessment, manager review, and optional peer reviews (360°).
    """
    _name = 'hr.performance.review'
    _description = 'Performance Review'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_start desc'

    name = fields.Char(required=True, tracking=True)
    employee_id = fields.Many2one(
        'hr.employee', required=True, index=True, tracking=True
    )
    reviewer_id = fields.Many2one(
        'hr.employee',
        string='Reviewer (Manager)',
        required=True,
        tracking=True,
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('self_assessment', 'Self Assessment'),
        ('manager_review', 'Manager Review'),
        ('calibration', 'Calibration'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)
    review_type = fields.Selection([
        ('annual', 'Annual Review'),
        ('mid_year', 'Mid-Year Review'),
        ('probation', 'End of Probation'),
        ('360', '360° Feedback'),
    ], default='annual', required=True)
    date_start = fields.Date(required=True, default=fields.Date.today)
    date_self_assessment_deadline = fields.Date(string='Self-Assessment Deadline')
    date_manager_review_deadline = fields.Date(string='Manager Review Deadline')

    line_ids = fields.One2many(
        'hr.performance.review.line', 'review_id', string='Competencies'
    )
    self_overall_score = fields.Selection([
        ('1', 'Below Expectations'),
        ('2', 'Partially Meets'),
        ('3', 'Meets Expectations'),
        ('4', 'Exceeds Expectations'),
        ('5', 'Outstanding'),
    ], string='Self Overall Rating')
    manager_overall_score = fields.Selection([
        ('1', 'Below Expectations'),
        ('2', 'Partially Meets'),
        ('3', 'Meets Expectations'),
        ('4', 'Exceeds Expectations'),
        ('5', 'Outstanding'),
    ], string='Manager Overall Rating', tracking=True)
    self_comments = fields.Text(string='Employee Comments')
    manager_comments = fields.Text(string='Manager Comments')
    objectives_next_period = fields.Text(string='Objectives for Next Period')
    development_plan = fields.Text(string='Development Plan')

    average_score = fields.Float(
        compute='_compute_average_score',
        store=True,
        digits=(3, 1),
    )

    @api.depends('line_ids.manager_score')
    def _compute_average_score(self):
        for review in self:
            scored_lines = review.line_ids.filtered(lambda l: l.manager_score)
            if scored_lines:
                total = sum(int(l.manager_score) for l in scored_lines)
                review.average_score = total / len(scored_lines)
            else:
                review.average_score = 0.0

    def action_start_self_assessment(self):
        for review in self:
            if review.state != 'draft':
                raise UserError(_('Review must be in Draft state to start.'))
            review.write({'state': 'self_assessment'})
            review.employee_id.user_id and review.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=review.employee_id.user_id.id,
                note=_('Please complete your self-assessment for review: %s') % review.name,
                date_deadline=review.date_self_assessment_deadline,
            )

    def action_submit_self_assessment(self):
        for review in self:
            review.write({'state': 'manager_review'})
            review.reviewer_id.user_id and review.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=review.reviewer_id.user_id.id,
                note=_('Please complete manager review for: %s') % review.name,
                date_deadline=review.date_manager_review_deadline,
            )

    def action_complete(self):
        for review in self:
            review.write({'state': 'completed'})
            review._update_employee_skills()

    def _update_employee_skills(self):
        """After review completion, update skill levels based on manager assessment."""
        self.ensure_one()
        for line in self.line_ids.filtered(lambda l: l.skill_id and l.new_level_id):
            existing = self.env['hr.employee.skill'].search([
                ('employee_id', '=', self.employee_id.id),
                ('skill_id', '=', line.skill_id.id),
            ], limit=1)
            if existing:
                existing.write({
                    'skill_level_id': line.new_level_id.id,
                    'last_evaluated': fields.Date.today(),
                })
            else:
                self.env['hr.employee.skill'].create({
                    'employee_id': self.employee_id.id,
                    'skill_id': line.skill_id.id,
                    'skill_level_id': line.new_level_id.id,
                    'skill_type_id': line.skill_id.skill_type_id.id,
                })

    @api.model
    def _cron_send_review_reminders(self):
        from datetime import date, timedelta
        today = date.today()
        in_3_days = today + timedelta(days=3)
        pending_self = self.search([
            ('state', '=', 'self_assessment'),
            ('date_self_assessment_deadline', '=', in_3_days),
        ])
        for review in pending_self:
            review.message_post(
                body=_('Reminder: Self-assessment deadline in 3 days.'),
                message_type='notification',
            )
        pending_manager = self.search([
            ('state', '=', 'manager_review'),
            ('date_manager_review_deadline', '=', in_3_days),
        ])
        for review in pending_manager:
            review.message_post(
                body=_('Reminder: Manager review deadline in 3 days.'),
                message_type='notification',
            )
