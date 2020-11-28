#Maria Jose Castro 
#181202
#Proyecto 4 Graficas
#una calaca psicodelica jeje


import pygame
import numpy
import glm
import pyassimp
from funciones import *

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texcoords;

uniform mat4 theMatrix;
uniform vec3 light;
uniform float time;

out float intensity;
out vec2 vertexTexcoords;
out vec3 v3Position;
out vec3 fnormal;
out float timer;

void main()
{
	fnormal = normal;
	vertexTexcoords = texcoords;
	v3Position = position;
	timer = time;
	intensity = dot(normal, normalize(light));
	gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1.0);
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 vertexTexcoords;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{

	fragColor = texture(tex, vertexTexcoords);
}
"""

#Lineas verticales que lo atraviezan
vertical_lines = """
#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 vertexTexcoords;
in vec3 v3Position;
in float timer;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;


void main()
{
	float tiempo = timer/0.5;
	float bright =  floor(mod(v3Position.x+timer, tiempo)*2.5) + floor(mod(v3Position.z*5.0, 1.0));
  vec4 color = mod(bright, 2.0) > .5 ? vec4(2.0, .0, 0.0, 1.0) : vec4(0.0, 3.0, 1.0, 1.0);
  fragColor = color * intensity;
}
"""

#este se miraba mas chilero en el mono 
#este cambia de azul a amarillo 
atlantis = """
#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 vertexTexcoords;
in vec3 v3Position;
in float timer;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{
	float tiempo = timer/1.5;
	float bright = floor(mod(v3Position.z*tiempo, 1.0)+timer);
  vec4 color = mod(bright, 2.0) > .8 ? vec4(5.0, 1.0, 0.0, 1.0) : vec4(.0, 0.0, 1.0, 1.0);
  fragColor = color * intensity;
}
"""

#El shader que traia por default pero se mira lindo
default = """
#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 vertexTexcoords;
in vec3 fnormal;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{
	fragColor = vec4(fnormal, 1.1);
}
"""

#Este son cuadritos que se hacen mas pequeno con el tiempo
psico = """
#version 460
layout(location = 0) out vec4 fragColor;

in float intensity;
in vec2 vertexTexcoords;
in vec3 v3Position;
in float timer;
in vec3 fnormal;

uniform sampler2D tex;
uniform vec4 diffuse;
uniform vec4 ambient;

void main()
{
	float tiempo = timer*0.5;
	float bright = floor(mod(v3Position.z, tiempo)*tiempo) +floor(mod(v3Position.y, tiempo)*tiempo);
  vec4 color = mod(bright, 1.5) > 0.007 ? vec4(0.0, 1.0, 0.0, 1.0) : vec4(1.0, 0.0, 1.0, 1.0);
  fragColor = color * intensity;
}
"""


shader = compileProgram(
		compileShader(vertex_shader, GL_VERTEX_SHADER),
		compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)


#scene = pyassimp.load('./pumpkin.obj')
#scene = pyassimp.load('./windmill.fbx')
scene = pyassimp.load('./skull.obj')


changeText(2)


def glize(node):
	# render
	for mesh in node.meshes:
		vertex_data = numpy.hstack([
			numpy.array(mesh.vertices, dtype=numpy.float32),
			numpy.array(mesh.normals, dtype=numpy.float32),
			numpy.array(mesh.texturecoords[0], dtype=numpy.float32),
		])

		index_data = numpy.hstack(
			numpy.array(mesh.faces, dtype=numpy.int32),
		)

		vertex_buffer_object = glGenVertexArrays(1)
		glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
		glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

		glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(0))
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(3 * 4))
		glEnableVertexAttribArray(1)
		glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 9 * 4, ctypes.c_void_p(6 * 4))
		glEnableVertexAttribArray(2)

		element_buffer_object = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)


		glUniform3f(
			glGetUniformLocation(shader, "light"),
			-100, 185, 0.2
		)

		glUniform4f(
			glGetUniformLocation(shader, "diffuse"),
			0.7, 0.2, 0, 1
		)

		glUniform4f(
			glGetUniformLocation(shader, "ambient"),
			0.2, 0.2, 0.2, 1
		)


		glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

	for child in node.children:
		glize(child)


camera = glm.vec3(0,0,5)
camera_speed = 5


i = glm.mat4()



glViewport(0, 0, 800, 600)

glEnable(GL_DEPTH_TEST)

paused = False
running = True

counter = 0
timecounter = 0

while running:
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glClearColor(6, 0.58, 0.58, 1.0)
	#glClearColor(0.7, 1.0, 0.7, 1.0) #el cuarto parametro es la transparencia

	glUseProgram(shader)

	theMatrix = createTheMatrix(counter, camera)

	theMatrixLocation = glGetUniformLocation(shader, 'theMatrix')


	timecounter += 0.01

	glUniform1f(
		glGetUniformLocation(shader, 'time'),
		timecounter
	)


	glUniformMatrix4fv(
	theMatrixLocation, #location
	1, # count
	GL_FALSE, 
	glm.value_ptr(theMatrix)
	)

	# glDrawArrays(GL_TRIANGLES, 0, 3)
	# glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)


	glize(scene.rootnode)

	pygame.display.flip()
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
			if event.key == pygame.K_f:
				glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
			if event.key == pygame.K_LEFT:
				camera.x -= camera_speed
			if event.key == pygame.K_RIGHT:
				camera.x += camera_speed
			if event.key == pygame.K_UP:
				camera.y -= camera_speed
			if event.key == pygame.K_DOWN:
				camera.y += camera_speed
			if event.key == pygame.K_q:
				changeText(0)
			if event.key == pygame.K_e:
				changeText(1)
			if event.key == pygame.K_r:
				changeText(2)
			if event.key == pygame.K_a:
				shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),compileShader(fragment_shader, GL_FRAGMENT_SHADER))
				glUseProgram(shader)
			if event.key == pygame.K_s:
				shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),compileShader(default, GL_FRAGMENT_SHADER))
				glUseProgram(shader)
			if event.key == pygame.K_d:
				shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),compileShader(vertical_lines, GL_FRAGMENT_SHADER))
				glUseProgram(shader)
			if event.key == pygame.K_g:
				shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),compileShader(atlantis, GL_FRAGMENT_SHADER))
				glUseProgram(shader)
			if event.key == pygame.K_h:
				shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),compileShader(psico, GL_FRAGMENT_SHADER))
				glUseProgram(shader)
			if event.key == pygame.K_x:
				paused = not paused

	if not paused:
		counter += 1
	clock.tick(0) 