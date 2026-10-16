class Mapmanager():
    """Kelola peta dan blok di dunia game."""

    def __init__(self):
        self.model = 'block'
        self.texture = 'block.png'
        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1),
        ]
        self.startNew()

    def startNew(self):
        """Membuat node induk baru untuk seluruh blok peta."""
        self.land = render.attachNewNode("Land")

    def addBlock(self, position):
        """Membuat satu blok pada posisi tertentu."""
        block = loader.loadModel(self.model)
        block.setTexture(loader.loadTexture(self.texture))
        block.setPos(position)
        block.setColor(self.getColor(int(position[2])))
        block.reparentTo(self.land)
        return block

    def clear(self):
        """Reset peta."""
        if hasattr(self, 'land'):
            self.land.removeNode()
        self.startNew()

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        return self.colors[-1]

    def loadLand(self, filename):
        """Membuat peta dari file teks dan mengembalikan ukuran peta."""
        self.clear()
        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                parts = line.strip().split()
                for value in parts:
                    for z in range(int(value) + 1):
                        self.addBlock((x, y, z))
                    x += 1
                y += 1
        return x, y