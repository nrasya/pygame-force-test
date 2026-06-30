import pygame
import math


# --------- INITIALIZATION ---------
pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
running = True

# ------------ CONSTANT ----------
ground_friction = 2
gravity = 9.8

# ------------ CLASS ------------

class box:
    def __init__(self,mass,x,y,size,vx,vy,color,static):
        self.mass = mass
        self.x = x
        self.y = y
        self.size = size
        self.width, self.height = self.size
        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.color = color
        self.default_color = color


        self.on_ground = False
        self.prev_on_ground = False

        self.static = static

        self.Fx_var = []
        self.Fy_var = []
        self.Fx_total = 0
        self.Fy_total = 0


    def physic(self):
        if not self.static:
            self.ax = self.Fx_total / self.mass
            self.ay = self.Fy_total / self.mass

            self.vx += self.ax * dt
            self.vy += self.ay * dt

            self.x += self.vx * dt
            self.y += self.vy * dt

    def add_force(self,force,degree):

        self.Fx_total += force * math.cos(degree)
        self.Fy_total += force * math.sin(degree)

    def remove_force(self,force,degree):

        self.Fx_total -= force * math.cos(degree)
        self.Fy_total -= force * math.sin(degree)

    def draw(self):
        box = pygame.Rect(0, 0, self.width, self.height)
        box.center = (self.x, self.y)
        pygame.draw.rect(screen, self.color, box)

        pygame.draw.line(screen,
                (150,200,150),
                (self.x,self.y),
                (self.x + self.Fx_total ,self.y),
                3
                )

        pygame.draw.line(screen,
                (100,50,100),
                (self.x,self.y),
                (self.x, self.y  + self.Fy_total),
                3
                )
        
    def x_collision(self,other):
        distance = abs(self.x - other.x)
        if distance < self.width/2 + other.width/2:
            return True
        else:
            return False
        
    def y_collision(self,other):
        distance_y = abs(self.y - other.y)

        if distance_y < self.height/2 + other.height/2:
            return True
        else:
            return False

# ----------- FUNCTION ------------
def draw_text(text, x, y):
    surface = font.render(text, True, (0, 0, 0))
    screen.blit(surface, (x, y))


# ------------ OBJECT -----------
boxes = [
    box(100,400,550,(800,100),0,0,(75,255,75),True),
    box(10,100,100,(100,100),30,0,(255,255,0),False),
    box(10,400,100,(100,100),0,0,(255,255,255),False)
]

#add initial force
for box in boxes:
    box.add_force(gravity * box.mass,3.14/2
    )

# ------------ RUN -------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((190,220,255))
    dt = clock.tick(60) / 1000  # 0.0167 s

    for box in boxes:       
        box.physic()

    
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            
            box1 = boxes[i]
            box2 = boxes[j]

            if box1.x_collision(box2) and box1.y_collision(box2):

                distance_x = abs(box1.x - box2.x)
                distance_y = abs(box1.y - box2.y)

                overlap_x = box1.width/2 + box2.width/2 - distance_x
                overlap_y = box1.height/2 + box2.height/2 - distance_y

                if overlap_x < overlap_y: # overlapping ---> contact
                    #x axis
                    vx_relative = box1.vx - box2.vx
                    if abs(vx_relative) > 0:
                        if box1.vx > 0:
                            box1.x -= overlap_x + overlap_x/100
                        else:
                            box1.x += overlap_x + overlap_x/100
                    
                    J = -((1 + 1)*(box2.vx - box1.vx)) / ((1/box1.mass)+(1/box2.mass)) 
                    if not box1.static:
                        box1.vx = box1.vx - J/box1.mass 
                        box1.add_force(box2.Fx_total,0)

                    if not box2.static:
                        box2.vx = box2.vx + J/box2.mass
                        box2.add_force(box1.Fx_total,0)


                    

                else:
                    #y axis
                    vy_relative = box1.vy - box2.vy
                    if abs(vy_relative) < 1:
                        if box1.vy > 0: 
                            box1.y -= overlap_y + overlap_y/100
                        else:
                            box1.y += overlap_y + overlap_y/100

                    J = -((1 + 1)*(box2.vy - box1.vy)) / ((1/box1.mass)+(1/box2.mass)) 
                    if not box1.static: 
                        box1.vy = box1.vy - J/box1.mass
                        
                    if not box2.static:
                        box2.vy = box2.vy + J/box2.mass
                




    # ------ TEXTS ---------
    y_offset = 10
    for i, box in enumerate(boxes):

        values = {
            "x": box.x,
            "y": box.y,
            "":"",
            "vx": box.vx,
            "vy": box.vy,
            " ":"",
            "Fx": box.Fx_total,
            "Fy": box.Fy_total
        }

        draw_text(f"Box {i}", 10, y_offset)
        y_offset += 20 #title

        for name, value in values.items():
            if isinstance(value, (bool, str, int)) == True:
                draw_text(f"{name}: {value}", 10, y_offset)
            elif isinstance(value, float):
                draw_text(f"{name}: {value:.1f}", 10, y_offset)
                
            y_offset += 20

        y_offset += 100 #gap


    for box in boxes:
        box.draw()
        box.color = box.default_color

    
    pygame.display.flip()

# ----------- QUIT -----------
pygame.quit()