import bge ,GameLogic, mathutils, math
from Enemy import Enemy


scene = bge.logic.getCurrentScene()
coin = scene.objectsInactive['Coin']
isDead = False

controller = bge.logic.getCurrentController()
own = controller.owner
Enemy().buildEnemy()

# plek voor beslissing nemen
player = scene.objects['defenderPlayer']


# follow stuff
direction = player.position - own.position
direction.normalize()

distanceX = player.position.x - own.position.x
distanceY = player.position.y - own.position.y
distance = math.sqrt(distanceX * distanceX + distanceY * distanceY)

# collision stuff
colsen = controller.sensors["colsen"]
hit = colsen.hitObject
print(hit)
if hit == "Arrow":
  isDead = True
if  distance <= -10 or distance >= 10:    
    #print(distance)
    own.setLinearVelocity(direction * 15, True)
else:
    own.setLinearVelocity(direction * 0, True)
    #isDead = True
    
if isDead:
    print("Coin is spawned")
    own.endObject()
    scene.addObject(coin, own)