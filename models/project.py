# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    sale_order_id = fields.Many2one(
        "sale.order",
        "Sales Order",
        store=True,
        help="Sales order to which the task is linked.",
    )

    order_line_table = fields.Html(
        string="HTML Field",
    )

    product_ids = fields.Many2many(
        "product.product", string="Products", compute="_compute_product_ids", store=True
    )
    warehouse_id = fields.Many2one(related="sale_order_id.warehouse_id")
    order_line = fields.One2many(
        comodel_name="sale.order.line",
        related="sale_order_id.order_line",
        readonly=False,
    )

    delivery_count = fields.Integer(related="sale_order_id.delivery_count")
    picking_ids = fields.One2many(related="sale_order_id.picking_ids")
    partner_id = fields.Many2one(related="sale_order_id.partner_id")
    child_id = fields.Many2one(related="sale_order_id.child_id", readonly=False)

    tag_ids = fields.Many2many("project.tags", string="Tags", readonly=False)
    company_id = fields.Many2one(comodel_name="res.company")

    has_default_tag = fields.Boolean(string="Default Tag Created", default=False)

    @api.depends("sale_order_id")
    def _compute_product_ids(self):
        for task in self:
            task.product_ids = task.sale_order_id.order_line.mapped("product_id")

    def action_view_delivery(self):
        return self._get_action_view_picking(self.picking_ids)

    def _get_action_view_picking(self, pickings):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.action_picking_tree_all"
        )
        if len(pickings) > 1:
            action["domain"] = [("id", "in", pickings.ids)]
        elif len(pickings) == 1:
            action["views"] = [(self.env.ref("stock.view_picking_form").id, "form")]
            action["res_id"] = pickings.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action

    def action_fs_navigate(self):
        if not self.child_id.city or not self.child_id.country_id:
            return {
                "name": _("Service Location"),
                "type": "ir.actions.act_window",
                "res_model": "res.partner",
                "res_id": self.child_id.id,
                "view_mode": "form",
                "view_id": self.env.ref(
                    "industry_fsm.view_partner_address_form_industry_fsm"
                ).id,
                "target": "new",
            }
        return self.child_id.action_partner_navigate()
