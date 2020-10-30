# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class Key(models.Model):
    _name = "blockchain.key"

    public_key = fields.Char("Public Key")
    private_key = fields.Char("Private Key")

    user_id = fields.Many2one("res.users", "User")
    active = fields.Boolean("Active", default=True)
