# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Blockchain',
    'version': '1.0',
    'category': 'Education',
    'sequence': 90,
    'summary': '',
    'description': "",
    'website': '',
    'depends': [
        'mail',
    ],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/approval_file.xml',
        'views/approval_track.xml',
        'views/key.xml',
        'views/res_user.xml',
        'views/menu.xml',
        # 'views/res_partner_view.xml',
        # 'views/web.xml',
        # 'views/hide_contract.xml',

    ],
    'demo': [

    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
