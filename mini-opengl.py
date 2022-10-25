import math
import numpy
import cyglfw3 as glfw
import random
import ctypes
import glm

import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders


# initialize glfw

glfw.Init()

# this makes opengl work on mac (https://developer.apple.com/library/content/documentation/GraphicsImaging/Conceptual/OpenGL-MacProgGuide/UpdatinganApplicationtoSupportOpenGL3/UpdatinganApplicationtoSupportOpenGL3.html)
glfw.WindowHint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.WindowHint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.WindowHint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)
glfw.WindowHint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.CreateWindow(800, 600, 'opengl')
glfw.MakeContextCurrent(window)

# initialize shaders

vertex_shader = """
#version 330
layout (location = 0) in vec4 position;

void main()
{
   gl_Position = position;
}
"""

fragment_shader = """
#version 330
layout(location = 0) out vec4 fragColor;

uniform vec4 pixelColor;

void main()
{
   fragColor = pixelColor;
}
"""



# initialize vertex data

vertex_data = numpy.array([
     -1.0,  -1.0,  0.0,
      1.0,  -1.0,  0.0, 
      1.0,   1.0,  0.0, 
     -1.0,   1.0,  0.0, 
], dtype=numpy.float32)

index_data = numpy.array([
    0, 1, 2, 
    0, 2, 3
], dtype=numpy.uint32)

vertex_array_object = gl.glGenVertexArrays(1)
gl.glBindVertexArray(vertex_array_object)

vertex_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer_object)
gl.glBufferData(gl.GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, gl.GL_STATIC_DRAW)

element_buffer_object = gl.glGenBuffers(1)
gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, gl.GL_STATIC_DRAW)

gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, False, 3 * 4, ctypes.c_void_p(0))
gl.glEnableVertexAttribArray(0)

# glfw requires shaders to be compiled after buffer binding

shader = shaders.compileProgram(
    shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER),
    shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
)

gl.glClearColor(0.5, 1.0, 0.5, 1.0)


def pixel(x, y, color):
  """
  gl.glUniform4f(
    gl.glGetUniformLocation(shader, "pixelColor"),
    color[0], color[1], color[2], 1
  )
  gl.glEnable(gl.GL_SCISSOR_TEST)
  gl.glScissor(x, y, 1, 1)
  gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
  gl.glDisable(gl.GL_SCISSOR_TEST)
  """
  gl.glEnable(gl.GL_SCISSOR_TEST)
  gl.glScissor(x, y, 1, 1 )
  gl.glClearColor(color[0], color[1], color[2], 1)
  gl.glClear(gl.GL_COLOR_BUFFER_BIT)
  gl.glDisable(gl.GL_SCISSOR_TEST)

# gl.glBindVertexArray(vertex_array_object)

x = 0
while not glfw.WindowShouldClose(window):
    gl.glClearColor(0.5, 1.0, 0.5, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # gl.glUseProgram(shader)


    for y in range(0, 600):
      for x1 in range(0, 800):
        pixel(x1, y, (0.0, 0.0, 1.0))

    # pixel(10, 10, (0.0, 0.0, 1.0))


    x += 1
    print(x)

    glfw.SwapBuffers(window)
    glfw.PollEvents()

gl.glBindVertexArray(0)

glfw.Terminate()