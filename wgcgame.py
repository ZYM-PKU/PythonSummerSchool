import sys
import math
import pgzrun
import random

#全局设置
WIDTH = 1280
HEIGHT = 720
BOTTOM=710

#地图地面
bottoms=[]
#升降平台
platforms=[]
#背景
backs=[]
#存档点
saves=[]
#按钮
buttons=[]
#树木
trees=[]

#尖刺
spines=[]



#人物
player=Actor('player_right')

RESET_POS=(0,BOTTOM)#设置重生点

music_played=False#保证死亡音乐只播放一次
test_mode=False#开发者模式（无敌）

def reset(): 
    global music_played,BOTTOM


    #初始化地面
    bottoms.clear()
    bottom=Actor('bottom')
    bottom.bottomleft=(0,750)
    bottoms.append(bottom)
    BOTTOM=750-bottom.height
    
    #初始化平台
    platforms.clear()
    platform=Actor('platform')
    platform.bottomright=(680,500)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    
    platform=Actor('platform')
    platform.bottomright=(550,300)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    
    platform=Actor('platform')
    platform.bottomright=(350,300)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    
    platform=Actor('platform')
    platform.bottomright=(150,300)
    platform.name='platform1'
    platform.animate_acted=False
    platforms.append(platform)
    
    platform=Actor('platform')
    platform.bottomright=(150,300)
    platform.name='platform2'
    platform.animate_acted=False
    platforms.append(platform)
    
    bottom=Actor('vertical')
    bottom.bottomright=(765,610)
    bottoms.append(bottom)
    
    bottom=Actor('vertical')
    bottom.bottomright=(830,350)
    bottoms.append(bottom)
    
    bottom=Actor('vertical2')
    bottom.bottomright=(800,450)
    bottoms.append(bottom)
    
    
    bottom=Actor('vertical2')
    bottom.bottomright=(830,190)
    bottoms.append(bottom)
    for i in range(4):
        bottom=Actor('platform')
        bottom.bottomright=(345+i*100,135)
        bottoms.append(bottom)
    for i in range(4):
        bottom=Actor('platform')
        bottom.bottomright=(820+i*100,135)
        bottoms.append(bottom)
    bottom=Actor('platform')
    bottom.bottomright=(1300,335)
    bottoms.append(bottom)
    
    bottom=Actor('platform')
    bottom.bottomright=(1200,335)
    bottoms.append(bottom)

    #初始化存档点
    saves.clear()
    save=Actor('saved')
    save.bottomleft=(0,BOTTOM)
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(640,449)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(800,90)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,BOTTOM)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='end'
    saves.append(save)
    

    
    

    #初始化尖刺
    spines.clear()
    
    
    #陷阱刺
    
    spine=Actor('spine_up')
    spine.bottomleft=(250,610)
    spine.points=[]
    spine.name="trap1"
    spine.animate_acted=False
    spines.append(spine)
    
    
    spine=Actor('spine_up')
    spine.bottomleft=(100,640)
    spine.points=[]
    spine.name="trap2"
    spine.animate_acted=False
    spines.append(spine)
    
    spine=Actor('spine_up')
    spine.bottomleft=(550,610)
    spine.points=[]
    spine.name="trap3"
    spine.animate_acted=False
    spines.append(spine)
    
    spine=Actor('spine_light')
    spine.pos=(170,250)
    spine.points=[]
    spine.name="spine_light"
    spine.name="trap4"
    spine.animate_acted=False
    spines.append(spine)
    
    spine=Actor('final')
    spine.bottomleft=(1580,250)
    spine.points=[]
    spine.name="trap5"
    spine.animate_acted=False
    spines.append(spine)
    
    spine=Actor('spine_right')
    spine.bottomleft=(750,610)
    spine.points=[]
    spine.name="trap6"
    spine.animate_acted=False
    spines.append(spine)
    
    spine=Actor('spine_up')
    spine.bottomleft=(1100,610)
    spine.points=[]
    spine.name="trap7"
    spine.animate_acted=False
    spines.append(spine)
    edge_sample()


    #初始化玩家
    player.image='player_right'
    player.bottomleft=RESET_POS
    #速度
    player.vx=0
    player.vy=0
    player.staticvx=0#惯性横向速度
    player.ay=2#垂直加速度
    #跳跃
    player.jumptime=0#连续跳跃次数
    player.onbottom=True#是否在地上
    #死亡
    player.death=False
    music_played=False
    animate_acted=False
    music.stop()



