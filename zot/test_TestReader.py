import unittest

from TestReader import TestReader
from TestWriter import TestWriter

class test_TestWriter(unittest.TestCase):
    def writeIncludeSection(self):
    	self.assertTrue(self._writeIncludeSection > 0)
    	self._writeIncludeSection = self._writeIncludeSection - 1    	
    
    def writeInclude(self, includeDef, inNamespace):
        pass
    
    def closeNamespaceIfOpen(self):
        pass
    
    def openTestFixture(self, suiteName):
    	self.assertTrue(len(self._openTextFixtureNames) > 0)
    	self.assertEquals(suiteName, self._openTextFixtureNames.pop())

    def closeTestFixture(self, suiteName):
    	self.assertTrue(len(self._closeTextFixtureNames) > 0)
    	self.assertEquals(suiteName, self._closeTextFixtureNames.pop())
    
    def writeMain(self):
    	self.assertTrue(self._writeMainCalls > 0)
    	self._writeMainCalls = self._writeMainCalls - 1
    	
    def passThroughLine(self, line):
    	pass
    
    def resolveInclude(self, includeFile):
    	return None
    	
    def rewriteInclude(self, includeFile):
    	return includeFile
	
    def test_write_a_simple_test_case(self):
        writer = TestWriter()
        reader = TestReader(writer, self)
        
        reader.traverseTestFile("examples/Singleton/EmailerTest.cpp")
        
    def test_retrieve_a_block_of_a_macro(self):
        reader = TestReader(None, self)
        lines = []
        lines.append('A simple macro\n')
        lines.append(');')
        block = reader._retrieveBlock('An initial line\n', iter(lines))
        self.assertEqual('An initial line\nA simple macro\n', block)
        
    def test_retrieve_a_block_of_a_macro_ending_with_content_on_last_line(self):
        reader = TestReader(None, self)
        lines = []
        lines.append('A simple macro\n')
        lines.append('with content on the last line.);')
        block = reader._retrieveBlock('An initial line\n', iter(lines))
        self.assertEqual('An initial line\nA simple macro\nwith content on the last line.', block)
        
    def test_retrieve_a_block_of_a_macro_containing_nested_open_and_close(self):
        reader = TestReader(None, self)
        lines = []
        lines.append('A simple macro (written in english)\n')
        lines.append(');')
        block = reader._retrieveBlock('An initial line\n', iter(lines))
        self.assertEqual('An initial line\nA simple macro (written in english)\n', block)

    def test_retrieve_a_block_of_a_macro_containing_an_across_line_nested_open_and_close(self):
        reader = TestReader(None, self)
        lines = []
        lines.append('A simple macro (written \n')
        lines.append('in english));')
        block = reader._retrieveBlock('An initial line\n', iter(lines))
        self.assertEqual('An initial line\nA simple macro (written \nin english)', block)

    def test_traverseTestFile_on_a_simple_example(self):
    	self._writeIncludeSection = 1
    	self._openTextFixtureNames = ['SomeTest']
    	self._closeTextFixtureNames = ['SomeTest']
    	self._writeMainCalls = 1
        reader = TestReader(self, self)
        reader.traverseTestFile('class SomeTest { };\nTEST_ENTRY_POINT()', '.')
        
    def test_traverseTestFile_on_a_simple_example_with_no_entry_point(self):
    	self._writeIncludeSection = 1
    	self._openTextFixtureNames = ['SomeTest']
    	self._closeTextFixtureNames = ['SomeTest']
        reader = TestReader(self, self)
        reader.traverseTestFile('class SomeTest { };\n', '.')        