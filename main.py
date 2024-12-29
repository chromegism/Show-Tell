import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Display:
  def __init__(self, width: int, height: int, window_flags: int, depth: int = 32, framerate: int = 60):
    self.screen = pygame.display.set_mode((width, height), window_flags | pygame.OPENGL | pygame.DOUBLEBUF, depth)

    self.clock = pygame.time.Clock()
    self.dt = 0.1
    self.framerate = framerate

    glEnable(GL_DEPTH_TEST)

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

  global events
  events = EventHandler()


def destroy():
  display.destroy()
  pygame.quit()


def renderloop():
  pass


def main():
  setup()

  running = True
  while running:

    events.setvals(pygame.event.get())
    for event in events:
      if event.type == pygame.QUIT:
        running = False
      
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False

    renderloop()

    display.tick()


if __name__ == "__main__":
  main()