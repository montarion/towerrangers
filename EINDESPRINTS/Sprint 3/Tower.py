from bge import logic

class Tower:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        self.tower = {}


    def buildTower(self):
        self.tower = {
            "type":"base",
            "name":"basuru",
            "health":100,
            "damage":1,
            "attackSpeed":0.5
            }
        print("\n\n\nCreated base stats\n\n\n")
        print(self.tower)
        logic.globalDict["Towers"] = self.tower

    def setHealth(self, healthToSet):
        healthToSet = 10
        self.tower["health"] += healthToSet
        print(self.tower)
        
    def getTower(self):
        print("tower stats!")
        print(self.tower)
        return self.tower
        
    def setSpeed(self):
        self.tower["attackSpeed"] = 10
    
    def takeDamage(self):
        print("Takes damage")


tower = Tower()

def main():
    Tower().buildTower()