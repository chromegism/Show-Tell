from OpenGL.GL import *
from OpenGL.GLU import *
from Buffer import *

class VAO:
  def __init__(self):
    self.id = glGenVertexArrays(1)

  def bind(self):
    glBindVertexArray(self.id)
  
  def unbind(self):
    glBindVertexArray(0)