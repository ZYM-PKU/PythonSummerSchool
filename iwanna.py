# coding=utf-8
import sys
import time
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
#苹果
apples=[]
#尖刺
spines=[]


#人物
player=Actor('player_right')

RESET_POS=(0,BOTTOM)#设置重生点
death_count=0#死亡次数

music_played=False#保证死亡音乐只播放一次
test_mode=False#开发者模式（无敌）

current_window=0#当前窗口（0表示初始化界面）
current_y=-200#结尾字幕位置
death_end=False#必死结局
tic=0.0


def init():
    global RESET_POS,music_played
    bottoms.clear()
    bottom=Actor('start_bottom')
    bottom.bottomleft=(0,720)
    bottoms.append(bottom)
    RESET_POS=(0,720-bottom.height)

    spines.clear()
    for i in range(8):
        spine=Actor('spine_up')
        spine.bottomleft=(50+i*150,720-bottom.height)
        spine.points=[]
        spine.name="bottom"
        spines.append(spine)
    edge_sample()
    
    apples.clear()
    center,radius=(220,260),120
    apple=Actor('apple')
    apple.pos=center
    apple.name="center"
    apples.append(apple)
    for sita in range(5):
        apple=Actor('apple')
        apple.pos=(center[0]+radius*math.cos(sita*30),center[1]-radius*math.sin(sita*30))
        apple.anchor=(center[0]-apple.pos[0],center[1]-apple.pos[1])
        apple.name="rotate"
        apples.append(apple)

    center,radius=(1050,260),120
    apple=Actor('apple')
    apple.pos=center
    apple.name="center"
    apples.append(apple)
    for sita in range(5):
        apple=Actor('apple')
        apple.pos=(center[0]+radius*math.cos(sita*30),center[1]-radius*math.sin(sita*30))
        apple.anchor=(center[0]-apple.pos[0],center[1]-apple.pos[1])
        apple.name="rotate"
        apples.append(apple)
    #初始化玩家
    player.image='player_right'
    player.bottomleft=(0,720-bottom.height)
    #速度
    player.vx=0
    player.vy=0
    player.staticvx=0#惯性横向速度
    player.ay=2#垂直加速度
    #跳跃
    player.jumptime=0#连续跳跃次数
    player.onbottom=True#是否在地上
    player.anchor=player.midbottom
    #死亡
    player.death=False

    save=Actor('save')
    save.bottomright=(1280,720-bottom.height)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='end'
    saves.append(save)

    music_played=False
    #music.stop()
    music.play('bgm')

def ending():
    global RESET_POS,music_played,test_mode,tic
    test_mode=True#结局默认开启无敌

    tic=time.time()
    music.play('death')

    bottoms.clear()
    bottom=Actor('start_bottom')
    bottom.bottomleft=(0,800)
    bottoms.append(bottom)
    RESET_POS=(600,60)

    spines.clear()
    for i in range(8):
        spine=Actor('spine_up')
        spine.bottomleft=(80+i*150,800-bottom.height)
        spine.points=[]
        spine.name="bottom"
        spines.append(spine)
    edge_sample()
    
    apples.clear()
    platforms.clear()
    backs.clear()
    saves.clear()
    buttons.clear()
    trees.clear()

    #初始化玩家
    player.image='player_right'
    player.bottomleft=RESET_POS
    #速度
    player.vx=0
    player.vy=0
    player.staticvx=0#惯性横向速度
    player.ay=0.2#垂直加速度
    #跳跃
    player.jumptime=0#连续跳跃次数
    player.onbottom=True#是否在地上
    player.anchor=player.midbottom
    #死亡
    player.death=False


def reset(): 
    if current_window==1:smyreset()
    elif current_window==2:zymreset()
    elif current_window==3:zmxreset()
    elif current_window==4:wgcreset()
    elif current_window==5:ending()


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


def recover_platform():#平台上升
    for platform in platforms:
        if platform.name=='platform1':
            animate(platform,tween='accelerate', duration=0.3,pos=(platform.pos[0],platform.pos[1]-160))
    

