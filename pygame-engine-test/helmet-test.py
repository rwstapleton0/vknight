import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)
    image = image.convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

class FaceGuard(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("face_guard.png", -1, 1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 0

class HelmetBody(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("helmet.png", -1, 1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 0, 0

class Helmet(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer

        helmet_body = HelmetBody()
        face_guard = FaceGuard()

        self.image = pg.Surface([200, 200])
        self.rect = self.image.get_rect()

        self.rect.topleft = 200, 200

        self.helmet_sprites = pg.sprite.RenderPlain((helmet_body, face_guard))


def main():
    
    pg.init()
    screen = pg.display.set_mode((800, 600), pg.SCALED)
    pg.display.set_caption("Captain Vee")

    # Create The Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 177, 64))

    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()

    helmet = Helmet()
    # allsprites = pg.sprite.RenderPlain((helmet))
    clock = pg.time.Clock()

    going = True
    while going:
        clock.tick(60)

        # Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False

        # Draw Everything
        screen.blit(background, (0, 0))
        helmet.helmet_sprites.draw(screen)
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()