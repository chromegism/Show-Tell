#version 330 core
layout (location = 0) in vec3 vPos;
layout (location = 1) in vec2 tPos;
layout (location = 2) in vec3 nVec;

out vec2 texCoord;
out vec3 col;
out vec3 norm;

out vec3 lightPos;
out vec3 camPos;
out vec3 FragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 Colour;

uniform vec3 LightPos;
uniform vec3 CamPos;

void main()
{
  mat4 MVP = projection * view * model;
  gl_Position = MVP * vec4(vPos, 1.0);

  texCoord = tPos;
  col = Colour;
  norm = mat3(model) * normalize(nVec);
  lightPos = LightPos;

  FragPos = mat3(model) * vPos;
  camPos = CamPos;
}