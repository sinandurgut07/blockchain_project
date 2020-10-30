# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from odoo import fields, models


class ResUser(models.Model):
    _inherit = "res.users"

    key_ids = fields.One2many("blockchain.key", 'user_id')

    def create_key(self):
        random_gen = Crypto.Random.new().read
        private_key = RSA.generate(1024, random_gen)
        public_key = private_key.publickey()

        self.write({
            'key_ids': [(0, 0, {'private_key': binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'),
                                'public_key': binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'),
                                })]
        })
