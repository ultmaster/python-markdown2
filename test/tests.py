import unittest
import sys
sys.path.append('..')
from markdown import convert

class MarkdownTest(unittest.TestCase):

    def test_markdown(self):
        import os
        dirname = os.path.dirname(__file__)
        for (path, dirs, files) in os.walk(dirname):
            for file in files:
                if file.endswith('.text'):
                    try:
                        s = open(os.path.join(path, file)).read()
                        out = convert(s).split('\n')
                        ans = open(os.path.join(path, file[:-5] + '.html')).readlines()
                        for i in range(len(out)):
                            if i < len(ans) and out[i].strip() != ans[i].strip():
                                print(file, file=sys.stderr)
                                print('out and ans diffs at line %d:' % i, file=sys.stderr)
                                print('out (len %d): %s' % (len(out[i]), out[i]), file=sys.stderr)
                                print('ans (len %d): %s' % (len(ans[i]), ans[i]), file=sys.stderr)
                                raise ValueError()
                    except ValueError:
                        pass
                    except Exception as e:
                        print(file, file=sys.stderr)


if __name__ == '__main__':
    unittest.main()
