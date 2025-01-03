import Buffer
import numpy

class VBO:
  "x, y, z, xt, yt, zt, xn, yn, zn..."
  def __init__(self, has_texture: bool, has_normal: bool):
    self.buff = Buffer(GL_VERTEX_BUFFER)
    self.has_texture = has_texture
    self.has_normal = has_normal

  def setData(self, data: numpy.array, dtype = GL_FLOAT):
    self.buff.setData(data, dtype)

  def setDataSep(self, verts: numpy.array, texverts: numpy.array | None = None, normverts: numpy.array | None = None, dtype = GL_FLOAT):
    mult = (1 + (1 if self.has_texture else 0) + (1 if self.has_normal else 0))
    data = numpy.zeros(len(verts) * mult)

    for i in range(len(verts)):
      data[i*mult] = verts[i*mult]
      if self.has_texture:
        data[i*mult+1] = texverts[i*mult+1]
      if self.has_normal:
        data[i*mult+2] = normverts[i*mult+2]

    self.setData(data, dtype)
