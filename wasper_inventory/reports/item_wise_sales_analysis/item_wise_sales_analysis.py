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
            "width": 200
        },
        {
            "label": _("Branch"),
            "fieldname": "branch",
            "fieldtype": "Link",
            "options": "Branch",
            "width": 120
        },
        {
            "label": _("Total Qty"),
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Total Amount"),
            "fieldname": "total_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Average Rate"),
            "fieldname": "avg_rate",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Total Tax"),
            "fieldname": "total_tax",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Net Amount"),
            "fieldname": "net_amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    data = frappe.db.sql("""
        SELECT 
            sii.item_code,
            sii.item_name,
            si.branch,
            SUM(sii.qty) as total_qty,
            SUM(sii.amount) as total_amount,
            SUM(sii.amount) / SUM(sii.qty) as avg_rate,
            SUM(sii.tax_amount) as total_tax,
            SUM(sii.net_amount) as net_amount
        FROM `tabSales Invoice Item` sii
        INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
        WHERE {conditions}
        GROUP BY sii.item_code, si.branch
        ORDER BY total_amount DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ["si.docstatus = 1"]
    
    if filters.get("company"):
        conditions.append("si.company = %(company)s")
        
    if filters.get("branch"):
        conditions.append("si.branch = %(branch)s")
        
    if filters.get("item_code"):
        conditions.append("sii.item_code = %(item_code)s")
        
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        
    return " AND ".join(conditions) 