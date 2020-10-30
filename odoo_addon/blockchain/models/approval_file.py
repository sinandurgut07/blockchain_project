# -*- coding: utf-8 -*-

import base64
import hashlib
from odoo import fields, models, api


class ApprovalFile(models.Model):
    _name = "blockchain.approval_file"
    _inherit = ['mail.thread']

    file = fields.Binary(attachment=True, required=True, track_visibility='onchange')
    file_name = fields.Char("File Name", track_visibility='onchange')
    state = fields.Selection([('waiting', 'Waiting'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             string="State", track_visibility='onchange', default='waiting')
    approval_track_ids = fields.One2many('blockchain.approval_track', 'approval_file_id', track_visibility='onchange')

    status = fields.Selection([
        ('file_change', 'File Change'),
        ('pending', 'Pending'),
        ('in_validation', 'In Validation'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='pending', required=True)
    hash = fields.Char("Hash", compute="compute_hash", store=True, track_visibility='onchange')

    @api.depends("file")
    def compute_hash(self):
        for i in self:
            if i.file:
                sha1_hash = hashlib.sha1(base64.b64decode(i.file))
                i.hash = sha1_hash.hexdigest()
            else:
                i.hash = False

    @api.onchange("file")
    def on_file_change(self):
        self.approval_track_ids.filtered(lambda x: x.status in ['approved', 'rejected']).write({
            'status': 'file_change'
        })

    def send_validation(self):
        for i in self:
            i.write({
                'status': 'in_validation'
            })

            i.approval_track_ids.write({
                'status': 'pending_review'
            })

    def cancel_validation(self):
        for i in self:
            i.write({
                'status': 'pending'
            })
            i.approval_track_ids.write({
                'status': 'pending_review'
            })