def draw():
    global current_y
    screen.clear()
    if current_window==4: screen.blit('cover1',(0,0))
    else: screen.blit('cover',(0,0))
    for back in backs:back.draw()
    for tree in trees:tree.draw()
    for spine in spines:spine.draw()
    for platform in platforms:platform.draw()
    for bottom in bottoms:bottom.draw()
    for save in saves:save.draw()
    for button in buttons:button.draw()
    for apple in apples:apple.draw()
    player.draw()

    screen.draw.text(f"Deaths: {death_count}",(0, 0),gcolor="green",fontsize=30,fontname="comic")
    if player.death:
        if current_window<5:screen.draw.text("            GAME OVER\n--------------------------------\n PRESS 'R' TO CONTINUE",(120, 180), shadow=(2,2), scolor="#202020",fontsize=80,fontname="comic")
        else: screen.draw.text("            GAME OVER\n-------------------------------\n     PRESS 'Esc' To Exit",(120,180), shadow=(2,2), scolor="#202020",fontsize=80,fontname="comic")
    if current_window==0 and not player.death:
        screen.draw.text("         I WANNA\n       BE THE GUY",(130, 100), shadow=(2,2), scolor="#202020",gcolor="red",fontsize=100,fontname="comic")
        screen.draw.text("Use left/right arrow keys to move, space to jump and 's' to save",(200, 380),color="black",fontsize=30,fontname="comic")
        screen.draw.text("Version: 2.1.0",(1080, 680),gcolor="cyan",fontsize=30,fontname="comic")
        screen.draw.text("POWERED BY PYTHON",(200, 550), color=(255,127,80),fontsize=80,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
    if current_window==5:
        if current_y<=2050:current_y+=1
        screen.draw.text("Thanks for playing!",(120, current_y), shadow=(2,2), scolor="#202020",gcolor="cyan",fontsize=120,fontname="comic")
        screen.draw.text("Developers:",(150, current_y-500), color=(220,20,60),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
        screen.draw.text("Zhao YiMing",(550, current_y-700), color=(255,215,0),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
        screen.draw.text("Zhang manxi",(200, current_y-900), color=(255,182,193),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
        screen.draw.text("Shen mingyu",(480, current_y-1100), color=(255,105,180),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
        screen.draw.text("Wang gongchen",(300, current_y-1300), color=(0,191,255),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
        screen.draw.text(f"Total Deaths: {death_count}",(250, current_y-2000), color=(0,255,127),fontsize=100,owidth=1.5, ocolor="black", alpha=0.8,fontname="comic")
    

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

        if current_window==0:zymupdate()
        elif current_window==1:smyupdate()
        elif current_window==2:zymupdate()
        elif current_window==3:zmxupdate()
        elif current_window==4:wgcupdate()
    #死亡处理
    elif not music_played and current_window!=5:
        global death_count
        death_count+=1
        music.play_once('fail')
        player.image='player_left_dead' if player.image=='player_left' else 'player_right_dead'
        music_played=True
        
    if current_window==5:endupdate()
    else:
        #运动
        player.left+=player.vx
        if player.bottom<=1000:player.bottom+=player.vy#<1000是为了防止死亡后一直下落






def on_key_down(key):
    global RESET_POS,test_mode,current_window
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
                if player.jumptime==0:
                    sounds.jump.play()
                else:sounds.jump1.play()
                player.vy=-20
                player.jumptime+=1
                player.onbottom=False

        #保存存档点
        if key==key.S:
            for save in saves:
                if player.colliderect(save) and save.image=='save' :
                    if save.name!='end':
                        tone.play('E4', 0.1)
                        save.image='saved' 
                        RESET_POS=save.bottomleft
                    else:
                        tone.play('A#5', 0.1)
                        current_window+=1
                        if current_window==1:RESET_POS=(0,606)
                        elif current_window==2:RESET_POS=(0,710)
                        elif current_window==3:RESET_POS=(0,710)
                        elif current_window==4:RESET_POS=(0,606)
                        reset()




    if player.death or test_mode:
        if key==key.R and current_window<5:
            if current_window==0:
                init()
            else:    
                reset()
    if key==key.P:test_mode=not test_mode
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


def smyreset(): 
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
    platform.bottomright=(900,300)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('platform')
    platform.bottomleft=(480,300)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('platform')
    platform.topleft=(340,350)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('platform')
    platform.bottomright=(200,500)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('platform')
    platform.bottomright=(1280,300)
    platform.name='platform'
    platform.animate_acted=False
    platforms.append(platform)
   


    #初始化存档点
    saves.clear()
    save=Actor('saved')
    save.bottomleft=(0,BOTTOM)
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,519)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='end'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,220)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)

    #初始化按钮
    buttons.clear()
    button=Actor('button')
    button.bottomright=(1280,BOTTOM)
    buttons.append(button)
    
    #初始化树
    trees.clear()
    tree=Actor('tree')
    tree.bottomleft=(1000,BOTTOM)
    trees.append(tree)

    #初始化苹果
    apples.clear()
    apple=Actor('apple')
    apple.pos=(1050,450)
    apple.name="normal"
    apples.append(apple)
    apple=Actor('apple')
    apple.pos=(1180,390)
    apple.name="normal"
    apples.append(apple)
    


    #初始化尖刺
    spines.clear()
    for i in range(2):
        spine=Actor('spine_right')
        spine.bottomleft=(100,380-i*80)
        spine.points=[]
        spine.name="middle"
        spines.append(spine)


    

    #陷阱刺
    for i in range(2):
        spine=Actor('spine_up')
        spine.bottomleft=(180+i*80,220)
        spine.points=[]
        spine.name="trap1"
        spine.animate_acted=False
        spines.append(spine)
    
    for i in range (8):
        spine=Actor('spine_up')
        spine.bottomleft=(100+100*i,750-bottom.height)
        spine.points=[]
        spine.name="trap2"
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
    #music.stop()
    music.play('bgm')

def zymreset(): 
    global music_played,BOTTOM


    #初始化地面
    bottoms.clear()
    bottom=Actor('bottom1')
    bottom.bottomleft=(0,800)
    bottoms.append(bottom)
    BOTTOM=800-bottom.height
    bottom=Actor('bottom_half')
    bottom.bottomright=(1174,580)
    bottoms.append(bottom)
    bottom=Actor('bottom_top_right')
    bottom.bottomright=(1280,250)
    bottoms.append(bottom)
    bottom=Actor('bottom_top_left')
    bottom.bottomright=(403,250)
    bottoms.append(bottom)
    bottom=Actor('vertical')
    bottom.bottomright=(1174,519)
    bottoms.append(bottom)
    bottom=Actor('vertical')
    bottom.bottomright=(1174-500,519)
    bottoms.append(bottom)

    bottom=Actor('platform')
    bottom.topleft=(237,392)
    bottoms.append(bottom)
    bottom=Actor('vertical1')
    bottom.bottomleft=(0,452)
    bottoms.append(bottom)
    bottom=Actor('vertical2')
    bottom.bottomleft=(900,162)
    bottoms.append(bottom)
    
    #初始化平台
    platforms.clear()
    platform=Actor('platform')
    platform.bottomleft=(1174,580)
    platform.name='platform1'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('bottom_middle')
    platform.topleft=(104,392)
    platform.name='platform2'
    platform.animate_acted=False
    platforms.append(platform)
    platform=Actor('bottom_top_middle')
    platform.bottomright=(503,250)
    platform.name='platform3'
    platform.animate_acted=False
    platforms.append(platform)

    #初始化背景
    backs.clear()
    back=Actor('back1')
    back.topright=(1280,580)
    backs.append(back)
    back=Actor('back2')
    back.topright=(1280,250)
    backs.append(back)

    #初始化存档点
    saves.clear()
    save=Actor('saved')
    save.bottomleft=(0,BOTTOM)
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,519)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,162)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='end'
    saves.append(save)
    save=Actor('save')
    save.bottomleft=(280,392)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)

    #初始化按钮
    buttons.clear()
    button=Actor('button')
    button.bottomright=(1280,BOTTOM)
    buttons.append(button)
    
    #初始化树木
    trees.clear()
    tree=Actor('tree')
    tree.bottomleft=(100,BOTTOM)
    trees.append(tree)

    #初始化苹果
    apples.clear()
    apple=Actor('apple')
    apple.pos=(220,560)
    apple.name="normal"
    apples.append(apple)
    apple=Actor('apple')
    apple.pos=(270,522)
    apple.name="normal"
    apples.append(apple)

    center,radius=(880,360),120
    apple=Actor('apple')
    apple.pos=center
    apple.name="center"
    apples.append(apple)
    for sita in range(5):
        apple=Actor('apple')
        apple.pos=(center[0]+radius*math.cos(sita*30),center[1]-radius*math.sin(sita*30))
        apple.anchor=(center[0]-apple.pos[0],center[1]-apple.pos[1])
        apple.name="rotate"
        apples.append(apple)


    #初始化尖刺
    spines.clear()
    for i in range(4):
        spine=Actor('spine_up')
        spine.bottomleft=(500+i*170,BOTTOM)
        spine.points=[]
        spine.name="bottom"
        spines.append(spine)
    for i in range(4):
        spine=Actor('spine_down')
        spine.topleft=(585+i*170,580)
        spine.points=[]
        spine.name="bottom"
        spines.append(spine)
    for i in range(2):
        spine=Actor('spine_right')
        spine.bottomleft=(104,320-i*140)
        spine.points=[]
        spine.name="middle"
        spines.append(spine)
        spine=Actor('spine_right')
        spine.bottomleft=(104,100+i*292)
        spine.points=[]
        spine.name="middle"
        spines.append(spine)

    for i in range(2):
        spine=Actor('spine_up')
        spine.bottomleft=(980+i*130,162)
        spine.points=[]
        spine.name="top"
        spines.append(spine)
    for i in range(3):
        spine=Actor('spine_up')
        spine.bottomleft=(503+i*130,162)
        spine.points=[]
        spine.name="top"
        spines.append(spine)
    spine=Actor('spine_left')
    spine.bottomright=(252,250)
    spine.points=[]
    spine.name="middle"
    spines.append(spine)    


    #陷阱刺
    spine=Actor('spine_up')
    spine.bottomright=(1170,500)
    spine.points=[]
    spine.name="trap1"
    spine.animate_acted=False
    spines.append(spine)
    spine=Actor('spine_left')
    spine.topright=(503,519)
    spine.points=[]
    spine.name="trap2"
    spine.animate_acted=False
    spines.append(spine)
    for i in range(2):
        spine=Actor('spine_up')
        spine.bottomleft=(252+i*25,162)
        spine.points=[]
        spine.name="trap3"
        spine.animate_acted=False
        spines.append(spine)




    edge_sample()#尖刺边界采样


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
    player.anchor=player.midbottom
    #死亡
    player.death=False
    music_played=False
    animate_acted=False
    #music.stop()
    music.play('bgm')


