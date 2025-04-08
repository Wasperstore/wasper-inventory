import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days, cint
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        filters = {}
        
    if not filters.get("branch"):
        frappe.throw(_("Please select a branch"))
        
    data = get_data(filters)
    columns = get_columns()
    chart_data = get_chart_data(data)
    
    return columns, data, None, chart_data

def get_columns():
    return [
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 150
        },
        {
            "label": _("Total Items"),
            "fieldname": "total_items",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Total Qty"),
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Total Value"),
            "fieldname": "total_value",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Low Stock Items"),
            "fieldname": "low_stock_items",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Slow Moving Items"),
            "fieldname": "slow_moving_items",
            "fieldtype": "Int",
            "width": 120
        }
    ]

def get_data(filters):
    data = frappe.db.sql("""
        SELECT 
            i.item_group,
            COUNT(DISTINCT b.item_code) as total_items,
            SUM(b.actual_qty) as total_qty,
            SUM(b.actual_qty * b.valuation_rate) as total_value,
            SUM(CASE WHEN b.actual_qty <= i.reorder_level AND i.reorder_level > 0 THEN 1 ELSE 0 END) as low_stock_items,
            SUM(CASE WHEN DATEDIFF(CURDATE(), i.last_sale_date) > 90 THEN 1 ELSE 0 END) as slow_moving_items
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty > 0
        GROUP BY i.item_group
        ORDER BY total_value DESC
    """, filters, as_dict=1)
    
    return data

def get_chart_data(data):
    return {
        "data": {
            "labels": [d.get("item_group") for d in data],
            "datasets": [
                {
                    "name": "Total Value",
                    "values": [d.get("total_value") for d in data]
                },
                {
                    "name": "Low Stock Items",
                    "values": [d.get("low_stock_items") for d in data]
                },
                {
                    "name": "Slow Moving Items",
                    "values": [d.get("slow_moving_items") for d in data]
                }
            ]
        },
        "type": "bar",
        "height": 300
    } 