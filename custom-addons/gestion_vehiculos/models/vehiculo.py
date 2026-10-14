from odoo import models, fields, api

class GestionVehiculo(models.Model):
    _name = 'gestion.vehiculo'
    _description = 'Registro de Vehículo'

    name = fields.Char(string='Matrícula / Placa', required=True)
    
    # Foto del vehículo
    image_1920 = fields.Image(string='Foto del Vehículo', max_width=1920, max_height=1920)

    marca = fields.Char(string='Marca', required=True)
    modelo = fields.Char(string='Modelo', required=True)
    anio = fields.Integer(string='Año del Modelo')
    estado = fields.Selection([
        ('disponible', 'Disponible'),
        ('mantenimiento', 'En Mantenimiento'),
        ('asignado', 'Asignado')
    ], string='Estado', default='disponible', required=True)
    
    # Relación Many2one con empleados
    conductor_id = fields.Many2one(
        comodel_name='hr.employee', 
        string='Conductor Asignado',
        ondelete='set null'
    )

    # Relación One2many hacia Mantenimientos
    mantenimiento_ids = fields.One2many(
        comodel_name='gestion.mantenimiento',
        inverse_name='vehiculo_id',
        string='Historial de Mantenimientos'
    )

    # Moneda referencial para el costo total (compañía actual)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id
    )

    # 1. CAMPO COMPUTADO: Contador de Mantenimientos
    mantenimiento_count = fields.Integer(
        string='N° Mantenimientos',
        compute='_compute_mantenimiento_stats'
    )

    # 2. CAMPO COMPUTADO: Costo Total Acumulado
    costo_total_mantenimiento = fields.Monetary(
        string='Total Mantenimientos',
        compute='_compute_mantenimiento_stats',
        currency_field='currency_id'
    )
    # Campo Computado : Promedio Total
    promedio_mantenimiento = fields.Monetary(
        string='Promedio Total',
        compute='_compute_mantenimiento_stats',
        currency_field='currency_id'
    )

    # Cálculo unificado de ambas métricas
    @api.depends('mantenimiento_ids', 'mantenimiento_ids.costo')
    def _compute_mantenimiento_stats(self):
        for record in self:
            record.mantenimiento_count = len(record.mantenimiento_ids)
            record.costo_total_mantenimiento = sum(m.costo for m in record.mantenimiento_ids)
            cantidad = 1 if record.mantenimiento_count == 0 else record.mantenimiento_count
            record.promedio_mantenimiento = (record.costo_total_mantenimiento / cantidad)

    # Acción invocada por los Smart Buttons
    def action_view_mantenimientos(self):
        self.ensure_one()
        return {
            'name': 'Historial de Mantenimientos',
            'type': 'ir.actions.act_window',
            'res_model': 'gestion.mantenimiento',
            'view_mode': 'list,form',
            'domain': [('vehiculo_id', '=', self.id)],
            'context': {'default_vehiculo_id': self.id},
        }

    notas = fields.Text(string='Notas adicionales')


class GestionMantenimiento(models.Model):
    _name = 'gestion.mantenimiento'
    _description = 'Registro de Mantenimiento de Vehículo'

    name = fields.Char(string='Descripción / Servicio', required=True)
    fecha = fields.Date(string='Fecha del Servicio', default=fields.Date.context_today, required=True)
    
    # Moneda referencial por defecto
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id,
        ondelete='restrict'
    )
    
    # Campo monetario
    costo = fields.Monetary(string='Costo', currency_field='currency_id', required=True)
    
    # Relación Many2one hacia Vehículo
    vehiculo_id = fields.Many2one(
        comodel_name='gestion.vehiculo',
        string='Vehículo',
        required=True,
        ondelete='cascade'
    )

    # Campos para registro fotográfico
    foto_ingreso = fields.Image(string='Foto de Ingreso', max_width=1920, max_height=1920)
    foto_salida = fields.Image(string='Foto de Salida', max_width=1920, max_height=1920)
    
    notas = fields.Text(string='Detalles del Taller')