def zmxreset(): 
    global music_played,BOTTOM

#初始化地面
    bottoms.clear()
    bottom=Actor('bottom1')
    bottom.bottomleft=(0,800)
    bottoms.append(bottom)
    BOTTOM=800-bottom.height
    bottom=Actor('bottom_top_left')
    bottom.bottomright=(240,649)
    bottoms.append(bottom)  
    bottom=Actor('vertical')
    bottom.bottomright=(375,610)
    bottoms.append(bottom)  
    bottom=Actor('vertical')
    bottom.bottomright=(1150,370)
    bottoms.append(bottom)   
    bottom=Actor('vertical')
    bottom.bottomright=(723,225)
    bottoms.append(bottom)   
    bottom=Actor('platform')
    bottom.topleft=(240,170)
    bottoms.append(bottom)  
    bottom=Actor('platform')
    bottom.topleft=(450,88)
    bottoms.append(bottom)   
    bottom=Actor('vertical1')
    bottom.bottomleft=(450,730)
    bottoms.append(bottom) 
    bottom=Actor('vertical2')
    bottom.bottomleft=(552,170)
    bottoms.append(bottom)
    bottom=Actor('vertical1')
    bottom.bottomleft=(510,730)
    bottoms.append(bottom)
    bottom=Actor('vertical1')
    bottom.bottomleft=(723,580)
    bottoms.append(bottom)
    bottom=Actor('vertical1')
    bottom.bottomleft=(900,500)
    bottoms.append(bottom)    

