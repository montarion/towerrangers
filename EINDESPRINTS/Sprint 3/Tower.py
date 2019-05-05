from bge import logic
from savestate import globaldictionary
class Tower:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        self.Tower = {}

    def buildTower(self):
        globaldictionary["Towers"] = {
            "type":"",
            "name":"",
            "health":100,
            "damage":1,
            "attackSpeed":0.5
            }
        print("\n\n\nCreated base stats\n\n\n")
        print(globaldictionary)


    def setHealth(self, healthToSet):
        healthToSet = 10
        globaldictionary["Towers"]["health"] += healthToSet
        print(globaldictionary)
        
    def getTower(self):
        print(globaldictionary["Towers"])
        #print(self.Tower)
        
    def setSpeed(self):
        globaldictionary["Towers"]["attackSpeed"] = 10
    
    def takeDamage(self):
        print("Takes damage")


#tower = Tower()

def main():
    Tower().buildTower()