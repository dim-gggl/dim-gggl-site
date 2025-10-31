from django import template


register = template.Library()


@register.filter
def mul(value, arg):
    """Multiply numeric value by arg (used for percentage widths)."""
    try:
        return float(value) * float(arg)
    except Exception:
        return 0
