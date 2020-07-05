import pgzrun
import random

#全局设置
WIDTH = 1280
HEIGHT = 720

BOTTOM=0
#地图地面
bottoms=[]
bottom=Actor('bottom1')
bottom.bottomleft=(0,720)
bottoms.append(bottom)
BOTTOM=720-bottom.height
bottom=Actor('bottom2')
bottom.bottomleft=(0,BOTTOM)
bottoms.append(bottom)

#存档点
save=Actor('save')
save.bottomleft=(0,BOTTOM)

#人物
player=Actor('player_right')
player.bottomleft=(1200,BOTTOM)
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

#尖刺
spines=[]
spine=Actor('spine_up')
spine.bottomleft=(500,BOTTOM)
spine.points=[]
spines.append(spine)
spine=Actor('spine_down')
spine.bottomleft=(250,BOTTOM)
spine.points=[]
#spines.append(spine)

def init():
    '''初始化函数，用于勾勒尖刺边界以进行边界检测'''
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
    for bottom in bottoms:bottom.draw()
    save.draw()
    for spine in spines:spine.draw()
    player.draw()
    

def update():
    #运动模块
    player.vy+=player.ay
    player.vx=player.staticvx

    #物体边界检测
    for bottom in bottoms:
        if bottom.top<=player.bottom+player.vy<=bottom.bottom and player.right<=bottom.right and player.left>=bottom.left :
            player.vy=0
            player.bottom=bottom.top
            player.onbottom=True
        if bottom.top<=player.top+player.vy<=bottom.bottom and player.right<=bottom.right and player.left>=bottom.left :
            player.vy=0
            player.top=bottom.bottom
        if bottom.left<=player.left+player.vx<=bottom.right and player.top>=bottom.top and player.bottom<=bottom.bottom :
            player.vx=0
            player.left=bottom.right
        if bottom.left<=player.right+player.vx<=bottom.right and player.top>=bottom.top and player.bottom<=bottom.bottom :
            player.vx=0
            player.right=bottom.left

    #全局边界检测
    if player.left<0:
        player.left=0
        player.vx=0
    if player.right>WIDTH:
        player.right=WIDTH
        player.vx=0

    #运动
    player.left+=player.vx
    player.bottom+=player.vy
    
    #碰撞检测
    for spine in spines:
        for point in spine.points:
            if player.collidepoint(point):
                player.death=True

    #死亡处理
    if player.death:
        player.image='player_left_dead' if player.image=='player_left' else 'player_right_dead'
        clock.schedule(reset,0.1)


def on_key_down(key):
    #运动控制
    if key==key.RIGHT:
        player.staticvx=8
        player.image='player_right'
    if key==key.LEFT:
        player.staticvx=-8
        player.image='player_left'
    if key==key.SPACE:
        if player.jumptime==2:
            if player.onbottom:player.jumptime=0
        if player.jumptime<2:
            player.vy=-20
            player.jumptime+=1
            player.onbottom=False

    #保存存档点
    if key==key.S:
        if player.colliderect(save) and save.image=='save':
            save.image='saved' 
    
def on_key_up(key):
    #运动控制
    if key==key.RIGHT:
        if not player.image=='player_left':
            player.staticvx=0
    if key==key.LEFT:
        if not player.image=='player_right':
            player.staticvx=0

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