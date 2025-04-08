import frappe
from frappe import _
from frappe.utils import getdate, add_days
from datetime import datetime

@frappe.whitelist()
def get_branch_details(branch):
    """Get detailed information about a branch"""
    if not branch:
        frappe.throw(_("Branch is required"))
        
    branch_doc = frappe.get_doc("Branch", branch)
    
    # Get branch manager details
    manager_details = {}
    if branch_doc.branch_manager:
        manager_details = frappe.get_doc("User", branch_doc.branch_manager).as_dict()
        
    # Get current stock value
    stock_value = frappe.db.sql("""
        SELECT SUM(b.actual_qty * b.valuation_rate) as total_value
        FROM `tabBin` b
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %s
        AND b.actual_qty > 0
    """, branch, as_dict=1)[0].total_value or 0
    
    # Get today's sales
    today_sales = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Invoice`
        WHERE branch = %s
        AND docstatus = 1
        AND posting_date = %s
    """, (branch, getdate()), as_dict=1)[0].total or 0
    
    # Get low stock items count
    low_stock_count = frappe.db.sql("""
        SELECT COUNT(DISTINCT b.item_code) as count
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %s
        AND b.actual_qty <= i.reorder_level
        AND i.reorder_level > 0
    """, branch, as_dict=1)[0].count or 0
    
    return {
        "branch_details": branch_doc.as_dict(),
        "manager_details": manager_details,
        "stock_value": stock_value,
        "today_sales": today_sales,
        "low_stock_items": low_stock_count
    }

@frappe.whitelist()
def get_branch_sales_summary(branch, from_date=None, to_date=None):
    """Get sales summary for a branch"""
    if not branch:
        frappe.throw(_("Branch is required"))
        
    if not from_date:
        from_date = add_days(getdate(), -30)
    if not to_date:
        to_date = getdate()
        
    # Get total sales
    total_sales = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Invoice`
        WHERE branch = %s
        AND docstatus = 1
        AND posting_date BETWEEN %s AND %s
    """, (branch, from_date, to_date), as_dict=1)[0].total or 0
    
    # Get sales by item group
    sales_by_group = frappe.db.sql("""
        SELECT 
            i.item_group,
            SUM(sii.qty) as total_qty,
            SUM(sii.amount) as total_amount
        FROM `tabSales Invoice` si
        INNER JOIN `tabSales Invoice Item` sii ON sii.parent = si.name
        INNER JOIN `tabItem` i ON i.name = sii.item_code
        WHERE si.branch = %s
        AND si.docstatus = 1
        AND si.posting_date BETWEEN %s AND %s
        GROUP BY i.item_group
        ORDER BY total_amount DESC
    """, (branch, from_date, to_date), as_dict=1)
    
    return {
        "total_sales": total_sales,
        "sales_by_group": sales_by_group
    }

@frappe.whitelist()
def get_branch_inventory_summary(branch):
    """Get inventory summary for a branch"""
    if not branch:
        frappe.throw(_("Branch is required"))
        
    # Get total items count
    total_items = frappe.db.sql("""
        SELECT COUNT(DISTINCT b.item_code) as count
        FROM `tabBin` b
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %s
        AND b.actual_qty > 0
    """, branch, as_dict=1)[0].count or 0
    
    # Get inventory by item group
    inventory_by_group = frappe.db.sql("""
        SELECT 
            i.item_group,
            COUNT(DISTINCT b.item_code) as item_count,
            SUM(b.actual_qty) as total_qty,
            SUM(b.actual_qty * b.valuation_rate) as total_value
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %s
        AND b.actual_qty > 0
        GROUP BY i.item_group
        ORDER BY total_value DESC
    """, branch, as_dict=1)
    
    return {
        "total_items": total_items,
        "inventory_by_group": inventory_by_group
    } 