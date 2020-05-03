# -*- coding:utf-8 -*-
# python3.6
# author: Hu Zhang
# email: dugujjiujian@gmail.com

import pygame, math
from pygame.locals import *
"""
点击图片换笔：
布置图片（载入图片，布置位置）
点击图片反应（改变画笔（载入brush图片,改变style），改变size（截取图片大小），改变颜色（改变每个像素点的颜色））
画brush（blit）
"""
class Brush():
    def __init__(self, screen):
        self.screen = screen
        self.color = (0, 0, 0)
        self.size = 1
        self.drawing = False
        self.last_pos = None
        self.backgroundcolor = (255, 255, 255)
        # True: png brush, False: pencil
        self.style = False
        self.brush_png = pygame.image.load("images/brush.png").convert_alpha()
        # set the current brush depends on size
        self.brush_png_now = self.brush_png.subsurface((0, 0), (self.size, self.size))

    def start_draw(self, pos):
        self.drawing = True
        self.last_pos = pos
    def end_draw(self):
        self.drawing = False

    def set_color(self, color):
        # set two pens' colors in the same time
        # pencil
        self.color = color
        # brush
        for i in range(self.brush_png.get_width()):
            for j in range(self.brush_png.get_height()):
                self.brush_png.set_at((i, j),
                                      color + (self.brush_png.get_at((i, j)).a,))# 这一句是两个元组的拼接,
                                                                                # .a后面必须加逗号，否则不会被认为是元组
                                                                                # .a指的是不透明度
                print(color)#(255, 0, 0)
                print(self.brush_png.get_at((i, j)))#(255, 0, 0, 17)

    def get_color(self):
        return self.color

    # def draw(self, pos):
    #     if self.drawing:
    #         pygame.draw.line(self.screen, self.color,
    #                          self.last_pos, pos, self.size * 2)
    #         self.last_pos = pos
    def draw(self, pos):
        if self.drawing:
            for p in self._get_points(pos):
                # draw eveypoint between them
                # pencil
                if self.style == False:
                    pygame.draw.circle(self.screen, self.color, p, int(self.size/2))
                # brush
                else:
                    self.screen.blit(self.brush_png_now, p)
            self.last_pos = pos

    def _get_points(self, pos):
        """ Get all points between last_point and now_point. """
        points = [ (self.last_pos[0], self.last_pos[1]) ]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        length = math.sqrt(len_x ** 2 + len_y ** 2)
        step_x = len_x / length
        step_y = len_y / length
        for i in range(int(length)):
            points.append(
                    (points[-1][0] + step_x, points[-1][1] + step_y))
        points = map(lambda x:(int(0.5+x[0]), int(0.5+x[1])), points)
        # return light-weight, uniq integer point list
        return list(set(points))


