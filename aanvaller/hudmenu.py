import bge, GameLogic

#standaard meuk
cont = bge.logic.getCurrentController()
own = cont.owner
scene = GameLogic.getCurrentScene()
name = own.name #naam van huidig object

#show cursor
bge.render.showMouse(True)

#sensors
mhover = cont.sensors["mhover"]
mlclick = cont.sensors["mlclick"]

#print(mhover.hitPosition) # !! gives precise location of mouse. use with mlclick for unit spawn, turret spawn, all the spawns.

if mhover.positive: # als je over map beweegt
    if mlclick.positive:# en klikt
        print(str(name + "pressed"))
        #print("location chosen : {}".format(name))
        #location = mhover.hitPosition # pak muis positie
        #print(location)
        #obj = own # readability
        #print(obj.worldPosition[0])
        #for altobj in scene.objects: # lijst van alle objecten in scene
        #    if altobj.name.startswith("spawn"): # filter lijst tot "spawn*"
        #        #print(altobj.name)
        #        if altobj.name != name: # als het niet dezelfde naam is verander kleur naar wit
        #            altobj.color = [1.0, 1.0, 1.0, 1.0]
        #        else:
        #            obj.color = [1.0, 0.0, 1.0, 1.0] # anders maak het paars, die is geselecteerd
        #            #global object om te laten zien welke selected is
        #            obj1 = scene.addObject("goblin", scene.objects['spawnpoint' + name[-1]])
        #            #obj1 = scene.addObject("goblin", obj)
        #            obj1.worldPosition.z = 3
