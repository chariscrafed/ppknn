from email.mime import base


key_switch_camera = 'c'
key_switch_mode = 'z'

key_forward = 'w'
key_back = 's'
key_left = 'a'
key_right = 'd'
key_up = 'e'
key_down = 'q'

key_turn_left = 'n'
key_turn_right = 'm'


class Hero():
    def __init__(self, pos, land):
        self.land = land
        self.mode = True
        self.cameraOn = False

        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)

        self.cameraBind()
        self.accept_events()

    def cameraBind(self):
        """Ikat kamera ke hero."""
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0, 0, 1.5)
        self.cameraOn = True

    def cameraUp(self):
        """Lepas kamera dari hero ke tampilan bebas."""
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        base.camera.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False

    def changeView(self):
        """Toggle tampilan kamera."""
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()

    def toggle_mode(self):
        """Toggle mode lewat dinding / tidak."""
        self.mode = not self.mode

    def turn_left(self):
        self.hero.setH((self.hero.getH() + 5) % 360)

    def turn_right(self):
        self.hero.setH((self.hero.getH() - 5) % 360)

    def look_at(self, angle):
        """Mengembalikan koordinat tujuan saat bergerak ke arah sudut tertentu."""
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())

        dx, dy = self.check_dir(angle)
        return x_from + dx, y_from + dy, z_from

    def check_dir(self, angle):
        if 0 <= angle <= 20:
            return (0, -1)
        elif angle <= 65:
            return (1, -1)
        elif angle <= 110:
            return (1, 0)
        elif angle <= 155:
            return (1, 1)
        elif angle <= 200:
            return (0, 1)
        elif angle <= 245:
            return (-1, 1)
        elif angle <= 290:
            return (-1, 0)
        elif angle <= 335:
            return (-1, -1)
        return (0, -1)

    def just_move(self, angle):
        """Pindahkan hero ke koordinat tujuan tanpa pengecekan."""
        self.hero.setPos(self.look_at(angle))

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)

    def forward(self):
        self.move_to(self.hero.getH() % 360)

    def back(self):
        self.move_to((self.hero.getH() + 180) % 360)

    def left(self):
        self.move_to((self.hero.getH() + 90) % 360)

    def right(self):
        self.move_to((self.hero.getH() + 270) % 360)

    def accept_events(self):
        base.accept(key_switch_camera, self.changeView)
        base.accept(key_switch_mode, self.toggle_mode)

        base.accept(key_turn_left, self.turn_left)
        base.accept(key_turn_left + '-repeat', self.turn_left)
        base.accept(key_turn_right, self.turn_right)
        base.accept(key_turn_right + '-repeat', self.turn_right)

        base.accept(key_forward, self.forward)
        base.accept(key_forward + '-repeat', self.forward)
        base.accept(key_back, self.back)
        base.accept(key_back + '-repeat', self.back)
        base.accept(key_left, self.left)
        base.accept(key_left + '-repeat', self.left)
        base.accept(key_right, self.right)
        base.accept(key_right + '-repeat', self.right)