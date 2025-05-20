import frappe
from frappe import _
import re

@frappe.whitelist(allow_guest=True)
def submit_contact(name=None, email=None, subject=None, message=None):
    # Accept POST or JSON body fields as well
    data = frappe.local.form_dict or {}
    name = name or data.get('name')
    email = email or data.get('email')
    subject = subject or data.get('subject')
    message = message or data.get('message')

    # Validate all fields
    missing = []
    if not name:
        missing.append('Name')
    if not email:
        missing.append('Email')
    if not subject:
        missing.append('Subject')
    if not message:
        missing.append('Message')

    if missing:
        frappe.local.response['http_status_code'] = 400
        return {'status': 'error', 'message': f"Missing values: {', '.join(missing)}"}

    # Validate email format (simple regex)
    if not re.match(r"^[^@]+@[^@]+\\.[^@]+$", email or ""):
        frappe.local.response['http_status_code'] = 400
        return {'status': 'error', 'message': 'Invalid email address.'}

    try:
        doc = frappe.get_doc({
            'doctype': 'Mycontact',
            'name1': name,
            'email_id': email,
            'subject': subject,
            'message': message,
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Submit Contact API Error')
        frappe.local.response['http_status_code'] = 500
        return {'status': 'error', 'message': _('Failed to submit message.')}

    return {'status': 'success', 'message': _('Your message has been submitted.')}
