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
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 120
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 120
        },
        {
            "label": _("Current Qty"),
            "fieldname": "current_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Reorder Level"),
            "fieldname": "reorder_level",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Reorder Qty"),
            "fieldname": "reorder_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Last Purchase Rate"),
            "fieldname": "last_purchase_rate",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    if not filters.get("branch"):
        frappe.throw(_("Please select a branch"))
        
    data = frappe.db.sql("""
        SELECT 
            i.item_code,
            i.item_name,
            b.warehouse,
            b.actual_qty as current_qty,
            i.reorder_level,
            i.reorder_qty,
            i.last_purchase_rate
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty <= i.reorder_level
        AND i.reorder_level > 0
        ORDER BY b.actual_qty ASC
    """, filters, as_dict=1)
    
    return data 