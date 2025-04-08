import frappe

def execute():
    """Add custom fields to various DocTypes"""
    
    # Add custom fields to Branch
    branch_fields = [
        {
            "fieldname": "branch_manager",
            "label": "Branch Manager",
            "fieldtype": "Link",
            "options": "User",
            "insert_after": "branch_name"
        },
        {
            "fieldname": "contact_number",
            "label": "Contact Number",
            "fieldtype": "Data",
            "insert_after": "branch_manager"
        },
        {
            "fieldname": "email_id",
            "label": "Email ID",
            "fieldtype": "Data",
            "insert_after": "contact_number"
        },
        {
            "fieldname": "opening_hours",
            "label": "Opening Hours",
            "fieldtype": "Small Text",
            "insert_after": "email_id"
        },
        {
            "fieldname": "target_sales",
            "label": "Monthly Sales Target",
            "fieldtype": "Currency",
            "insert_after": "opening_hours"
        },
        {
            "fieldname": "branch_type",
            "label": "Branch Type",
            "fieldtype": "Select",
            "options": "Retail\nWholesale\nWarehouse",
            "insert_after": "target_sales"
        },
        {
            "fieldname": "is_active",
            "label": "Is Active",
            "fieldtype": "Check",
            "default": "1",
            "insert_after": "branch_type"
        }
    ]
    
    for field in branch_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Branch", "fieldname": field["fieldname"]}):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Branch",
                **field
            }).insert()
            
    # Add custom fields to Item
    item_fields = [
        {
            "fieldname": "min_selling_price",
            "label": "Minimum Selling Price",
            "fieldtype": "Currency",
            "insert_after": "standard_rate"
        },
        {
            "fieldname": "max_selling_price",
            "label": "Maximum Selling Price",
            "fieldtype": "Currency",
            "insert_after": "min_selling_price"
        },
        {
            "fieldname": "shelf_life",
            "label": "Shelf Life (Days)",
            "fieldtype": "Int",
            "insert_after": "max_selling_price"
        },
        {
            "fieldname": "is_serialized",
            "label": "Is Serialized",
            "fieldtype": "Check",
            "default": "0",
            "insert_after": "shelf_life"
        },
        {
            "fieldname": "is_batch_item",
            "label": "Is Batch Item",
            "fieldtype": "Check",
            "default": "0",
            "insert_after": "is_serialized"
        },
        {
            "fieldname": "hsn_code",
            "label": "HSN Code",
            "fieldtype": "Data",
            "insert_after": "is_batch_item"
        },
        {
            "fieldname": "gst_rate",
            "label": "GST Rate",
            "fieldtype": "Percent",
            "insert_after": "hsn_code"
        },
        {
            "fieldname": "item_barcode",
            "label": "Barcode",
            "fieldtype": "Data",
            "insert_after": "gst_rate"
        }
    ]
    
    for field in item_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": field["fieldname"]}):
            frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Item",
                **field
            }).insert()
            
    frappe.db.commit() 