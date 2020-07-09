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

#苹果
apples=[]

#尖刺
spines=[]

#人物
player=Actor('player_right')
RESET_POS=(0,BOTTOM)#设置重生点
music_played=False#保证死亡音乐只播放一次
test_mode=False#开发者模式（无敌）


def reset(): 
    global music_played,BOTTOM
    #初始化地面——有待修改
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
    bottom.bottomright=(723,205)
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
    bottom.bottomleft=(552,150)
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
    save.bottomleft=(350,265)
    if save.bottomleft==RESET_POS:save.image='saved'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(1280,519)
    if save.bottomleft==RESET_POS:save.image='saved'
    saves.append(save)
    save=Actor('save')
    save.bottomright=(770,170)
    if save.bottomleft==RESET_POS:save.image='saved'
    saves.append(save)
    save=Actor('save')
    save.bottomleft=(480,90)
    if save.bottomleft==RESET_POS:save.image='saved'
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

def recover_platform():#平台上升
    for platform in platforms:
        if platform.name=='platform1':
            animate(platform,tween='accelerate', duration=0.3,pos=(platform.pos[0],platform.pos[1]-400))

def draw():
    screen.clear()
    screen.blit('cover',(0,0))
    for back in backs:back.draw()
    for tree in trees:tree.draw()
    for spine in spines:spine.draw()
    for platform in platforms:platform.draw()
    for bottom in bottoms:bottom.draw()
    for save in saves:save.draw()
    for button in buttons:button.draw()
    for apple in apples:apple.draw()
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
        for apple in apples:
            if apple.name=='normal' and abs(apple.left-player.left)<45 and player.top+20>apple.top:
                animate(apple,tween='bounce_end', duration=0.1,pos=(apple.pos[0],BOTTOM-apple.height/2))
            if apple.name in ('rotate','center'):
                apple.angle+=1
        for spine in spines:
            if spine.name=='trap1'and abs(spine.right-player.left)<10 and player.bottom<350 :
                if not spine.animate_acted:
                    animate(spine,tween='accelerate', duration=0.5,pos=(spine.pos[0],spine.pos[1]-1000))
                    music.play_once('up')
                    spine.animate_acted=True
            if spine.name=='trap2'and spine.right-player.left>3 and player.bottom<=spine.top :
                if not spine.animate_acted:
                    spine.image='spine_left_long'
                    music.play_once('up')
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
                    music.play_once('up')
                    clock.schedule_unique(recover_platform,1)
            elif platform.name=='platform2':
                if player.right<platform.right and player.bottom==platform.top and not platform.animate_acted:
                    animate(platform,tween='linear', duration=4,pos=(platform.pos[0],platform.pos[1]-600))
                    music.play_once('up')
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
                if player.jumptime==0:
                    music.play_once('jump')
                else:music.play_once('jump1')
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

