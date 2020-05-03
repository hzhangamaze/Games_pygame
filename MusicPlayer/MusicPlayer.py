# -*- coding:utf-8 -*-
# python3.6
# author: Hu Zhang
# email: dugujjiujian@gmail.com

# 用一个按键控制暂停和继续（标志位判断）
# 界面
# 全局变量
# 歌单(文件)
# 显示歌曲列表（部分+全部）
# 歌曲列表中选中播放
import pygame, os, math, random
from time import sleep

def myPauseAndUnpause():    # 括号里加不加Music都可以
    global myPaused
    if not myPaused:
        Music.pause()
        myPaused = True
    else:
        Music.unpause()
        myPaused = False

def get_musics(musicpath):
    filenames = os.listdir(musicpath)
    MusicNames, Musics, MusicsRect, myMusicsListSelected = [], [], [], []
    for i in range(len(filenames)):
        if filenames[i].lower().endswith(".mp3"):
            newfilename = filenames[i].split(".")[0]
            MusicNames.append(newfilename)
            Musics.append(os.path.join(myMusicPath, filenames[i]))
            MusicsRect.append(pygame.Rect(600, i * 20, LENGTH - 600, 20))
            myMusicsListSelected.append(False)
    MusicAmounts = len(Musics)
    return MusicNames, Musics, MusicsRect,myMusicsListSelected, MusicAmounts

def change_music():
    global myFontSurface
    Music.load(myMusics[i])
    myFontSurface = myFont1.render(myMusicNames[i], True, myColors["black"], myColors["yellow"])
    Music.play()


def musics_font(MusicNames):
    j = 0
    myMusicNameSurfaces1, myMusicNameSurfaces2 = [], []
    myFont2 = pygame.font.SysFont(name="华文宋体", size=15)
    myFont3 = pygame.font.SysFont(name="华文宋体", size=15, bold=True, italic=False)
    for musicname in MusicNames:
        namesurface1 = myFont2.render(musicname, True, myColors["black"], myColors["white"])
        myMusicNameSurfaces1.append(namesurface1)
        namesurface2 = myFont3.render(musicname, True, myColors["black"], myColors["yellow"])
        myMusicNameSurfaces2.append(namesurface2)
    return myMusicNameSurfaces1, myMusicNameSurfaces2

def musics_font_display(myMusicNameSurfaces1, myMusicNameSurfaces2, i):
    for j in range(-2, 3):
        m = i
        k = m + j
        if k < 0:
            m = len(myMusicNameSurfaces1) + i
            k = m + j
        elif k >= len(myMusicNameSurfaces1):
            m = -1
            k = m + j
        myScreen.blit(myMusicNameSurfaces1[k], (600, 400 + j * myRawGap))
    myScreen.blit(myMusicNameSurfaces2[i], (600, 400))

def all_musics_font_display(myMusicNameSurfaces1, myMusicNameSurfaces2, pagenumber):
    # 如果函数内某一参数的名字与主程序内的变量相同，则可直接使用，不用传参
    startnumber = int((HEIGHT-60)/myRawGap) * pagenumber
    endnumber = int((HEIGHT-60)/myRawGap) * (pagenumber + 1)
    if endnumber >= len(myMusicNameSurfaces1):
        endnumber = len(myMusicNameSurfaces1)
    for j in range(startnumber, endnumber):
        myScreen.blit(myMusicNameSurfaces1[j], (600, (j - startnumber) * myRawGap))
        if myMusicsListSelected[j-startnumber]:
            myScreen.blit(myMusicNameSurfaces2[j], (600, (j - startnumber) * myRawGap))
    myFont4 = pygame.font.SysFont(name="华文宋体", size=15, bold=True, italic=False)
    myPageNumberFontSurface = myFont4.render("第" + str(pagenumber + 1) + "/" + str(myPageAmounts) + "页", True, myColors["black"], myColors["white"])
    myScreen.blit(myPageNumberFontSurface, (770, HEIGHT - 20))
    myScreen.fill(color=myColors["white"], rect=myButtonLastPageRect)
    myScreen.fill(color=myColors["white"], rect=myButtonNextPageRect)
    pygame.draw.line(myScreen, myColors["greyblack"], (750, HEIGHT - 15 + 5), (750 + 10, HEIGHT - 15), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (750, HEIGHT - 15 + 5), (750 + 10, HEIGHT - 15 + 10), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (750 + 10, HEIGHT - 15), (750 + 10, HEIGHT - 15 + 10), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (835, HEIGHT - 15), (835 + 10, HEIGHT - 15 + 5), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (835, HEIGHT - 15 + 10), (835 + 10, HEIGHT - 15 + 5), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (835, HEIGHT - 15), (835, HEIGHT - 15 + 10), 1)




myMusicPath = "D:\文件\音乐\歌曲"
LENGTH, HEIGHT = 1000, 600
myRawGap = 20
myPageNumber = 0
myPaused, myMusicsListDisplayed = False, False
myColors = {"black": (0, 0, 0),
            "white": (255, 255, 255),
            "greyblack": (100, 100, 100),
            "greywhite": (220, 220, 220),
            "red": (255, 0, 0),
            "green": (0, 255, 0),
            "blue": (0, 0, 255),
            "yellow": (255, 255, 0)
            }
