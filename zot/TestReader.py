import CppHeaderParser
from difflib import SequenceMatcher
import os, re, glob

class CppHeader(object):
    def __init__(self):
        pass

class TestReader(object):
    def __init__(self, writer, includeResolver = None):
        self.writer = writer
        self._includeResolver = includeResolver

    def _handleInclude(self):
        pass

    def _handleTestClass(self):
        pass

    def _handleTestCase(self):
        pass

    def _resolveCppHeaderParser(self, includeFile, fileDirectory):
        try:
            resolvedFile = self._includeResolver.resolveInclude(includeFile)
            if resolvedFile != None:
                cppHeader = CppHeaderParser.CppHeader(resolvedFile)
                return cppHeader

        except CppHeaderParser.CppParseError as e:
            print(e)

    def _resolveHeaderGuards(self, includeFile, fileDirectory):
        cppHeader = self._resolveCppHeaderParser(includeFile, fileDirectory)
        closestHeader = 'Header_h'
        longestSize = 0
        if cppHeader == None:
            return includeFile.replace('/', '_').replace('.', '_').replace('<', '').replace('>', '').replace('"', '')
        for define in cppHeader.defines:
            match = SequenceMatcher(None, includeFile, closestHeader).find_longest_match(0, len(includeFile), 0, len(closestHeader))
            if match.size > longestSize:
                closestHeader = define
                longestSize = match.size
        return closestHeader

    def _retrieveBlock(self,
                       line,
                       fileIterator,
                       openString = '(',
                       closeString = ')'):
        found_lines = []
        open_count = 1
        while open_count > 0:
            index = 0
            while index < len(line):
                next_open = line.find(openString, index)
                next_close = line.find(closeString, index)

                if next_open == -1 and next_close == -1:
                    break
                if next_open == -1 or (next_close != -1 and next_close < next_open):
                    open_count = open_count - 1
                    index = next_close + 1
                    if open_count <= 0:
                        found_lines.append(line[:next_close])
                        return ''.join(found_lines)
                    continue
                elif next_close == -1 or (next_open != -1 and next_open < next_close):
                    open_count = open_count + 1
                    index = next_open + 1
                    continue
            found_lines.append(line)
            line = next(fileIterator)
        return ''.join(found_lines)

    def _handleMockInclude(self, line, fileIterator):
        include_start = line.find('MOCK_INCLUDE(')
        if include_start == -1:
            return False
        open_count = 1
        macro_lines = []
        begin_index = include_start + len('MOCK_INCLUDE(')

        macro_block = self._retrieveBlock(line[begin_index:],
                                          fileIterator)

        first_comma_index = macro_block.find(',')
        if first_comma_index != -1:
            include_definition = macro_block[0:first_comma_index].strip()
            macro_block = macro_block[first_comma_index + 1:].strip()
            self.declaration_macros[include_definition] = macro_block
        return True

    def _handleEntryPoint(self, line, fileIterator):
        entry_point_index = line.find('TEST_ENTRY_POINT(')
        if entry_point_index == -1:
            return False
        self.writer.writeMain()
        return True

    def _handleIncludeLine(self,
                           line,
                           fileIterator,
                           writtenIncludes,
                           fileDirectory):
        pound_include_index = line.find('#include')
        if pound_include_index == -1:
            return False
        match = re.match('\s*(["<].*[">])\s*', line[pound_include_index + 8:])
        if match == None:
            return False
        self._writeIncludeOrStub(match.group(1),
                                 writtenIncludes,
                                 fileDirectory,
                                 True)
        return True

    def _handleClassStart(self,
                          line,
                          fileIterator,
                          writtenIncludes,
                          fileDirectory):
        class_index = line.find('class')
        if class_index == -1:
            return False
        match = re.search('class\s+(\w+)', line)
        if match == None:
            return False

        open_peren_index = line.find('{')
        if open_peren_index == -1:
            return False
        self._retrieveBlock(line[open_peren_index + 1:],
                            fileIterator, '{', '}')

        someClass = match.group(1)
        if someClass in self.cppHeader.classes:
            if not someClass.endswith('Test'):
                return False

            for underTestClass in self.classesUnderTest:
                self._writeIncludeOrStub('"%s.cpp"' % (underTestClass),
                                         writtenIncludes,
                                         fileDirectory,
                                         True)

            self.writer.closeNamespaceIfOpen()

            self.writer.openTestFixture(someClass)

            for someMethod in self.cppHeader.classes[someClass]['methods']['public']:
                if someMethod['name'] == 'setUp':
                    continue
                if someMethod['name'] == 'tearDown':
                    continue
                self.writer.writeTestRegistration(someClass, someMethod['name'])

            for someMethod in self.cppHeader.classes[someClass]['methods']['public']:
                if someMethod['name'] == 'setUp':
                    continue
                if someMethod['name'] == 'tearDown':
                    continue
                self.writer.writeTestDeclaration(someClass, someMethod['name'])

            for someMethod in self.cppHeader.classes[someClass]['methods']['public']:
                if someMethod['name'] == 'setUp':
                    self.writer.writeSetUp(someMethod['method_body'])
                if someMethod['name'] == 'tearDown':
                    self.writer.writeTearDown(someMethod['method_body'])

            self.writer.closeTestFixture(someClass)

            for someMethod in self.cppHeader.classes[someClass]['methods']['public']:
                if someMethod['name'] == 'setUp':
                    continue
                if someMethod['name'] == 'tearDown':
                    continue
                self.writer.writeTestCase(someClass, someMethod['name'], someMethod['method_body'])

        return True

    def _retrieveSourceLines(self, testFile):
        with open(testFile, 'r') as headerFile:
            self._sourceLines = []
            fileIterator = iter(headerFile)
            for line in fileIterator:
                self._sourceLines.append(line)

    def _retrieveMethodBodies(self):
        for someClass in self.cppHeader.classes:
            for someMethod in self.cppHeader.classes[someClass]['methods']['public']:
                bodyStartIter = iter(self._sourceLines)
                lineNumber = 1
                for line in bodyStartIter:
                    if lineNumber < someMethod['line_number']:
                        lineNumber = lineNumber + 1
                        continue
                    openIndex = line.find('{')
                    if openIndex != -1:
                        methodBody = self._retrieveBlock(line[openIndex + 1:], bodyStartIter, '{', '}')
                        someMethod['method_body'] = methodBody[:-1]
                        break

    def _writeIncludeOrStub(self,
                            someInclude,
                            writtenIncludes,
                            fileDirectory,
                            writeIncludeHeaders):
        if someInclude in writtenIncludes:
            return
        if someInclude in self.declaration_macros:
            headerGuardMacro = self._resolveHeaderGuards(someInclude,
                                                         fileDirectory)
            self.writer.writeMockInclude(headerGuardMacro,
                                         self.declaration_macros[someInclude])
            return
        if writeIncludeHeaders:
            cppHeader = self._resolveCppHeaderParser(someInclude,
                                                     fileDirectory)
            if cppHeader != None:
                for subHeader in cppHeader.includes:
                    self._writeIncludeOrStub(subHeader,
                                             writtenIncludes,
                                             fileDirectory,
                                             False)
            match = re.match('\s*["<](.*)[">]\s*', someInclude)
            if match == None:
                is_under_test = False
            else:
                fileName = match.group(1)
                dotIndex = fileName.find('.')
                if dotIndex != -1:
                    fileName = fileName[0:dotIndex]
                is_under_test = (fileName in self.classesUnderTest)
                relativeInclude = self._includeResolver.rewriteInclude(someInclude)
            self.writer.writeInclude(relativeInclude, is_under_test)
        else:
            self.writer.writeInclude(someInclude, False)
        writtenIncludes.add(someInclude)

    def _listAllClassesUnderTest(self):
        self.classesUnderTest = set()
        for someClass in self.cppHeader.classes:
            if not someClass.endswith('Test'):
                continue
            self.classesUnderTest.add(someClass[:-4])

    def traverseTestFile(self, testFileOrSource, fileDirectory = None):
        if fileDirectory == None:
            self._retrieveSourceLines(testFileOrSource)
            fileDirectory = os.path.dirname(testFileOrSource)
        else:
            self._sourceLines = testFileOrSource.split('\n')
        if fileDirectory == '':
            fileDirectory = '.'

        writtenIncludes = set()
        writtenIncludes.add('"TestFramework.h"')

        try:
            self.cppHeader = CppHeaderParser.CppHeader(''.join(self._sourceLines), 'string')
        except CppHeaderParser.CppParseError as e:
            print(e)

        self._retrieveMethodBodies()

        self._listAllClassesUnderTest()
        self.declaration_macros = {}

        self.writer.writeIncludeSection()

        sourceLinesIterator = iter(self._sourceLines)
        for line in sourceLinesIterator:
            if self._handleEntryPoint(line,
                                      sourceLinesIterator):
                continue
            if self._handleIncludeLine(line,
                                       sourceLinesIterator,
                                       writtenIncludes,
                                       fileDirectory):
                continue
            if self._handleClassStart(line,
                                      sourceLinesIterator,
                                      writtenIncludes,
                                      fileDirectory):
                continue
            if self._handleMockInclude(line,
                                       sourceLinesIterator):
                continue

            self.writer.passThroughLine(line)

