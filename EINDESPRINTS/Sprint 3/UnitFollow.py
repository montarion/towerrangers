import bge, GameLogic, mathutils, math
from Enemy import Enemy
from savestate import globaldictionary

scene = bge.logic.getCurrentScene()
coin = scene.objectsInactive['Coin']
isDead = False

controller = bge.logic.getCurrentController()
own = controller.owner


if globaldictionary['enemybuilt'] == False:
    Enemy().buildEnemy()
    globaldictionary['enemybuilt'] = True
    

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

try:
    arrow = scene.objects["Arrow"]
    if hit == arrow:
        print("\n\n\nHIT BY AN ARROW TO THE KNEE\n\n\n")
        # isDead = True
        Enemy().takeDamage(arrow)

except:
    pass

if distance <= -10 or distance >= 10:
    own.setLinearVelocity(direction * 15, True)
else:
    own.setLinearVelocity(direction * 0, True)

if isDead:
    print("Coin is spawned")
    own.endObject()
    scene.addObject(coin, own)
