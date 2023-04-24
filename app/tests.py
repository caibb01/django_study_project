# from PIL import Image,ImageDraw,ImageFont
#
#
# # 生成一个新的图片
# img = Image.new(mode="RGB", size=(1200, 800), color=(255, 255, 255))
#
#
# # 导入Draw进行画图操作
# ddraw = ImageDraw.Draw(img,mode="RGB")
#
#
# # 引入字体文件
# font = ImageFont.truetype("Monaco.ttf",28)
#
# # 2.填写文本，font使用字体文件
# ddraw.text([0,0],'python','red',font=font)
#
#
# # 3. 画点 第一个参数代表坐标，第二个代表颜色
# # ddraw.point([100,100],fill='red')
# # ddraw.point([111,100],fill='red')
#
# # 4.画线 第一个参数代表 起始坐标前两位和结束坐标后两位，第二个参数代表颜色
# # ddraw.line((1200,800,0,0),fill='red')
#
#
# # 5.画圆 第一个参数代表起始坐标和结束坐标，圆要画在其中间，第二个表示开始角度，第三个标是结束角度，第四个表示颜色
# # ddraw.arc((100,100,300,300),0,1370,fill='red')
#
# with open('code.png', 'wb') as f:
#     img.save(f, format='png')
#
#
# # ddraw.line()

import random
def random_Char():
    """生成随机字母"""
    return chr(random.randint(65, 90))   # 这里生成的数字后对应ASCII的A~Z
if __name__ == '__main__':
    a = random_Char()
    print(a,type(a))
