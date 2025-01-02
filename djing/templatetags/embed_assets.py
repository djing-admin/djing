from django import template
from django.utils.safestring import mark_safe
from djing.core.Facades.Djing import Djing

register = template.Library()


@register.simple_tag
def embed_styles(**attrs):
    styles = [style.get("url") for style in Djing._styles]

    style_tags = [f'<link rel="stylesheet" href="{style}" />' for style in styles]

    return mark_safe("\n".join(style_tags))


@register.simple_tag
def embed_scripts(**attrs):
    scripts = [script.get("url") for script in Djing._scripts]

    script_tags = [
        f'<script src="{script}" type="module" crossorigin></script>'
        for script in scripts
    ]

    return mark_safe("\n".join(script_tags))
