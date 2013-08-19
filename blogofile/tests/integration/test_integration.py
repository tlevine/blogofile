# -*- coding: utf-8 -*-
"""Integration tests for blogofile.
"""
import os
import shutil
from tempfile import mkdtemp
try:
    import unittest2 as unittest        # For Python 2.6
except ImportError:
    import unittest                     # flake8 ignore # NOQA
from ... import main


class TestBlogofileCommands(unittest.TestCase):
    """Intrgration tests for the blogofile commands.
    """
    def _call_entry_point(self, *args):
        main.main(*args)

    def test_blogofile_init_bare_site(self):
        """`blogofile init src` initializes bare site w/ _config.py file
        """
        src_dir = mkdtemp()
        self.addCleanup(shutil.rmtree, src_dir)
        os.rmdir(src_dir)
        self._call_entry_point(['blogofile', 'init', src_dir])
        self.assertEqual(os.listdir(src_dir), ['_config.py'])

    def test_blogofile_build_bare_site(self):
        """`blogofile build` on bare site creates _site directory
        """
        self.addCleanup(os.chdir, os.getcwd())
        src_dir = mkdtemp()
        self.addCleanup(shutil.rmtree, src_dir)
        os.rmdir(src_dir)
        self._call_entry_point(['blogofile', 'init', src_dir])
        self._call_entry_point(['blogofile', 'build', '-s', src_dir])
        self.assertIn('_site', os.listdir(src_dir))

    def testGitSubmodule(self):
        '''
        When the `_site` directory is a submodule (contains a `.git` file),
        the `.git` file remains after the rebuild.'''
        src_dir = mkdtemp()

        git_file = os.path.join(src_dir, '_site', '.git')
        submodule_dir = '../.git/modules/foo-site.git'
        open(git_file, 'w').write(submodule_dir)


        self._call_entry_point(['blogofile', 'init', src_dir])
        self._call_entry_point(['blogofile', 'build', '-s', src_dir])

        self.assertIn(submodule_dir, open(git_file).read())

