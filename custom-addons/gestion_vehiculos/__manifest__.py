{
    'name': 'Gestión de Vehículos',
    'version': '19.0.1.0.0',
    'summary': 'Módulo para el control y seguimiento de flota vehicular',
    'category': 'Operations',
    'author': 'Jorge',
    'depends': ['base', 'hr'],  # hr Dependencia para acceder a los empleados 
    'data': [
        'security/ir.model.access.csv',
        'wizards/mantenimiento_wizard_views.xml',  # Vista del wizard 
        'views/vehiculo_views.xml',
        'report/vehiculo_report_views.xml',
        'report/vehiculo_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}