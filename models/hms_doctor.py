from odoo import fields, models, api


class HMSDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor Model'

    first_name = fields.Char(string='First name')
    last_name = fields.Char(string='Last name')
    image = fields.Binary(string='Image')
    patient_ids = fields.One2many('hms.patient', 'doctor_id', string='Patients')
    name = fields.Char(string='Name', compute='_compute_name')


    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.first_name} {record.last_name}"
