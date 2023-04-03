Tested on: 
Python 3.11.1
Flask 2.2.2


Install requirements  
```pip install Flask```  

Run the code and send the desired payload to ```127.0.0.1:5000/calculate``` or ```localhost:5000/calculate``` and you get calculated fee as json response.  
Example body for POST request ``` {"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2021-10-12T13:00:00Z"} ```  

If you run this project on Python 3.10 remove the "Z" from the time ISO format.