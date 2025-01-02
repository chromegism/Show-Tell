from VAO import *
from Buffer import *

class Mesh:
  def __init__(self):
    self.vao = None
    self.program = None

  def addVAO(self, vao: VAO):
    self.vao = vao

  def addProgram(self, program):
    self.program = program

  def enable(self):
    self.vao.bind()
    glUseProgram(self.program)

  