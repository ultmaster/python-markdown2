import re
import execjs


class KatexInterpreter:

    def __init__(self):
        self.source = open('./katex.js').read()
        print(self.source)
        self.katex = execjs.get('Node.js (V8)').eval(self.source)
        print(self.katex)

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

        try:
            return self.katex.call("katex.renderToString", "E = mc^2")
        except ReferenceError:
            print("Error rendering KaTeX HTML. Please ensure that you have")
            print("imported KaTeX into the Python namespace.")
            return False


    def replace_eqn(string):
        """ Takes a block of text, finds the equations and replaces the text with
        HTML code """

        pass


k = KatexInterpreter()
tt = execjs.compile('function abc(){return 3;}')
print(tt.call('abc'))
k.eqn_to_html('')