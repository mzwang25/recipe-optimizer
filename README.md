# Recipe-Optimizer

## Info
Deployed on google cloud <br/>

https://recipe-optimizer.wl.r.appspot.com/

## Units 
Here are all the units I can think of that are used in cooking <br/>
<ul>
    <li> volume </li>
    <li> weight </li>
</ul>

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