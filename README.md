# ConditionalTest [![Build Status](https://travis-ci.org/niccroad/zot.svg?branch=master)](https://travis-ci.org/niccroad/zot)
Test C/C++ code without hastle and modification.

ConditionalTest uses the C++ preprocessor #include mechanism to introduce compile time mocks
into your tests. By introducing mocks at compile time, rather than runtime, the implementation
code can be tested with no design artifacts introduced by requirements for testing. This
includes testing for code which depends on the implementation of static methods, variables and
constructor calls.

## Usage

### Test Code

When using Conditional Test the tests are written in simple C++ code. This is then run through
a code parser and generator which further converts the test classes into final C++ code which
is the code which gets compiled and executed in practice. This eliminates a large amount of the
boiler plate code which tends to go with C++ test frameworks. It also allows code mocking to be
implemented at compile time by test code.

Maybe we have the following code to test,
Angle.h
```cpp
#ifndef Angle_h
#define Angle_h

class Angle {
public:
    void degreesToRadians(double a);
};

#endif // Angle_h
```

Angle.cpp
```cpp
#include "Angle.h"
#include "Math.h"

double Angle::degreesToRadians(double deg) {
    return Math::PI() * deg / 180.0;
}
```

Angle-Test.cxx
```cpp
#include "Angle.h"

MOCK_INCLUDE("Math.h",
class Math {
    static double PI() {
        return 3.14159;
    }
};
);

class AngleTest {
public:
    void testDegreesToRadians() {
        Angle angle;
        assertEquals(6.282, angle.degreesToRadians(360.0), 0.001);
    }
};
```

This is then compiled into the explicit test code.

```cpp
namespace {
#ifndef Math_h
#define Math_h
    class Math {
        static double PI() {
            return 3.14159;
        }
    };
#endif // Math_h

    #include "Angle.h"
    #include "Angle.cpp"
}

class AngleTest : public CppUnit::TestFixture {
    CPPUNIT_TEST_SUITE(AngleTest);
    CPPUNIT_TEST(testDegreesToRadians);
    CPPUNIT_TEST_SUITE_END();

public:
    void testDegreesToRadians() {
        Angle angle;
        testAssert(6.282, angle.degreesToRadians(360.0), 0.001);
    }
}
CPPUNIT_TEST_REGISTRATION(AngleTest);
```
