from markdown2 import Markdown
import re


class AIPMarkdown(Markdown):

    def __init__(self):
        super().__init__(self, safe_mode=True, extras=['fenced-code-blocks'])

    def convert(self, text):
        """Convert the given text."""
        # Main function. The order in which other subs are called here is
        # essential. Link and image substitutions need to happen before
        # _EscapeSpecialChars(), so that any *'s or _'s in the <a>
        # and <img> tags get encoded.

        # Modified version:

        # Remove: utf-8 support
        # Remove: a lot of extras

        # Modify: safe mode automatically turned on
        # Modify: render h1 to title, h2 to heading, h3/h4/h5/h6 to heading-2

        # Add: Katex support

        # Clear the global hashes. If we don't clear these, you get conflicts
        # from other articles when generating a page which contains more than
        # one article (e.g. an index page that shows the N most recent
        # articles):
        self.reset()

        # Standardize line endings:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Make sure $text ends with a couple of newlines:
        text += "\n\n"

        # Convert all tabs to spaces.
        text = self._detab(text)

        # Strip any lines consisting only of spaces and tabs.
        # This makes subsequent regexen easier to write, because we can
        # match consecutive blank lines with /\n+/ instead of something
        # contorted like /[ \t]*\n+/ .
        text = self._ws_only_line_re.sub("", text)

        text = self.preprocess(text)

        # Used in safe mode
        text = self._hash_html_spans(text)

        # Turn block-level HTML blocks into hash entries
        text = self._hash_html_blocks(text, raw=True)

        # Used in safe mode and for code highlight
        text = self._do_fenced_code_blocks(text)

        # Strip link definitions, store in hashes.
        text = self._strip_link_definitions(text)

        text = self._run_block_gamut(text)

        text = self.postprocess(text)

        text = self._unescape_special_chars(text)

        # Used in safe mode
        text = self._unhash_html_spans(text)

        text += "\n"

        return text

    def _do_fenced_code_blocks(self, text):
        self._fenced_code_block_re = re.compile(r'''
            (?:\n+|\A\n?)
            ^(`+)([\w+-]+)[ \t]*\n      # opening fence, language mandatory
            (.*?)                       # code block content
            ^\1[ \t]*\n                # closing fence
            ''', re.M | re.X | re.S)
        return self._fenced_code_block_re.sub(self._fenced_code_block_sub, text)

    def _code_block_sub(self, match, is_fenced_code_block=False):
        if not is_fenced_code_block:
            return super()._code_block_sub(self, match)
        lexer_name = match.group(2)
        formatter_opts = self.extras['fenced-code-blocks'] or {}
        codeblock = match.group(3)
        codeblock = codeblock[:-1]  # drop one trailing newline

        def unhash_code(codeblock):
            for key, sanitized in list(self.html_spans.items()):
                codeblock = codeblock.replace(key, sanitized)
            replacements = [
                ("&amp;", "&"),
                ("&lt;", "<"),
                ("&gt;", ">")
            ]
            for old, new in replacements:
                codeblock = codeblock.replace(old, new)
            return codeblock
        lexer = self._get_pygments_lexer(lexer_name)
        if lexer:
            codeblock = unhash_code( codeblock )
            colored = self._color_with_pygments(codeblock, lexer,
                                                **formatter_opts)
            return "\n\n%s\n\n" % colored

        codeblock = self._encode_code(codeblock)
        pre_class_str = self._html_class_str_from_tag("pre")
        code_class_str = self._html_class_str_from_tag("code")
        return "\n\n<pre%s><code%s>%s\n</code></pre>\n\n" % (
            pre_class_str, code_class_str, codeblock)

    def _run_block_gamut(self, text):
        # These are all the transformations that form block-level
        # tags like paragraphs, headers, and list items.

        text = self._do_headers(text)

        # Do Horizontal Rules:
        # On the number of spaces in horizontal rules: The spec is fuzzy: "If
        # you wish, you may use spaces between the hyphens or asterisks."
        # Markdown.pl 1.0.1's hr regexes limit the number of spaces between the
        # hr chars to one or two. We'll reproduce that limit here.
        hr = "\n<hr"+self.empty_element_suffix+"\n"
        text = re.sub(self._hr_re, hr, text)

        text = self._do_lists(text)
        text = self._do_code_blocks(text)
        text = self._do_block_quotes(text)

        # We already ran _HashHTMLBlocks() before, in Markdown(), but that
        # was to escape raw HTML in the original Markdown source. This time,
        # we're escaping the markup we've just created, so that we don't wrap
        # <p> tags around block-level tags.
        text = self._hash_html_blocks(text)

        text = self._form_paragraphs(text)

        return text

    def _h_sub(self, match):
        if match.group(1) is not None:
            # Setext header
            n = {"=": 1, "-": 2}[match.group(3)[0]]
            header_group = match.group(2)
        else:
            # atx header
            n = len(match.group(5))
            header_group = match.group(6)

        html = self._run_span_gamut(header_group)
        if n == 1:
            tag = 'title'
        elif n == 2:
            tag = 'heading'
        else:
            tag = 'heading-2'
        return '<div class="%s">%s</div>\n\n' % (tag, html)

    def _form_paragraphs(self, text):
        text = text.strip('\n')

        # Wrap <p> tags.
        grafs = []
        for i, graf in enumerate(re.split(r"\n{1,}", text)):
            if graf in self.html_blocks:
                # Unhashify HTML blocks
                grafs.append(self.html_blocks[graf])
            else:
                # Wrap <p> tags.
                graf = self._run_span_gamut(graf)
                grafs.append("<p>" + graf.lstrip(" \t") + "</p>")

        return "\n\n".join(grafs)

    def _katex(self, text):
        """ katex format """
        text = self._hash_html_blocks(text)

        from katex.katex import katex_convert
        text = self._hash_html_blocks(text)
        text = katex_convert(text)

        return text
