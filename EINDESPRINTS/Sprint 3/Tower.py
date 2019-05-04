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
        print(self.Tower['health'])

    def setHealth(self, healthToSet):
        healthToSet = 10
        self.Tower["health"] += healthToSet
        print(self.Tower)
        
    def getTower(self):
        print(self.Tower)
        
    def setSpeed(self):
        self.Tower["attackSpeed"] = 10        
    
    def takeDamage(self):
        print("Takes damage")




def main():
    Tower().buildTower()