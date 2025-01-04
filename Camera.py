import glm


def pythag(*args):
  s = 0
  for i in args:
    s += i ** 2
  return glm.sqrt(s)


class Camera:
  def __init__(self, pos: glm.vec3, origin: glm.vec3, ratio: float):
    self.pos = pos
    self.origin = origin
    self.ratio = ratio

    self.view = glm.lookAt(pos, origin, glm.vec3(0, 1, 0))
    self.projection = glm.perspective(glm.radians(45.0), ratio, 0.1, 100.0)
    
  def regen(self, pos: glm.vec3, origin: glm.vec3, ratio: float):
    self.pos = pos
    self.origin = origin
    self.ratio = ratio

    self.view = glm.lookAt(pos, origin, glm.vec3(0, 1, 0))
    self.projection = glm.perspective(glm.radians(45.0), ratio, 0.1, 100.0)

  def updateView(self):
    self.view = glm.lookAt(self.pos, self.origin, glm.vec3(0, 1, 0))

  def move_by(self, offset: glm.vec3):
    self.pos += offset
    self.updateView()

  def move_to(self, pos: glm.vec3):
    self.pos = pos
    self.updateView()

  def move_both_by(self, offset: glm.vec3):
    self.pos += offset
    self.origin += offset
    self.updateView()

  def move_both_to(self, pos: glm.vec3):
    self.pos = pos
    self.origin = pos
    self.updateView()    

  def move_origin_by(self, offset: glm.vec3):
    self.origin += offset
    self.updateView()

  def move_origin_to(self, pos: glm.vec3):
    self.origin = pos
    self.updateView()

  def move_forward(self, amt: float):
    dir = self.dir()
    self.move_both_by(dir * amt)

  def move_backward(self, amt: float):
    self.move_forward(-amt)

  def move_left(self, amt: float):
    dir = self.dir()
    dir = glm.normalize(glm.cross(dir, glm.vec3(dir.x, dir.y - 1, dir.z)))
    self.move_both_by(dir * amt)

  def move_right(self, amt: float):
    self.move_left(-amt)

  def move_up(self, amt: float):
    dir = self.dir()
    dir = glm.normalize(glm.cross(dir, glm.vec3(dir.x + 1, dir.y, dir.z - 1)))
    self.move_both_by(dir * amt)

  def move_down(self, amt: float):
    self.move_up(-amt)

  def flip_pos_origin(self):
    tmp = self.pos
    self.pos = self.origin
    self.origin = tmp
    self.updateView()

  def dir(self):
    return glm.normalize(self.origin - self.pos)
  
  def rotate_yaw_by(self, radians: float):
    offset = self.origin - self.pos
    rot = glm.rotate(offset, radians, glm.vec3(0, 1, 0))
    self.origin = rot + self.pos
    self.updateView()

  def rotate_pitch_by(self, radians: float):
    offset = self.origin - self.pos
    dir = self.dir()
    dir = glm.normalize(glm.cross(dir, glm.vec3(dir.x, dir.y - 1, dir.z)))
    rot = glm.rotate(offset, radians, dir)
    self.origin = rot + self.pos
    self.updateView()
  
  def __str__(self):
    return f"<Camera object - pos: {tuple(self.pos)} - origin: {tuple(self.origin)} - ratio: {self.ratio}"
  
if __name__ == "__main__":
  cam = Camera(glm.vec3(1, 1, 1), glm.vec3(0, 0, 0), 1280 / 720)
  cam.rotate_pitch_by(glm.radians(45))
  cam.move_origin_by(glm.vec3(-1, -1, -1))
  print(str(cam))

  print(pythag(3, 4))