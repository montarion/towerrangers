from bge import logic, events, render
from client import networking
from Tower import tower

scene = logic.getCurrentScene()
render.showMouse(True)
cont = logic.getCurrentController()
own = cont.owner

mouse = logic.mouse
mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]

if mouseClick:
    print("spawn got mouse click")
    print("CLICKING WAS DONE")
    #spawn unit
    msg = {"spawn": {"minion":{"name":"Goblin", "location":"SpawnPointSouth"}}}
    networking.sender(msg)
    
    # test to hurt base
    print("get tower stats")
    tower.main()
    print("\n\n\n\n WAITIIIIING\n\n\n")
    print(tower.getTower())
