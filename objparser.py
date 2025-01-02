import numpy
from OpenGL.GL import GLfloat, GLuint

class OBJparser:
  def __init__(self, filename: str):
    self.filename = filename

    self.identifiers = {"v": self.parse_vertex,
                        "f": self.parse_face}
    
    self.datatypes = {"v": GLfloat,
                      "f": GLuint}

  def parse_vertex(self, raw: str):
    l = []
    for i in raw.split():
      l.append(float(i))

    return l

  def parse_face(self, raw: str):
    l = []
    for i in raw.split():
      l.append(int(i))

    return l

  def str_to_parsed(self, s):
    s = s.rstrip().lstrip()
    tmp = ""
    for i in s:
      if i == " ":
        break

      else:
        tmp += i

    return (tmp, s[len(tmp)+1:])

  def full_parse(self):
    with open(self.filename, "r") as f:
      lines = f.readlines()

    p_lines = map(self.str_to_parsed, lines)
    
    output = {i: [] for i in self.identifiers}
    
    for i in p_lines:
      # Looks like a mess, but is simply appending the value with the key of the identifier to the return \
      # of the function in self.identifiers with the key which is also the ifentifier (it's a mess :( )
      extension = self.identifiers[i[0]](i[1])
      output[i[0]].extend(extension)

    for i in output:
      output[i] = numpy.array(output[i], dtype=self.datatypes[i])

    return output


if __name__ == "__main__":
  parser = OBJparser("objects/cube.obj")
  parsed = parser.full_parse()

  print(parsed)