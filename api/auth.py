import frappe
from frappe.utils.password import update_password

@frappe.whitelist(allow_guest=True)
def create_pending_user(full_name, email, password, company):
    if frappe.db.exists("User", email):
        return "Email already registered."

    user = frappe.get_doc({
        "doctype": "User",
        "email": email,
        "first_name": full_name,
        "send_welcome_email": 1,
        "roles": [{"role": "Pending User"}],
        "user_type": "Website User"
    })
    user.insert(ignore_permissions=True)
    update_password(user.name, password)

    frappe.sendmail(
        recipients=["admin@example.com"],
        subject="New User Signup Request",
        message=f"User {full_name} requested to join company {company}. Please review and approve."
    )

    return "Account created. Waiting for admin approval."