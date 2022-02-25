import pygame
import time
import pickle

from pygame.locals import*
from time import sleep

class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        screen_size = (1000, 500)
        #self.screen = pygame.display.set_mode(screen_size, 32)


    def update(self):
        pass
    def isTube(self):
        return False
    def isMario(self):
        return False
    def isGoomba(self):
        return False
    def isFireball(self):
        return False
    def isGoombaFire(self):
        return False
    def drawImg(self):
        pass




class Tube (Sprite):
    def __init__(self, x, y):
        super(). __init__(x, y)
        self.tubeImage = pygame.image.load("tube.png")
        self.w = 55
        self.h = 400

    def didIClickOnTube(self, mouse_x, mouse_y):
        if mouse_x < self.x:
            return False
        if mouse_x > self.x + self.w:
            return False
        if mouse_y < self.y:
            return False
        if mouse_y > self.y + self.h:
            return False
        return True

    def isTube(self):
        return True
    def drawImg(self):
        #self.screen.blit(self.tubeImage, (self.x - mariosX, self.y)) #fix as well
        pass

class Mario(Sprite):
    marioOffset = 200
    def __init__(self, x, y):
        super(). __init__(x, y)
        self.w = 60
        self.h = 95
        self.px = 0
        self.py = 0
        self.marioImages = [5]
        self.mario1 = pygame.image.load("mario1.png")
        self.mario2 = pygame.image.load("mario2.png")
        self.mario3 = pygame.image.load("mario3.png")
        self.mario4 = pygame.image.load("mario4.png")
        self.mario5 = pygame.image.load("mario5.png")
        self.marioImages.append(self.mario1)
        self.marioImages.append(self.mario2)
        self.marioImages.append(self.mario3)
        self.marioImages.append(self.mario4)
        self.marioImages.append(self.mario5)
        self.vert_velocity = 5.7
        self.numAirFrames = 0
        self.imageNum = 1


    def savePrevCoords(self):
        self.px = self.x
        self.py = self.y

    def update(self):
        self.vert_velocity += 5
        self.y += self.vert_velocity
        self.numAirFrames += 1
        if self.y > 300:
            self.vert_velocity = 0.0
            self.y = 300
            self.numAirFrames = 0

        if self.y < 0:
            self.y = 0

    def getOutOfTube(self, sprite):
        if (self.x + self.w )>= sprite.x and (self.px + self.w) < sprite.x:
            self.x = sprite.x - self.w - 3
        if self.x <= (sprite.x + sprite.w) and self.px >= (sprite.x + sprite.w):
            self.x = (sprite.x + sprite.w) + 1
        if (self.y + self.h) >= sprite.y and (self.py + self.h) < sprite.y:
            self.y = sprite.y - self.h - 1
            self.vert_velocity = 0
            self.numAirFrames = 0
        if self.y <= (sprite.y + sprite.h) and self.py > (sprite.y + sprite.h):
            self.y = sprite.y + sprite.h - 1


    def flipImageForward(self):
        self.imageNum+=1
        if self.imageNum > 5:
            self.imageNum = 1
    def flipImageBack(self):
        self.imageNum-=1
        if self.imageNum <= 1:
            self.imageNum = 5

    def isMario(self):
        return True

    def drawImg(self):
        #self.screen.blit(self.mario1, (self.x - Mario.marioOffset, self.y))
        pass

    def didIClickOnTube(self, mousex, mousey):
        pass

    def jumpMario(self):
        if self.numAirFrames <= 2:
            self.vert_velocity = -8.5

class Goomba(Sprite):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.w = 55
        self.h = 65
        self.px = 0
        self.py = 0
        self.goomimage = pygame.image.load("goomba.png")
        self.vert_velocity = 0
        self.direction = 1

    def savePrevCoords(self):
        self.px = self.x
        self.py = self.y

    def update(self):
        self.vert_velocity += 3.5
        self.y += self.vert_velocity
        if self.y > 335:
            self.vert_velocity = 0
            self. y = 335
        if self.y < 0:
            self.y = 1
        self.savePrevCoords()
        self.x += 3 * self.direction
        #move self.x += 3 * direction and when hit tube go other way

    def didIClickOnGoomba(self, mouse_x, mouse_y):
        if mouse_x < self.x:
            return False
        if mouse_x > self.x + self.w:
            return False
        if mouse_y < self.y:
            return False
        if mouse_y > self.y + self.h:
            return False
        return True

    def goombaOutOfTube(self, sprite):
        directionTF = False
        if (self.x + self.w) >= sprite.x and (self.px + self.w) < sprite.x: #collided left
            self.x = sprite.x - self.w - 1
            directionTF = True
            self.setDirection(directionTF)

        if self.x <= (sprite.x + sprite.w) and self.px >= (sprite.x + sprite.w): #collided right
            self.x = (sprite.x + sprite.w) + 1
            directionTF = False
            self.setDirection(directionTF)


    def setDirection(self, tfDirect):
        if tfDirect == True:
            self.direction = -1
        else:
            self.direction = 1

    def isGoomba(self):
        return True

