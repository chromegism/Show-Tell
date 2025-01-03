from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes
import numpy
from ctypes import sizeof

class Buffer:
  def __init__(self, _type):
    self._type = _type
    self.id = glGenBuffers(1)
    
    self.dtype = None
    self.dlen = 0

  def bind(self):
    glBindBuffer(self._type, self.id)

  def unbind(self):
    glBindBuffer(self._type, 0)

  def setData(self, data: numpy.array, dataType: type, usage = GL_STATIC_DRAW):
    self.bind()
    glBufferData(self._type,
                 data.nbytes,
                 data,
                 usage)
    
    self.dtype = dataType
    self.dlen = len(data)

  def VertexAttribPointer(self, index, components, normalised, _stride, offset):
    if not self.dtype:
      raise ValueError("Buffer has no data and therefore no type")
    
    glVertexAttribPointer(index, components, self.dtype, normalised, _stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(index)