from bge import logic, events
from client import networking

scene = logic.getCurrentScene()

cont = logic.getCurrentController()
own = cont.owner

mouse = logic.mouse
mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]

if mouseClick:
    print("spawn got mouse click")
    #spawn unit
    msg = {"spawn": {"minion":{"name":"Goblin", "location":"SpawnPointWest"}}}
    networking.sender(msg)
    