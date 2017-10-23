# The test writer class implements a specific test library interface for
# test case code generation. The specifics of the includes, test fixtures and
# so on are implemented by this class.
class TestWriter(object):
    def __init__(self):
        self._hasFixture = False
        self._namespaceOpen = False
        self._outputLines = []
        self._indentSpaces = 4
        self._indentTabs = 0
        self._openOnNewLine = False

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
        self._outputLines.append("#include <gtest/gtest.h>")

    def writeMain(self):
        self._outputLines.append("int main(int argc, char **argv) {")
        self._outputLines.append(self._indentToLevel(1) + "::testing::InitGoogleTest(&argc, argv);");
        self._outputLines.append(self._indentToLevel(1) + "return RUN_ALL_TESTS();");
        self._outputLines.append("}");

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
        pass

    def writeTestDeclaration(self, suiteName, testName):
        pass

    def writeTestCase(self, suiteName, testName, testBody):
        if (self._hasFixture):
            self._outputLines.append("TEST_F(%s, %s)" % (suiteName, testName) + self._openPeren(1))
        else:
            self._outputLines.append("TEST(%s, %s)" % (suiteName, testName) + self._openPeren(1))
        self._outputLines.append("%s\n}" % (testBody))

    def openTestFixture(self, suiteName):
        self._hasFixture = True
        self._outputLines.append(("class %s : public ::testing::Test" % (suiteName) + self._openPeren(0)))

    def closeTestFixture(self, suiteName):
        self._hasFixture = True
        self._outputLines.append("};")

    def writeSetUp(self, setUpBody):
        self._outputLines.append(self._indentToLevel(1) + "virtual void SetUp()" + self._openPeren(1) + "\n%s\n}" % (setUpBody));

    def writeTearDown(self, tearDownBody):
        self._outputLines.append(self._indentToLevel(1) + "virtual void TearDown()" + self._openPeren(1) + "\n%s\n}" % (tearDownBody));

    def passThroughLine(self, line):
        self._outputLines.append(line)

    def writeAssertEq(self, expectedStatement, actualStatement):
        self._outputLines.append("ASSERT_EQ(%s, %s);" % (expectedStatement, actualStatement))