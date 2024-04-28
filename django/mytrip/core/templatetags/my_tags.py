from django import template

register = template.Library()

@register.filter
def length_real(array):
    return len(array) - 1

@register.filter
def get_relationship_distance(array, index):
    try:
        return array[index].distance
    except IndexError:
        return None
    
@register.filter
def get_relationship_travel_time(array, index):
    try:
        return array[index].travel_time
    except IndexError:
        return None

@register.filter
def sum_relationship_distance(relationships_array):
    sum = 0
    for item in relationships_array:
        sum += item.distance
    return sum

@register.filter
def sum_relationship_travel_time(relationships_array):
    sum = 0
    for item in relationships_array:
        sum += item.travel_time
    return sum

@register.filter
def calculate_trip_duration(relationships_array):
    # Neg udurt 500km yvna gej uzev
    return round(float(sum_relationship_travel_time(relationships_array)) / 500, 1)

@register.filter
def calculate_trip_cost(relationships_array, locations_array, vehicle):
    return calculate_total_gas_cost(relationships_array, vehicle) + calculate_total_ticket_cost(locations_array)

@register.filter
def calculate_total_ticket_cost(locations_array):
    total_ticket_cost = 0
    for item in locations_array:
        total_ticket_cost = item.price
    return round(total_ticket_cost)

@register.filter
def calculate_total_gas_cost(relationships_array, vehicle):
    total_gas_cost = 0
    GAS_PRICE = 2390
    fuel_consumption = calculate_fuel_consumption(vehicle=vehicle)
    total_distance = sum_relationship_distance(relationships_array=relationships_array)
    total_gas_cost = 2 * GAS_PRICE * fuel_consumption * round(total_distance/100, 2)
    return round(total_gas_cost)

@register.filter
def get_parent_soum(location):
    return location.soum.single()

@register.filter
def get_parent_province(location):
    return location.soum.single().province.single()

@register.filter
def get_parent_province(location):
    return location.soum.single().province.single()


def calculate_fuel_consumption(vehicle):
    fuel_consumption = 0
    if(vehicle == 'prius'):
        fuel_consumption = 10
    elif(vehicle == 'landcruiser'):
        fuel_consumption = 18
    else:
        fuel_consumption = 14
    return fuel_consumption