#初始化平台
    platforms.clear()    
    platform=Actor('platform')
    platform.bottomleft=(1174,580)
    platform.name='platform1'
    platform.animate_acted=False
    platforms.append(platform)        

#初始化存档点
    saves.clear()
    save=Actor('save')
    save.bottomleft=(0,BOTTOM)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomleft=(350,265)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,519)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='end'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(770,170)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)
    save=Actor('save')
    save.bottomleft=(480,90)
    if save.bottomleft==RESET_POS:save.image='saved'
    save.name='normal'
    saves.append(save)

#初始化按钮
    buttons.clear()
    button=Actor('button')
    button.bottomright=(1280,BOTTOM)
    buttons.append(button)  

#初始化树木
    trees.clear()
    tree=Actor('tree')
    tree.bottomleft=(100,BOTTOM)
    trees.append(tree)
    tree=Actor('tree')
    tree.bottomleft=(970,BOTTOM)
    trees.append(tree)

#初始化苹果
    apples.clear()    
    apple=Actor('apple')
    apple.pos=(220,545)
    apple.name="normal"
    apples.append(apple)    
    apple=Actor('apple')
    apple.pos=(270,522)
    apple.name="normal"  
    apples.append(apple)    
    apple=Actor('apple')
    apple.pos=(1130,470)
    apple.name="normal"
    apples.append(apple)    
    apple=Actor('apple')
    apple.pos=(1150,522)
    apple.name="normal"
    apples.append(apple)    

