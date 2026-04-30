from odoo import api, fields, models


class HrEmployeeSkill(models.Model):
    _inherit = 'hr.employee.skill'

    validated_by_id = fields.Many2one(
        'res.users',
        string='Validated By',
        readonly=True,
    )
    validation_date = fields.Date(readonly=True)
    target_level_id = fields.Many2one(
        'hr.skill.level',
        string='Target Level',
        help='Desired proficiency to reach — drives training plan.',
    )
    notes = fields.Text(string='Assessment Notes')
    last_evaluated = fields.Date(
        string='Last Evaluated',
        default=fields.Date.today,
    )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.target_level_id and rec.skill_level_id:
                if rec.target_level_id.level_progress > rec.skill_level_id.level_progress:
                    self.env['hr.training.plan'].sudo().create({
                        'employee_id': rec.employee_id.id,
                        'skill_id': rec.skill_id.id,
                        'current_level_id': rec.skill_level_id.id,
                        'target_level_id': rec.target_level_id.id,
                        'state': 'draft',
                    })
        return records

    def action_validate(self):
        for rec in self:
            rec.write({
                'validated_by_id': self.env.user.id,
                'validation_date': fields.Date.today(),
            })
