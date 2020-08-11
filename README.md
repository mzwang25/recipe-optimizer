# Recipe-Optimizer

## Info
Deployed on google cloud <br/>

https://recipe-optimizer.wl.r.appspot.com/

## Units 
To not confuse any units, all units are converted to

<ul>
    <li> cm^3 </li>
    <li> g </li>
</ul>

and here are the following conversions

<ul>
    <li> tbsp = 14.7868 cm^3 </li>
    <li> tsp  = 4.92892 cm^3</li>
    <li> cups = 236.588 cm^3 </li>
    <li> li = 1000 cm^3</li>
    <li> ml = 1 cm^3 </li>
    <li> gal = 3785.41 cm^3 </li>
    <li> g = 1g </li>
    <li> oz = 28.3495 g </li>
</ul>


## GET requests

<ul>
    <li> /get-recipes</li>
    <li> /add-recipe?name=<>&ingredients=<>&notes=<></li>
    <li> /delete-recipe?id=<></li>
    <li> /get-schedule?</li>
    <li> /add-schedule?recipe_id=<>?notes=<></li>
    <li> /delete-schedule?id=<></li>
    <li> /recipe-schedule</li>
    <li> /ingredients-needed</li>
    <li> /send-needed-ingredients</li>
</ul>

## /ingredients-needed
This sends back units. Only weight/volume is used. If the original 
user input was in weight, all volume units are 0. Same other way.
```json
    {
        "name": "WATER",
        "tbsp": 1.3333297265128357,
        "tsp": 4.0,
        "cups": 0.08333338969009417,
        "li": 0.01971568,
        "ml": 19.71568,
        "gal": 0.005208334103835516,
        "g": 0,
        "oz": 0
    },
    {
        "name": "HELLO",
        "tbsp": 0,
        "tsp": 0,
        "cups": 0,
        "li": 0,
        "ml": 0,
        "gal": 0,
        "g": 21.0,
        "oz": 0.7407538051817493
    },
```
