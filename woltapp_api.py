from datetime import datetime
from flask import Flask, request, Response
import math
import json



RUSH_HOUR_MULTIPLIER = 1.2      #Multiplier for rush hour delivery fee
BASE_TRANSPORT_FEE = 200        #Base transport fee in cents
ADDITIONAL_DISTANCE_FEE = 100   #Additional fee for every 500m in cents
BULK_ORDER_FEE = 120            #Fee for orders containing more than 12 items in cents
EXTRA_ITEM_FEE = 50             #Fee for orders containing 5 or more items. Per item incl. 5th in cents.
SMALL_ORDER_FEE = 1000          #Small order fee for orders under this constant in cents. This const - cart_value
MAXIMUM_FEE = 1500              #Maximum price of delivery in cents.



app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate():
    request_data = request.get_json()   #This could be improved with async request handling
    
    try:
        validate_input(request_data['cart_value'], request_data['delivery_distance'], request_data['number_of_items'])
        fee = calculate_fee(request_data['cart_value'], request_data['delivery_distance'], request_data['number_of_items'], request_data['time'])
        responsejson = json.dumps({"delivery_fee": fee})
        return Response(responsejson, mimetype='application/json')
    
    except Exception as e:
        return Response(repr(e))


def validate_input(cart_value ,delivery_distance, number_of_items):

    #Check that values inputted are positive
    if cart_value < 0 or delivery_distance < 0 or number_of_items < 0:
        raise Exception('Numbers must be positive')
    else:
        return


def calculate_fee(cart_value ,delivery_distance, number_of_items, time):
    
    delivery_fee = 0  # set delivery fee 0
    
    #The delivery is free (0€) when the cart value is equal or more than 100€.
    if cart_value >= 10000:
        return delivery_fee   # stop function because it will be 0 anyway if this procs
        
    #If the cart value is less than 10€, a small order surcharge is added to the delivery price.
    #The surcharge is the difference between the cart value and 10€.
    
    if cart_value < SMALL_ORDER_FEE:              
        delivery_fee += SMALL_ORDER_FEE - cart_value
        
    #A delivery fee for the first 1000 meters (=1km) is 2€. 
    #If the delivery distance is longer than that, 1€ is added for every additional 500 meters that the courier needs to travel before reaching the destination. 
    #Even if the distance would be shorter than 500 meters, the minimum fee is always 1€.
    
    if delivery_distance <= 1000:      #if distance is shorter than 1km
        delivery_fee += BASE_TRANSPORT_FEE           #first km is 2€
        
    if delivery_distance > 1000:        #if distance is longer than 1km
        delivery_fee += BASE_TRANSPORT_FEE            #first km is 2€
        delivery_fee += math.ceil((delivery_distance - 1000) / 500) * ADDITIONAL_DISTANCE_FEE  
    # remove 1km distance because it is calculated. Divide remaining distance with 500(m) and multiply with 100 (1€)    
    
    #If the number of items is five or more, an additional 50 cent surcharge is added for each item above and including the fifth item. 
    #An extra "bulk" fee applies for more than 12 items of 1,20€
    
    if number_of_items >= 5:
        delivery_fee += 50  #50 cent extra for 5 items
        delivery_fee += (number_of_items - 5) * EXTRA_ITEM_FEE  #if number of items is over 5 50cent for every item, if number of items is 5 then this will add 0
        if number_of_items > 12:
            delivery_fee += BULK_ORDER_FEE         # 120 (1,2€) if number of items is more than 12
    
    #During the Friday rush (3 - 7 PM UTC), the delivery fee (the total fee including possible surcharges) will be multiplied by 1.2x.
    #However, the fee still cannot be more than the max (15€).
    
    order_date = datetime.fromisoformat(time)  # date of the order 
    order_hour = order_date.hour #hour of the order
        
    if order_date.weekday() == 4:                                 
        if order_hour >= 15 and order_hour <= 19:                
            delivery_fee = delivery_fee * RUSH_HOUR_MULTIPLIER
        
    #The delivery fee can never be more than 15€, including possible surcharges.
    if delivery_fee > MAXIMUM_FEE: #if delivery is more than MAXIMUM_FEE set delivery_fee as MAXIMUM_FEE
        delivery_fee = MAXIMUM_FEE
    
    return delivery_fee


if __name__ == '__main__':
    app.run()