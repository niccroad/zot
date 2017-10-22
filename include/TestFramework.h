#ifndef TestFramework_h
#define TestFramework_h

void assertTrue(bool condition);

template <typename Kind>
void assertEquals(Kind expected, Kind actual) {
	assertTrue(expected == actual);
}

void assertEquals(double expected, double actual, double margin);

#define MOCK_INCLUDE(IncludeFile, ...)
#define TEST_ENTRY_POINT()                                      \
    int main(int argc, char** argv) { return 0; }

#endif // TestFramework_h
