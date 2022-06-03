#version 330

layout (location = 0) in vec2 a_position;

layout (location = 0) uniform mat4 u_projection;
layout (location = 1) uniform mat4 u_model_view;

void main() 
{
    gl_Position = u_projection * u_model_view * vec4(a_position, 0.0, 1.0);
}