import bge, GameLogic, mathutils, math
from Enemy import Enemy
from savestate import globaldictionary
from time import sleep

scene = bge.logic.getCurrentScene()
coin = scene.objectsInactive['Coin']
isDead = False

controller = bge.logic.getCurrentController()
own = controller.owner


if globaldictionary['enemybuilt'] == False:
    Enemy().buildEnemy()
    globaldictionary['enemybuilt'] = True
    

# plek voor beslissing nemen
tracklist = {}
for obj in scene.objects:
    try:
        if obj["trackme"] == True:
            tracklist[obj] = obj.name
    except:
        pass

#print(tracklist)
#print(list(tracklist.keys())[0])
target = ""
try:
    closestd = sorted([tracklist[t] for t in tracklist])
    closestobj = [c for c in tracklist if tracklist[c] == closestd[0]][0]
    #print("Closest object is:")
    #print(closestobj)
    #print(type(closestobj))
    #target = scene.objects[closestobj]
    target = closestobj
    #print(type(target))
    print("TRACKING {} at position {}".format(target.name, target.position))
except IndexError:
    print("No objects to track!")
except Exception as e:
    print(e)
#distanceX = obj.position.x - own.position.x
#distanceY = obj.position.y - own.position.y
#distance = math.sqrt(distanceX * distanceX + distanceY * distanceY)


# follow stuff
direction = target.position - own.position
direction.normalize()

distanceX = target.position.x - own.position.x
distanceY = target.position.y - own.position.y
distance = math.sqrt(distanceX * distanceX + distanceY * distanceY)

# collision stuff
print("\n\WAITING FOR COLLISION STUFF")
colsen = controller.sensors["colsen"]
hit = colsen.hitObject

try:
    arrow = scene.objects["Arrow"]
    if hit == arrow:
        print("\n\n\nHIT BY AN ARROW TO THE KNEE\n\n\n")
        isDead = True
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