#初始化尖刺
    spines.clear()
    for i in range(4):
        spine=Actor('spine_up')
        spine.bottomleft=(622+i*120,BOTTOM)
        spine.points=[]
        spine.name="bottom"
        spines.append(spine)    
    spine=Actor('spine_right')
    spine.bottomleft=(608,420)
    spine.points=[]
    spine.name="middle"
    spines.append(spine)  
    spine=Actor('spine_up')
    spine.bottomleft=(835,170)
    spine.points=[]
    spine.name="top"
    spines.append(spine)    

#陷阱刺
    spine=Actor('spine_up')
    spine.bottomright=(1179,440)
    spine.points=[]
    spine.name="trap1"
    spine.animate_acted=False
    spines.append(spine)
    spine=Actor('spine_left')
    spine.topright=(450,519)
    spine.points=[]
    spine.name="trap2"
    spine.animate_acted=False
    spines.append(spine) 
    spine=Actor('spine_up')
    spine.bottomleft=(175,190)
    spine.points=[]
    spine.name="trap3"
    spine.animate_acted=False
    spines.append(spine)

    edge_sample()#尖刺边界采样

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
    player.anchor=player.midbottom

#死亡
    player.death=False
    music_played=False
    animate_acted=False
    #music.stop()
    music.play('bgm')

def wgcreset(): 
    global music_played,BOTTOM

    apples.clear()
    buttons.clear()


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
    #music.stop()
    music.play('bgm')




def smyupdate():
    global music_played

    #陷阱
    for apple in apples:
        if apple.name=='normal' and abs(apple.left-player.left)<45 and player.top+20>apple.top:
            animate(apple,tween='bounce_end', duration=0.1,pos=(apple.pos[0],BOTTOM-apple.height/2))
        if apple.name in ('rotate','center'):
            apple.angle+=1
    for spine in spines:
        if spine.name=='trap1'and player.left-spine.right>80 and player.bottom<=spine.bottom :
            if not spine.animate_acted:
                sounds.up.play()
                spine.angle-=90
                animate(spine,tween='linear', duration=5,pos=(spine.pos[0]+900,spine.pos[1]))
                spine.animate_acted=True
        if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
            if not spine.animate_acted:
                sounds.up.play()
                spine.image='spine_left_long'
                spine.animate_acted=True
        

    
    if not test_mode:
        #碰撞检测
        for spine in spines:
            if spine.name in ("trap1","trap2") and player.colliderect(spine):
                player.death=True
            for point in spine.points:
                if player.collidepoint(point):
                    player.death=True

        for apple in apples:
            if player.colliderect(apple):
                player.death=True

    for button in buttons:
        if player.colliderect(button):
            button.image='button_pressed'
            button.bottomright=(1280,BOTTOM)
    for platform in platforms:
        if platform.name=='platform1':
            if buttons[0].image=='button_pressed' and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.3,pos=(platform.pos[0],platform.pos[1]+160))
                platform.animate_acted=True
                clock.schedule_unique(recover_platform,1)
        elif platform.name=='platform2':
            if player.right<platform.right and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='linear', duration=4,pos=(platform.pos[0],platform.pos[1]-600))
                platform.animate_acted=True
        elif platform.name=='platform3':
            if player.left>platform.left and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.5,pos=(platform.pos[0],platform.pos[1]+1000))
                platform.animate_acted=True



