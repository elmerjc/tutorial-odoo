from odoo import models, fields


class MantenimientoWizard(models.TransientModel):
    _name = 'gestion.mantenimiento.wizard'
    _description = 'Asistente para Registrar Mantenimiento'

    vehiculo_id = fields.Many2one(
        comodel_name='gestion.vehiculo',
        string='Vehículo',
        required=True,
        default=lambda self: self.env.context.get('active_id')
    )
    name = fields.Char(string='Descripción / Servicio', required=True)
    fecha = fields.Date(string='Fecha del Servicio', default=fields.Date.context_today, required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        required=True
    )
    costo = fields.Monetary(string='Costo', currency_field='currency_id', required=True)
    foto_ingreso = fields.Image(string='Foto de Ingreso', max_width=1920, max_height=1920)
    foto_salida = fields.Image(string='Foto de Salida', max_width=1920, max_height=1920)
    notas = fields.Text(string='Detalles del Taller')

    def action_registrar_mantenimiento(self):
        """Crea el registro real en gestion.mantenimiento, cambia el estado del vehículo y cierra la ventana."""
        self.ensure_one()
        self.env['gestion.mantenimiento'].create({
            'vehiculo_id': self.vehiculo_id.id,
            'name': self.name,
            'fecha': self.fecha,
            'currency_id': self.currency_id.id,
            'costo': self.costo,
            'foto_ingreso': self.foto_ingreso,
            'foto_salida': self.foto_salida,
            'notas': self.notas,
        })
        
        # Cambiar el estado del vehículo a 'mantenimiento'
        if self.vehiculo_id:
            self.vehiculo_id.estado = 'mantenimiento'
            
        return {'type': 'ir.actions.act_window_close'}