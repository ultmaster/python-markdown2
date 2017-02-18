import re
import subprocess


class KatexInterpreter:

    def __init__(self):
        pass

    def find_equations(self, string):
        """ Take in a string, and convert everything between $ ... $ into an inline
        equation and everything between $$ ... $$ into a centred equation. """

        doubledollar = re.compile(r"\$\$([^$]+)\$\$")
        singledollar = re.compile(r"(?<![\$])\$([^$]+)\$(?!\$)")

        inline_equations = re.findall(singledollar, string)
        centred_equations = re.findall(doubledollar, string)

        return inline_equations, centred_equations

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
print(k.eqn_to_html(''))
print(k.eqn_to_html("E=mc^2"))
print(k.eqn_to_html("c = \\pm\\sqrt{a^2 + b^2}"))