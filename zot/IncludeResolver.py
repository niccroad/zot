import glob, os, re

class IncludeResolver(object):
    def __init__(self, fileDirectory, includeFolders, relativePath):
        self._fileDirectory = fileDirectory
        self._includeFolders = includeFolders
        self._systemFolders = []
        for path in os.getenv('INCLUDE', '').split(';'):
            self._systemFolders.append(path)

        self._relativePath = relativePath

    def resolveInclude(self, includeFile):
        match = re.match('\s*["<](.*)[">]\s*', includeFile)
        if match == None:
            return None
        files = glob.glob('%s/%s' % (self._fileDirectory, match.group(1)))
        if len(files) > 0:
            return files[0]
        for includePath in self._includeFolders:
            files = glob.glob('%s/%s' % (includePath, match.group(1)))
            if len(files) > 0:
                return files[0]
        for includePath in self._systemFolders:
            files = glob.glob('%s/%s' % (includePath, match.group(1)))
            if len(files) > 0:
                return files[0]

    def rewriteInclude(self, includeFile):
        match = re.match('\s*"(.*)"\s*', includeFile)
        if match == None:
            return includeFile
        files = glob.glob('%s/%s' % (self._fileDirectory, match.group(1)))
        if len(files) > 0:
            return '"' + self._joinHeaderPaths(self._relativePath, match.group(1)) + '"'
        return includeFile

    def relativePathFileName(self, filePath):
        if self._relativePath != None:
            return os.path.join(self._relativePath, filePath)
        else:
            return filePath

    def _joinHeaderPaths(self, firstPath, secondPath):
        if firstPath == '.':
            return secondPath
        elif firstPath.endswith('/'):
            return firstPath + secondPath
        else:
            return firstPath + '/' + secondPath