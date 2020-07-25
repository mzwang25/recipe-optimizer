import re

        

class Ingredients_Parser:
    conversionFactor = {
        "tbsp" : (14.7868, "cm3"),
        "tsp" : (4.92892, "cm3"),
        "cups" : (236.588, "cm3"),
        "li" : (1000, "cm3"),
        "ml" : (1, "cm3"),
        "gal" : (3785.41, "cm3"),
        "g" : (1, "g"),
        "oz" : (28.3495, "g")
    }

    def __init__(self, raw_ingredients):

        self.isValid = True
        self.clean_ingredients = ""
        rilist = raw_ingredients.replace(" ", "").split(',')

        for ing in rilist:
            if(re.search('.*\(.*\)', ing)):

                name = ing.split('(')[0]
                amount = ing.split('(')[1][0:-1]

                match = re.compile("[^\W\d]").search(amount)

                if(match == None):
                    self.isValid = False
                    break

                value = float(amount[:match.start()])
                unit = amount[match.start():]

        
                try:
                    factor = self.conversionFactor[unit]
                except:
                    self.isValid = False
                    break

                if(self.clean_ingredients == ""):
                    self.clean_ingredients += name + "({}:{})".format(value * factor[0], factor[1])
                else:
                    self.clean_ingredients += "," + name + "({}:{})".format(value * factor[0], factor[1])


            else:
                self.isValid = False
                break