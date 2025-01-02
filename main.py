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

  parser = objparser.OBJparser("objects/test.obj")
  triangle = parser.array_parse()

  vertices = triangle["v"]
  indices = triangle["f"]

  with open("shaders/test.vert.glsl", "r") as vertexShader, open("shaders/test.frag.glsl", "r") as fragmentShader:
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
  vbo = Buffer(GL_ARRAY_BUFFER)
  vbo.bind()
  vbo.setData(vertices, GL_FLOAT)

  ebo = Buffer(GL_ELEMENT_ARRAY_BUFFER)
  ebo.bind()
  ebo.setData(indices, GL_UNSIGNED_INT)

  vbo.bind()
  vbo.VertexAttribPointer(0, 3, GL_FALSE, 3 * sizeof(GLfloat), 0)

  vao.unbind()

  glBindVertexArray(0)

  Projection = glm.perspective(glm.radians(45.0), WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 100.0)
  View = glm.lookAt(glm.vec3(1, 1, 1),
                    glm.vec3(0, 0, 0),
                    glm.vec3(0, 1, 0))
  Model = glm.mat4(1.0)
  
  MVP = Projection * View * Model
  print(MVP)

  mvpID = glGetUniformLocation(program, "MVP")
  print(mvpID)


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
    glUniformMatrix4fv(mvpID, 1, GL_FALSE, glm.value_ptr(MVP))
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, ctypes.c_void_p(0))

    display.update()

    display.tick()


if __name__ == "__main__":
  main()