#version 330 core
out vec4 FragColor;

in vec2 texCoord;
in vec3 col;
in vec3 norm;

uniform sampler2D Texture;

void main()
{
    // FragColor = texture(Texture, texCoord) * vec4(col, 1.f);
    FragColor = abs(vec4(norm, 1.f));
} 