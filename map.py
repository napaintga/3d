from panda3d.core import CollisionTraverser, CollisionNode, CollisionBox, CollisionRay, CollisionHandlerQueue

class Mapmanager:
    def __init__(self):
        self.grass_block = 'grass-block.glb'
        self.dirt_block = "dirt-block.glb"
        self.stone_block = "stone-block.glb"
        self.startNew()
        self.blocks = []
        
    def add_block(self, position, model):
        block_model = loader.loadModel(model)
        block_model.setPos(position)
        block_model.setHpr(0, 90, 0)  
        block_model.reparentTo(self.land)  
        self.blocks.append(block_model)
        
        blockSolid = CollisionBox((-1, -1, -2), (1, 1,2))  
        blockNode = CollisionNode('block-collision-node') 
        blockNode.addSolid(blockSolid)  
        
        collider = block_model.attachNewNode(blockNode)  
        collider.setPythonTag('owner', block_model) 

    def startNew(self):
        self.land = render.attachNewNode("Land")
        
    def clear(self):
        self.land.removeNode()
        self.startNew()
        
    def loadland(self, filename):
        self.clear()  
        with open(filename) as f:
            y = 0
            for line in f:
                x = 0
                line = line.split(" ")  # Split the line into separate block heights
                for z in line:
                    for z0 in range(0, int(z) * 2 + 2, 2):
                        self.add_block((x, y, z0 + 4), self.select_block(int(z) * 2 + 2, z0))
                    x += 2  
                y += 2  
        return x, y, int(z) 

    def select_block(self, z, z0):
        if z0 <= z // 3:
            return self.stone_block  # Stone 
        elif z0 + 2 == z:
            return self.grass_block  # Grass 
        else:
            return self.dirt_block  # Dirt 
