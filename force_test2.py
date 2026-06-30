import pygame
import math


# --------- INITIALIZATION ---------
pygame.init()
font = pygame.font.SysFont(None, 24)
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
running = True

# ------------ CONSTANT ----------
ground = 500
ground_friction = 2
gravity = 9.8

# ------------ CLASS ------------

class box:
    def __init__(self,mass,x,y,size,vx,vy,color):
        self.mass = mass
        self.x = x
        self.y = y
        self.size = size
        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.color = color
        self.default_color = color


        self.on_ground = False
        self.prev_on_ground = False

        self.Fx_total = 0
        self.Fy_total = 0


    def physic(self):
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
        box = pygame.Rect(0, 0, self.size, self.size)
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



        if distance < self.size/2 + other.size/2:
            return True
        else:
            return False
        
    def y_collision(self,other):
        distance_y = abs(self.y - other.y)
        distance_x = abs(self.x - other.x)

        if distance_y < self.size/2 + other.size/2:
            return True
        else:
            return False

# ----------- FUNCTION ------------
def draw_text(text, x, y):
    surface = font.render(text, True, (0, 0, 0))
    screen.blit(surface, (x, y))



x_col = False
y_col = False
# ------------ OBJECT -----------
boxes = [
    box(10,100,100,100,50,0,(255,255,0)),
    box(10,400,300,100,0,0,(255,255,255))
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
        pygame.draw.rect(screen, (75,255,75), (0,ground,800,600 - ground))

        ground_relative = ground - box.size/2

        #Ground Collisison
        if box.y > ground_relative:
            box.on_ground = True
            box.vy = 0
        else:
            box.on_ground = False

        #Ground Logic
        if box.on_ground != box.prev_on_ground:

            if box.on_ground:
                box.add_force(gravity * box.mass, 3.14 * 3/2)

        box.prev_on_ground = box.on_ground

        #
            

    
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            
            box_1 = boxes[i]
            box_2 = boxes[j]

            x_distance = abs(box_1.x - box_2.x)
            y_distance = abs(box_1.y - box_2.y)

            x_collideDistance = box_1.size/2 - box_2.size/2
            y_collideDistance = box_1.size/2 - box_2.size/2

            x_overlap = x_distance - x_collideDistance
            y_overlap = y_distance - y_collideDistance

            if x_distance < x_collideDistance and y_distance < y_collideDistance: #overlapping on both axis
                if x_overlap < y_overlap:
                    
                    #correction
                    correction = x_overlap/2
                    if box_1.x < box_2.x:       
                        box_1.x -= correction
                        box_2.x += correction
                    else:
                        box_1.x += correction
                        box_2.x -= correction

                else:
                    correction = y_overlap/2
                    if box_1.y < box_2.y:       
                        box_1.y -= correction
                        box_2.y += correction
                    else:
                        box_1.y += correction
                        box_2.y -= correction






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