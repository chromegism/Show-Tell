from OpenGL.GL import *
from OpenGL.GLU import *

import glm

import numpy

from VAO import *
from Buffer import *
from VBO import *
from Texture import *
from objparser import *
from Camera import *


def genModelMatrix(offsets, rotations, scales):
  t = glm.mat4([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [offsets[0], offsets[1], offsets[2], 1]])
  
  r = glm.mat4(1)
  r = glm.rotate(r, rotations[0], glm.vec3(1, 0, 0))
  r = glm.rotate(r, rotations[1], glm.vec3(0, 1, 0))
  r = glm.rotate(r, rotations[2], glm.vec3(0, 0, 1))

  s = glm.mat4([[scales[0], 0, 0, 0],
                [0, scales[1], 0, 0],
                [0, 0, scales[2], 0],
                [0, 0, 0, 1]])
  
  model = t * r * s
  return model


class Mesh:
  def __init__(self):
    self.vao = None
    self.program = None
    self.vbo = None
    self.ebo = None
    self.texture = None

    self.camera = None
    self.MVP = None
    self.mvpID = 0
    self.model = None

    self.pos = glm.vec3(0)
    self.rot = glm.vec3(0)
    self.scale = glm.vec3(1)

  def updateMatrices(self):
    self.model = genModelMatrix(self.pos, self.rot, self.scale)
    self.MVP = self.camera.calcMVP(self.model)

  def render(self):
    glUseProgram(self.program)
    self.vao.bind()
    self.texture.bind()
    glUniformMatrix4fv(self.mvpID, 1, GL_FALSE, glm.value_ptr(self.MVP))
    glDrawElements(GL_TRIANGLES, len(self.ebo), GL_UNSIGNED_INT, ctypes.c_void_p(0))
    self.vao.unbind()
    glUseProgram(0)
    self.texture.unbind()

  def setVAO(self, vao: VAO):
    self.vao = vao

  def setVBO(self, vbo: VBO):
    self.vbo = vbo

  def setProgram(self, program: int, mvpVarName: str = "MVP"):
    self.program = program
    self.mvpID = glGetUniformLocation(self.program, mvpVarName)

  def setEBO(self, ebo: Buffer):
    self.ebo = ebo

  def setTexture(self, texture: Texture):
    self.texture = texture

  def setCamera(self, camera: Camera):
    self.camera = camera
    self.updateMatrices()
  

def loadMeshFromFile(camera: Camera, path: str, texpath: str | None = None):
  m = Mesh()

  parser = OBJparser(path)
  d = parser.unpack_parse()
  
  has_tex = len(d["vt"]) > 0
  has_norm = len(d["vn"]) > 0

  verts = d["v"]
  texs = d["vt"]
  norms = d["vn"]

  vao = VAO()
  vao.bind()

  vbo = VBO(has_tex, has_norm)
  vbo.setDataSep(verts, texs, norms)

  ebo = Buffer(GL_ELEMENT_ARRAY_BUFFER)
  indices = numpy.array(range(len(verts)))
  ebo.setData(indices, GL_UNSIGNED_INT)

  if texpath:
    tex = Texture()
    tex.loadImgFile(texpath)
    tex.setWrapping(GL_REPEAT)
    tex.enableMipmap()
  else:
    tex = None

  m.setVAO(vao)
  m.setVBO(vbo)
  m.setEBO(ebo)
  m.setTexture(tex)
  m.setCamera(camera)

  return m

  
if __name__ == "__main__":
  loadMeshFromFile("objects/cubeWTex.obj", "materials/test.jpg")