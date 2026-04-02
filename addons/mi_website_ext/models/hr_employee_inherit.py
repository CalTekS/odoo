from odoo import models, fields, api

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    birthday = fields.Date(string="Birthday")

    has_incomplete_private_info = fields.Boolean(compute='_compute_incomplete_info')

    x_bank_account_num = fields.Char(string="Número de Cuenta Bancaria")
    x_bank_name = fields.Char(string="Nombre del Banco")

    @api.depends('private_email', 'private_phone', 'image_1920', 'identification_id', 'x_bank_account_num', 'x_bank_name', 'gender', 'birthday', 'place_of_birth', 'country_of_birth', 'marital', 'certificate', 'study_field', 'study_school', 'children', 'emergency_contact', 'emergency_phone') 
    def _compute_incomplete_info(self):
        for employee in self:
            required_fields = [
                employee.private_email,
                employee.private_phone,
                employee.image_1920,
                employee.x_bank_account_num,
                employee.x_bank_name,
                employee.identification_id,
                employee.country_id,
                employee.gender,
                employee.birthday,
                employee.place_of_birth,
                employee.country_of_birth,
                employee.certificate,
                employee.study_field,
                employee.study_school,
                employee.children,
                employee.emergency_contact,
                employee.emergency_phone
            ]
            employee.has_incomplete_private_info = not all(required_fields)

    @api.model
    def check_my_private_info(self):
        user = self.env.user
        employee = user.employee_id
        
        if not employee:
            return {'is_incomplete': False, 'url': '#', 'missing_fields': []}
        
        fields_to_check = {
            'image_1920': 'Foto de Perfil',
            'private_email': 'Correo Electrónico Privado',
            'private_phone': 'Teléfono Privado',
            'x_bank_account_num': 'Cuenta Bancaria', 
            'country_id': 'País de Nacimiento/Origen',
            'identification_id': 'Número de Identificación (Cédula/DNI)',
            'gender': 'Género',
            'x_bank_account_num': 'Número de Cuenta Bancaria',
            'x_bank_name': 'Nombre del Banco',
            'birthday': 'Fecha de Nacimiento',
            'place_of_birth': 'Lugar de Nacimiento',
            'marital': 'Estado Civil',
            'certificate': 'Nivel de Certificado',
            'study_field': 'Campo de Estudio',
            'study_school': 'Escuela/Universidad',
            'emergency_contact': 'Nombre del Contacto de Emergencia',
            'emergency_phone': 'Teléfono de Emergencia'
        }
        
        missing_fields = []
        
        for field, label in fields_to_check.items():
            if hasattr(employee, field) and not getattr(employee, field):
                missing_fields.append(label)
                
        profile_url = f"/odoo/action-198/{user.id}"
        
        return {
            'is_incomplete': len(missing_fields) > 0,
            'url': profile_url,
            'missing_fields': missing_fields 
        }

    def action_save_private_info(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}
    
    @api.depends('user_id', 'user_id.partner_id')
    def _compute_my_bank_partner(self):
        for record in self:
            if record.user_id and record.user_id.partner_id:
                record.my_bank_partner_id = record.user_id.partner_id.id
            else:
                record.my_bank_partner_id = False