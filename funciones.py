import pygame
import numpy
import glm
import pyassimp


from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

i = glm.mat4()

def createTheMatrix(counter, camera):
	translate = glm.translate(i, glm.vec3(0,0,0))
	rotate = glm.rotate(i, glm.radians(counter), glm.vec3(0,1,0))
	scale = glm.scale(i, glm.vec3(1,1,1))

	model = translate * rotate * scale
	#model = translate * scale
  #en este primer glm.vec3 modifico la camara
  #view = glm.lookAt(glm.vec3(0, 0, 5), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
	view = glm.lookAt(camera, glm.vec3(0,0,0), glm.vec3(0,1,0))
	projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000)

	return projection * view * model


def changeText(number):
	texturas = ['./psico1.png', './dark.png','./bone2.png']
	texture_surface = pygame.image.load(texturas[number])
	texture_data = pygame.image.tostring(texture_surface, 'RGB')
	width = texture_surface.get_width()
	height = texture_surface.get_height()

	view = glm.mat4(1)
	projection = glm.perspective(glm.radians(45),800/600,0.1,1000.0)
	model = glm.mat4(1)

	texture = glGenTextures(1)
	glBindTexture(GL_TEXTURE_2D, texture)
	glTexImage2D(
		GL_TEXTURE_2D,
		0,
		GL_RGB,
		width,
		height,
		0,
		GL_RGB,
		GL_UNSIGNED_BYTE,
		texture_data
	)
	glGenerateMipmap(GL_TEXTURE_2D)

changeText(2)

