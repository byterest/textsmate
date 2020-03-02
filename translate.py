import copy,re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown

class WikiLinkRenderer(Renderer):
    def wiki_link(self, alt, link):
        return '<a href="%s" class="referlink">%s</a>' % (link, alt)
class WikiLinkInlineLexer(InlineLexer):
    def enable_wiki_link(self):
        self.rules.wiki_link = re.compile(
            r'\[\['                   
            r'([\s\S]+?\|[\s\S]+?)'   
            r'\]\](?!\])'           
        )
        self.default_rules.insert(3, 'wiki_link')
    def output_wiki_link(self, m):
        text = m.group(1)
        alt, link = text.split('|')
        return self.renderer.wiki_link(alt, link)
renderer = WikiLinkRenderer()
inline = WikiLinkInlineLexer(renderer)
inline.enable_wiki_link()
markdown = Markdown(renderer, inline=inline)
def trans(txt):
    return markdown(txt)
