import pygame
import math

pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()



ground = 500
ground_friction = 2
gravity = 9.8

# ------------ CLASS ---------

class box:
    def __init__(self,mass,x,y,size,vx,vy,color):
        self.mass = mass
        self.x = x
        self.y = y
        self.ax = 0
        self.ay = 0
        self.size = size
        self.vx = vx
        self.vy = vy
        self.color = color
        self.default_color = color
        self.Fx_total = 0
        self.Fy_total = 0
        self.on_ground = False
        self.F_normal = 0.0
        self.F_airres = 2.0
        self.F_friction = 0.0


    def physic(self):

        if self.y >= ground - self.size/2:
            self.on_ground = True
        else:
            self.on_ground = False

        # ----- X FORCE ------

        # air res
        if self.vx > 0: 
            F_airres = -self.F_airres
        elif self.vx < 0:
            F_airres = self.F_airres
        else:
            F_airres = 0


        # ground friction
        if self.on_ground:
            if self.vx > 0: 
                F_friction = -abs(self.F_normal) * ground_friction
            elif self.vx < 0:
                F_friction = abs(self.F_normal) * ground_friction
            else:
                F_friction = 0.0
            
        else:
            F_friction = 0.0

        self.F_friction = F_friction


        # ----- Y FORCE ------

        F_weight = self.mass * gravity

        if self.on_ground:
            self.y = ground - self.size/2
            self.vy = 0
            self.F_normal = -F_weight
        else:
            self.F_normal = 0.0

        # ---------- EQUATION -----------
        
        self.Fx_total = F_airres + F_friction
        self.Fy_total = F_weight + self.F_normal

        self.ax = self.Fx_total / self.mass
        self.ay = self.Fy_total / self.mass

        if abs(self.vx) > 0.2 :
            self.vx += self.ax * dt
        else:
            self.vx = 0.0

        self.vy += self.ay * dt

        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        box = pygame.Rect(0, 0, self.size, self.size)
        box.center = (self.x, self.y)
        pygame.draw.rect(screen, self.color, box)

        #gravity
        pygame.draw.line(screen,
                (150,200,150),
                (self.x,self.y),
                (self.x + self.Fx_total ,self.y),
                3
                )
        

        #normal
        pygame.draw.line(screen,
                (100,50,100),
                (self.x,self.y),
                (self.x, self.y  + self.Fy_total ),
                3
                )
    def x_collision(self,other):
        distance = abs(self.x - other.x)

        if distance < self.size/2 + other.size/2:
            return True
        else:
            return False
        
    def y_collision(self,other):
        distance = abs(self.y - other.y)

        if distance < self.size/2 + other.size/2:
            return True
        else:
            return False


# ----------- FUNCTION ------------
def draw_text(text, x, y):
    surface = font.render(text, True, (0, 0, 0))
    screen.blit(surface, (x, y))

    
running = True

boxes = []

box1 = box(10,100,300,100,50,0,(255,255,0))
box2 = box(10,400,300,100,0,0,(255,255,255))
boxes.append(box1)
boxes.append(box2)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((190,220,255))
    dt = clock.tick(60) / 1000  # sekitar 0.0167 detik

    for box in boxes:       #run box
        box.physic()
        pygame.draw.rect(screen, (75,255,75), (0,ground,800,600 - ground))
        

    
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            
            box_1 = boxes[i]
            box_2 = boxes[j]

            if box1.x_collision(box_2) == True and box1.y_collision(box_2) == True:
                box_1.color = (200,50,50)
                box_2.color = (200,50,50)

                if box1.x_collision(box_2) == True:
                    vx1 = box_1.vx
                    vx2 = box_2.vx

                    box_1.vx = vx2
                    box_2.vx = vx1

                if box1.y_collision(box_2) == True:
                    vy1 = box_1.vy
                    vy2 = box_2.vy

                    box_1.vy = vy2
                    box_2.vy = vy1



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
            "ax": box.ax,
            "ay": box.ay,
            #"  ":"",
            #"x_collision":box.x_collision,
            #"y_collision":box.y_collision
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

pygame.quit()