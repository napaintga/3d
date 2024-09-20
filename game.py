from direct.showbase.ShowBase import ShowBase
from map import Mapmanager
from hero import Hero
from direct.gui.OnscreenText import OnscreenText

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        
        self.land = Mapmanager()
        x,y,z = self.land.loadland("land.txt")
        self.hero = Hero((x-2,y-2,z+14), self.land)
        print(x,y,z)
        self.camera.setH(90)
        self.camLens.setFov(90)
        
        self.setupSkybox()


        
    def setupSkybox(self):
        skybox = loader.loadModel('skybox/skybox.egg')
        skybox.setScale(500)
        skybox.setBin('background', 1)
        skybox.setDepthWrite(0)
        skybox.setLightOff()
        skybox.reparentTo(render)

game = Game()
game.run()
        