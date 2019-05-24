import bge
from client import networking

scene = bge.logic.getCurrentScene()
arrow = scene.objectsInactive["Arrow"]

cont = bge.logic.getCurrentController()
own = cont.owner

mouse = bge.logic.mouse
mouseClick = bge.logic.KX_INPUT_JUST_ACTIVATED == mouse.events[bge.events.LEFTMOUSE]

life_time = 120
velocity = 15

if mouseClick:
    #print("Shooting?")
    
    msg = {"shooting": "shot"}
    networking.sender(msg, role="cmd")
    #new_arrow = scene.addObject(arrow, own, life_time)
    #new_arrow.setLinearVelocity((0, velocity, 0), True)


