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
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150
        },
        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
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
            "label": _("Average Order Value"),
            "fieldname": "avg_order_value",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Total Orders"),
            "fieldname": "total_orders",
            "fieldtype": "Int",
            "width": 100
        },
        {
            "label": _("Last Order Date"),
            "fieldname": "last_order_date",
            "fieldtype": "Date",
            "width": 100
        }
    ]

def get_data(filters):
    conditions = get_conditions(filters)
    data = frappe.db.sql("""
        SELECT 
            si.customer,
            c.customer_name,
            si.branch,
            SUM(si.grand_total) as total_sales,
            SUM(sii.qty) as total_qty,
            SUM(si.grand_total) / COUNT(DISTINCT si.name) as avg_order_value,
            COUNT(DISTINCT si.name) as total_orders,
            MAX(si.posting_date) as last_order_date
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        INNER JOIN `tabCustomer` c ON c.name = si.customer
        WHERE {conditions}
        GROUP BY si.customer, si.branch
        ORDER BY total_sales DESC
    """.format(conditions=conditions), filters, as_dict=1)
    
    return data

def get_conditions(filters):
    conditions = ["si.docstatus = 1"]
    
    if filters.get("company"):
        conditions.append("si.company = %(company)s")
        
    if filters.get("branch"):
        conditions.append("si.branch = %(branch)s")
        
    if filters.get("customer"):
        conditions.append("si.customer = %(customer)s")
        
    if filters.get("from_date"):
        conditions.append("si.posting_date >= %(from_date)s")
        
    if filters.get("to_date"):
        conditions.append("si.posting_date <= %(to_date)s")
        
    return " AND ".join(conditions) 