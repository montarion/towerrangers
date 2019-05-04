from bge import logic, events, render
from client import networking
from Tower import Tower

scene = logic.getCurrentScene()
render.showMouse(True)
cont = logic.getCurrentController()
own = cont.owner

mouse = logic.mouse
mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]

if mouseClick:
    print("spawn got mouse click")
    #spawn unit
    msg = {"spawn": {"minion":{"name":"Goblin", "location":"SpawnPointWest"}}}
    networking.sender(msg)
    
    # test to hurt base
    Tower().getTower()
