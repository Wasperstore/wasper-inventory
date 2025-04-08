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
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Supplier"),
            "fieldname": "supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "width": 150
        },
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
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 80
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        }
    ]

def get_data(filters):
    if not filters.get("branch"):
        frappe.throw(_("Please select a branch"))
        
    if not filters.get("from_date"):
        filters["from_date"] = add_days(getdate(), -30)
        
    if not filters.get("to_date"):
        filters["to_date"] = getdate()
        
    data = frappe.db.sql("""
        SELECT 
            pi.posting_date,
            pi.supplier,
            pii.item_code,
            pii.item_name,
            pii.qty,
            pii.rate,
            pii.amount,
            pi.status
        FROM `tabPurchase Invoice` pi
        INNER JOIN `tabPurchase Invoice Item` pii ON pii.parent = pi.name
        WHERE pi.docstatus = 1
        AND pi.branch = %(branch)s
        AND pi.posting_date BETWEEN %(from_date)s AND %(to_date)s
        ORDER BY pi.posting_date DESC, pi.creation DESC
    """, filters, as_dict=1)
    
    return data 