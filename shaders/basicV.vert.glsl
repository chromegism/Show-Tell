#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 col;

uniform mat4 MVP;
uniform vec3 Colour;

void main()
{
  gl_Position = MVP * vec4(aPos, 1.0);
  col = Colour;
}