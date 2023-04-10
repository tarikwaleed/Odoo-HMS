from odoo import models, fields


class HmsPatient(models.Model):
    _name = 'hms.patient'


    first_name = fields.Char(string='First name')
    last_name = fields.Char(string='Last name')
    birth_date = fields.Date(string='Birth date')
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection(
        string='Blood type',
        selection=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')],
    )
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)

    def _compute_age(self):
        for record in self:
            if record.birth_date:
                record.age = (fields.Date.today() - record.birth_date) // 365
