# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestResPartnerFieldService(TransactionCase):
    def setUp(self):
        super(TestResPartnerFieldService, self).setUp()

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "type": "field_service",
                "field_service_type": "solar",
            }
        )

    def test_get_field_service(self):
        # Test the get_field_service method
        action = self.partner.get_field_service()

        self.assertEqual(action["type"], "ir.actions.act_window")
        self.assertEqual(action["res_model"], "res.partner")
        self.assertIn(("type", "=", "field_service"), action["domain"])
        self.assertIn(("id", "in", self.partner.child_ids.ids), action["domain"])
        self.assertEqual(
            action["context"],
            {
                "create": False,
                "view_mode": "tree,form",
                "target": "main",
            },
        )

    def test_compute_count(self):
        # Test the compute_count method
        self.partner.compute_count()
        self.assertEqual(self.partner.service_field_count, 0)

        # Create a child partner with field_service type
        child_partner = self.env["res.partner"].create(
            {
                "name": "Child Partner",
                "type": "field_service",
                "field_service_type": "water_heater",
                "parent_id": self.partner.id,
            }
        )

        # Recompute the count
        self.partner.compute_count()
        self.assertEqual(self.partner.service_field_count, 1)
