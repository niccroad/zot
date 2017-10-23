# The test writer class implements a specific test library interface for
# test case code generation. The specifics of the includes, test fixtures and
# so on are implemented by this class.
class CppUnitTestWriter(object):
    def __init__(self):
        self._hasFixture = False
        self._namespaceOpen = False
        self._outputLines = []
        self._indentSpaces = 4
        self._indentTabs = 0
        self._openOnNewLine = False
        self._hasIncludedHelperMacros = False

    def _indentToLevel(self, level):
        return ' ' * (self._indentSpaces * level) + '\t' * (self._indentTabs * level)

    def setIndentLevel(self, numSpacesPerLevel = 4, numTabsPerLevel = 0):
        self._indentSpaces = numSpacesPerLevel
        self._indentTabs = numTabsPerLevel

    def _openPeren(self, level):
        if self._openOnNewLine:
            return '\n' + self._indentToLevel(level) + '{'
        else:
            return ' {'

    def setOpenPerenOnNewLine(self, openOnNewLine):
        self._openOnNewLine = openOnNewLine

    def getOutputLines(self):
        return self._outputLines

    def writeIncludeSection(self):
        self._outputLines.append("#include <TestCase.h>")

    def writeMain(self):
        self._outputLines.append('#include <cppunit/extensions/TestFactoryRegistry.h>')
        self._outputLines.append('#include <cppunit/ui/text/TestRunner.h>')
        self._outputLines.append('')
        self._outputLines.append('int main( int argc, char **argv)')
        self._outputLines.append('{')
        self._outputLines.append(self._indentToLevel(1) + 'CppUnit::TextUi::TestRunner runner;')
        self._outputLines.append(self._indentToLevel(1) + 'CppUnit::TestFactoryRegistry &registry = CppUnit::TestFactoryRegistry::getRegistry();')
        self._outputLines.append(self._indentToLevel(1) + 'runner.addTest(registry.makeTest());')
        self._outputLines.append(self._indentToLevel(1) + 'bool wasSuccessful = runner.run("", false);')
        self._outputLines.append(self._indentToLevel(1) + 'return !wasSuccessful;')
        self._outputLines.append('}')

    def writeInclude(self, includeDef, inNamespace):
        if inNamespace != self._namespaceOpen:
            if self._namespaceOpen:
                self._outputLines.append("}")
            else:
                self._outputLines.append("namespace {")
            self._namespaceOpen = inNamespace
        self._outputLines.append("#include %s" % (includeDef))

    def closeNamespaceIfOpen(self):
        if self._namespaceOpen:
            self._outputLines.append("}")
            self._namespaceOpen = False

    def writeMockInclude(self, mockGuard, mockDefinition):
        if not self._namespaceOpen:
            self._outputLines.append("namespace {")
            self._namespaceOpen = True
        self._outputLines.append("#define %s" % mockGuard)
        self._outputLines.append(mockDefinition)

    def writeTestRegistration(self, suiteName, testName):
        if not self._hasWrittenSuite:
            self._outputLines.append("CPPUNIT_TEST_SUITE(%s);" % (suiteName))
            self._hasWrittenSuite = True
        self._outputLines.append("CPPUNIT_TEST(%s);" % (testName))

    def writeTestDeclaration(self, suiteName, testName):
        if self._hasWrittenSuite:
            self._outputLines.append("CPPUNIT_TEST_SUITE_END();")
            self._hasWrittenSuite = False
        if not self._hasWrittenPublic:
            self._hasWrittenPublic = True
            self._outputLines.append("public:")
        self._outputLines.append(self._indentToLevel(1) + "void %s();" % (testName))

    def writeTestCase(self, suiteName, testName, testBody):
        self._outputLines.append("void %s::%s()" % (suiteName, testName) + self._openPeren(1))
        self._outputLines.append("%s\n}" % (testBody))

    def openTestFixture(self, suiteName):
        self._hasFixture = True
        if not self._hasIncludedHelperMacros:
            self._outputLines.append('#include <cppunit/extensions/HelperMacros.h>')
            self._hasIncludedHelperMacros = True
        self._outputLines.append(("class %s : public CppUnit::TestCase" % (suiteName) + self._openPeren(0)))
        self._hasWrittenPublic = False
        self._hasWrittenSuite = False

    def closeTestFixture(self, suiteName):
        self._hasFixture = True
        self._outputLines.append("};")
        self._outputLines.append("CPPUNIT_TEST_SUITE_REGISTRATION(%s);" % (suiteName))

    def writeSetUp(self, setUpBody):
        if self._hasWrittenSuite:
            self._outputLines.append("CPPUNIT_TEST_SUITE_END();")
            self._hasWrittenSuite = False
        if not self._hasWrittenPublic:
            self._hasWrittenPublic = True
            self._outputLines.append("public:")
        self._outputLines.append(self._indentToLevel(1) + "virtual void setUp()" + self._openPeren(1) + "\n%s\n}" % (setUpBody));

    def writeTearDown(self, tearDownBody):
        if self._hasWrittenSuite:
            self._outputLines.append("CPPUNIT_TEST_SUITE_END();")
            self._hasWrittenSuite = False
        if not self._hasWrittenPublic:
            self._hasWrittenPublic = True
            self._outputLines.append("public:")
        self._outputLines.append(self._indentToLevel(1) + "virtual void tearDown()" + self._openPeren(1) + "\n%s\n}" % (tearDownBody));

    def passThroughLine(self, line):
        self._outputLines.append(line)

    def writeAssertEq(self, expectedStatement, actualStatement):
        self._outputLines.append("ASSERT_EQ(%s, %s);" % (expectedStatement, actualStatement))