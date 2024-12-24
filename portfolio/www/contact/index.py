import frappe

def get_context(context):
    context.show_message = False
    
    # Check if the form has been submitted
    if frappe.form_dict:
        # Get the form data
        name = frappe.form_dict.get('name')
        email = frappe.form_dict.get('email')
        subject = frappe.form_dict.get('subject')
        message = frappe.form_dict.get('message')
        
        # Create a new Contact Message document
        if name and email and message:
            doc = frappe.get_doc({
                'doctype': 'Mycontact',
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            })
            doc.insert(ignore_permissions=True)
            
            # Show a success message in the template
            context.show_message = True
            context.message_text = "Thank you for your message. We will get back to you soon!"
    
    return context
