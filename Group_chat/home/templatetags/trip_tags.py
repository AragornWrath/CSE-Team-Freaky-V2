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

@register.simple_tag
def tripUsername(trip):
    return trip["username"]

@register.simple_tag
def tripLikes(trip):
    numberOfLikes = trip.get("likes", 0)
    if numberOfLikes == 0:
        return 0
    return len(numberOfLikes)

@register.simple_tag
def tripID(trip):
    return trip.get("tripID", "none")