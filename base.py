import pgzrun
import random


WIDTH = 1280
HEIGHT = 720


bottom=Actor('bottom1')
bottom.bottomleft=(0,720)
BOTTOM=720-bottom.height



player=Actor('player_right')
player.bottomleft=(0,BOTTOM)
player.vx=0
player.vy=0
player.ax=0
player.ay=2

spine=Actor('spine')
spine.bottomleft=(70,720)
save=Actor('saved')
save.bottomleft=(0,BOTTOM)



def draw():
    screen.clear()
    screen.blit('cover',(0,0))
    bottom.draw()
    save.draw()
    player.draw()
    
def update():
    player.vy+=player.ay
    player.left+=player.vx
    player.bottom+=player.vy
    if player.bottom>BOTTOM:
        player.vy=0
        player.bottom=BOTTOM
    if player.left<0:
        player.left=0
        player.vx=0
    if player.right>WIDTH:
        player.right=WIDTH
        player.vx=0

def on_key_down(key):
    if key==key.RIGHT:
        player.vx=10
        player.image='player_right'
    if key==key.LEFT:
        player.vx=-10
        player.image='player_left'
    if key==key.SPACE:
        player.vy=-20
    
def on_key_up(key):
    if key==key.RIGHT:
        if not player.image=='player_left':player.vx=0
    if key==key.LEFT:
        if not player.image=='player_right':player.vx=0


pgzrun.go()