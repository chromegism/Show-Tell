from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image
import numpy

from matplotlib import pyplot as plt

from functools import cache


class Texture:
  def __init__(self):
    self.id = glGenTextures(1)

  def setWrapping(self, option):
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, option)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, option)

  def setBorderColour(self, colour):
    glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, colour)
  
  def setFiltering(self, option1, option2 = None):
    if not option2:
      option2 = option1
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, option1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, option2)

  def enableMipmap(self):
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

  @cache
  def loadImgFile(self, filename):
    image = Image.open(filename).transpose(Image.FLIP_TOP_BOTTOM)
    w = image.width; h = image.height

    pix = numpy.array(image, dtype=GLubyte)
    if len(pix[0]) > 3:
      pix = pix[:,:,:3]

    self.bind()
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, pix)
    glGenerateMipmap(GL_TEXTURE_2D)

  def bind(self):
    glBindTexture(GL_TEXTURE_2D, self.id)

  def unbind(self):
    glBindTexture(GL_TEXTURE_2D, 0)

if __name__ == "__main__":
  tex = Texture("materials/test.png")