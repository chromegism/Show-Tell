#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 colour;

uniform mat4 MVP;
uniform vec3 col;

void main()
{
  gl_Position = MVP * vec4(aPos, 1.0);
  colour = col;
}