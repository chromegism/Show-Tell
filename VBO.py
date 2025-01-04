from Buffer import *
import numpy
from OpenGL.GL import *
from OpenGL.GLU import *


class VBO:
  "x, y, z, xt, yt, zt, xn, yn, zn..."
  def __init__(self, has_texture: bool, has_normal: bool):
    self.buff = Buffer(GL_ARRAY_BUFFER)
    self.has_texture = has_texture
    self.has_normal = has_normal

  def setData(self, data: numpy.array, dtype = GL_FLOAT):
    self.buff.setData(data, dtype)

    size = int(data.nbytes / len(data))
    self.VertexAttribPointers(size)

  def setDataSep(self, verts: numpy.array, texverts: numpy.array = None, normverts: numpy.array = None, dtype = GL_FLOAT):
    self.bind()
    stride = (3 + (2 if self.has_texture else 0) + (3 if self.has_normal else 0))
    pairs = round(len(verts) / 3)
    data = numpy.zeros(pairs * stride, GLfloat)

    for i in range(0, pairs):
      a = i * 3
      j = i * stride
      data[j] = verts[a]; data[j+1] = verts[a+1]; data[j+2] = verts[a+2]
      if self.has_texture:
        b = i * 2
        data[j+3] = texverts[b]
        data[j+4] = texverts[b+1]
      if self.has_normal:
        data[j+5] = normverts[a]; data[j+6] = normverts[a+1]; data[j+7] = normverts[a+2]

    self.setData(data, dtype)

  def bind(self):
    self.buff.bind()

  def unbind(self):
    self.buff.unbind()

  def VertexAttribPointers(self, size):
    stride = (3 + (2 if self.has_texture else 0) + (3 if self.has_normal else 0))
    self.buff.VertexAttribPointer(0, 3, GL_FALSE, stride * size, 0)
    if self.has_texture:
      self.buff.VertexAttribPointer(1, 2, GL_FALSE, stride * size, 3 * size)
    if self.has_normal:
      self.buff.VertexAttribPointer(2, 3, GL_FALSE, stride * size, 5 * size)