import random

from PIL import Image, ImageFont, ImageFilter, ImageDraw
from tornado import gen


class CodeGen(object):
    def __init__(self, text_str=None, size=None, background=None):
        self.text_str = text_str or '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.size = size or (150, 50)
        self.background = background or 'white'
        self.text_list = list(self.text_str)

    def create_pic(self):
        self.width, self.height = self.size
        self.img = Image.new('RGB', self.size, self.background)
        self.draw = ImageDraw.Draw(self.img)

    def create_point(self, num, color):
        for i in range(num):
            self.draw.point(
                (random.randint(0, self.width), random.randint(0, self.height)),
                fill=color,
            )

    def create_line(self, num, color):
        for i in range(num):
            self.draw.line(
                [
                    (random.randint(0, self.width), random.randint(0, self.height)),
                    (random.randint(0, self.width), random.randint(0, self.height)),
                ],
                fill=color,
            )

    def create_text(self, font_type, font_size, font_color, font_num, start_xy):
        font = ImageFont.truetype(font_type, font_size)
        check = random.sample(self.text_list, font_num)
        self.draw.text(start_xy, " ".join(check), fill=font_color, font=font)
        return check

    def transform(self):
        """将画出的线条，文字扭曲，缩放等"""
        params = [
            1 - float(random.randint(1, 2)) / 100,
            0,
            0,
            0,
            1 - float(random.randint(1, 10)) / 100,
            float(random.randint(1, 2)) / 500,
            0.001,
            float(random.randint(1, 2)) / 500
        ]
        self.img = self.img.transform(self.size, Image.PERSPECTIVE, params)
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)


@gen.coroutine
def get_pic_code():
    __cg = CodeGen()
    __cg.create_pic()
    __cg.create_point(500, (220, 220, 220))
    __cg.create_line(30, (220, 220, 220))
    __check = __cg.create_text('static/font/simsun.ttf', 24, (0, 0, 205), 4, (7, 7))
    __cg.transform()
    raise gen.Return((__cg.img, __check))
