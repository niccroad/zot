import argparse, os

from IncludeResolver import IncludeResolver
from TestWriter import TestWriter
from TestReader import TestReader

# Zot stands for 'zero overhead tests'. This is a code generator converting
# test files (which look like regular cpp files) into cpp files containing
# include based mocking.
class ZotCodeGenerator(object):
    def generateTestCode(self, testFile, generatedFile = None, includePaths=[]):
        relativePath = os.path.relpath('.', os.path.dirname(generatedFile))
        resolver = IncludeResolver('.',
                                   includePaths,
                                   relativePath)
        writer = TestWriter()
        reader = TestReader(writer, resolver)
        reader.traverseTestFile(testFile)
        
        output = writer.getOutputLines()
        if (os.path.exists(generatedFile)):
            with open(generatedFile, 'r') as f:
                allLinesSame = True
                outputLines = writer.getOutputLines()
                i = 0
                for line in generatedFile:
                    if line != outputLines[i]:
                        allLinesSame = False
                        break
                    i = i + 1
                if allLinesSame:
                    return
                    
        generatedFolderPath = os.path.dirname(generatedFile)
        if len(generatedFolderPath) > 0:
            if not os.path.isdir(generatedFolderPath):
                os.makedirs(generatedFolderPath)
            
        with open(generatedFile, 'w') as f:
            for outputLine in writer.getOutputLines():
                f.write(outputLine)
                f.write('\n')
