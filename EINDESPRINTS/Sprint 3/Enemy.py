class Enemy:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        pass


    def buildEnemy(self):
        self.Enemy = {
            "type":"",
            "name":"",
            "health":100,
            "damage":1,
            "attackSpeed":.5,
            "movementSpeed":.02,
            "coins":0
        }
        print("CENTAUR")
        print(self.Enemy['health'])

    def setHealth(self, healthToSet):
        healthToSet = 10
        self.Enemy["health"] += healthToSet
        print(self.Enemy)
        
    def getEnemy(self):
        print(self.Enemy)
        
    def setSpeed(self):
        self.Enemy["movementSpeed"] = 10        
    
    def takeDamage(self):
        print("Takes damage")


enemy = Enemy()

def main():
    Enemy().buildEnemy()