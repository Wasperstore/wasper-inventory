import frappe
from frappe import _
from frappe.utils import getdate, add_days, flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Date"),
            "fieldname": "date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Total Sales"),
            "fieldname": "total_sales",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Total Qty"),
            "fieldname": "total_qty",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("Total Transactions"),
            "fieldname": "total_transactions",
            "fieldtype": "Int",
            "width": 120
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
            si.posting_date as date,
            SUM(si.grand_total) as total_sales,
            SUM(sii.qty) as total_qty,
            COUNT(DISTINCT si.name) as total_transactions
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        WHERE si.docstatus = 1
        AND si.branch = %(branch)s
        AND si.posting_date BETWEEN %(from_date)s AND %(to_date)s
        GROUP BY si.posting_date
        ORDER BY si.posting_date
    """, filters, as_dict=1)
    
    return data 