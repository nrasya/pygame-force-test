import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()


class box:
    def __init__(self,x,y,size,color,vx,vy):
        self.x = x
        self.y = y
        self.width, self.height = size
        self.vx = vx
        self.vy = vy
        self.color = color

    def process(self):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self):
        box = pygame.Rect(0,0,self.width,self.height)
        box.center = (self.x, self.y)
        pygame.draw.rect(screen,self.color, box)

    def border_collision(self):
        if self.x - self.width/2 <= 0 or self.x + self.width/2 >= 800: 
            self.vx = -self.vx
        if self.y + self.height/2 >= 600 or self.y - self.height/2 <= 0:
            self.vy = -self.vy

    def x_collision(self, other):
        return not (
            self.x + self.width/2 < other.x - other.width/2 or
            self.x - self.width/2 > other.x + other.width/2
        )
    
    def y_collision(self, other):
        return not (
            self.y + self.height/2 < other.y - other.height/2 or
            self.y - self.height/2 > other.y + other.height/2
        )


boxes = [
    box(100,300,(100,100),(255,255,0),2000,2000),
    box(400,300,(200,100),(0,0,255),0,0)
]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255,255,255))
    dt = clock.tick(60) / 1000  # sekitar 0.0167 detik


    for box in boxes:
        box.process()
        box.draw()
        box.border_collision()

    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            
            box1 = boxes[i]
            box2 = boxes[j]

        if box1.x_collision(box2) and box1.y_collision(box2):

            distance_x = abs(box1.x - box2.x)
            distance_y = abs(box1.y - box2.y)

            overlap_x = box1.width/2 + box2.width/2 - distance_x
            overlap_y = box1.height/2 + box2.height/2 - distance_y

            if overlap_x < overlap_y:
                if box1.vx > 0:
                    box1.x -= overlap_x + overlap_x/100
                else:
                    box1.x += overlap_x + overlap_x/100
                box1.vx = -box1.vx
            else:
                if box1.vy > 0:
                    box1.y -= overlap_y + overlap_y/100
                else:
                    box1.y += overlap_y + overlap_y/100
                box1.vy = -box1.vy
            print(overlap_x)
            print(overlap_y)



    pygame.display.flip()

pygame.QUIT()