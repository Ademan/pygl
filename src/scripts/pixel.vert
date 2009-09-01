varying vec3 position;
varying vec3 normal;
varying vec3 diffuse;
varying vec2 texcoord;

void main(void)
{
    normal = normalize(gl_NormalMatrix * gl_Normal);

    diffuse = gl_Color.rgb;

    gl_Position = ftransform();
    position = gl_Position.xyz;
    texcoord = gl_MultiTexCoord0.st;
}
