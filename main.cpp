#include <iostream>	
#include "glad/gl.h"
#include <GLFW/glfw3.h>

GLFWwindow *window;

void paint(float r, float g, float b) {
  glEnable(GL_SCISSOR_TEST);

  for(int y=0; y < 600; y++) {
    for(int x=0; x < 800; x++) {
      glClearColor(r, g, b, 1);
      glScissor(x, y, 1, 1);
      glClear(GL_COLOR_BUFFER_BIT);
    }
  }

  glDisable(GL_SCISSOR_TEST);
}

int main(int argc, const char * argv[]) {
    std::cout << "Hello World!" << std::endl;

    if (!glfwInit())
    {
      fprintf(stderr, "Failed to initialize\n");
      exit(EXIT_FAILURE);
    }

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    window = glfwCreateWindow(300, 300, "opengl", NULL, NULL);

    if (!window)
    {
      fprintf(stderr, "Failed to open window\n");
      glfwTerminate();
      exit(EXIT_FAILURE);
    }

    glfwMakeContextCurrent(window);

    if (!gladLoadGL(glfwGetProcAddress)) {
      std::cout << "Failed to initalize glad\n";
      glfwDestroyWindow(window);
      glfwTerminate();
    }


    while(!glfwWindowShouldClose(window))
    {
      glClearColor(1.0f, 0.0f, 0.0f, 1.0f);
      glClear(GL_COLOR_BUFFER_BIT);

      paint(0.0f, 1.0f, 0.0f);

      glfwSwapBuffers(window);
      glfwPollEvents();
    }



    return 0;
} 

