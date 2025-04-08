import frappe

def execute():
    """Add branch fields to relevant DocTypes"""
    
    # Add branch field to Sales Invoice
    if not frappe.db.exists("Custom Field", {"dt": "Sales Invoice", "fieldname": "branch"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Sales Invoice",
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "company",
            "reqd": 1
        }).insert()
        
    # Add branch field to Purchase Invoice
    if not frappe.db.exists("Custom Field", {"dt": "Purchase Invoice", "fieldname": "branch"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Purchase Invoice",
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "company",
            "reqd": 1
        }).insert()
        
    # Add branch field to Stock Entry
    if not frappe.db.exists("Custom Field", {"dt": "Stock Entry", "fieldname": "branch"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Stock Entry",
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "company",
            "reqd": 1
        }).insert()
        
    # Add branch field to Warehouse
    if not frappe.db.exists("Custom Field", {"dt": "Warehouse", "fieldname": "branch"}):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Warehouse",
            "fieldname": "branch",
            "label": "Branch",
            "fieldtype": "Link",
            "options": "Branch",
            "insert_after": "parent_warehouse",
            "reqd": 1
        }).insert()
        
    frappe.db.commit() 