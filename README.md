# shoting
This is a Space Invaders game which is created by turtle but I'm gonna change it pygame when I will finish coding in turtle.
import turtle
sc=turtle.Screen()
sc.bgpic("space.png")
sc.title("infinity shot2")
sc.setup(700,700)


#player
player=turtle.Turtle(shape="circle")
player.speed(0)
player.color("white")
player.penup()
player.setposition(0,-250)
player.setheading(90)
pl_pos=20

#enemy#goto=setposition=setpos
enemy=turtle.Turtle(shape="triangle")
enemy.speed(0)
enemy.color("red")
enemy.penup()
enemy.goto(-250, 250)
enemy.setheading(270)
en_pos=1
en_posy=20

#bullet
bullet=turtle.Turtle()
bullet.shape("triangle")
bullet.shapesize(0.5,0.5)
bullet.speed(0)
bullet.color("yellow")
bullet.penup()
bullet.setheading(90)
bullet.hideturtle()
bl_pos=20

ste_position="ready"
#click
def c_left():
    x=player.xcor()
    x-=pl_pos
    if x<-290:
        x=-290
    player.setx(x)

def c_right():
    x=player.xcor()
    x+=pl_pos
    if x>290:
        x=290
    player.setx(x)
    
def fire():
    global state_position
    x=player.xcor()
    y=player.ycor()
    bullet.goto(x,y+10)
    bullet.showturtle()


#wn listen
sc.listen()
sc.onkey(c_left, "Left")
sc.onkey(c_right, "Right")
sc.onkey(fire, "space")

while True:
    y=enemy.ycor()
    x=enemy.xcor()
    x+=en_pos
    enemy.setx(x)

    if x>290:
        y-=en_posy
        enemy.sety(y)
        en_pos*=-1

    if x<-290:
        y-=en_posy
        enemy.sety(y)
        en_pos*=-1

    y=bullet.ycor()
    y+=bl_pos
    bullet.sety(y)

