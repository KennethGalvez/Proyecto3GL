from pickle import TRUE
import pygame
from pygame.locals import *

from shaders import *

from gl import Renderer, Model

from math import cos, sin, radians

width = 960
height = 540

deltaTime = 0.0

pygame.init()
pygame.mixer.music.load('C418.mp3')
pygame.mixer.music.play(5)
screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

rend.setShaders(vertex_shader, fragment_shader)

rend.target.z = -5

earth = Model("earth.obj", "earthNight.bmp")
tuna = Model("tuna.obj", "yellow.bmp")
submarine = Model("submarine.obj", "metalica.bmp")
mlrs = Model("mlrs.obj", "oro.bmp")
aqua = Model("Aquarail.obj", "rojo.bmp")

modelos = [("1", earth), ("2", tuna), ("3", submarine), ("4", mlrs), ('5', aqua)]
contador = 0

model = modelos[contador]
rend.scene = []
rend.scene.append(model[1])
    
isRunning = True

while isRunning:

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            elif event.key == pygame.K_z:
                rend.filledMode()
            elif event.key == pygame.K_x:
                rend.wireframeMode()

    if keys[K_q]:
        if rend.camDistance > 2:
            rend.camDistance -= 2 * deltaTime
    elif keys[K_e]:
        if rend.camDistance < 10:
            rend.camDistance += 2 * deltaTime

    if keys[K_a]:
        rend.angle -= 30 * deltaTime
    elif keys[K_d]:
        rend.angle += 30 * deltaTime


    if keys[K_w]:
        if rend.camPosition.y < 2:
            rend.camPosition.y += 5 * deltaTime
    elif keys[K_s]:
        if rend.camPosition.y > -2:
            rend.camPosition.y -= 5 * deltaTime
    
    elif keys[K_1] or keys[K_2] or keys[K_3] or keys[K_4] or keys[K_5]:
        n = 0 if keys[K_1] else 1 if keys[K_2] else 2 if keys[K_3] else 3 if keys[K_4] else 4 
        if not n == contador:
            model = modelos[n]
            rend.scene = []
            rend.scene.append(model[1])

    rend.target.y = rend.camPosition.y

    rend.camPosition.x = rend.target.x + sin(radians(rend.angle)) * rend.camDistance
    rend.camPosition.z = rend.target.z + cos(radians(rend.angle)) * rend.camDistance
    
    if keys[K_LEFT]:
        rend.pointLight.x -= 10 * deltaTime
    elif keys[K_RIGHT]:
        rend.pointLight.x += 10 * deltaTime
    elif keys[K_UP]:
        rend.pointLight.y += 10 * deltaTime
    elif keys[K_DOWN]:
        rend.pointLight.y -= 10 * deltaTime


    deltaTime = clock.tick(60) / 1000
    rend.time += deltaTime

    rend.update()
    rend.render()
    pygame.display.flip()

pygame.quit()
