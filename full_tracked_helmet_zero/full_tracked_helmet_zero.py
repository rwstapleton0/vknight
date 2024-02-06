
class HelmetFull():

    def __init__(self, pos):
        self.pos = pos

        self.helmet_body = Actor('helmet_body_a.png', center=(WIDTH/2, HEIGHT/2), scale=0.5)
        self.face_guard = Actor('face_guard_a.png', center=(WIDTH/2, HEIGHT/2), anchor=((WIDTH/2)+140, (HEIGHT/2)-30), scale=0.5)


    def update(self):
        # self.face_guard.angle = 90
        animate(self.face_guard, tween='bounce_start_end', duration=0.4 , angle=-90)

    def draw(self, screen):

        self.helmet_body.draw()
        self.face_guard.draw()
    
    # def set_is_open(self):
    #     self.set_is_open()



WIDTH = 1024
HEIGHT = 800

helmet = HelmetFull((400,300))

def on_key_down():
    if keyboard[keys.SPACE]:
        print(keyboard)


def draw():
    screen.clear()
    screen.fill((128, 0, 0))

    helmet.update()

    helmet.draw(screen)