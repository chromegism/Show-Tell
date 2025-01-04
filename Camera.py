import glm

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

  def move_origin_by(self, offset: glm.vec3):
    self.origin += offset
    self.updateView()

  def move_origin_to(self, pos: glm.vec3):
    self.origin = pos
    self.updateView()

  def flip_pos_origin(self):
    tmp = self.pos
    self.pos = self.origin
    self.origin = tmp
    self.updateView()

  def calcMVP(self, model: glm.mat4):
    MVP = self.projection * self.view * model
    return MVP
  
  def __str__(self):
    return f"<Camera object - pos: {tuple(self.pos)} - origin: {tuple(self.origin)} - ratio: {self.ratio}"
  
if __name__ == "__main__":
  cam = Camera(glm.vec3(1, 0, 0), glm.vec3(0, 0, 0), 1280 / 720)
  cam.move_by(glm.vec3(10, 5, 3))
  print(str(cam))