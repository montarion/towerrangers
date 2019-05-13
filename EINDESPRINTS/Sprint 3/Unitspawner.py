import bge
from bge import logic, events
from client import networking
from savestate import globaldictionary

cont = bge.logic.getCurrentController()
own = cont.owner

scene = bge.logic.getCurrentScene()
try:
    mouse = logic.mouse
    mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]
    mhover = cont.sensors["mhover"]
    if mhover.positive:
        print("STOP HOVERING")
        if mouseClick:
            print("Spawnpoint:")
            print(own.name)
            print("was clicked!")
            msg = {"spawn": {"minion": {"location":own.name, "name":"Centaur"}}}
            networking.sender(msg)
except Exception as e:
    print(e)