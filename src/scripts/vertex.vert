varying vec3 diffuse;

void main(void)
{
    vec3 light_position = (gl_ProjectionMatrix * vec4(-2, 2, -10, 1.0)).xyz; //FIXME: pre-translated coords

    vec3 normal = normalize(gl_NormalMatrix * gl_Normal);

    gl_Position = ftransform();
    vec3 position = gl_Position.xyz;
    vec3 light = normalize(light_position - position);
    diffuse = dot(normalize(light), normalize(normal)) * gl_Color.rgb;
}
