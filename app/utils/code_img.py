from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

def check_code(width=120, height=50, char_lengh=5, font_file=r"D:\Mycode\djangoProject\myprocess\app\Monaco.ttf", font_size=28):
    code = []
    img = Image.new(mode="RGB", size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def random_Char():
        """生成随机字母"""
        return str(random.randint(0, 9))
        # return chr(random.randint(65, 90))

    def random_Color():
        """生成随机颜色"""
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_lengh):
        char = random_Char()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_lengh, h], char, font=font, fill=random_Color())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=random_Color())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)

#
# if __name__ == '__main__':
#     img, code_str = check_code()
#     print(code_str)
