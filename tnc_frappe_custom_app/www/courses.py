import frappe

def get_banner_data(type_filter=None):
    # Define filters: fetch only published banners
    filters = {'is_published': 1}
    
    if type_filter:
        filters['type'] = type_filter

    banners = frappe.get_all('Banner Images', filters=filters, fields=['name', 'image','type', 'is_published'])

    return banners

def get_context(context):
    slider_settings = banners
    context.banners = slider_settings
    
    return context

banners = get_banner_data(type_filter='courses')
