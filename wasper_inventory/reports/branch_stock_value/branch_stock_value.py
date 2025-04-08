import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

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
            "label": _("Average Rate"),
            "fieldname": "avg_rate",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    if not filters.get("branch"):
        frappe.throw(_("Please select a branch"))
        
    data = frappe.db.sql("""
        SELECT 
            i.item_group,
            SUM(b.actual_qty) as total_qty,
            SUM(b.actual_qty * b.valuation_rate) as total_value,
            SUM(b.actual_qty * b.valuation_rate) / SUM(b.actual_qty) as avg_rate
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty > 0
        GROUP BY i.item_group
        ORDER BY total_value DESC
    """, filters, as_dict=1)
    
    return data 