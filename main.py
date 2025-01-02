import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.GLU import *
import ctypes
import numpy
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


sizeOfFloat = ctypes.sizeof(GLfloat)
# Three vertices, with an x,y,z for each.
vertices = numpy.array([
  -0.5, -0.5, 0.0,
   0.5, -0.5, 0.0,
   0.0,  0.5, 0.0
], GLfloat)

# indices = numpy.array([0, 1, 2], GLfloat)


def main():
  setup()

  with open("shaders/test.vert.glsl", "r") as vertexShader, open("shaders/test.frag.glsl", "r") as fragmentShader:
    vertStr = vertexShader.read()
    fragStr = fragmentShader.read()

    program = compileProgram(
        compileShader(vertStr, GL_VERTEX_SHADER),
        compileShader(fragStr, GL_FRAGMENT_SHADER)
    )

  # Create Vertex Array Object
  VAO = glGenVertexArrays(1)
  glBindVertexArray(VAO)

  # Create Vertex Buffer Object
  VBO = glGenBuffers(1)
  glBindBuffer(GL_ARRAY_BUFFER, VBO)
  glBufferData(GL_ARRAY_BUFFER, 
               vertices.nbytes, 
               vertices, 
               GL_STATIC_DRAW)

  glBindBuffer(GL_ARRAY_BUFFER, VBO)
  glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeOfFloat, ctypes.c_void_p(0))
  glEnableVertexAttribArray(0)

  glBindBuffer(GL_ARRAY_BUFFER, 0)

  glBindVertexArray(0)


  running = True
  while running:

    events.setvals(pygame.event.get())
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
    glBindVertexArray(VAO)
    glDrawArrays(GL_TRIANGLES, 0, 3)

    display.update()

    display.tick()


if __name__ == "__main__":
  main()