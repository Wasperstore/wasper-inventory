import frappe
from frappe import _
from frappe.utils import getdate, flt

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data

def get_columns():
    return [
        {
            "label": _("Time"),
            "fieldname": "time",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Invoice"),
            "fieldname": "invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Payment Method"),
            "fieldname": "payment_method",
            "fieldtype": "Data",
            "width": 150
        }
    ]

def get_data(filters):
    today = getdate()
    data = frappe.db.sql("""
        SELECT 
            TIME_FORMAT(si.posting_time, '%%H:%%i') as time,
            si.name as invoice,
            si.customer,
            si.grand_total as amount,
            GROUP_CONCAT(DISTINCT sip.mode_of_payment) as payment_method
        FROM `tabSales Invoice` si
        LEFT JOIN `tabSales Invoice Payment` sip ON sip.parent = si.name
        WHERE si.docstatus = 1
        AND si.posting_date = %s
        AND si.branch = %s
        GROUP BY si.name
        ORDER BY si.posting_time DESC
        LIMIT 10
    """, (today, filters.get("branch")), as_dict=1)
    
    return data 