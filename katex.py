import re
import subprocess


class KatexInterpreter:

    _katex_span_re = re.compile(r'''
        (?<!\\)
        \$
        (?!\$)
        (.+?)
        (?<![\\\$])
        \$
        (?!\$)
    ''', re.X | re.S)

    def find_equations(self, string):
        """ Take in a string, and convert everything between $ ... $ into an equation. """

        equations = self._katex_span_re.findall(string)
        return equations

    def remove_dollars(self, string):
        """ Takes equation delimited by dollars as input, and removes the dollar
        signs at the beginning and end. """

        return re.sub(r"[\$]", "", string)


    def eqn_to_html(self, eqn_string):
        """ Takes equation string, e.g. "E = mc^2", and outputs KaTeX HTML """

        command = ['node', './katex/katex.port.js', eqn_string]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            process.wait(20)
            if process.returncode != 0:
                raise ReferenceError
            return process.stdout.read().decode()
        except ReferenceError:
            print("Error rendering KaTeX HTML. Please ensure that you have")
            print("imported KaTeX into the Python namespace.")
            return ''


    def replace_eqn(string):
        """ Takes a block of text, finds the equations and replaces the text with
        HTML code """

        pass


k = KatexInterpreter()
print(k.find_equations("$hello$"))