# -*- coding: utf-8 -*-
{
    'name': "Alumbrado Xalapa Florece",

    'summary': """
        Realice su reporte por favor """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Charly ",
    'website': "https://www.youtube.com/channel/UCLYNXm3oExJwUnV8eJU7dMQ/videos",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/energia.xml',
        'views/templates.xml',
     
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}