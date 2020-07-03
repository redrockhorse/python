# 调用sys模块，负责程序与python解释器的交互，提供了一系列的函数和变量，用于操控python的运行时环境
import sys
# 调用pygame库
import pygame
# 调用pygame中的所有常量，便于使用（主要是懒）
from pygame.locals import *

white = 255, 255, 255
bule = 0, 0, 255
# 初始化pygame
pygame.init()
# 获取对显示系统的访问，并创建一个窗口，分别率位（600x500）screen:屏幕
screen = pygame.display.set_mode((900, 600))
#screen = screen.convert_alpha()
screen.set_alpha(0)
screen.fill((255,255,255))
# 创建字体对象，用于绘制文本(None,60)：none为默认字体，60是字体大小
myfont = pygame.font.Font(None, 60)
# 第一个参数是文本内容，第二个为抗锯齿字体，第三位颜色
# textImage = myfont.render("Hello PyGame_PieGame",True,white)
# 等待退出（任意键退出）
tick = pygame.time.Clock()


def drawCircle(screen, color, position, radius, width):
    pygame.draw.circle(screen, color, position, radius, width)


# alpa = 255
# color = 255, 0, 0
position = 300, 250
radius = 40
width = 10
#surface = pygame.Surface((900, 600))

#surface.convert_alpha()
#surface.fill((255, 255, 255, 255))

surface2 = screen.convert_alpha()
surface2.fill((255,255,255,0))#alpha=0,全透明
#pygame.draw.rect(surface2, (69, 137, 148, 100), pygame.Rect(14, 2, 660, 129))
#screen.blit(surface2,(0,0))
transparency = 255
while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    # screen.fill([0, 0, 0, 0])  # 清屏
    # 绘制一个圆

    # screen.blit(textImage,(100,100))#进行绘制
    # pygame.draw.circle(screen, color, position, radius, width)

    if radius < 200:
        # drawCircle(screen, color, position, radius, width)
        radius = radius + 5
        # drawCircle(surface, (255, 0, 0, 100), position, radius, width)
        if transparency > 10:
            transparency = transparency - 10
        else:
            transparency = 0
    else:
        radius = 40
        transparency = 255
        # drawCircle(surface, (255, 0, 0, 100), position, radius, width)
    drawCircle(surface2, (255, 0, 0,transparency), position, radius, width)
    #pygame.draw.circle(screen, (255, 0, 0, 100), position, radius, width)
    print(radius)

    screen.blit(surface2, (0, 0))
    pygame.display.update()
    screen.fill((255, 255, 255))
    surface2.fill((255, 255, 255, 0))
    # 刷新显示
    tick.tick(4)
# pygame.display.flip()