class Menu():
    def __init__(self, screen):
        self.screen = screen
        self.brush  = None
        self.rect_add = pygame.Rect(10, 140, 30, 30)
        self.rect_dec = pygame.Rect(44, 140, 30, 30)
        self.eraser = pygame.Rect(10, 100, 60, 30)
        self.rect_theX = pygame.Rect(10, 60, 30, 30)
        self.size_font = pygame.font.SysFont(None, 50)
        # OSError: unable to read font file 'D:\文件\Python\venv\lib\site-packages\pygame\freesansbold.ttf'
        # 路径有中文，读不了
        # self.size_font = pygame.font.Font(r"D:\PythonFont\freesansbold.ttf", 12)
        self.colors = [
                (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
                (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
                (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
                (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
                (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
                (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
                (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
                (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
            ]
        self.colors_rect = []
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            #if i=1: type(i)=int, i/2=0.5, type(i/2)=float
            self.colors_rect.append(rect)

        # load 2 pens' icons
        self.pens = [
            pygame.image.load("images/pen1.png").convert_alpha(),
            pygame.image.load("images/pen2.png").convert_alpha()
        ]
        # set 2 pens' icons position
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10 + i * 64, 540, 64, 64)
            self.pens_rect.append(rect)

    def draw(self):
        # draw current color
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        if self.brush.style == False:
            pygame.draw.line(self.screen,self.brush.get_color(), (15, 210), (68, 210), self.brush.size)
        else:
            self.screen.blit(self.brush.brush_png_now, (42 - self.brush.size / 2, 212 - self.brush.size / 2))
        # draw colors panel
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])

        # draw "+" "-"
        # "+"
        self.screen.fill((255, 255, 255), self.rect_add)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect_add, 1)
        pygame.draw.line(self.screen, (0, 0, 0), (12, 154), (37, 154), 3)
        pygame.draw.line(self.screen, (0, 0, 0), (24, 142), (24, 166), 3)
        # "-"
        self.screen.fill((255, 255, 255), self.rect_dec)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect_dec, 1)
        pygame.draw.line(self.screen, (0, 0, 0), (46, 154), (71, 154), 3)

        # draw the eraser
        pygame.draw.rect(self.screen, (0, 0, 0), self.eraser )

        # draw the "X"
        self.screen.fill((255, 255, 255), self.rect_theX)
        pygame.draw.rect(self.screen, (0, 0, 0), self.rect_theX, 1)
        pygame.draw.line(self.screen, (255, 0, 0), (12, 62), (36, 86), 5)
        pygame.draw.line(self.screen, (255, 0, 0), (12, 86), (36, 62), 5)

        # draw size font
        self.size_font_surface = self.size_font.render(str(self.brush.size), True, (0, 0, 0), (255, 255, 0))
        self.screen.blit(self.size_font_surface, (57, 225))

        # draw pens icons
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)

    def click_button(self, pos):
        # color buttons
        for (i, rect) in enumerate(self.colors_rect):
            if rect.collidepoint(pos):
                self.brush.set_color(self.colors[i])
        # click "+" "-"
        if self.rect_add.collidepoint(pos):
            if self.brush.size < 20:
                self.brush.size += 1
                self.brush.brush_png_now = self.brush.brush_png.subsurface((0, 0), (self.brush.size, self.brush.size))
        if self.rect_dec.collidepoint(pos):
            if self.brush.size > 1:
                self.brush.size -= 1
                self.brush.brush_png_now = self.brush.brush_png.subsurface((0, 0), (self.brush.size, self.brush.size))
        # click the eraser
        if self.eraser.collidepoint(pos):
            self.brush.set_color(self.brush.backgroundcolor)
        # click the "X"
        if self.rect_theX.collidepoint(pos):
            self.screen.fill(self.brush.backgroundcolor)
        # click pens' icons, change styles
        for (i, rect) in enumerate(self.pens_rect):
            if rect.collidepoint(pos):
                self.brush.style = bool(i)
        # if self.pens_rect[0].collidepoint(pos):
        #     self.brush.set_style(False)
        # if self.pens_rect[1].collidepoint(pos):
        #     self.brush.set_style(True)


class Painter():
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Painter")
        self.brush = Brush(self.screen)
        ###
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.menu.brush = self.brush

    def run(self):
        self.screen.fill(self.brush.backgroundcolor)
        while 1:
            ###
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                ###
                elif event.type == pygame.KEYDOWN:
                    # press esc to clear screen
                    if event.key == pygame.K_ESCAPE:
                        self.screen.fill(self.brush.backgroundcolor)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # <= 74, coarse judge here can save much time
                    if ((event.pos)[0] <= 150 and
                            self.menu.click_button(event.pos)):
                        # if not click on a functional button, do drawing
                        pass
                    else:
                        self.brush.start_draw(event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    self.brush.draw(event.pos)
                ###
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()

            self.menu.draw()
            pygame.display.update()

if __name__ == '__main__':
    pygame.init()
    app = Painter()
    app.run()
    pygame.quit()