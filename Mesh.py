from OpenGL.GL import *
from OpenGL.GLU import *

import numpy

from VAO import *
from Buffer import *
from VBO import *
from Texture import *
from objparser import *


class Mesh:
  def __init__(self):
    self.vao = VAO()
    self.program = None
    self.vbo = None
    self.ebo = None
    self.Texture = None

  def render(self):
    self.vao.bind()
    glUseProgram(self.program)
    self.texture.bind()
    glDrawElements(GL_TRIANGLES, len(self.ebo), GL_UNSIGNED_INT, ctypes.c_void_p(0))
    self.vao.unbind()
    glUseProgram(0)
    self.texture.unbind()
  

def loadMeshFromFile(path: str, texpath: str | None = None):
  m = Mesh()

  parser = OBJparser(path)
  d = parser.unpack_parse()
  
  has_tex = len(d["vt"]) > 0
  has_norm = len(d["vn"]) > 0

  verts = d["v"]
  texs = d["vt"]
  norms = d["vn"]

  vbo = VBO(has_tex, has_norm)
  vbo.setDataSep(verts, texs, norms)

  
if __name__ == "__main__":
  loadMeshFromFile("objects/cubeWTex.obj", "materials/test.jpg")