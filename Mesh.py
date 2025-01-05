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
import copy


def genModelMatrix(offsets, rotations, scales):
  t = glm.mat4([[1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [offsets[0], offsets[1], offsets[2], 1]])
  
  r = rotationMatrix(rotations)

  s = glm.mat4([[scales[0], 0, 0, 0],
                [0, scales[1], 0, 0],
                [0, 0, scales[2], 0],
                [0, 0, 0, 1]])
  
  model = t * r * s
  return model


def rotationMatrix(rotations):
  r = glm.mat4(1)
  r = glm.rotate(r, rotations[0], glm.vec3(1, 0, 0))
  r = glm.rotate(r, rotations[1], glm.vec3(0, 1, 0))
  r = glm.rotate(r, rotations[2], glm.vec3(0, 0, 1))

  return r


class Mesh:
  def __init__(self):
    self.vao = None
    self.program = None
    self.vbo = None
    self.ebo = None
    self.texture = None
    self.colour = None

    self.camera = None
    self.model = None

    self.modelID = 0
    self.viewID = 0
    self.projID = 0
    self.colourID = 0
    self.lightPosID = 0
    self.camPosID = 0

    self.pos = glm.vec3(0)
    self.rot = glm.vec3(0)
    self.scale = glm.vec3(1)

  def updateMatrices(self):
    self.model = genModelMatrix(self.pos, self.rot, self.scale)

  def render(self):
    glUseProgram(self.program)
    self.vao.bind()

    if self.texture:
      self.texture.bind()
    
    # Need to implement a Light class and allow for multiple lights
    lightPos = glm.vec3(1, 3, 3)

    glUniformMatrix4fv(self.modelID, 1, GL_FALSE, glm.value_ptr(self.model))
    glUniformMatrix4fv(self.viewID, 1, GL_FALSE, glm.value_ptr(self.camera.view))
    glUniformMatrix4fv(self.projID, 1, GL_FALSE, glm.value_ptr(self.camera.projection))
    glUniform3fv(self.colourID, 1, glm.value_ptr(self.colour))
    glUniform3fv(self.lightPosID, 1, glm.value_ptr(lightPos))
    glUniform3fv(self.camPosID, 1, glm.value_ptr(self.camera.pos))
    glDrawElements(GL_TRIANGLES, len(self.ebo), GL_UNSIGNED_INT, ctypes.c_void_p(0))

    self.vao.unbind()
    glUseProgram(0)

    if self.texture:
      self.texture.unbind()

  def setVAO(self, vao: VAO):
    self.vao = vao

  def setVBO(self, vbo: VBO):
    self.vbo = vbo

  def setProgram(self, program: int, modelVarName: str = "model", viewVarName: str = "view", projectionVarName: str = "projection", colourVarName: str = "Colour"):
    self.program = program
    self.modelID = glGetUniformLocation(self.program, modelVarName)
    self.viewID = glGetUniformLocation(self.program, viewVarName)
    self.projID = glGetUniformLocation(self.program, projectionVarName)
    self.colourID = glGetUniformLocation(self.program, colourVarName)
    self.lightPosID = glGetUniformLocation(self.program, "LightPos")
    self.camPosID = glGetUniformLocation(self.program, "CamPos")

  def setEBO(self, ebo: Buffer):
    self.ebo = ebo

  def setTexture(self, texture: Texture):
    self.texture = texture

  def setCamera(self, camera: Camera):
    self.camera = camera
    self.updateMatrices()

  def setColour(self, colour: glm.vec3):
    self.colour = colour

  def move_by(self, offset: glm.vec3):
    self.pos += offset
    self.model = glm.translate(self.model, offset)

  def move_to(self, pos: glm.vec3):
    self.pos = pos
    self.updateMatrices()

  def rotate_by(self, r: glm.vec3):
    self.rot += r
    self.model = self.model * rotationMatrix(r)

  def rotate_to(self, r: glm.vec3):
    self.rot = r
    self.updateMatrices()

  def scale_by(self, s: glm.vec3):
    self.scale *= s
    self.model = glm.scale(self.model, s)

  def scale_to(self, s: glm.vec3):
    self.scale = s
    self.updateMatrices()

  def copy(self):
    m = Mesh()
    m.vao = self.vao
    m.program = self.program
    m.vbo = self.vbo
    m.ebo = self.ebo
    m.texture = self.texture
    m.colour = self.colour

    m.camera = self.camera
    m.model = self.model

    m.modelID = self.modelID
    m.viewID = self.viewID
    m.projID = self.projID
    m.colourID = self.colourID
    m.lightPosID = self.lightPosID
    m.camPosID = self.camPosID

    m.pos = self.pos
    m.rot = self.rot
    m.scale = self.scale

    return m
  

def loadMeshFromFile(camera: Camera, path: str, texpath: str | None = None, colour: glm.vec3 = None):
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

  if colour:
    m.setColour(colour)
  elif texpath:
    m.setColour(glm.vec3(1.0, 1.0, 1.0))
  else:
    m.setColour(glm.vec3(1.0, 0.0, 1.0))

  m.setVAO(vao)
  m.setVBO(vbo)
  m.setEBO(ebo)
  m.setTexture(tex)
  m.setCamera(camera)

  return m

  
if __name__ == "__main__":
  loadMeshFromFile("objects/cubeWTex.obj", "materials/test.jpg")
  