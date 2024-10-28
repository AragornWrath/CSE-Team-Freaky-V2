from django import template

register = template.Library()

@register.simple_tag
def tripName(trip):
    print("*****TRIP*****")
    print(trip, flush=True)
    return trip["tripname"]

@register.simple_tag
def tripDestination(trip):
    return trip["destination"]
