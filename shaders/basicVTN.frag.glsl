#version 330 core
out vec4 FragColor;

in vec2 texCoord;
in vec3 col;
in vec3 norm;

in vec3 lightPos;
in vec3 camPos;
in vec3 FragPos;

uniform sampler2D Texture;

void main()
{
    float specularStrength = 3.f;

    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    diff = (diff + 0.1) / 0.9f;

    vec3 camDir = normalize(camPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(camDir, reflectDir), 0.0), 32);
    float specular = specularStrength * spec;

    FragColor = texture(Texture, texCoord) * vec4(col, 1.f) * (diff + specular);
    // FragColor = vec4(1.f, 0.f, 1.f, 1.f) * (diff + specular);
    // FragColor = abs(vec4(norm, 1.f)) * diff;
} 