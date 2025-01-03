import numpy
from OpenGL.GL import GLfloat, GLuint

class OBJparser:
  def __init__(self, filename: str):
    self.filename = filename

    self.identifiers = {"v": self.parse_vertex,
                        "vt": self.parse_tex,
                        "vn": self.parse_norm,
                        "f": self.parse_face,
                        "mtllib": lambda x: x,
                        "o": lambda x: x,
                        "usemtl": lambda x: x}
    
    self.datatypes = {"v": GLfloat,
                      "vt": GLfloat,
                      "vn": GLfloat,
                      "f": GLuint}
    
    self.vertices = []
    self.texverts = []
    self.normverts = []
    self.vertindices = []
    self.texindices = []
    self.normindices = []
  
  def parse_vertex(self, raw: str):
    splitted = raw.split()
    splitted = [float(i) for i in splitted]
    self.vertices.extend(splitted)

  def parse_tex(self, raw: str):
    splitted = raw.split()
    splitted = [float(i) for i in splitted]
    self.texverts.extend(splitted)

  def parse_norm(self, raw: str):
    splitted = raw.split()
    splitted = [float(i) for i in splitted]
    self.normverts.extend(splitted)

  def parse_face(self, raw: str):
    splitted = raw.split()

    t_spl = splitted[0].split("/")
    has_tex = len(t_spl) >= 2
    has_norm = len(t_spl) >= 3

    splitted = [i.split("/") for i in splitted]
    for i in splitted:
      self.vertindices.append(int(i[0])-1)
      if has_tex:
        self.texindices.append(int(i[1])-1)
      if has_norm:
        self.normindices.append(int(i[2])-1)

  def splitID(self, raw: str):
    raw = raw.rstrip().lstrip()
    tmp = ""
    for i in raw:
      if i == " ":
        break
      else:
        tmp += i
    
    return (tmp, raw[len(tmp)+1:])

  def unpack_parse(self):
    with open(self.filename, "r") as f:
      lines = f.readlines()

    for i in lines:
      s = self.splitID(i)
      self.identifiers[s[0]](s[1])

    upkverts = []
    upktexs = []
    upknorms = []
    for i in range(len(self.vertindices)):
      a = self.vertindices[i]*3; b = (self.vertindices[i]+1)*3
      upkverts.extend(self.vertices[a:b])
      if len(self.texverts) > 0:
        a = self.texindices[i]*2; b = (self.texindices[i]+1)*2
        upktexs.extend(self.texverts[a:b])
      if len(self.normverts) > 0:
        a = self.normindices[i]*3; b = (self.normindices[i]+1)*3
        upknorms.extend(self.normverts[a:b])

    output = {"v": numpy.array(upkverts, GLfloat),
              "vt": numpy.array(upktexs, GLfloat),
              "vn": numpy.array(upknorms, GLfloat)}

    return output


if __name__ == "__main__":
  parser = OBJparser("objects/cubeWTexNormal.obj")
  parsed = parser.unpack_parse()

  print(parsed)