from sys import platform
if platform == "linux" or platform == "linux2":
  import os
  os.environ["SDL_VIDEO_X11_FORCE_EGL"] = "1"

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLU import *

import glm

import ctypes
from ctypes import sizeof
import numpy
import objparser

from VAO import *
from Buffer import *
from VBO import *
from Texture import *
print("Imports successful")


pygame.init()

class Display:
  def __init__(self, width: int, height: int, window_flags: int, depth: int = 32, framerate: int = 60):
    self.screen = pygame.display.set_mode((width, height), window_flags | pygame.OPENGL | pygame.DOUBLEBUF, depth)

    self.clock = pygame.time.Clock()
    self.dt = 0.1
    self.framerate = framerate

    glViewport(0, 0, width, height)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

  def setCaption(self, caption: str):
    pygame.display.set_caption(caption)

  def update(self):
    pygame.display.flip()
  
  def tick(self):
    self.dt = self.clock.tick(self.framerate)

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


def renderloop():
  pass


def main():
  setup()

  parser = objparser.OBJparser("objects/cubeWTex.obj")
  triangle = parser.unpack_parse()

  vertices = triangle["v"]
  texs = triangle["vt"]
  indices = numpy.array(range(len(vertices)), dtype=GLuint)
  print(texs)

  with open("shaders/basicVT.vert.glsl", "r") as vertexShader, open("shaders/basicVT.frag.glsl", "r") as fragmentShader:
    vertStr = vertexShader.read()
    fragStr = fragmentShader.read()

    program = compileProgram(
        compileShader(vertStr, GL_VERTEX_SHADER),
        compileShader(fragStr, GL_FRAGMENT_SHADER)
    )

  # Create Vertex Array Object
  vao = VAO()
  vao.bind()

  # Create Vertex Buffer Object
  vbo = VBO(True, False)
  vbo.bind()
  vbo.setDataSep(vertices, texs)

  ebo = Buffer(GL_ELEMENT_ARRAY_BUFFER)
  ebo.bind()
  ebo.setData(indices, GL_UNSIGNED_INT)

  vao.unbind()

  glBindVertexArray(0)

  Projection = glm.perspective(glm.radians(45.0), WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)
  View = glm.lookAt(glm.vec3(1, 1, 1),
                    glm.vec3(0, 0, 0),
                    glm.vec3(0, 1, 0))
  # Model = glm.mat4(1.0)

  Model = glm.mat4([[0.333, 0, 0, 0],
                    [0, 0.333, 0, 0],
                    [0, 0, 0.333, 0],
                    [0, 0, 0, 1]]) * \
          glm.rotate(glm.radians(10.0), glm.vec3(1, -1, 0))

  MVP = Projection * View * Model
  mvpID = glGetUniformLocation(program, "MVP")

  # 1.0f, 0.5f, 0.2f
  colour = glm.vec3(1.0, 0.5, 0.2)
  colID = glGetUniformLocation(program, "col")


  tex = Texture("materials/test.jpg")
  tex.setWrapping(GL_REPEAT)
  tex.enableMipmap()
  tex.unbind()

  running = True
  while running:

    events.fetch()
    for event in events:
      if event.type == pygame.QUIT:
        running = False
      
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False

    # renderloop()

    glClearColor(0.2, 0.3, 0.3, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(program)
    vao.bind()
    tex.bind()
    glUniformMatrix4fv(mvpID, 1, GL_FALSE, glm.value_ptr(MVP))
    glUniform3fv(colID, 1, glm.value_ptr(colour))
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))

    display.update()

    display.tick()

    MVP = MVP * glm.rotate(glm.radians(0.5), glm.vec3(1, 1, 0.5))


if __name__ == "__main__":
  main()
