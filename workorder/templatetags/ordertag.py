from django import template
register = template.Library()

@register.filter(name='orderfile_name')
def orderfile_name(file_path):
    file_name = str(file_path).split('/')[-1]
    return file_name