myMusicsListRectColor = myColors["white"]
pygame.init()
myScreen = pygame.display.set_mode((LENGTH, HEIGHT))
myCaption = pygame.display.set_caption("Music Player")
myFont1 = pygame.font.SysFont("华文新魏", 30)
myMusicNames, myMusics, myMusicsRect, myMusicsListSelected, myMusicAmounts = get_musics(myMusicPath)
i = random.randint(0, myMusicAmounts)
myPageAmounts = math.ceil(myMusicAmounts / int((HEIGHT-60) / myRawGap))
myPicturePause = pygame.image.load("images/pause.png")
myPictureUnpause = pygame.image.load("images/unpause.png")
myPictureStop = pygame.image.load("images/stop.png")
myPictureLast = pygame.image.load("images/last.png")
myPictureNext = pygame.image.load("images/next.png")
myPictureRectPause = pygame.Rect(150, 125, 50, 50)
myPictureRectStop = pygame.Rect(210, 125, 50, 50)
myPictureRectLast = pygame.Rect(90, 125, 50, 50)
myPictureRectNext = pygame.Rect(270, 125, 50, 50)
myMusicsListRect = pygame.Rect(LENGTH - 20, HEIGHT - 20, 20, 20)
myButtonLastPageRect = pygame.Rect(750, HEIGHT - 15, 10, 10)
myButtonNextPageRect = pygame.Rect(835, HEIGHT - 15, 10, 10)
myEveryMusicRect = []
Music = pygame.mixer.music
Music.set_volume(10)
Music.load(myMusics[i])
myFontSurface = myFont1.render(myMusicNames[i],
                               True, myColors["black"], myColors["yellow"])
myMusicNameSurfaces1, myMusicNameSurfaces2 = musics_font(myMusicNames)
Music.play()

while 1:
    if not Music.get_busy():
        i += 1
        change_music()
    myScreen.fill(color=myColors["white"])
    myScreen.blit(myFontSurface, (140, 50))
    if not myPaused:
        myScreen.blit(myPicturePause, (150, 125))
    else:
        myScreen.blit(myPictureUnpause, (150, 125))
    myScreen.blit(myPictureStop, (210, 125))
    myScreen.blit(myPictureLast, (90, 125))
    myScreen.blit(myPictureNext, (270, 125))
    musics_font_display(myMusicNameSurfaces1, myMusicNameSurfaces2, i)
    if myMusicsListDisplayed:
        myScreen.fill(color=myColors["white"], rect=(600, 0, 400, 600))
        all_musics_font_display(myMusicNameSurfaces1, myMusicNameSurfaces2, pagenumber=myPageNumber)
    myScreen.fill(color=myMusicsListRectColor, rect=myMusicsListRect)
    pygame.draw.rect(myScreen, myColors["greyblack"], myMusicsListRect, 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (LENGTH - 20, HEIGHT - 15), (LENGTH, HEIGHT - 15), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (LENGTH - 20, HEIGHT - 10), (LENGTH, HEIGHT - 10), 1)
    pygame.draw.line(myScreen, myColors["greyblack"], (LENGTH - 20, HEIGHT - 5), (LENGTH, HEIGHT - 5), 1)
    pygame.display.update()
    for event in pygame.event.get():
        # 所有的事件都会被记录下来按顺序等待判断
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                myPauseAndUnpause()
            elif event.key == pygame.K_ESCAPE:
                Music.stop()
            elif event.key == pygame.K_LEFT:
                if i <= 0:
                    i = myMusicAmounts - 1
                else:
                    i -= 1
                change_music()
            elif event.key == pygame.K_RIGHT:
                if i >= myMusicAmounts - 1:
                    i = 0
                else:
                    i += 1
                change_music()
            elif event.key == pygame.K_TAB:
                if not myMusicsListDisplayed:
                    myMusicsListDisplayed = True
                else:
                    myMusicsListDisplayed = False
            elif event.key == pygame.K_UP and myMusicsListDisplayed:
                myPageNumber -= 1
                if myPageNumber < 0:
                    myPageNumber = myPageAmounts - 1
            elif event.key == pygame.K_DOWN and myMusicsListDisplayed:
                myPageNumber += 1
                if myPageNumber >= myPageAmounts:
                    myPageNumber = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if myPictureRectPause.collidepoint(event.pos):
                myPauseAndUnpause()
            elif myPictureRectStop.collidepoint(event.pos):
                Music.stop()
            elif myPictureRectLast.collidepoint(event.pos):
                if i <= 0:
                    i = myMusicAmounts - 1
                else:
                    i -= 1
                change_music()
            elif myPictureRectNext.collidepoint(event.pos):
                if i >= myMusicAmounts - 1:
                    i = 0
                else:
                    i += 1
                change_music()
            elif myMusicsListRect.collidepoint(event.pos):
                if not myMusicsListDisplayed:
                    myMusicsListDisplayed = True
                else:
                    myMusicsListDisplayed = False
            elif myButtonLastPageRect.collidepoint(event.pos) and myMusicsListDisplayed:
                myPageNumber -= 1
                if myPageNumber < 0:
                    myPageNumber = myPageAmounts - 1
            elif myButtonNextPageRect.collidepoint(event.pos) and myMusicsListDisplayed:
                myPageNumber += 1
                if myPageNumber >= myPageAmounts:
                    myPageNumber = 0
            if myMusicsListDisplayed:
                for j1 in range(int((HEIGHT - 60) / myRawGap)):
                    if myMusicsRect[j1].collidepoint(event.pos):
                        i = j1 + int((HEIGHT - 60) / myRawGap) * myPageNumber
                        change_music()
        elif event.type == pygame.MOUSEMOTION:
            if myMusicsListRect.collidepoint(event.pos) and myMusicsListDisplayed == False:
                    myMusicsListRectColor = myColors["greywhite"]
            else:
                myMusicsListRectColor = myColors["white"]
            if myMusicsListDisplayed:
                for i in range(int((HEIGHT - 60) / myRawGap)):
                    if myMusicsRect[i].collidepoint(event.pos):
                        myMusicsListSelected[i] = True
                    else:
                        myMusicsListSelected[i] = False