def zymupdate():
    global music_played


    #陷阱
    for apple in apples:
        if apple.name=='normal' and abs(apple.left-player.left)<45 and player.top+20>apple.top:
            animate(apple,tween='bounce_end', duration=0.1,pos=(apple.pos[0],BOTTOM-apple.height/2))
        if apple.name in ('rotate','center'):
            apple.angle+=1
    for spine in spines:
        if spine.name=='trap1'and abs(spine.right-player.left)<10 and player.bottom<350 :
            if not spine.animate_acted:
                animate(spine,tween='accelerate', duration=0.5,pos=(spine.pos[0],spine.pos[1]-1000))
                sounds.up.play()
                spine.animate_acted=True
        if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
            if not spine.animate_acted:
                spine.image='spine_left_long'
                sounds.up.play()
                spine.animate_acted=True
        if spine.name=='trap3'and player.left-spine.right>80 and player.bottom<=spine.bottom :
            if not spine.animate_acted:
                spine.angle-=90
                animate(spine,tween='linear', duration=5,pos=(spine.pos[0]+900,spine.pos[1]))
                spine.animate_acted=True

    
    if not test_mode:
        #碰撞检测
        for spine in spines:
            if spine.name in ("trap1","trap2","trap3") and player.colliderect(spine):
                player.death=True
            for point in spine.points:
                if player.collidepoint(point):
                    player.death=True

        for apple in apples:
            if player.colliderect(apple):
                player.death=True

    for button in buttons:
        if player.colliderect(button):
            button.image='button_pressed'
            button.bottomright=(1280,BOTTOM)
    for platform in platforms:
        if platform.name=='platform1':
            if buttons[0].image=='button_pressed' and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.3,pos=(platform.pos[0],platform.pos[1]+160))
                platform.animate_acted=True
                sounds.up.play()
                clock.schedule_unique(recover_platform,1)
        elif platform.name=='platform2':
            if player.right<platform.right and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='linear', duration=4,pos=(platform.pos[0],platform.pos[1]-600))
                platform.animate_acted=True
        elif platform.name=='platform3':
            if player.left>platform.left and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.5,pos=(platform.pos[0],platform.pos[1]+1000))
                sounds.up.play()
                platform.animate_acted=True

    
        
        
def zmxupdate():
    global music_played

#陷阱
    for apple in apples:
        if apple.name=='normal' and abs(apple.left-player.left)<45 and player.top+20>apple.top:
            animate(apple,tween='bounce_end', duration=0.1,pos=(apple.pos[0],BOTTOM-apple.height/2))
        if apple.name in ('rotate','center'):
            apple.angle+=1
    for spine in spines:
        if spine.name=='trap1'and abs(spine.right-player.left)<10 and player.bottom<350 :
            if not spine.animate_acted:
                animate(spine,tween='accelerate', duration=0.5,pos=(spine.pos[0],spine.pos[1]-1000))
                sounds.up.play()
                spine.animate_acted=True
        if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
            if not spine.animate_acted:
                spine.image='spine_left_long'
                sounds.up.play()
                spine.animate_acted=True
        if spine.name=='trap3'and player.left-spine.right>80 and player.bottom<=spine.bottom :
            if not spine.animate_acted:
                spine.angle-=90
                animate(spine,tween='linear', duration=5,pos=(spine.pos[0]+1020,spine.pos[1]))
                spine.animate_acted=True        
    if not test_mode:

