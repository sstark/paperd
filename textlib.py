
from PIL import Image, ImageDraw, ImageFont
import textwrap

class WrappedText():
    
    def __init__(self, text, size, font, minfontsize=4, maxlines=False):
        """ Text should not contain newlines
        """
        self.text = text
        self.size = size
        self.font = font
        self.minfontsize = minfontsize
        self.maxlines = maxlines

    def charCountPerLine(self, fontsize=False):
        """ Find how many characters of the text would fit in the given box
        """
        if not fontsize:
            fontsize = self.font.size
        xs, ys = self.size
        for c in range(len(self.text), 0, -1):
            width, height = self.font.font_variant(size=fontsize).getsize(self.text[0:c])
            if width < xs:
                return c
        # if we could not find a good font size at least we should return a
        # valid count value
        return 1

    def wrapped(self, fontsize=False):
        """ Insert line breaks where needed
        """
        if not fontsize:
            fontsize = self.font.size
        wrap_at = self.charCountPerLine(fontsize)
        lines = textwrap.wrap(self.text, width=wrap_at)
        if self.maxlines:
            lines = lines[0:self.maxlines]
        return "\n".join(lines)

    def smartWrapped(self):
        """ Try shrinking font size down to half, then wrap

            Returns the original text, eventually wrapped,
            and the new suggested font size.
        """
        xs, ys = self.size
        minNewFontSize = max(self.font.size//2, self.minfontsize)
        for c in range(self.font.size, minNewFontSize, -1):
            width, height = self.font.font_variant(size=c).getsize(self.text)
            if width <= xs and height <= ys:
                # we found a font size that works without wrapping
                return (self.text, c)
        return (self.wrapped(fontsize=minNewFontSize), minNewFontSize)
