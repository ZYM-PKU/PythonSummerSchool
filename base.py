import pgzrun
import random

#全局设置
WIDTH = 1280
HEIGHT = 720


#地图底部
bottom=Actor('bottom1')
bottom.bottomleft=(0,720)
BOTTOM=720-bottom.height

#存档点
save=Actor('save')
save.bottomleft=(0,BOTTOM)

#人物
player=Actor('player_right')
player.bottomleft=(0,BOTTOM)
#速度
player.vx=0
player.vy=0
#加速度
player.ax=0
player.ay=2
#跳跃
player.jumptime=0#连续跳跃次数
player.onbottom=True#是否在地上
#死亡
player.death=False

#尖刺
spines=[]
spine=Actor('spine_up')
spine.bottomleft=(500,BOTTOM)
spine.points=[]
spines.append(spine)
spine=Actor('spine_down')
spine.bottomleft=(250,BOTTOM)
spine.points=[]
spines.append(spine)

def init():
    for spine in spines:
        if spine.image=='spine_up':
            x,y=spine.bottomleft
            for i in range(100):
                x+=(spine.width/2)/100
                y-=spine.height/100
                spine.points.append((x,y))
            for i in range(100):
                x+=(spine.width/2)/100
                y+=spine.height/100
                spine.points.append((x,y))
        else:
            x,y=spine.topleft
            for i in range(100):
                x+=(spine.width/2)/100
                y+=spine.height/100
                spine.points.append((x,y))
            for i in range(100):
                x+=(spine.width/2)/100
                y-=spine.height/100
                spine.points.append((x,y))




def draw():
    screen.clear()
    screen.blit('cover',(0,0))
    bottom.draw()
    save.draw()
    for spine in spines:spine.draw()
    player.draw()
    
def update():
    #运动模块
    player.vy+=player.ay
    player.left+=player.vx
    player.bottom+=player.vy

    #边界检测
    if player.colliderect(bottom) and player.vy>0:
        player.vy=0
        player.bottom=bottom.top
        player.onbottom=True
    if player.left<0:
        player.left=0
        player.vx=0
    if player.right>WIDTH:
        player.right=WIDTH
        player.vx=0
    
    #碰撞检测
    for spine in spines:
        for point in spine.points:
            if player.collidepoint(point):
                player.death=True
    if player.death:
        player.image='player_left_dead' if player.image=='player_left' else 'player_right_dead'
        clock.schedule(reset,0.1)

def on_key_down(key):
    #运动控制
    if key==key.RIGHT:
        player.vx=8
        player.image='player_right'
    if key==key.LEFT:
        player.vx=-8
        player.image='player_left'
    if key==key.SPACE:
        if player.jumptime==2:
            if player.onbottom:player.jumptime=0
        if player.jumptime<2:
            player.vy=-20
            player.jumptime+=1
            player.onbottom=False

    #保存
    if key==key.S:
        if player.colliderect(save) and save.image=='save':
            save.image='saved' 
    
def on_key_up(key):
    #运动控制
    if key==key.RIGHT:
        if not player.image=='player_left':player.vx=0
    if key==key.LEFT:
        if not player.image=='player_right':player.vx=0

def reset():
    player.image='player_right'
    player.bottomleft=(0,BOTTOM)
    player.vx=0
    player.vy=0
    player.jumptime=0#连续跳跃次数
    player.onbottom=True#是否在地上
    player.death=False


init()
pgzrun.go()