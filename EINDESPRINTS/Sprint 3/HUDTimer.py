import bge
scene = bge.logic.getCurrentScene()
cont = bge.logic.getCurrentController()
own = cont.owner

own['timeLeft'] = 40
own['wave'] = 1
own['newWaveStarted'] = False
own['waveEnded'] = True

#if wave ended timeleft = 40
#timeleft --
#Waveended = False
#newavestarted = True
#timeleft = 300 sec
#timeleft --
#wave ++
#Waveended = true

def getSeconds(): 

    if own['timeLeft'] > 0:
        own['timeLeft'] -= 1 / (60 * 1)
        timeLeftRounded = round(own['timeLeft'], 2)
        scene.objects['TextTimeLeft'].text = "Time Left: " + str(timeLeftRounded)
        scene.objects['TextWave'].text = "Wave: " + str(own['wave'])
    else:
        own['wave'] += 1
        own['timeLeft'] = 5
        


