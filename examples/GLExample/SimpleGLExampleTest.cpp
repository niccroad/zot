#include "TestFramework.h"
#include "SimpleGLExample.h"

MOCK_INCLUDE(<cstdlib>,
    int lastExitCode;
    int numExitCalls = 0;

    void exit(int exitCode) {
        numExitCalls++;
        lastExitCode = exitCode;
    });

MOCK_INCLUDE(<GL/glut.h>,
    int numGlutInitCalls = 0;
    int numGlutCreateWindowCalls = 0;
    int numGlutDisplayFuncCalls = 0;
    int numGlutKeyboardFuncCalls = 0;
    int numGlutMainLoopCalls = 0;
    int numGlBeginCalls = 0;
    int numGlEndCalls = 0;
    int numGlVertex2fCalls = 0;
    int numGlFlushCalls = 0;
    int numGlClearCalls = 0;
    int numGlColor3fCalls = 0;

    int GL_POLYGON = 5;
    int GL_COLOR_BUFFER_BIT = 11;

    void glBegin(int) {
        numGlBeginCalls++;
    }

    void glEnd() {
        numGlEndCalls++;
    }

    void glVertex2f(float, float) {
        numGlVertex2fCalls++;
    }

    void glFlush() {
        numGlFlushCalls++;
    }

    void glClear(int) {
        numGlClearCalls++;
    }

    void glColor3f(float, float, float) {
        numGlColor3fCalls++;
    }

    void glutInit(int* argc, char** argv) {
        numGlutInitCalls++;
    }

    void glutCreateWindow(const char* windowName) {
        numGlutCreateWindowCalls++;
    }

    void glutDisplayFunc(void* func) {
        numGlutDisplayFuncCalls++;
    }

    void glutKeyboardFunc(void* func) {
        numGlutKeyboardFuncCalls++;
    }

    void glutMainLoop() {
        numGlutMainLoopCalls++;
    }

    );

class SimpleGLExampleTest {
public:
    void setUp() {
        numExitCalls = 0;
    }

    void tearDown() {
        numExitCalls = 0;
    }

    void test_initialize_the_main_loop() {
        initializeMainLoop(0, nullptr);
        ASSERT_EQ(1, numGlutInitCalls);
        ASSERT_EQ(1, numGlutCreateWindowCalls);
        ASSERT_EQ(1, numGlutDisplayFuncCalls);
        ASSERT_EQ(1, numGlutKeyboardFuncCalls);
        ASSERT_EQ(1, numGlutMainLoopCalls);
    }

    void testDisplayFunction() {
        display();
        ASSERT_EQ(1, numGlClearCalls);
        ASSERT_EQ(1, numGlBeginCalls);
        ASSERT_EQ(1, numGlEndCalls);
        ASSERT_EQ(1, numGlFlushCalls);
        ASSERT_EQ(4, numGlVertex2fCalls);
        ASSERT_EQ(1, numGlColor3fCalls);
    }

    void test_exit_is_called_when_the_q_key_is_pressed() {
        keyboard('q', 5, 6);
        ASSERT_EQ(1, numExitCalls);
        ASSERT_EQ(EXIT_SUCCESS, lastExitCode);
    }

    void test_exit_is_called_when_the_Q_key_is_pressed() {
        keyboard('Q', 5, 6);
        ASSERT_EQ(1, numExitCalls);
        ASSERT_EQ(EXIT_SUCCESS, lastExitCode);
    }
}

TEST_ENTRY_POINT()