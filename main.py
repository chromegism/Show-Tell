from sys import platform
if platform == "linux" or platform == "linux2":
  import os
  os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLU import *

import glm
import random

# import ctypes
# from ctypes import sizeof
# import numpy
# import objparser

from VAO import *
from Buffer import *
from VBO import *
from Texture import *
from Mesh import *
print("Imports successful")


pygame.init()

class Display:
  def __init__(self, width: int, height: int, window_flags: int, depth: int = 32, framerate: int = 60, multisamples: int = 4):
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, multisamples)

    self.screen = pygame.display.set_mode((width, height), window_flags | pygame.OPENGL | pygame.DOUBLEBUF, depth)

    self.clock = pygame.time.Clock()
    self.dt = 0.1
    self.framerate = framerate

    glViewport(0, 0, width, height)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_TEXTURE_2D)

    error = glGetError()
    if error != GL_NO_ERROR:
      print("OpenGL Error:", error)

  def setCaption(self, caption: str):
    pygame.display.set_caption(caption)

  def update(self):
    pygame.display.flip()
  
  def tick(self):
    self.dt = self.clock.tick(self.framerate) / 1000

  def destroy(self):
    pygame.display.quit()
    del self.screen
    del self.clock


class EventHandler(list):
  def __init__(self):
    super().__init__([])

  def __setitem__(self, index, item: pygame.Event):
    super().__setitem__(index, item)

  def setvals(self, items: list[pygame.Event]):
    super().__init__(items)

  def fetch(self):
    super().__init__(pygame.event.get())


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_FLAGS = pygame.WINDOWSHOWN

def setup():
  global display
  display = Display(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_FLAGS)
  display.setCaption("pygame + pyopengl testing")

  global events
  events = EventHandler()


def destroy():
  display.destroy()
  pygame.quit()


def checkKeyDown(key):
  return pygame.key.get_pressed()[key]

def grabMouse(check: bool):
  pygame.event.set_grab(check)
  pygame.mouse.set_visible(not check)


def test1():
  setup()

  with open("shaders/basicVTN.vert.glsl", "r") as vertexShader, open("shaders/basicVTN.frag.glsl", "r") as fragmentShader:
    vertStr = vertexShader.read()
    fragStr = fragmentShader.read()

    program = compileProgram(
        compileShader(vertStr, GL_VERTEX_SHADER),
        compileShader(fragStr, GL_FRAGMENT_SHADER)
    )

  cam = Camera(glm.vec3(1, 1, 1), glm.vec3(0, 0, 0), WINDOW_WIDTH / WINDOW_HEIGHT)
  mesh = loadMeshFromFile(cam, "objects/cubeWTexNormal.obj", "materials/test.jpg")
  mesh.setProgram(program)
  mesh.scale = glm.vec3(0.333, 0.333, 0.333)
  mesh.updateMatrices()

  mesh2 = loadMeshFromFile(cam, "objects/skull.obj", "materials/MissingTexture.png")
  mesh2.setProgram(program)
  mesh2.scale = glm.vec3(0.05, 0.05, 0.05)
  mesh2.updateMatrices()
  mesh2.move_to(glm.vec3(-1, -1, 0))
  mesh2.rotate_by(glm.vec3(glm.radians(-90), 0, 0))

  tex = Texture()
  tex.loadImgFile("materials/white.png")

  cubeArr = []
  for i in range(15):
    for j in range(15):
      m = mesh.copy()
      m.move_to(glm.vec3(5+i*2, 3 * glm.sin(glm.radians(-i*10+j*10)) - 1.5, 5+j*2))
      m.setTexture(tex)
      m.setColour(glm.vec3(i / 15, 0, j / 15))
      m.rotate_to(glm.vec3(glm.radians(random.randint(0, 360)), glm.radians(random.randint(0, 360)), glm.radians(random.randint(0, 360))))
      cubeArr.append(m)

  movement_speed = 5

  mouse_sensitivity = 16
  grabMouse(True)
  mouse_mov = (0, 0)
  mouse_grabbing = True

  running = True
  while running:

    events.fetch()
    for event in events:
      if event.type == pygame.QUIT:
        running = False
      
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False

        elif event.key == pygame.K_TAB:
          cam.move_origin_to(glm.vec3(0, 0, 0))
          cam.move_to(glm.vec3(1, 1, 1))

        elif event.key == pygame.K_F2:
          mouse_grabbing = not mouse_grabbing
          grabMouse(mouse_grabbing)

      elif event.type == pygame.MOUSEMOTION:
        mouse_mov = event.rel

    if mouse_grabbing:
      pygame.mouse.set_pos((int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)))

    if checkKeyDown(pygame.K_w):
      cam.move_forward(movement_speed * display.dt)
    elif checkKeyDown(pygame.K_s):
      cam.move_backward(movement_speed * display.dt)

    if checkKeyDown(pygame.K_a):
      cam.move_left(movement_speed * display.dt)
    elif checkKeyDown(pygame.K_d):
      cam.move_right(movement_speed * display.dt)

    if checkKeyDown(pygame.K_q):
      cam.move_down(movement_speed * display.dt)
    elif checkKeyDown(pygame.K_e):
      cam.move_up(movement_speed * display.dt)

    if checkKeyDown(pygame.K_u):
      cam.rotate_pitch_by(glm.radians(-50 * display.dt))
    elif checkKeyDown(pygame.K_j):
      cam.rotate_pitch_by(glm.radians(50 * display.dt))

    if checkKeyDown(pygame.K_h):
      cam.rotate_yaw_by(glm.radians(100 * display.dt))
    elif checkKeyDown(pygame.K_k):
      cam.rotate_yaw_by(glm.radians(-100 * display.dt))

    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    mesh.render()
    mesh2.render()
    mesh.rotate_by(glm.vec3(glm.radians(100 * display.dt), 0, glm.radians(1)))
    # mesh2.rotate_by(glm.vec3(glm.radians(3), 0, 0))
    # cam.move_by(glm.vec3(0.01, 0, 0))

    for i in cubeArr:
      i.render()

    display.update()

    if mouse_mov != (0, 0):
      cam.rotate_yaw_by(-glm.radians(mouse_mov[0] * mouse_sensitivity * display.dt))
      cam.rotate_pitch_by(glm.radians(mouse_mov[1] * mouse_sensitivity * display.dt))

    mouse_mov = (0, 0)

    display.tick()


if __name__ == "__main__":
  test1()
