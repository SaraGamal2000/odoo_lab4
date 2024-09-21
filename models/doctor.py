
from odoo  import models ,fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'

    first_name=fields.Char( required=True)
    last_name=fields.Char( required=True)
    image=fields.Binary()
    # patient_ids=fields.One2many('hms.patient','doctor_id')
    patient_ids=fields.Many2many('hms.patient','hms_patient_doctor', 'patient_id', 'doctor_id')