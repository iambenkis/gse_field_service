# -*- coding: utf-8 -*-

{
    "name": "GSE Field Service",
    "summary": """
        Customisation of Field Service module for GoShop Energy""",
    "description": """
    """,
    "author": "Benjamin Kisenge",
    "website": "https://github.com/GoShop-Energy/field-service",
    "category": "Customizations",
    "version": "0.1.8.7",
    "license": "LGPL-3",
    "depends": ["base", 
                "delivery",
                "industry_fsm",
                "industry_fsm_report",
                "project", 
                "product", 
                "sale",
                "sale_project",
                "sale_management",
                "stock"
                ],
    "data": [
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/project_task_views.xml",
        "reports/project_report_views.xml",
    ],
    "images": [
        "static/src/img/location.png",
    ],
    "assets": {"web.assets_backend": []},
}
