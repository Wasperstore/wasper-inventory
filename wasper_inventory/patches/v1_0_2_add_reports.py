import frappe

def execute():
    """Add custom reports to the system"""
    
    # Add Branch Sales Trend Report
    if not frappe.db.exists("Report", "Branch Sales Trend"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Branch Sales Trend",
            "report_name": "Branch Sales Trend",
            "ref_doctype": "Sales Invoice",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    # Add Branch Stock Value Report
    if not frappe.db.exists("Report", "Branch Stock Value"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Branch Stock Value",
            "report_name": "Branch Stock Value",
            "ref_doctype": "Stock Ledger Entry",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    # Add Low Stock Items Report
    if not frappe.db.exists("Report", "Low Stock Items"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Low Stock Items",
            "report_name": "Low Stock Items",
            "ref_doctype": "Item",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    # Add Recent Transactions Report
    if not frappe.db.exists("Report", "Recent Transactions"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Recent Transactions",
            "report_name": "Recent Transactions",
            "ref_doctype": "Sales Invoice",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    # Add Customer-wise Sales Analysis Report
    if not frappe.db.exists("Report", "Customer-wise Sales Analysis"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Customer-wise Sales Analysis",
            "report_name": "Customer-wise Sales Analysis",
            "ref_doctype": "Sales Invoice",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    # Add Today's Sales Report
    if not frappe.db.exists("Report", "Today's Sales"):
        frappe.get_doc({
            "doctype": "Report",
            "name": "Today's Sales",
            "report_name": "Today's Sales",
            "ref_doctype": "Sales Invoice",
            "is_standard": "No",
            "module": "Wasper Inventory",
            "report_type": "Report Builder"
        }).insert()
        
    frappe.db.commit() 