#碰撞检测
        for spine in spines:
            if spine.name in ("trap1","trap2","trap3") and player.colliderect(spine):
                player.death=True
            for point in spine.points:
                if player.collidepoint(point):
                    player.death=True
        for apple in apples:
            if player.colliderect(apple):
                player.death=True
    for button in buttons:
        if player.colliderect(button):
            button.image='button_pressed'
            button.bottomright=(1280,BOTTOM)
    for platform in platforms:
        if platform.name=='platform1':
            if buttons[0].image=='button_pressed' and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.3,pos=(platform.pos[0],platform.pos[1]+160))
                platform.animate_acted=True
                sounds.up.play()
                clock.schedule_unique(recover_platform,1)
        elif platform.name=='platform2':
            if player.right<platform.right and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='linear', duration=4,pos=(platform.pos[0],platform.pos[1]-600))
                sounds.up.play()
                platform.animate_acted=True
        elif platform.name=='platform3':
            if player.left>platform.left and player.bottom==platform.top and not platform.animate_acted:
                animate(platform,tween='accelerate', duration=0.5,pos=(platform.pos[0],platform.pos[1]+1000))
                platform.animate_acted=True





def wgcupdate():
    global music_played


    #陷阱
    
    for spine in spines:
        if spine.name=='trap1'and player.left-spine.right>10 and player.bottom<=spine.bottom :
            if not spine.animate_acted:
                sounds.up.play()
                spine.angle-=90
                animate(spine,tween='linear', duration=4,pos=(spine.pos[0]+1000,spine.pos[1]))
                spine.animate_acted=True
        if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
            if not spine.animate_acted:
                sounds.up.play()
                spine.image='spine_left_long'
                spine.animate_acted=True
        if spine.name=='trap3'and player.height-spine.height<=10 and spine.left<=player.right:
            if not spine.animate_acted:
                sounds.up.play()
                spine.angle-=0
                animate(spine,tween='linear', duration=2,pos=(spine.pos[0],spine.pos[0]-900))
                spine.animate_acted=True
        if spine.name=='trap4'and player.right>=(720) and player.bottom>=( 300) :
            if not spine.animate_acted:
                sounds.up.play()
                spine.angle-=90
                animate(spine,tween='linear', duration=1,pos=(spine.pos[0]+1300,spine.pos[1]))
                spine.animate_acted=True
                
        if spine.name=='trap5'and player.right>=(620) and player.bottom<=(100) :
            if not spine.animate_acted:
                sounds.up.play()
                spine.angle-=0
                animate(spine,tween='linear', duration=5,pos=(spine.pos[0]-1900,spine.pos[1]))
                spine.animate_acted=True
        if spine.name=='trap6'and player.right>=(1100) and player.top>=550 :
            if not spine.animate_acted:
                sounds.up.play()
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

    


def endupdate():
    global music_played,death_count
    
    
    a_num=len(apples)
    if a_num<=100:
        apple=Actor('apple')
        apple.topleft=(random.randint(0,1250),0)
        apple.ay=0.5
        apple.vy=0
        apple.name='normal'
        apples.append(apple)
    
    for apple in apples:
        if apple.name=='normal':
            apple.vy+=apple.ay
            apple.top+=apple.vy
            if apple.top>720: apples.remove(apple)

    toc=time.time()
    global death_end
    if (toc-tic)>=40:
        apple=Actor('bigapple')
        apple.bottomleft=(0,0)
        apple.name='bigapple'
        apples.append(apple)
        if not death_end:
            animate(apple,tween='accelerate', duration=1,pos=(apple.pos[0],apple.pos[1]+1000))
            death_count+=1
            death_end=True

    for apple in apples:
        if apple.name=='bigapple':
            if player.colliderect(apple):player.death=True


    #运动
    player.jumptime=0#无限跳跃
    player.left+=player.vx
    if player.bottom<=1000:player.bottom+=player.vy#<1000是为了防止死亡后一直下落


init()
pgzrun.go()
