import glm

class Light:
  def __init__(self, pos: glm.vec3, dir: glm.vec3):
    self.pos = pos
    self.dir = dir