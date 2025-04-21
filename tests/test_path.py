import os
import tempfile
import unittest

from file_forward.path import insert_before_ext
from file_forward.path import rename_unique

class TestRenameUnique(unittest.TestCase):

    def test_insert_before_ext(self):
        self.assertEqual(insert_before_ext('file.txt', 1, '.'), 'file.1.txt')
        self.assertEqual(insert_before_ext('archive.tar.gz', 2, '_'), 'archive.tar_2.gz')
        self.assertEqual(insert_before_ext('/path/to/file', 99, '-'), '/path/to/file-99')

    def test_rename_unique(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'data.txt')

            # Create a file at the original path
            with open(path, 'w') as f:
                f.write('original')

            # Create a few numbered versions
            numbered = []
            for i in range(1, 4):
                candidate = insert_before_ext(path, i, '.')
                with open(candidate, 'w') as f:
                    f.write(f'conflict {i}')
                numbered.append(candidate)

            result = rename_unique(path)
            self.assertTrue(result.endswith('.4.txt'))
            # Should just return the path, not create it
            self.assertFalse(os.path.exists(result))

    def test_rename_unique_with_sep(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, 'logfile.log')
            with open(path, 'w'):
                pass
            with open(insert_before_ext(path, 1, '_'), 'w'):
                pass

            expected = insert_before_ext(path, 2, '_')
            self.assertEqual(rename_unique(path, sep='_'), expected)


if __name__ == '__main__':
    unittest.main()

