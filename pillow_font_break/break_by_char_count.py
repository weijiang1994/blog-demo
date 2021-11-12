"""
# coding:utf-8
@Time    : 2021/11/12
@Author  : jiangwei
@File    : break_by_char_count.py
@Desc    : break_by_char_count
@email   : qq804022023@gmail.com
@Software: PyCharm
"""

from PIL import Image, ImageFont, ImageDraw

texts = ['燕子去了，有再来的时候；杨柳枯了，有再青的时候；桃花谢了，有再开的时候。但是，聪明的，你告诉我，我们的日子为什么一去不复返呢？——是有人偷了他们罢：那是谁？又藏在何处呢？是他们自己逃走了罢：现在又到了哪里呢？',
         '我不知道他们给了我多少日子；但我的手确乎是渐渐空虚了。在默默里算着，八千多日子已经从我手中溜去；像针尖上一滴水滴在大海里，我的日子滴在时间的流里，没有声音，也没有影子。我不禁头涔涔而泪潸潸了。']

picture = 'congcong.png'
font_size = 24
font_file = 'simhei.ttf'
position = [34, 106]


def add_text():
    with Image.open(picture) as im:
        if im.mode.upper() == 'RGBA':
            layer = Image.new(
                'RGBA', im.size, color=(255, 255, 255, 255)
            )
            im = Image.alpha_composite(layer, im)
        draw = ImageDraw.Draw(im)

        font = ImageFont.truetype(font_file, font_size)
        for text in texts:
            index = 0
            while index < len(text):
                draw.text(tuple(position), text[index:index+21], font=font, fill='black')
                index += 21
                position[1] += 30
            position[1] += 20
        im.show()
        im.save('break_by_char_count.png', format='PNG')


add_text()
