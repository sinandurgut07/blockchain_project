# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
from odoo import _, fields, http
from odoo.http import Controller, route, request


class MiningCallback(Controller):

    @http.route('/test_view', type='http', auth="public", website=True)
    def test_view(self, **kw):
        return http.request.render('test_website.test_view')

    @route('/mining/callback', type='json', auth='none', methods=['POST'], csrf=False)
    def set_complete(self, **post):
        if post['sender_address'] != 'THE BLOCKCHAIN':
            recipient_address = json.loads(post['recipient_address'])

            q = request.env['blockchain.approval_track'].sudo().search([('id', '=', recipient_address['track_id'])])
            if q:
                if q.approval_file_id.hash == recipient_address['hash']:
                    q.write({
                        'status': 'approved' if post['value'] == "1" else 'rejected'
                    })
                    record = request.env['blockchain.approval_file'].sudo().search(
                        [('id', '=', recipient_address['record_id'])])
                    if post['value'] == '0':
                        q.approval_file_id.write({
                            'status': 'rejected'
                        })
                    elif record.approval_track_ids.filtered(
                            lambda x: x.status in ['approved']).__len__() == record.approval_track_ids.__len__():
                        q.approval_file_id.write({
                            'status': 'approved'
                        })
                else:
                    q.write({
                        'status': 'file_error'
                    })

            request.env['blockchain.mining_response'].sudo().create({
                'sender_address': post['sender_address'],
                'recipient_address': post['recipient_address'],
                'amount': post['value'],
            })
        return {}
