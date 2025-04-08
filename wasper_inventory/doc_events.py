import frappe
from frappe import _
from frappe.utils import flt

def validate_item(doc, method):
    """Validate item before saving"""
    if not doc.is_stock_item:
        return
        
    # Validate reorder level
    if flt(doc.reorder_level) < 0:
        frappe.throw(_("Reorder Level cannot be negative"))
        
    # Validate minimum order qty
    if flt(doc.min_order_qty) < 0:
        frappe.throw(_("Minimum Order Qty cannot be negative"))
        
    # Validate safety stock
    if flt(doc.safety_stock) < 0:
        frappe.throw(_("Safety Stock cannot be negative"))

def on_submit_pos_invoice(doc, method):
    """Handle POS Invoice submission"""
    # Update stock
    for item in doc.items:
        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Material Issue"
        stock_entry.company = doc.company
        stock_entry.branch = doc.branch
        stock_entry.append("items", {
            "item_code": item.item_code,
            "qty": item.qty,
            "basic_rate": item.rate,
            "cost_center": doc.cost_center,
            "s_warehouse": doc.warehouse
        })
        stock_entry.submit()
        
    # Create Sales Invoice
    sales_invoice = frappe.new_doc("Sales Invoice")
    sales_invoice.customer = doc.customer
    sales_invoice.company = doc.company
    sales_invoice.branch = doc.branch
    sales_invoice.posting_date = doc.posting_date
    sales_invoice.due_date = doc.posting_date
    sales_invoice.cost_center = doc.cost_center
    
    for item in doc.items:
        sales_invoice.append("items", {
            "item_code": item.item_code,
            "qty": item.qty,
            "rate": item.rate,
            "amount": item.amount
        })
        
    for payment in doc.payments:
        sales_invoice.append("payments", {
            "mode_of_payment": payment.mode_of_payment,
            "amount": payment.amount
        })
        
    sales_invoice.submit()

def on_cancel_pos_invoice(doc, method):
    """Handle POS Invoice cancellation"""
    # Cancel linked Sales Invoice
    sales_invoice = frappe.get_all("Sales Invoice",
        filters={"pos_invoice": doc.name},
        fields=["name"])
        
    if sales_invoice:
        frappe.get_doc("Sales Invoice", sales_invoice[0].name).cancel()
        
    # Cancel Stock Entries
    stock_entries = frappe.get_all("Stock Entry",
        filters={
            "pos_invoice": doc.name,
            "docstatus": 1
        },
        fields=["name"])
        
    for stock_entry in stock_entries:
        frappe.get_doc("Stock Entry", stock_entry.name).cancel()

def on_submit_stock_entry(doc, method):
    """Handle Stock Entry submission"""
    if doc.stock_entry_type == "Material Receipt":
        # Update item valuation rate
        for item in doc.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            if item_doc.valuation_method == "Moving Average":
                item_doc.valuation_rate = flt(
                    (item_doc.valuation_rate * item_doc.total_qty + item.amount) /
                    (item_doc.total_qty + item.qty)
                )
                item_doc.save()

def on_cancel_stock_entry(doc, method):
    """Handle Stock Entry cancellation"""
    if doc.stock_entry_type == "Material Receipt":
        # Revert item valuation rate
        for item in doc.items:
            item_doc = frappe.get_doc("Item", item.item_code)
            if item_doc.valuation_method == "Moving Average":
                item_doc.valuation_rate = flt(
                    (item_doc.valuation_rate * item_doc.total_qty - item.amount) /
                    (item_doc.total_qty - item.qty)
                )
                item_doc.save() 