from datetime import date

from odoo import models, fields, api
import logging

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HMSPatient(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char(string='First name', required=True)
    last_name = fields.Char(string='Last name', required=True)
    birth_date = fields.Date(string='Birth date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio', required=True, domain="[('pcr', '=', True)]", )
    blood_type = fields.Selection(
        string='Blood type',
        selection=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
    )
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age')
    department_id = fields.Many2one('hms.department', string='Department', domain=[('is_opened', '=', True)])
    doctor_id = fields.Many2one('hms.doctor', string='Doctor')
    STATE_SELECTION = [('undetermined', 'Undetermined'),
                       ('good', 'Good'),
                       ('fair', 'Fair'),
                       ('serious', 'Serious')]
    state = fields.Selection(STATE_SELECTION, default='undetermined')
    is_age_less_than_50 = fields.Boolean(compute='_compute_is_age_less_than_50', store=False)
    department_capacity = fields.Integer(string='Department Capacity', related='department_id.capacity')

    @api.constrains('cr_ratio', 'pcr')
    def _check_cr_ratio_required(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError('CR Ratio is required when PCR is checked.')

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                today = date.today()
                age = today.year - patient.birth_date.year - (
                        (today.month, today.day) < (patient.birth_date.month, patient.birth_date.day))
                patient.age = age
            else:
                patient.age = 0

    @api.depends('age')
    def _compute_is_age_less_than_50(self):
        for rec in self:
            rec.is_age_less_than_50 = rec.age < 50

    @api.model
    def create(self, vals):
        patient = super(HMSPatient, self).create(vals)
        log_vals = {
            'patient_id': patient.id,
            'note': 'New patient created'
        }
        self.env['hms.patient.log'].create(log_vals)
        return patient

    @api.onchange('state')
    def onchange_state(self):
        if self.state:
            note = f'State changed to {self.state}'
            self.env['hms.patient.log'].create({
                'patient_id': self.id,
                'note': note
            })

    @api.onchange('age')
    def _onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR field checked',
                    'message': 'The PCR field has been automatically checked due to the patient\'s age.'
                }
            }
        else:
            self.pcr = False
            return {}
#
# @api.model
# def create(self, vals):
#     patient = super(HMSPatient, self).create(vals)
#     department = patient.department_id
#     if department:
#         department_id = department.id
#         self.env['hms.department'].browse(department_id).write({'capacity': department.capacity + 1})
#     return patient

# @api.model
# def create(self, vals):
#     _logger.info("Creating a patient...")
#     patient = super(HMSPatient, self).create(vals)
#     department = patient.department_id
#     if department:
#         _logger.info("Incrementing department capacity...")
#         department.write({'capacity': department.capacity + 1})
#     _logger.info("Patient created.")
#     return patient