def edge_sample():
    '''边缘采样函数，用于勾勒尖刺边缘以进行碰撞检测'''
    level=4#采样等级，数值越小越容易发生碰撞，游戏难度越高
    for spine in spines:
        if spine.image=='spine_up':
            x,y=spine.bottomleft
            x+=level
            for i in range(100):
                x+=(spine.width-level*2)/200
                y-=(spine.height-level)/100
                spine.points.append((x,y))
            for i in range(100):
                x+=(spine.width-level*2)/200
                y+=(spine.height-level)/100
                spine.points.append((x,y))
        elif spine.image=='spine_down':
            x,y=spine.topleft
            x+=level
            for i in range(100):
                x+=(spine.width-level*2)/200
                y+=(spine.height-level)/100
                spine.points.append((x,y))
            for i in range(100):
                x+=(spine.width-level*2)/200
                y-=(spine.height-level)/100
                spine.points.append((x,y))
        elif spine.image in ('spine_left','spine_left_long') :
            x,y=spine.topright
            y+=level
            for i in range(100):
                x-=(spine.width-level)/100
                y+=(spine.height-level*2)/200
                spine.points.append((x,y))
            for i in range(100):
                x+=(spine.width-level)/100
                y+=(spine.height-level*2)/200
                spine.points.append((x,y))
        elif spine.image =='spine_right' :
            x,y=spine.topleft
            y+=level
            for i in range(100):
                x+=(spine.width-level)/100
                y+=(spine.height-level*2)/200
                spine.points.append((x,y))
            for i in range(100):
                x-=(spine.width-level)/100
                y+=(spine.height-level*2)/200
                spine.points.append((x,y))



    

def draw():
    screen.clear()
    screen.blit('cover1',(0,0))
    for back in backs:back.draw()
    for tree in trees:tree.draw()
    for spine in spines:spine.draw()
    for platform in platforms:platform.draw()
    for bottom in bottoms:bottom.draw()
    for save in saves:save.draw()
    for button in buttons:button.draw()
    
    player.draw()
    if player.death:
        screen.draw.text("           GAME OVER\n------------------------------------\nPRESS 'R' TO CONTINUE",(250, 250), shadow=(2,2), scolor="#202020",fontsize=100)
    

