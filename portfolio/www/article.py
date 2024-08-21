import frappe


def get_context(context):
    # Get the current page number from the query parameters (default to 1)
    page = frappe.form_dict.get('page', 1)
    page = int(page)
    
    # Define the number of items per page
    page_length = 6  # Display 4 blogs per page
    
    # Calculate the start index
    start = (page - 1) * page_length
    
    # Fetch the paginated blog posts
    blogs = frappe.get_all('Blog Post', 
                           filters={'published': 1},
                           fields=['*'],
                           order_by='published_on desc',
                           start=start,
                           limit=page_length)
    
    # Total number of blogs
    total_blogs = frappe.db.count('Blog Post', filters={'published': 1})
    
    # Calculate the total number of pages
    total_pages = (total_blogs + page_length - 1) // page_length
    
    # Add data to context
    context.blogs = blogs
    context.current_page = page
    context.total_pages = total_pages
    context.has_next = page < total_pages
    context.has_previous = page > 1
    
    return context
