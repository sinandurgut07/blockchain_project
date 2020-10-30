# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import requests
import json
from odoo import fields, models
from odoo.addons.blockchain.models.transaction import Transaction


class ApprovalTrack(models.Model):
    _name = "blockchain.approval_track"

    user_id = fields.Many2one('res.users', 'User')
    approval_file_id = fields.Many2one('blockchain.approval_file')
    status = fields.Selection([
        ('file_error', 'File Error'),
        ('file_change', 'File Change'),
        ('waiting_for_mining', 'Waiting for Mining'),
        ('approved', 'Approved'),
        ('pending', 'Pending'),
        ('pending_review', 'Pending Review'),
        ('rejected', 'Rejected'),
    ], string="Status", default='pending_review')
    process_time = fields.Datetime('Time')
    show_button = fields.Boolean(compute='compute_show_button')

    def compute_show_button(self):
        for i in self:
            if i.user_id.id == self.env.uid and i.status not in ['approved',
                                                              'rejected'] and i.approval_file_id.status == 'in_validation':
                i.show_button = True
            else:
                i.show_button = False

    def approve(self):
        for i in self:
            if len(i.user_id.key_ids) == 0:
                i.user_id.create_key()
            sender_pub_key = i.user_id.key_ids[0].public_key
            sender_pri_key = i.user_id.key_ids[0].private_key

            receiver = {
                'record_id': i.approval_file_id.id,
                'track_id': i.id,
                'user_id': i.user_id.id,
                'hash': i.approval_file_id.hash
            }
            receiver_str = json.dumps(receiver)
            transaction = Transaction(sender_pub_key, sender_pri_key,
                                      receiver_str, "1")
            url = "http://localhost:5000/transactions/new"
            data = {"sender_address": sender_pub_key, "recipient_address": receiver_str,
                    "amount": "1", "signature": transaction.sign_transaction()}

            requests.post(url, data)
            i.write({
                'status': 'waiting_for_mining'
            })

    def reject(self):
        for i in self:
            if len(i.user_id.key_ids) == 0:
                i.user_id.create_key()
            sender_pub_key = i.user_id.key_ids[0].public_key
            sender_pri_key = i.user_id.key_ids[0].private_key

            receiver = {
                'record_id': i.approval_file_id.id,
                'track_id': i.id,
                'user_id': i.user_id.id,
                'hash': i.approval_file_id.hash
            }
            receiver_str = json.dumps(receiver)
            transaction = Transaction(sender_pub_key, sender_pri_key,
                                      receiver_str, "0")
            url = "http://localhost:5000/transactions/new"
            data = {"sender_address": sender_pub_key, "recipient_address": receiver_str,
                    "amount": "0", "signature": transaction.sign_transaction()}

            requests.post(url, data)
            i.write({
                'status': 'waiting_for_mining'
            })

