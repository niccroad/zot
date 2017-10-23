import unittest

from IncludeResolver import IncludeResolver

class test_IncludeResolver(unittest.TestCase):
    def test_rewriteInclude_on_a_local_include(self):
        resolver = IncludeResolver('.', [], '.')
        self.assertEquals('"../include/TestFramework.h"',
                          resolver.rewriteInclude('"../include/TestFramework.h"'))

    def test_rewriteInclude_on_a_local_include_generated_to_another_folder(self):
        resolver = IncludeResolver('.', [], '../..')
        self.assertEquals('"../../include/TestFramework.h"',
                          resolver.rewriteInclude('"include/TestFramework.h"'))

    def test_rewriteInclude_on_a_system_include(self):
        resolver = IncludeResolver('.', [], '../..')
        self.assertEquals('<include/TestFramework.h>',
                          resolver.rewriteInclude('<include/TestFramework.h>'))