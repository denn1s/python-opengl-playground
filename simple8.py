# import the pygame module, so you can use it
import pygame
import random
import numpy
import glm  # pip3 install pyglm
import pyassimp # pip3 install pyassimp
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

# define a main function

# initialize the pygame module
pygame.init()

# create a surface on screen that has the size of 240 x 180
screen = pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

glClearColor(0.5, 1.0, 0.5, 1.0)
glEnable(GL_DEPTH_TEST)

vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
uniform mat4 superMatriz;

void main()
{
  gl_Position = superMatriz * vec4(position.x, position.y, position.z, 1.0);
}
"""

fragment_shader = """
#version 460
layout(location = 0) out vec4 fragColor;

in vec3 ourColor;

void main()
{
   fragColor = vec4(1.0f, 0.0f, 1.0f, 1.0f);
}
"""

shader = compileProgram(
    compileShader(vertex_shader, GL_VERTEX_SHADER),
    compileShader(fragment_shader, GL_FRAGMENT_SHADER)
)

def glize(node):
  for mesh in node.meshes:
    vertex_data = numpy.hstack((
        numpy.array(mesh.vertices, dtype=numpy.float32),
        numpy.array(mesh.normals, dtype=numpy.float32),
        numpy.array(mesh.texturecoords[0], dtype=numpy.float32)
    ))

    faces = numpy.hstack(
        numpy.array(mesh.faces, dtype=numpy.int32)
    )

    vertex_buffer_object = glGenVertexArrays(1)
    glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, False, 9 * 4, None)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, False, 9 * 4, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 3, GL_FLOAT, False, 9 * 4, ctypes.c_void_p(6 * 4))
    glEnableVertexAttribArray(2)

    element_buffer_object = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, faces.nbytes, faces, GL_STATIC_DRAW)

    glDrawElements(GL_TRIANGLES, len(faces), GL_UNSIGNED_INT, None)

  for child in node.children:
    glize(child)



i = glm.mat4(1)

translate = glm.translate(i, glm.vec3(0, 0, 0))
rotate = glm.rotate(i, 15, glm.vec3(0, 1, 0))
scale = glm.scale(i, glm.vec3(1, 1, 1))

model = translate * rotate * scale
view = glm.lookAt(glm.vec3(0, 0, 200), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))
projection = glm.perspective(glm.radians(45), 800/600, 0.1, 1000.0)

superMatriz = projection * view * model

glViewport(0, 0, 800, 600)



def process_input():
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
      elif event.key == pygame.K_f:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


scene = pyassimp.load('./models/OBJ/spider.obj')
print(scene)


while True:
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glUseProgram(shader)

    glUniformMatrix4fv(
      glGetUniformLocation(shader, "superMatriz"),
      1,
      GL_FALSE,
      glm.value_ptr(superMatriz)
    )

    # glDrawArrays(GL_TRIANGLES, 0, 6)
    # glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

    # GL_LINE_LOOP

    glize(scene.rootnode)

    pygame.display.flip()

    process_input()
    clock.tick(15)

