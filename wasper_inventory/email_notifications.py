import frappe
from frappe import _
from frappe.utils import getdate, add_days, flt
from frappe.core.doctype.communication.email import make
from frappe.utils import get_url

def send_low_stock_alert():
    """Send email alerts for items with low stock"""
    # Get all items with stock below reorder level
    items = frappe.db.sql("""
        SELECT 
            b.item_code,
            i.item_name,
            b.actual_qty,
            i.reorder_level,
            w.branch
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE b.actual_qty <= i.reorder_level
        AND b.actual_qty > 0
    """, as_dict=1)
    
    # Group items by branch
    branch_items = {}
    for item in items:
        if item.branch not in branch_items:
            branch_items[item.branch] = []
        branch_items[item.branch].append(item)
    
    # Send emails to branch managers
    for branch, items in branch_items.items():
        branch_doc = frappe.get_doc("Branch", branch)
        if branch_doc.branch_manager:
            make(
                recipients=[branch_doc.branch_manager],
                subject=f"Low Stock Alert - {branch}",
                content=frappe.render_template(
                    "wasper_inventory/email_templates/low_stock_alert.html",
                    {
                        "recipient_name": frappe.get_value("User", branch_doc.branch_manager, "full_name"),
                        "branch": branch,
                        "items": items
                    }
                )
            )

def send_branch_performance_summary():
    """Send weekly branch performance summary"""
    # Get all branches
    branches = frappe.get_all("Branch", fields=["name", "branch_manager"])
    
    for branch in branches:
        if branch.branch_manager:
            # Get performance data
            from_date = add_days(getdate(), -7)
            to_date = getdate()
            
            # Get sales data
            sales_data = frappe.db.sql("""
                SELECT 
                    SUM(grand_total) as total_sales,
                    COUNT(name) as total_transactions
                FROM `tabSales Invoice`
                WHERE branch = %s
                AND posting_date BETWEEN %s AND %s
                AND docstatus = 1
            """, (branch.name, from_date, to_date), as_dict=1)[0]
            
            # Get purchase data
            purchase_data = frappe.db.sql("""
                SELECT SUM(grand_total) as total_purchases
                FROM `tabPurchase Invoice`
                WHERE branch = %s
                AND posting_date BETWEEN %s AND %s
                AND docstatus = 1
            """, (branch.name, from_date, to_date), as_dict=1)[0]
            
            # Get top selling items
            top_items = frappe.db.sql("""
                SELECT 
                    sii.item_name,
                    SUM(sii.qty) as qty,
                    SUM(sii.amount) as amount
                FROM `tabSales Invoice Item` sii
                INNER JOIN `tabSales Invoice` si ON si.name = sii.parent
                WHERE si.branch = %s
                AND si.posting_date BETWEEN %s AND %s
                AND si.docstatus = 1
                GROUP BY sii.item_code
                ORDER BY amount DESC
                LIMIT 5
            """, (branch.name, from_date, to_date), as_dict=1)
            
            # Calculate metrics
            total_sales = flt(sales_data.total_sales)
            total_purchases = flt(purchase_data.total_purchases)
            gross_profit = total_sales - total_purchases
            profit_margin = (gross_profit / total_sales * 100) if total_sales else 0
            
            make(
                recipients=[branch.branch_manager],
                subject=f"Branch Performance Summary - {branch.name}",
                content=frappe.render_template(
                    "wasper_inventory/email_templates/branch_performance_summary.html",
                    {
                        "recipient_name": frappe.get_value("User", branch.branch_manager, "full_name"),
                        "branch": branch.name,
                        "from_date": from_date,
                        "to_date": to_date,
                        "total_sales": total_sales,
                        "total_purchases": total_purchases,
                        "gross_profit": gross_profit,
                        "profit_margin": profit_margin,
                        "total_transactions": sales_data.total_transactions,
                        "top_items": top_items
                    }
                )
            )

def send_pos_daily_summary():
    """Send daily POS summary"""
    # Get all branches with POS profiles
    branches = frappe.db.sql("""
        SELECT DISTINCT branch
        FROM `tabPOS Profile`
        WHERE enabled = 1
    """, as_dict=1)
    
    for branch in branches:
        branch_doc = frappe.get_doc("Branch", branch.branch)
        if branch_doc.branch_manager:
            date = getdate()
            
            # Get POS data
            pos_data = frappe.db.sql("""
                SELECT 
                    SUM(grand_total) as total_sales,
                    COUNT(name) as total_transactions,
                    SUM(grand_total) / COUNT(name) as avg_transaction_value
                FROM `tabPOS Invoice`
                WHERE branch = %s
                AND posting_date = %s
                AND docstatus = 1
            """, (branch.branch, date), as_dict=1)[0]
            
            # Get payment methods data
            payment_methods = frappe.db.sql("""
                SELECT 
                    pip.mode_of_payment,
                    SUM(pip.amount) as amount,
                    (SUM(pip.amount) / (SELECT SUM(grand_total) 
                        FROM `tabPOS Invoice` 
                        WHERE branch = %s 
                        AND posting_date = %s 
                        AND docstatus = 1)) * 100 as percentage
                FROM `tabPOS Invoice Payment` pip
                INNER JOIN `tabPOS Invoice` pi ON pi.name = pip.parent
                WHERE pi.branch = %s
                AND pi.posting_date = %s
                AND pi.docstatus = 1
                GROUP BY pip.mode_of_payment
            """, (branch.branch, date, branch.branch, date), as_dict=1)
            
            # Get top selling items
            top_items = frappe.db.sql("""
                SELECT 
                    pii.item_name,
                    SUM(pii.qty) as qty,
                    SUM(pii.amount) as amount
                FROM `tabPOS Invoice Item` pii
                INNER JOIN `tabPOS Invoice` pi ON pi.name = pii.parent
                WHERE pi.branch = %s
                AND pi.posting_date = %s
                AND pi.docstatus = 1
                GROUP BY pii.item_code
                ORDER BY amount DESC
                LIMIT 5
            """, (branch.branch, date), as_dict=1)
            
            make(
                recipients=[branch_doc.branch_manager],
                subject=f"POS Daily Summary - {branch.branch}",
                content=frappe.render_template(
                    "wasper_inventory/email_templates/pos_daily_summary.html",
                    {
                        "recipient_name": frappe.get_value("User", branch_doc.branch_manager, "full_name"),
                        "branch": branch.branch,
                        "date": date,
                        "total_sales": pos_data.total_sales,
                        "total_transactions": pos_data.total_transactions,
                        "avg_transaction_value": pos_data.avg_transaction_value,
                        "payment_methods": payment_methods,
                        "top_items": top_items
                    }
                )
            ) 