from bge import logic

class Tower:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        pass

    def buildTower(self):
        self.Tower = {
            "type":"",
            "name":"",
            "health":100,
            "damage":1,
            "attackSpeed":0.5
            }
        print("\n\n\nCreated base stats\n\n\n")
        print(self.Tower)
        logic.globalDict["Towers"] = self.Tower

    def setHealth(self, healthToSet):
        healthToSet = 10
        self.Tower["health"] += healthToSet
        print(self.Tower)
        
    def getTower(self):
        print(logic.globalDict["Towers"])
        print(self.Tower)
        
    def setSpeed(self):
        self.Tower["attackSpeed"] = 10        
    
    def takeDamage(self):
        print("Takes damage")


tower = Tower()

def main():
    tower.buildTower()

