
from odoo  import models ,fields,api
from odoo.exceptions import ValidationError, UserError
from odoo.tools.populate import compute
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    first_name=fields.Char( required=True)
    last_name=fields.Char( required=True)
    birth_date=fields.Date()
    history=fields.Html()
    cr_ratio=fields.Float()
    pcr = fields.Boolean(compute='_compute_pcr',store=True)
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='calculate_age',store=True)
    blood_type=fields.Selection([
        ('a','A'),
        ('b','B'),
        ('o','O'),
        ('ab','AB')])
    state=fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious')],default="fair")
    department_id=fields.Many2one('hms.department',domain=[('is_opened','=',True)])
    department_capacity = fields.Integer(compute='compute_department_capacity',store=True)
    # doctor_id=fields.Many2one('hms.doctor')
    doctor_ids=fields.Many2many('hms.doctor','hms_patient_doctor', 'doctor_id','patient_id')
    log_history_ids=fields.One2many('hms.patient.log.history','log_patient_id')

    log_state_ids=fields.One2many("hms.log.state","patient_state_id")

    @api.depends('birth_date')
    def calculate_age(self):
        for rec in self:
            if rec.birth_date:
                rec.age=relativedelta(fields.Date.today(), rec.birth_date).years
            else:
                rec.age= 0

    def state_good(self):
        for rec in self:
            rec.write({'state':'good'})
            rec.env['hms.log.state'].create({
                'patient_state_id' : rec.id,
                'description':'state changed to good'
            })
    def state_fair(self):
        for rec in self:
            rec.write({'state': 'fair'})
            rec.env['hms.log.state'].create({
                'patient_state_id': rec.id,
                'description': 'state changed to fair'
            })
    def state_undetermined(self):
        for rec in self:
            rec.write({'state': 'undetermined'})
            rec.env['hms.log.state'].create({
                'patient_state_id': rec.id,
                'description': 'state changed to undetermined'
            })
    def state_serious(self):
        for rec in self:
            rec.write({'state': 'serious'})
            rec.env['hms.log.state'].create({
                'patient_state_id': rec.id,
                'description': 'state changed to serious'
            })


    @api.depends('department_id')
    def compute_department_capacity(self):
        for cap in self:
            if cap.department_id:
                cap.department_capacity = cap.department_id.capacity
            else:
                cap.department_capacity = 0

    @api.depends('age')
    def _compute_pcr(self):
        for rec in self:
            if rec.age < 30:
                rec.pcr = True
            else:
                rec.pcr = False


    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR Ratio is required please")



class Log_State(models.Model):
    _name = "hms.log.state"
    _description = "add new log for every state"

    patient_state_id = fields.Many2one('hms.patient', string="Patient log", required=True)
    description=fields.Text()



class Log_History(models.Model):
    _name = "hms.patient.log.history"
    _description = " log history of patient"

    log_patient_id=fields.Many2one('hms.patient')
    created_by=fields.Char()
    date=fields.Date()
    description=fields.Text()







# description = fields.Text(string="Description")
#     state = fields.Selection([
#         ('undetermined', 'Undetermined'),
#         ('good', 'Good'),
#         ('fair', 'Fair'),
#         ('serious', 'Serious')], string="State")
#
#     log_state_id=fields.Many2one('hms.patient')