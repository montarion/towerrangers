import bge
from bge import logic, events
from client import networking
from savestate import globaldictionary

cont = bge.logic.getCurrentController()
own = cont.owner

scene = bge.logic.getCurrentScene()

mouse = logic.mouse
mouseClick = logic.KX_INPUT_JUST_ACTIVATED == mouse.events[events.LEFTMOUSE]
mhover = cont.sensors["mhover"]
if mhover.positive:
    if mouseClick:
        msg = {"spawn": {"minion": {"location":own.name, "name":"Centaur"}}}
        networking.sender(msg)