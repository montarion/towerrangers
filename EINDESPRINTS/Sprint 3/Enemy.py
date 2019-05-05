from bge import logic
from savestate import globaldictionary
class Enemy:
    #Create the Player object // Dictionary
    
    def __init__(self):        
        pass


    def buildEnemy(self):
        globaldictionary["EnemyDict"] = {
            "type":"minion",
            "name":"centaur",
            "health":100,
            "damage":1,
            "attackSpeed":.5,
            "movementSpeed":.02,
            "coins":0
        }
        print("CENTAUR")

        #print(self.Enemy['health'])


    def setHealth(self, healthToSet):
        healthToSet = 10
        self.Enemy["health"] += healthToSet
        print(globaldictionary["EnemyDict"])
        
    def getEnemy(self):
        print(globaldictionary["EnemyDict"])
        
    def setSpeed(self):
        self.Enemy["movementSpeed"] = 10        
    
    def takeDamage(self, object):
        print("Takes damage")
        #print(type(self.GD))
        name = object.name
        #print(name)
        print(name == "Arrow")
        if str(name) == "Arrow":
            print("hello")
            globaldictionary["EnemyDict"]["health"] = globaldictionary["EnemyDict"]["health"] - 1

            print("hey")
            try:
                print(globaldictionary["EnemyDict"])
                print("I see you!")
            except Exception as e:
                print(e)

            print("there")
            print("{} has {} health left.".format(globaldictionary["EnemyDict"]["name"], globaldictionary["EnemyDict"]["health"]))




enemy = Enemy()

def main():
    Enemy().buildEnemy()