def update():
    global music_played
    #运动模块
    player.vy+=player.ay
    player.vx=player.staticvx

    if not player.death:
        #物体边界检测
        for bottom in bottoms:
            if bottom.top<=player.bottom+player.vy<=bottom.bottom and player.left<bottom.right and player.right>bottom.left :
                player.vy=0
                player.bottom=bottom.top
                player.onbottom=True
            if bottom.top<=player.top+player.vy<=bottom.bottom and player.left<bottom.right and player.right>bottom.left :
                player.vy=0
                player.top=bottom.bottom
            if bottom.left<=player.left+player.vx<=bottom.right and player.bottom>bottom.top and player.top<bottom.bottom :
                player.vx=0
                player.left=bottom.right
            if bottom.left<=player.right+player.vx<=bottom.right and player.bottom>bottom.top and player.top<bottom.bottom :
                player.vx=0
                player.right=bottom.left
        for platform in platforms:
            if platform.top<=player.bottom+player.vy<=platform.bottom and player.left<platform.right and player.right>platform.left :
                player.vy=0
                player.bottom=platform.top
                player.onbottom=True
            if platform.top<=player.top+player.vy<=platform.bottom and player.left<platform.right and player.right>platform.left :
                if not test_mode:player.death=True
                else:
                    player.vy=0
                    player.bottom=platform.top
                    player.onbottom=True
            if platform.left<=player.left+player.vx<=platform.right and player.bottom>platform.top+5 and player.top<platform.bottom :#+5偏移量为了防止平台升起时造成瞬时高度差给判断带来影响
                player.vx=0
                player.left=platform.right
            if platform.left<=player.right+player.vx<=platform.right and player.bottom>platform.top+5 and player.top<platform.bottom :
                player.vx=0
                player.right=platform.left

        #全局边界检测
        if player.left+player.vx<0:
            player.left=0
            player.vx=0
        if player.right+player.vx>WIDTH:
            player.right=WIDTH
            player.vx=0
        if player.top+player.vy<0:
            player.top=0
            player.vy=0


        #陷阱
        
        for spine in spines:
            if spine.name=='trap1'and player.left-spine.right>10 and player.bottom<=spine.bottom :
                if not spine.animate_acted:
                    spine.angle-=90
                    animate(spine,tween='linear', duration=4,pos=(spine.pos[0]+1000,spine.pos[1]))
                    spine.animate_acted=True
            if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
                if not spine.animate_acted:
                    spine.image='spine_left_long'
                    spine.animate_acted=True
            if spine.name=='trap3'and player.height-spine.height<=10 and spine.left<=player.right:
                if not spine.animate_acted:
                    spine.angle-=0
                    animate(spine,tween='linear', duration=2,pos=(spine.pos[0],spine.pos[0]-900))
                    spine.animate_acted=True
            if spine.name=='trap4'and player.right>=(720) and player.bottom>=( 300) :
                if not spine.animate_acted:
                    spine.angle-=90
                    animate(spine,tween='linear', duration=1,pos=(spine.pos[0]+1300,spine.pos[1]))
                    spine.animate_acted=True
                    
            if spine.name=='trap5'and player.right>=(620) and player.bottom<=(100) :
                if not spine.animate_acted:
                    spine.angle-=0
                    animate(spine,tween='linear', duration=5,pos=(spine.pos[0]-1900,spine.pos[1]))
                    spine.animate_acted=True
            if spine.name=='trap6'and player.right>=(1100) and player.top>=550 :
                if not spine.animate_acted:
                    spine.angle-=0
                    animate(spine,tween='linear', duration=1,pos=(spine.pos[0]+1000,spine.pos[1]))
                    spine.animate_acted=True
                    
            

        
        if not test_mode:
            #碰撞检测
            for spine in spines:
                if spine.name in ("trap1","trap2","trap3","trap4","trap5","trap6","trap7") and player.colliderect(spine):
                    player.death=True
                else:
                    for point in spine.points:
                        if player.collidepoint(point):
                            player.death=True

            

        
        for platform in platforms:
            if platform.name=='platform2':
                if player.right<platform.right and player.bottom==platform.top and not platform.animate_acted:
                    animate(platform,tween='linear', duration=4,pos=(platform.pos[0],platform.pos[1]-600))
                    platform.animate_acted=True
            elif platform.name=='platform3':
                if player.left>platform.left and player.bottom==platform.top and not platform.animate_acted:
                    animate(platform,tween='accelerate', duration=0.5,pos=(platform.pos[0],platform.pos[1]+1000))
                    platform.animate_acted=True

    #死亡处理
    elif not music_played :
        music.play_once('fail')
        player.image='player_left_dead' if player.image=='player_left' else 'player_right_dead'
        music_played=True
        

    #运动
    player.left+=player.vx
    if player.bottom<=1000:player.bottom+=player.vy#<1000是为了防止死亡后一直下落



def on_key_down(key):
    global RESET_POS,test_mode
    #运动控制
    if not player.death:
        if key==key.RIGHT:
            player.staticvx=8
            player.image='player_right'
        if key==key.LEFT:
            player.staticvx=-8
            player.image='player_left'
        if key==key.SPACE:
            if player.onbottom:player.jumptime=0
            if player.jumptime<2:
                player.vy=-20
                player.jumptime+=1
                player.onbottom=False

        #保存存档点
        if key==key.S:
            for save in saves:
                if player.colliderect(save) and save.image=='save':
                    save.image='saved' 
                    RESET_POS=save.bottomleft
    if player.death or test_mode:
        if key==key.R :reset()
    if key==key.P:test_mode=True
    if key==key.ESCAPE:sys.exit(0)


def on_key_up(key):
    #运动控制
    if not player.death:
        if key==key.RIGHT:
            if not player.image=='player_left':
                player.staticvx=0
        if key==key.LEFT:
            if not player.image=='player_right':
                player.staticvx=0


reset()
pgzrun.go()