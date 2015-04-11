# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import truncatewords, striptags
from django.utils.safestring import mark_safe
import mistune
import re
import copy


register = template.Library()


class MyRenderer(mistune.Renderer):
    def vimeo_link(self, vimeo_id, width, height):
        embed = '''
        <iframe src="//player.vimeo.com/video/{vimeo_id}?title=0&amp;byline=0&amp;portrait=0"
            width="{width}" height="{height}" frameborder="0"
            webkitallowfullscreen mozallowfullscreen allowfullscreen>
        </iframe>'''.format(vimeo_id=vimeo_id, width=width, height=height)
        return embed

    def youtube_link(self, youtube_id, width, height):
        embed = '''
        <iframe width="{width}" height="{height}"
            src="//www.youtube.com/embed/{youtube_id}?rel=0&amp;showinfo=0"
            frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen>
        </iframe>
        '''.format(youtube_id=youtube_id, width=width, height=height)
        return embed

    def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        if src.startswith('javascript:'):
            src = ''
        text = mistune.escape(text, quote=True)
        if title:
            title = mistune.escape(title, quote=True)
            html = '<img class="img-responsive" src="%s" alt="%s" title="%s"' % (src, text, title)
        else:
            html = '<img class="img-responsive" src="%s" alt="%s"' % (src, text)
        if self.options.get('use_xhtml'):
            return '%s />' % html
        return '%s>' % html

class MyInlineGrammar(mistune.InlineGrammar):
    # regex for embeded Vimeo videos
    # ![:vimeo 600x400](13697303)
    vimeo_link = re.compile(
        r'!\['                              # ![
        r':vimeo'                           # :vimeo
        r'([\s\S]*?)'                       # widthxheight
        r'\]'                               # ]
        r'\(([\s\S]+?)\)'                   # (vimeo_id)
    )

    # regex for embedding youtube videos
    # ![:youtube 600x400](G-M7ECt3-zY)
    youtube_link = re.compile(
        r'!\['                              # ![
        r':youtube'                           # :youtube
        r'([\s\S]*?)'                       # widthxheight
        r'\]'                               # ]
        r'\(([\s\S]+?)\)'                   # (youtube_id)
    )

class MyInlineLexer(mistune.InlineLexer):
    default_features = copy.copy(mistune.InlineLexer.default_features)

    # Add youtube_link and vimeo_link parser to default features
    # you can insert it any place you like
    default_features.insert(1, 'vimeo_link')
    default_features.insert(1, 'youtube_link')

    def __init__(self, renderer, rules=None, **kwargs):
        if rules is None:
            # use the inline grammar
            rules = MyInlineGrammar()

        super(MyInlineLexer, self).__init__(renderer, rules, **kwargs)

    def create_embedded_video(self, m, render_func):
        # get the user specified size for the embedded video
        size = m.group(1)
        if len(size) > 0 and 'x' in size:
            width, height = size.split('x')
        else:
            # default values
            width = '100%'
            height = 420

        # which video to play?
        video_id = m.group(2)

        # call the supplied render_func to make the HTML
        return render_func(video_id, width, height)

    def output_vimeo_link(self, m):
        return self.create_embedded_video(m, self.renderer.vimeo_link)

    def output_youtube_link(self, m):
        return self.create_embedded_video(m, self.renderer.youtube_link)

renderer = MyRenderer()
inline=MyInlineLexer(renderer)
markdown_render = mistune.Markdown(renderer, inline=inline)

@register.filter(name='markdown', is_safe=True)
def markdown(value):
    return mark_safe(markdown_render(value))

@register.filter(name='markdownexcerpt', is_safe=True)
def markdown_excerpt(value):
    text = striptags(markdown_render(value))
    return mark_safe(truncatewords(text, 20))
