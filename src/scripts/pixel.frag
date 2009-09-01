varying vec3 position;
varying vec3 normal;
varying vec3 diffuse;
varying vec2 texcoord;

uniform sampler2D checkerboard;

void main(void)
{
    vec3 light_position = (gl_ProjectionMatrix * vec4(-2, 2, -10, 1.0)).xyz; //FIXME: pre-translated coords
    vec3 light = normalize(light_position - position);

    vec4 color = texture2D(checkerboard, texcoord.st);
    gl_FragColor = 1.3 * color * vec4(
                                      dot(normalize(light), normalize(normal)) * diffuse,
                                      1.0);
}
