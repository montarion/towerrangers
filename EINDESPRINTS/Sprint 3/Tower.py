class Tower:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        self.tower = {}


    def buildTower(self):
        self.tower = {
            "type":"",
            "name":"",
            "health":100,
            "damage":1,
            "attackSpeed":0.5
        }
        print(self.tower['health'])

    def setHealth(self, healthToSet):
        healthToSet = 10
        self.tower["health"] += healthToSet
        print(self.tower)
        
    def getTower(self):
        print(self.tower)
        
    def setSpeed(self):
        self.tower["attackSpeed"] = 10
    
    def takeDamage(self):
        print("Takes damage")




def main():
    Tower().buildTower()