#include <cstdlib>
#include <GL/glut.h>

// Display callback ------------------------------------------------------------

void display()
{
    // clear the draw buffer.
    glClear(GL_COLOR_BUFFER_BIT);   // Erase everything

    // set the color to use in draw
    glColor3f(0.5, 0.5, 0.0);
    // create a polygon ( define the vertexs)
    glBegin(GL_POLYGON);
    {
        glVertex2f(-0.5, -0.5);
        glVertex2f(-0.5,  0.5);
        glVertex2f( 0.5,  0.5);
        glVertex2f( 0.5, -0.5);
    }
    glEnd();

    // flush the drawing to screen.
    glFlush();
}

// Keyboard callback function ( called on keyboard event handling )
void keyboard(unsigned char key, int x, int y)
{
    if (key == 'q' || key == 'Q')
    {
        exit(EXIT_SUCCESS);
    }
}

void initializeMainLoop(int argc, char** argv)
{
    glutInit(&argc, argv);      // Initialize GLUT
    glutCreateWindow("OpenGL example");  // Create a window
    glutDisplayFunc(display);   // Register display callback
    glutKeyboardFunc(keyboard); // Register keyboard callback
    glutMainLoop();             // Enter main event loop
}
