import pgzrun
import random

#全局设置
WIDTH = 1280
HEIGHT = 720

BOTTOM=0
#地图地面
bottoms=[]
bottom=Actor('bottom1')
bottom.bottomleft=(0,800)
bottoms.append(bottom)
BOTTOM=800-bottom.height
bottom=Actor('bottom_half')
bottom.bottomright=(1280,580)
bottoms.append(bottom)

#存档点
saves=[]
save=Actor('save')
save.bottomleft=(0,BOTTOM)
saves.append(save)

#树木
trees=[]
tree=Actor('tree')
tree.bottomleft=(100,BOTTOM)
trees.append(tree)

#苹果
apples=[]
apple=Actor('apple')
apple.pos=(220,560)
apples.append(apple)
apple=Actor('apple')
apple.pos=(270,522)
apples.append(apple)

#人物
player=Actor('player_right')
player.bottomleft=(0,BOTTOM)
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


played=False

def init():
    '''初始化函数，用于勾勒尖刺边界以进行边界检测'''
    for spine in spines:
        if spine.image=='spine_up':
            x,y=spine.bottomleft
            x+=2
            for i in range(100):
                x+=((spine.width-4)/2)/100
                y-=(spine.height-2)/100
                spine.points.append((x,y))
            for i in range(100):
                x+=((spine.width-4)/2)/100
                y+=(spine.height-2)/100
                spine.points.append((x,y))
        else:
            x,y=spine.topleft
            x+=2
            for i in range(100):
                x+=((spine.width-4)/2)/100
                y+=(spine.height-2)/100
                spine.points.append((x,y))
            for i in range(100):
                x+=((spine.width-4)/2)/100
                y-=(spine.height-2)/100
                spine.points.append((x,y))




def draw():
    screen.clear()
    screen.blit('cover',(0,0))
    for bottom in bottoms:bottom.draw()
    for save in saves:save.draw()
    for tree in trees:tree.draw()
    for apple in apples:apple.draw()
    for spine in spines:spine.draw()
    player.draw()
    

def update():
    global played
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

        #全局边界检测
        if player.left+player.vx<0:
            player.left=0
            player.vx=0
        if player.right+player.vx>WIDTH:
            player.right=WIDTH
            player.vx=0

        #陷阱
        for apple in apples:
            if abs(apple.left-player.left)<45:
                animate(apple,tween='bounce_end', duration=0.1,pos=(apple.pos[0],BOTTOM-apple.height/2))
        
        #碰撞检测
        for spine in spines:
            for point in spine.points:
                if player.collidepoint(point):
                    player.death=True
        #for apple in apples:
        #    if player.colliderect(apple):
        #        player.death=True

    #死亡处理
    elif not played :
        music.play_once('fail')
        player.image='player_left_dead' if player.image=='player_left' else 'player_right_dead'
        played=True
        clock.schedule_unique(reset,6)
        

    #运动
    player.left+=player.vx
    if player.bottom<=1000:player.bottom+=player.vy


def on_key_down(key):
    #运动控制
    if not player.death:
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
    else:
        if key==key.R :reset()


def on_key_up(key):
    #运动控制
    if not player.death:
        if key==key.RIGHT:
            if not player.image=='player_left':
                player.staticvx=0
        if key==key.LEFT:
            if not player.image=='player_right':
                player.staticvx=0

def reset(): 
    global played
    if player.death:
        music.stop()
        #恢复尖刺
        spines.clear()
        spine=Actor('spine_up')
        spine.bottomleft=(500,BOTTOM)
        spine.points=[]
        spines.append(spine)
        init()
        
        #恢复苹果
        apples.clear()
        apple=Actor('apple')
        apple.pos=(220,560)
        apples.append(apple)
        apple=Actor('apple')
        apple.pos=(270,522)
        apples.append(apple)


        #恢复玩家
        player.image='player_right'
        player.bottomleft=(0,BOTTOM)
        player.staticvx=0
        player.vy=0
        player.jumptime=0#连续跳跃次数
        player.onbottom=True#是否在地上
        player.death=False
        played=False





init()
pgzrun.go()