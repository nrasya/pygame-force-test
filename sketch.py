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
        distance_x = abs(self.x - other.x)

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
    box(1,400,600,(800,100),0,0,(75,255,75),True),
    box(10,100,100,(100,100),30,0,(255,255,0),False),
    box(10,400,300,(100,100),0,0,(255,255,255),False)
]
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
            
            box_1 = boxes[i]
            box_2 = boxes[j]

            x_distance = abs(box_1.x - box_2.x)
            y_distance = abs(box_1.y - box_2.y)

            x_collideDistance = box_1.width/2 + box_2.width/2
            y_collideDistance = box_1.height/2 + box_2.height/2
                
            x_overlap = x_collideDistance - x_distance 
            y_overlap = y_collideDistance - y_distance 

            if x_distance < x_collideDistance and y_distance < y_collideDistance: #overlapping on both axis
                if x_overlap < y_overlap:       #collide on x
                    if box_1.static:
                        if box_1.x < box_2.x:
                            box_2.x += x_overlap
                        else:
                            box_2.x -= x_overlap

                    elif box_2.static:
                        if box_1.x < box_2.x:
                            box_1.x -= x_overlap
                        else:
                            box_1.x += x_overlap

                    else:
                        correction = x_overlap / 2
                        if box_1.x < box_2.x:
                            box_1.x -= correction
                            box_2.x += correction
                        else:
                            box_1.x += correction
                            box_2.x -= correction

                    relative_velocity = abs(box_1.vx - box_2.vx)

                    if relative_velocity > 0 :
                        J = -((1 + 0)*(box_2.vx - box_1.vx)) / ((1/box_1.mass)+(1/box_2.mass)) 
                        box_1.vx = box_1.vx - J/box_1.mass 
                        box_2.vx = box_2.vx + J/box_2.mass




                else:       # collide on y
                    if box_1.static:
                        if box_1.y < box_2.y:
                            box_2.y += y_overlap
                        else:
                            box_2.y -= y_overlap

                    elif box_2.static:
                        if box_1.y < box_2.y:
                            box_1.y -= y_overlap
                        else:
                            box_1.y += y_overlap

                    else:
                        correction = y_overlap / 2
                        if box_1.y < box_2.y:
                            box_1.y -= correction
                            box_2.y += correction
                        else:
                            box_1.y += correction
                            box_2.y -= correction
                    

                    relative_velocity = abs(box_1.vy - box_2.vy)

                    if relative_velocity > 0 :
                        J = -((1 + 0)*(box_2.vy - box_1.vy)) / ((1/box_1.mass)+(1/box_2.mass)) 
                        box_1.vy = box_1.vy - J/box_1.mass 
                        box_2.vy = box_2.vy + J/box_2.mass







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