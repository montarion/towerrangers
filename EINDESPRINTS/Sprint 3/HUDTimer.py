import bge
scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner


own['buildWave'] = True
own['fightWave'] = False
own['timeLeft'] = 5
own['buildTime'] = 5
own['fightTime'] = 10
own['wave'] = 1

def getSeconds(): 
    #own['timeLeft'] = 5
    if own['buildWave']:
        own['timeLeft'] -= 1 / (60 * 1)
        timeLeftRounded = round(own['timeLeft'], 2)
        scene.objects['TextTimeLeft'].text = "Time Left: " + str(timeLeftRounded)
        scene.objects['TextWave'].text = "Wave: " + str(own['wave'])
        if own['timeLeft'] <= 0:
            own['buildWave'] = False 
            own['fightWave'] = True 
            own['timeLeft'] += own['fightTime']
    if own['fightWave']:
        own['timeLeft'] -= 1 / (60 * 1)
        timeLeftRounded = round(own['timeLeft'], 2)
        scene.objects['TextTimeLeft'].text = "Time Left: " + str(timeLeftRounded)
        scene.objects['TextWave'].text = "Wave: " + str(own['wave'])
        if own['timeLeft'] <= 0:
            own['wave'] += 1
            own['buildWave'] = True
            own['fightWave'] = False
            own['timeLeft'] += own['buildTime']

        
    #else:
    #own['wave'] += 1
    #own['timeLeft'] = 5
        
def resetSeconds():
    cont['timer'] = cont['timeLeft']
    scene.objects['TextTimeLeft'].text = str(cont['timer'])
    



