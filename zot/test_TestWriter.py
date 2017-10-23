import unittest

from TestWriter import TestWriter

class test_TestWriter(unittest.TestCase):
    def test_write_a_simple_test_case(self):
        writer = TestWriter()
        writer.writeIncludeSection()
        writer.openTestFixture("FooTest")
        writer.writeSetUp("// Code here will be called immediately after the constructor (right\n// before each test).\n")
        writer.writeTearDown("// Code here will be called immediately after each test (right\n// before the destructor).\n")
        writer.closeTestFixture("FooTest")
        writer.writeTestCase("FooTest",
                             "MethodBarDoesAbc",
                             "const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n")
        writer.writeTestCase("FooTest",
                             "DoesXyz",
                             "// Exercises the Xyz feature of Foo.")
        writer.writeMain()

    def test_the_writer_writes_the_correct_include_section(self):
        writer = TestWriter()
        writer.writeIncludeSection()
        self.assertEquals(['#include <gtest/gtest.h>'], writer.getOutputLines())

    def test_the_writer_writes_the_correct_setup_function(self):
        writer = TestWriter()
        writer.openTestFixture("FooTest")
        writer.writeSetUp("// Code here will be called immediately after the constructor (right\n// before each test).\n")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['class FooTest : public ::testing::Test {',
                           '    virtual void SetUp() {\n// Code here will be called immediately after the constructor (right\n// before each test).\n\n}',
                           '};'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_setup_function_peren_own_line(self):
        writer = TestWriter()
        writer.setOpenPerenOnNewLine(True)
        writer.openTestFixture("FooTest")
        writer.writeSetUp("// Code here will be called immediately after the constructor (right\n// before each test).\n")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['class FooTest : public ::testing::Test\n{',
                           '    virtual void SetUp()\n    {\n// Code here will be called immediately after the constructor (right\n// before each test).\n\n}',
                           '};'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_teardown_function(self):
        writer = TestWriter()
        writer.openTestFixture("FooTest")
        writer.writeTearDown("// Code here will be called immediately after each test (right\n// before the destructor).\n")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['class FooTest : public ::testing::Test {',
                           '    virtual void TearDown() {\n// Code here will be called immediately after each test (right\n// before the destructor).\n\n}',
                           '};'],
                          writer.getOutputLines())

    def test_the_writer_writes_the_correct_teardown_function_peren_own_line(self):
        writer = TestWriter()
        writer.setOpenPerenOnNewLine(True)
        writer.openTestFixture("FooTest")
        writer.writeTearDown("// Code here will be called immediately after each test (right\n// before the destructor).\n")
        writer.closeTestFixture("FooTest")
        self.assertEquals(['class FooTest : public ::testing::Test\n{',
                           '    virtual void TearDown()\n    {\n// Code here will be called immediately after each test (right\n// before the destructor).\n\n}',
                           '};'],
                          writer.getOutputLines())

    def test_write_test_case_in_a_fixture(self):
        writer = TestWriter()
        writer.openTestFixture("FooTest")
        writer.closeTestFixture("FooTest")
        writer.writeTestCase("FooTest",
                             "MethodBarDoesAbc",
                             "const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n")
        self.assertEquals(['class FooTest : public ::testing::Test {',
                           '};',
                           'TEST_F(FooTest, MethodBarDoesAbc) {',
                           'const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n\n}',],
                          writer.getOutputLines())

    def test_write_test_case_outside_a_fixture(self):
        writer = TestWriter()
        writer.writeTestCase("FooTest",
                             "MethodBarDoesAbc",
                             "const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n")
        self.assertEquals(['TEST(FooTest, MethodBarDoesAbc) {',
                           'const string input_filepath = \"this/package/testdata/myinputfile.dat\";\nconst string output_filepath = \"this/package/testdata/myoutputfile.dat\";\nFoo f;\nEXPECT_EQ(0, f.Bar(input_filepath, output_filepath));\n\n}',],
                          writer.getOutputLines())

    def test_write_main(self):
        writer = TestWriter()
        writer.writeMain()
        self.assertEquals(['int main(int argc, char **argv) {',
                           '    ::testing::InitGoogleTest(&argc, argv);',
                           '    return RUN_ALL_TESTS();',
                           '}'],
                          writer.getOutputLines())
