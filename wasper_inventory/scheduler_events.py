import frappe
from frappe.utils import get_datetime, now_datetime
from wasper_inventory.email_notifications import (
    send_low_stock_alert,
    send_branch_performance_summary,
    send_pos_daily_summary
)

def daily():
    """Run daily tasks"""
    # Send POS daily summary at 11 PM
    if get_datetime().hour == 23:
        send_pos_daily_summary()

def weekly():
    """Run weekly tasks"""
    # Send branch performance summary on Monday at 9 AM
    if get_datetime().weekday() == 0 and get_datetime().hour == 9:
        send_branch_performance_summary()

def hourly():
    """Run hourly tasks"""
    # Send low stock alerts every hour
    send_low_stock_alert()

def all():
    """Run all tasks"""
    daily()
    weekly()
    hourly() 