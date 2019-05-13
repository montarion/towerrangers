import bge ,GameLogic, mathutils, math

scene = bge.logic.getCurrentScene()

controller = bge.logic.getCurrentController()
own = controller.owner
unit = scene.objects['Centaur']


direction = unit.position - own.position
direction.normalize()

distanceX = unit.position.x - own.position.x
distanceY = unit.position.y - own.position.y
distance = math.sqrt(distanceX * distanceX + distanceY * distanceY)

targetList = []

#print(player.position)
#print(own.position)

if  distance <= -.001 or distance >= .001:    
    #print(distance)
    targetList.append(unit)
    for target in targetList:
        direction = unit.position - own.position
        own.setLinearVelocity(direction * 15, True)
        print("targetList" + str(targetList))
        target.endObject()
else:
    own.setLinearVelocity(direction * 0, True)   