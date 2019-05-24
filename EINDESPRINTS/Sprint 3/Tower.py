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

        cont = logic.getCurrentController()
        own = cont.owner
        own["trackme"] = True

    def setHealth(self, healthToSet):
        healthToSet = 10
        globaldictionary["Towers"]["health"] += healthToSet
        print(globaldictionary)
        
    def getTower(self):
        print(globaldictionary["Towers"])
        #print(self.Tower)
        
    def setSpeed(self):
        globaldictionary["Towers"]["attackSpeed"] = 10
    
    def takeDamage(self, object):
        print("Takes damage")
        name = object.name



#tower = Tower()

def main():
    Tower().buildTower()


