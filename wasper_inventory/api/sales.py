import frappe
from frappe import _
from frappe.utils import getdate, add_days
from datetime import datetime

@frappe.whitelist()
def get_sales_summary(branch=None, from_date=None, to_date=None):
    """Get sales summary with filters"""
    if not from_date:
        from_date = add_days(getdate(), -30)
    if not to_date:
        to_date = getdate()
        
    conditions = []
    params = [from_date, to_date]
    
    if branch:
        conditions.append("si.branch = %s")
        params.append(branch)
        
    # Get total sales
    total_sales = frappe.db.sql("""
        SELECT 
            SUM(si.grand_total) as total_sales,
            COUNT(DISTINCT si.name) as total_invoices,
            AVG(si.grand_total) as avg_invoice_value
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        {conditions}
    """.format(conditions=" AND " + " AND ".join(conditions) if conditions else ""), 
    params, as_dict=1)[0]
    
    # Get sales by payment method
    sales_by_payment = frappe.db.sql("""
        SELECT 
            sip.mode_of_payment,
            SUM(sip.amount) as total_amount,
            COUNT(DISTINCT si.name) as invoice_count
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Payment` sip ON sip.parent = si.name
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        {conditions}
        GROUP BY sip.mode_of_payment
        ORDER BY total_amount DESC
    """.format(conditions=" AND " + " AND ".join(conditions) if conditions else ""), 
    params, as_dict=1)
    
    # Get sales by customer
    sales_by_customer = frappe.db.sql("""
        SELECT 
            si.customer,
            c.customer_name,
            SUM(si.grand_total) as total_sales,
            COUNT(DISTINCT si.name) as invoice_count,
            AVG(si.grand_total) as avg_invoice_value
        FROM `tabSales Invoice` si
        INNER JOIN `tabCustomer` c ON c.name = si.customer
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        {conditions}
        GROUP BY si.customer
        ORDER BY total_sales DESC
        LIMIT 10
    """.format(conditions=" AND " + " AND ".join(conditions) if conditions else ""), 
    params, as_dict=1)
    
    return {
        "total_sales": total_sales,
        "sales_by_payment": sales_by_payment,
        "top_customers": sales_by_customer
    }

@frappe.whitelist()
def get_sales_trend(branch=None, period="monthly"):
    """Get sales trend data"""
    if period == "monthly":
        group_by = "DATE_FORMAT(si.posting_date, '%Y-%m')"
        date_format = "%Y-%m"
    elif period == "weekly":
        group_by = "YEARWEEK(si.posting_date)"
        date_format = "%Y-%W"
    else:  # daily
        group_by = "si.posting_date"
        date_format = "%Y-%m-%d"
        
    conditions = []
    params = []
    
    if branch:
        conditions.append("si.branch = %s")
        params.append(branch)
        
    query = """
        SELECT 
            {group_by} as period,
            SUM(si.grand_total) as total_sales,
            COUNT(DISTINCT si.name) as invoice_count,
            AVG(si.grand_total) as avg_invoice_value
        FROM `tabSales Invoice` si
        WHERE si.docstatus = 1
    """
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
        
    query += " GROUP BY {group_by} ORDER BY period DESC LIMIT 12"
    
    return frappe.db.sql(query.format(group_by=group_by), params, as_dict=1)

@frappe.whitelist()
def get_sales_person_performance(branch=None, from_date=None, to_date=None):
    """Get sales performance by sales person"""
    if not from_date:
        from_date = add_days(getdate(), -30)
    if not to_date:
        to_date = getdate()
        
    conditions = []
    params = [from_date, to_date]
    
    if branch:
        conditions.append("si.branch = %s")
        params.append(branch)
        
    query = """
        SELECT 
            si.sales_person,
            u.full_name,
            COUNT(DISTINCT si.name) as invoice_count,
            SUM(si.grand_total) as total_sales,
            AVG(si.grand_total) as avg_invoice_value
        FROM `tabSales Invoice` si
        INNER JOIN `tabUser` u ON u.name = si.sales_person
        WHERE si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        AND si.sales_person IS NOT NULL
    """
    
    if conditions:
        query += " AND " + " AND ".join(conditions)
        
    query += " GROUP BY si.sales_person ORDER BY total_sales DESC"
    
    return frappe.db.sql(query, params, as_dict=1) 