import re
import subprocess


class KatexInterpreter:

    _katex_span_re = re.compile(r'''
        (?<!\\)
        (\$)
        (?!\$)
        (.+?)
        (?<!\\)
        (\$)
        (?!\$)
    ''', re.X | re.S)
    _katex_error_message = '<span class="katex">ERROR</span>'
    _katex_empty_message = '<span class="katex"></span>'


    def _katex_convert(self, text):
        return self._katex_span_re.sub(self._sub_katex, text)


    def _sub_katex(self, match):
        if match.group(2):
            return self._eqn_to_html(match.group(2))
        return self._katex_error_message


    def _eqn_to_html(self, eqn_string):
        """ Takes equation string, e.g. "E = mc^2", and outputs KaTeX HTML """

        command = ['node', './katex.port.js', eqn_string]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            process.wait(20)
            if process.returncode != 0:
                raise ReferenceError
            return process.stdout.read().decode()
        except ReferenceError:
            return self._katex_error_message


def katex_convert(text):
    return KatexInterpreter()._katex_convert(text)


def demo():
    print(katex_convert("$hello$"))
    print(katex_convert("$hello\$hfhfhf$"))
    print(katex_convert("fdsfkljf$$   jdkdkdkd $fjlkjdjfjfjf"))


if __name__ == '__main__':
    demo()
