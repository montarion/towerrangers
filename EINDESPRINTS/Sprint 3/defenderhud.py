from bge import logic, events, render
from client import networking

scene = logic.getCurrentScene()
render.showMouse(True)
cont = logic.getCurrentController()
own = cont.owner

keyb = logic.keyboard
fkey = logic.KX_INPUT_ACTIVE == keyb.events[events.FKEY]

if fkey:
    print("spawn got f")
    #spawn unit
    msg = {"spawn": {"tower":{"name":"Tower1"}}}
    networking.sender(msg)