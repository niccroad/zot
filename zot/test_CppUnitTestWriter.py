import unittest

from CppUnitTestWriter import CppUnitTestWriter

class test_CppUnitTestWriter(unittest.TestCase):
    def test_the_writer_writes_the_correct_include_section(self):
        writer = CppUnitTestWriter()
        writer.writeIncludeSection()
        self.assertEquals(['#include <TestCase.h>'], writer.getOutputLines())

    def test_the_writer_writes_the_correct_setup_function(self):
        writer = CppUnitTestWriter()
        writer.openTestFixture("FooTest")
        writer.writeTestRegistration("FooTest", "MethodBarDoesAbc")
        writer.writeSetUp("// Code here will be called immediately after the constructor (right\n// before each test).\n")
        writer.writeTestDeclaration("FooTest", "MethodBarDoesAbc")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['#include <cppunit/extensions/HelperMacros.h>',
                           'class FooTest : public CppUnit::TestCase {',
                           'CPPUNIT_TEST_SUITE(FooTest);',
                           'CPPUNIT_TEST(MethodBarDoesAbc);',
                           'CPPUNIT_TEST_SUITE_END();',
                           'public:',
                           '    virtual void setUp() {\n// Code here will be called immediately after the constructor (right\n// before each test).\n\n}',
                           '    void MethodBarDoesAbc();',
                           '};',
                           'CPPUNIT_TEST_SUITE_REGISTRATION(FooTest);'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_setup_function_peren_own_line(self):
        writer = CppUnitTestWriter()
        writer.setOpenPerenOnNewLine(True)
        writer.openTestFixture("FooTest")
        writer.writeTestRegistration("FooTest", "MethodBarDoesAbc")
        writer.writeSetUp("// Code here will be called immediately after the constructor (right\n// before each test).\n")
        writer.writeTestDeclaration("FooTest", "MethodBarDoesAbc")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['#include <cppunit/extensions/HelperMacros.h>',
                           'class FooTest : public CppUnit::TestCase\n{',
                           'CPPUNIT_TEST_SUITE(FooTest);',
                           'CPPUNIT_TEST(MethodBarDoesAbc);',
                           'CPPUNIT_TEST_SUITE_END();',
                           'public:',
                           '    virtual void setUp()\n    {\n// Code here will be called immediately after the constructor (right\n// before each test).\n\n}',
                           '    void MethodBarDoesAbc();',
                           '};',
                           'CPPUNIT_TEST_SUITE_REGISTRATION(FooTest);'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_teardown_function(self):
        writer = CppUnitTestWriter()
        writer.openTestFixture("FooTest")
        writer.writeTestRegistration("FooTest", "MethodBarDoesAbc")
        writer.writeTearDown("// Code here will be called immediately after each test (right\n// before the destructor).\n")
        writer.writeTestDeclaration("FooTest", "MethodBarDoesAbc")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['#include <cppunit/extensions/HelperMacros.h>',
                           'class FooTest : public CppUnit::TestCase {',
                           'CPPUNIT_TEST_SUITE(FooTest);',
                           'CPPUNIT_TEST(MethodBarDoesAbc);',
                           'CPPUNIT_TEST_SUITE_END();',
                           'public:',
                           '    virtual void tearDown() {\n// Code here will be called immediately after each test (right\n// before the destructor).\n\n}',
                           '    void MethodBarDoesAbc();',
                           '};',
                           'CPPUNIT_TEST_SUITE_REGISTRATION(FooTest);'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_teardown_function_peren_own_line(self):
        writer = CppUnitTestWriter()
        writer.setOpenPerenOnNewLine(True)
        writer.openTestFixture("FooTest")
        writer.writeTestRegistration("FooTest", "MethodBarDoesAbc")
        writer.writeTearDown("// Code here will be called immediately after each test (right\n// before the destructor).\n")
        writer.writeTestDeclaration("FooTest", "MethodBarDoesAbc")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['#include <cppunit/extensions/HelperMacros.h>',
                           'class FooTest : public CppUnit::TestCase\n{',
                           'CPPUNIT_TEST_SUITE(FooTest);',
                           'CPPUNIT_TEST(MethodBarDoesAbc);',
                           'CPPUNIT_TEST_SUITE_END();',
                           'public:',
                           '    virtual void tearDown()\n    {\n// Code here will be called immediately after each test (right\n// before the destructor).\n\n}',
                           '    void MethodBarDoesAbc();',
                           '};',
                           'CPPUNIT_TEST_SUITE_REGISTRATION(FooTest);'],
                          writer.getOutputLines())

    def test_write_test_case_in_a_fixture(self):
        writer = CppUnitTestWriter()
        writer.openTestFixture("FooTest")
        writer.writeTestRegistration("FooTest", "MethodBarDoesAbc")
        writer.writeTestDeclaration("FooTest", "MethodBarDoesAbc")
        writer.closeTestFixture("FooTest")
        writer.writeTestCase("FooTest",
                             "MethodBarDoesAbc",
                             "const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n")
        self.assertEquals(['#include <cppunit/extensions/HelperMacros.h>',
                           'class FooTest : public CppUnit::TestCase {',
                           'CPPUNIT_TEST_SUITE(FooTest);',
                           'CPPUNIT_TEST(MethodBarDoesAbc);',
                           'CPPUNIT_TEST_SUITE_END();',
                           'public:',
                           '    void MethodBarDoesAbc();',
                           '};',
                           'CPPUNIT_TEST_SUITE_REGISTRATION(FooTest);',
                           'void FooTest::MethodBarDoesAbc() {',
                           'const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n\n}',],
                          writer.getOutputLines())

    def test_write_test_case_outside_a_fixture(self):
        writer = CppUnitTestWriter()
        writer.writeTestCase("FooTest",
                             "MethodBarDoesAbc",
                             "const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n")
        self.assertEquals(['void FooTest::MethodBarDoesAbc() {',
                           'const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n\n}',],
                          writer.getOutputLines())

    def test_write_main(self):
        writer = CppUnitTestWriter()
        writer.writeMain()
        self.assertEquals(['#include <cppunit/extensions/TestFactoryRegistry.h>',
                           '#include <cppunit/ui/text/TestRunner.h>',
                           '',
                           'int main( int argc, char **argv)',
                           '{',
                           '    CppUnit::TextUi::TestRunner runner;',
                           '    CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();',
                           '    runner.addTest(registry.makeTest());',
                           '    bool wasSuccessful = runner.run("", false);',
                           '    return !wasSuccessful;',
                           '}'],
        writer.getOutputLines())


