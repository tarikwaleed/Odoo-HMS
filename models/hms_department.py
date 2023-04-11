from odoo import fields, models, api


class HMSDepartment(models.Model):
    # this will be the name of the newly created table in the database
    # the dot will be replaced with userscore so the name will be hms_department

    # The underscore before _name and _description in the example code indicates that
    # these are internal variables for the Odoo framework to use,
    # and should not be modified directly by users of the module.

    _name = 'hms.department'
    _description = 'Department Model'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    is_opened = fields.Boolean(string='Is Opened', default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')

