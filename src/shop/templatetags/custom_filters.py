import random

from django import template

register = template.Library()

@register.filter
def random_color(username):
    colors = [
        "#FF5733", "#33FF57", "#3357FF", "#F39C12", "#8E44AD", "#1ABC9C", "#E74C3C", "#3498DB"
    ]
    random.seed(username)  # Seed based on username for consistent color per user
    return random.choice(colors)