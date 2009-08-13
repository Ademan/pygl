varying vec3 position;
varying vec3 normal;
varying vec3 diffuse;
//varying vec3 light;

void main(void)
{
    vec3 light_position = (gl_ProjectionMatrix * vec4(-2, 2, -10, 1.0)).xyz; //FIXME: pre-translated coords
    vec3 light = normalize(light_position - position);
    gl_FragColor = vec4(
                        dot(normalize(light), normalize(normal)) * diffuse,
                       1.0);
}