class Fireball(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.fireballimage = pygame.image.load("fireball.png")
        self.w = 47
        self.h = 47
        self.vert_velocity = 0
        self.px = 0
        self.py = 0

    def savePrevCoords(self):
        self.px = self.x
        self.py = self.y

    def update(self):
        self.savePrevCoords()
        self.vert_velocity += 3.5
        self.y += self.vert_velocity
        self.x += 10 #change value later
        if self.y > 335:
            self.vert_velocity = 0
            self.y = 335
            self.vert_velocity = -20.5
        if self.y < 0:
            self.y = 1
    def isFireball(self):
        return True

class GoombaFire(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.goomFireImage = pygame.image.load("goomba_fire.png")

    def isGoombaFire(self):
        return True


class Model:
    def __init__(self):
        self.dest_x = 0
        self.dest_y = 0
        self.sprites = []
        #self.tube = Tube(60, 200)
        #self.sprites.append(self.tube)
        self.mario = Mario(200, 50)
        self.sprites.append(self.mario)
        self.frameCount = 0
        self.loadMap()



    def update(self):
        self.frameCount+=1
        for obj in self.sprites:
            if obj.isMario():
                obj.update()
            if obj.isGoomba():
                obj.update()
                self.collisionDetectGoomba(obj)
            if obj.isFireball():
                obj.update()
                self.collisionFireball(obj)
                if obj.x > self.mario.x + 1000:
                    self.sprites.remove(obj)
            if obj.isGoombaFire():
                if self.frameCount == 20:
                    self.sprites.remove(obj)

        self.collisionDetectTube()
        if self.frameCount > 60:
            self.frameCount = 0
        # if self.rect.left < self.dest_x:
        #     self.rect.left += 1
        # if self.rect.left > self.dest_x:
        #     self.rect.left -= 1
        # if self.rect.top < self.dest_y:
        #     self.rect.top += 1
        # if self.rect.top > self.dest_y:
        #     self.rect.top -= 1
    def saveMap(self):
        listGoom = []
        listTube = []
        #listMario

        #iterating through sprites list and saving x,y variables to separate lists to pickle
        for save in self.sprites:
            if save.isGoomba():
                xvar = save.x
                yvar = save.y
                xyVar = xvar, yvar
                listGoom.append(xyVar)
            if save.isTube():
                xvar = save.x
                yvar = save.y
                xyVar = xvar, yvar
                listTube.append(xyVar)

        #pickle save
        #print(listGoom)
        #print(listTube)
        pickle.dump(listGoom, open("goomsprites.dat", "wb"))
        pickle.dump(listTube, open("tubesprites.dat", "wb"))
        print("saved map...")

    def loadMap(self):
        #load goomba pickle x,y variables
        goombas = pickle.load(open("goomsprites.dat", "rb"))
        gLength = len(goombas)

        #load tube pickle x,y variables
        tubes = pickle.load(open("tubesprites.dat", "rb"))
        tLength = len(tubes)

        #load goombas
        for i in range(gLength):
            x, y = goombas[i]
            goom = Goomba(x, y)
            self.sprites.append(goom)

        #load tube
        for j in range(tLength):
            x, y = tubes[j]
            temptube = Tube(x, y)
            self.sprites.append(temptube)

    def addFireball(self, x, y):
        fireball = Fireball(x, y)
        self.sprites.append(fireball)

    def set_dest(self, pos):
        self.dest_x = pos[0]
        self.dest_y = pos[1]

    def addTube(self, mousex, mousey):
        tubeExists = False
        #iterate through sprites and find tube and check if it exists
        for obj in self.sprites:
            if obj.isTube():
                temptube = obj
                if temptube.didIClickOnTube(mousex, mousey):
                    tubeExists = True
                    self.sprites.remove(obj)
                    break
        if not tubeExists:
            self.sprites.append(Tube(mousex, mousey))

    def addGoom(self, mousex, mousey):
        goomExists = False
        for sprite in self.sprites:
            if sprite.isGoomba():
                tempgoom = sprite
                if tempgoom.didIClickOnGoomba(mousex, mousey):
                    goomExists = True
                    self.sprites.remove(sprite)
                    break
        if not goomExists:
            self.sprites.append(Goomba(mousex, mousey))

    def collisionDetectGoomba(self, object):
        collided = False
        for var in self.sprites:
            if var.isTube():
                tube = var
                if (object.x + object.w) < tube.x:
                    collided = False
                elif object.x > (tube.x + tube.w):
                    collided = False
                elif object.y + object.h < tube.y:
                    collided = False
                elif object.y > (tube.y + tube.h):
                    collided = False
                else:
                    collided = True
                    if collided:
                        object.goombaOutOfTube(tube)

    def collisionDetectTube(self):
        collided = False
        for var in self.sprites:
            if var.isTube():
                tube = var
                if (self.mario.x + self.mario.w) < tube.x:
                    collided = False
                elif self.mario.x > (tube.x + tube.w):
                    collided = False
                elif (self.mario.y + self.mario.h) < tube.y:
                    collided = False
                elif self.mario.y > (tube.y + tube.h):
                    collided = False
                else:
                    collided = True
                    if collided:
                        self.mario.getOutOfTube(tube)
                    self.mario.numAirFrames = 0

    def collisionFireball(self, object):
        collided = False
        for var in self.sprites:
            if var.isGoomba():
                goomba = var
                if (object.x + object.w) < goomba.x:
                    collided = False
                elif object.x > goomba.x + goomba.w:
                    collided = False
                elif object.y + object.h < goomba.y:
                    collided = False
                elif object.y > object.y + goomba.h:
                    collided = False
                else:
                    collided = True
                    if collided:
                        goomOnFire = GoombaFire(goomba.x, goomba.y)
                        self.sprites.append(goomOnFire)
                        self.sprites.remove(goomba)
class View(): # needs fixing
    def __init__(self, model):
        self.model = model
        screen_size = (1000, 500)
        self.screen = pygame.display.set_mode(screen_size, 32)
        #self.turtle_image = pygame.image.load("turtle.png") #loading turtle image

        #self.model.rect = self.turtle_image.get_rect()


    def update(self):
        self.screen.fill([52, 177, 235])
        pygame.draw.rect(self.screen, (102, 51, 0), (0, 400, 1000, 200), 0)
        #draw the sprites on screen
        for obj in self.model.sprites:
            if obj.isTube():
                temptube = obj
                #obj.drawImg(self.model.mario.x)
                self.screen.blit(temptube.tubeImage, (temptube.x - self.model.mario.x + Mario.marioOffset, temptube.y))
            if obj.isMario():
                #obj.drawImg(Mario.marioOffset)
                #print(self.model.mario.marioImages[1])
                tempmario = obj
                self.screen.blit(tempmario.marioImages[tempmario.imageNum], (Mario.marioOffset, self.model.mario.y))
            if obj.isGoomba():
                tempgoom = obj
                self.screen.blit(tempgoom.goomimage, (tempgoom.x - self.model.mario.x + Mario.marioOffset, tempgoom.y))
            if obj.isFireball():
                self.screen.blit(obj.fireballimage, (obj.x - self.model.mario.x + Mario.marioOffset, obj.y))
            if obj.isGoombaFire():
                self.screen.blit(obj.goomFireImage, (obj.x - self.model.mario.x + Mario.marioOffset, obj.y))
        pygame.display.flip()


class Controller():
    def __init__(self, model):
        self.model = model
        self.keep_going = True
        self.tubeEditor = False
        self.goombaEditor = False


    def update(self):
        self.model.mario.savePrevCoords()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
                if event.key == K_LCTRL:
                    self.model.addFireball(self.model.mario.x, self.model.mario.y)
                if event.key == K_x:
                   if self.tubeEditor:
                       self.tubeEditor = False
                       print("Tube editor off")
                   else:
                        self.tubeEditor = True
                        print("Tube editor on")
                # if event.key == K_s:
                #     self.model.saveMap()
                #     print("saving map...")
                # if event.key == K_l:
                #     print("loading map..")
                #     self.model.loadMap()
                if event.key == K_z:
                    if self.goombaEditor:
                        self.goombaEditor = False
                        print("Goomba editor off")
                    else:
                        self.goombaEditor = True
                        print("Goomba editor on")
            elif event.type == pygame.MOUSEBUTTONUP:
                #self.model.set_dest(pygame.mouse.get_pos())
                if self.tubeEditor:
                    x, y = pygame.mouse.get_pos()
                    self.model.addTube(x + self.model.mario.x - Mario.marioOffset, y)
                if self.goombaEditor:
                    x, y = pygame.mouse.get_pos()
                    self.model.addGoom(x + self.model.mario.x - Mario.marioOffset, y)


        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.model.mario.x -= 9
            self.model.mario.flipImageBack()
        if keys[K_RIGHT]:
            self.model.mario.x += 9
            self.model.mario.flipImageForward()
        if keys[K_SPACE]:
            self.model.mario.jumpMario()
            if self.model.mario.numAirFrames < 8:
                self.model.mario.vert_velocity -= 7.5

        #if keys[K_DOWN]:
         #   self.model.dest_y += 1





print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")
