import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days

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
            "label": _("Last Purchase Date"),
            "fieldname": "last_purchase_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Last Sale Date"),
            "fieldname": "last_sale_date",
            "fieldtype": "Date",
            "width": 120
        },
        {
            "label": _("Days Since Last Sale"),
            "fieldname": "days_since_last_sale",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Current Value"),
            "fieldname": "current_value",
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
            i.last_purchase_date,
            i.last_sale_date,
            DATEDIFF(CURDATE(), i.last_sale_date) as days_since_last_sale,
            b.actual_qty * b.valuation_rate as current_value
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty > 0
        ORDER BY days_since_last_sale DESC, current_value DESC
    """, filters, as_dict=1)
    
    return data 