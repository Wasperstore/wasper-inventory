import frappe
from frappe import _
from frappe.utils import flt, getdate, add_days, cint
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        filters = {}
        
    if not filters.get("branch"):
        frappe.throw(_("Please select a branch"))
        
    if not filters.get("from_date"):
        filters["from_date"] = add_days(getdate(), -30)
        
    if not filters.get("to_date"):
        filters["to_date"] = getdate()
        
    data = get_data(filters)
    columns = get_columns()
    chart_data = get_chart_data(data)
    
    return columns, data, None, chart_data

def get_columns():
    return [
        {
            "label": _("Metric"),
            "fieldname": "metric",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Value"),
            "fieldname": "value",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Change"),
            "fieldname": "change",
            "fieldtype": "Percent",
            "width": 100
        }
    ]

def get_data(filters):
    data = []
    
    # Get sales metrics
    sales_data = get_sales_metrics(filters)
    data.extend(sales_data)
    
    # Get purchase metrics
    purchase_data = get_purchase_metrics(filters)
    data.extend(purchase_data)
    
    # Get inventory metrics
    inventory_data = get_inventory_metrics(filters)
    data.extend(inventory_data)
    
    return data

def get_sales_metrics(filters):
    metrics = []
    
    # Current period sales
    current_sales = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Invoice`
        WHERE branch = %(branch)s
        AND docstatus = 1
        AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=1)[0].total or 0
    
    # Previous period sales
    prev_filters = filters.copy()
    prev_filters["from_date"] = add_days(filters["from_date"], -30)
    prev_filters["to_date"] = add_days(filters["to_date"], -30)
    
    prev_sales = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabSales Invoice`
        WHERE branch = %(branch)s
        AND docstatus = 1
        AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, prev_filters, as_dict=1)[0].total or 0
    
    # Calculate change
    change = ((current_sales - prev_sales) / prev_sales * 100) if prev_sales else 0
    
    metrics.append({
        "metric": "Total Sales",
        "value": current_sales,
        "change": change
    })
    
    # Get average order value
    avg_order_value = frappe.db.sql("""
        SELECT AVG(grand_total) as avg_value
        FROM `tabSales Invoice`
        WHERE branch = %(branch)s
        AND docstatus = 1
        AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=1)[0].avg_value or 0
    
    metrics.append({
        "metric": "Average Order Value",
        "value": avg_order_value,
        "change": 0  # Not calculating change for this metric
    })
    
    return metrics

def get_purchase_metrics(filters):
    metrics = []
    
    # Current period purchases
    current_purchases = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabPurchase Invoice`
        WHERE branch = %(branch)s
        AND docstatus = 1
        AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, filters, as_dict=1)[0].total or 0
    
    # Previous period purchases
    prev_filters = filters.copy()
    prev_filters["from_date"] = add_days(filters["from_date"], -30)
    prev_filters["to_date"] = add_days(filters["to_date"], -30)
    
    prev_purchases = frappe.db.sql("""
        SELECT SUM(grand_total) as total
        FROM `tabPurchase Invoice`
        WHERE branch = %(branch)s
        AND docstatus = 1
        AND posting_date BETWEEN %(from_date)s AND %(to_date)s
    """, prev_filters, as_dict=1)[0].total or 0
    
    # Calculate change
    change = ((current_purchases - prev_purchases) / prev_purchases * 100) if prev_purchases else 0
    
    metrics.append({
        "metric": "Total Purchases",
        "value": current_purchases,
        "change": change
    })
    
    return metrics

def get_inventory_metrics(filters):
    metrics = []
    
    # Current stock value
    stock_value = frappe.db.sql("""
        SELECT SUM(b.actual_qty * b.valuation_rate) as total_value
        FROM `tabBin` b
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty > 0
    """, filters, as_dict=1)[0].total_value or 0
    
    metrics.append({
        "metric": "Current Stock Value",
        "value": stock_value,
        "change": 0  # Not calculating change for this metric
    })
    
    # Low stock items count
    low_stock_count = frappe.db.sql("""
        SELECT COUNT(DISTINCT b.item_code) as count
        FROM `tabBin` b
        INNER JOIN `tabItem` i ON i.name = b.item_code
        INNER JOIN `tabWarehouse` w ON w.name = b.warehouse
        WHERE w.branch = %(branch)s
        AND b.actual_qty <= i.reorder_level
        AND i.reorder_level > 0
    """, filters, as_dict=1)[0].count or 0
    
    metrics.append({
        "metric": "Low Stock Items",
        "value": low_stock_count,
        "change": 0  # Not calculating change for this metric
    })
    
    return metrics

def get_chart_data(data):
    return {
        "data": {
            "labels": [d.get("metric") for d in data],
            "datasets": [
                {
                    "name": "Value",
                    "values": [d.get("value") for d in data]
                }
            ]
        },
        "type": "bar",
        "height": 300
    } 