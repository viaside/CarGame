import pygame
import sys
import random

WIDTH = 1200
HEIGHT = 900
FPS = 60
n=35# количество клеток квадратного поля игры
width  = 35#ширина клетки( и объекта)
height = 35#высота клетки ( и объекта)
margin = 0# промежуток между клетками

# Создаем игру, окно, машины
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
screen = pygame.Surface(((1200, 920)))
pygame.display.set_caption("ПДД")
clock = pygame.time.Clock()
map2 = pygame.image.load('res/3.png').convert_alpha()
koo = []# список нач. координат до перемещения
all_s = []# список всех объектов
all_stop = []
all_car = []# список машин


koor = []# список координат разницы между обьуктом и мышкой
grid = []# список занятых и свободных клеток

znaki_stop = []# спикок координат знаков
znaki_pryamo = []
znaki_park = []
znaki_peshehod = []

# сфетофоры
swet_right = [[140, 245], [420, 245], [805, 245], [1085, 245], [420, 525], [805, 525], [385, 420], [105, 420], [770, 420], [1050, 420]]
swet_left =  [[70, 210], [350, 210], [735, 210], [1015, 210], [70, 490], [350, 490], [735, 490], [1015, 490], [1120, 175], [1120, 455], [840, 455], [840, 175], [455, 175], [455, 455], [175, 455], [175, 175]]

# полные перекрестки
prv_left = [[455, 455], [455, 175], [840, 175], [840, 455]]
prv_up = [[385, 140], [770, 140], [385, 420], [770, 420]]
prv_right = [[350, 490], [350, 210], [735, 210], [735, 490]]
prv_down = [[420, 525], [420, 245], [805, 245], [805, 525]]

# неполные перекрестки
neprv_1 = [[175, 455], [1120, 455]]
neprv_1_2 = [[140, 245], [1085, 245]]
neprv_1_3 = [[105, 420], [1050, 420]]
neprv_1_4 = [[70, 490], [1015, 490]]
neprv_2 = [[175, 175], [1120,175]]
neprv_3_1 = [[385, 700]]
neprv_3_2 = [[420, 805]]
neprv_3_3 = [[455, 735]]
neprv_3_4 = [[735, 770]]
neprv_3_5 = [[770, 700]]
neprv_3_6 = [[805, 805]]
list = [175,210,455,490,735, 175,210,455,490,735 ]# спавн машин
random.shuffle(list)

global STOP_right
STOP_right = 0
global STOP_left
STOP_left = 0

for row in range(n):
    # заполняем пустую матрицу
    
    grid.append([])
    for column in range(n):
        grid[row].append(0)
class Sprite:
    # (нач.коорд-х,у,имя файла,нач.скорость-х,у)
    def __init__(self,xpos,ypos,filename):
        self.x = xpos
        self.y = ypos
        self.image=pygame.image.load(filename) # создаем рисунок-загрузка из файла
        self.rect = self.image.get_rect() # представляем его прямоугольником
        all_s.append(self)
        self.w = self.image.get_width()   #ширина
        self.h = self.image.get_height()  #высота
        self.action = False
        self.column = self.x // (width + margin)
        self.row = self.y // (height + margin)            
        grid[self.row][self.column] = 1
    def bum (self):# проверка попадания мышки на объект
        if self.x<mp[0]<self.x+self.w and self.y<mp[1]<self.y+self.h:
            a = mp[0]-self.x# разница кооздинаты мышки и объекта
            b = mp[1]-self.y  
            koor.append(a)# запись в список координат
            koor.append(b)
            self.action = True# разрешение на перемещение
            c = self.x# первоначальные кооздинаты объекта
            d = self.y
            koo.append(c)# запись первоначального положения выбранного объекта
            koo.append(d)
    def render (self):# отображение обьекта на игровом поле(экране)
        screen.blit(self.image,(self.x,self.y))
       
    def mouv(self):# движение объекта с мышкой     
        # Получить текущее положение мыши. Это возвращает позицию
        # в виде списка двух чисел.
        pos = pygame.mouse.get_pos()
        
        # Теперь  игрок имеет координаты мышки с учетом разницы координат           
        self.x = pos[0]-koor[0]
        self.y = pos[1]-koor[1]
        # условие границ поля
        
        if self.x<-10 :
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.x+width>((margin+width)*n+10+margin):
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.y<-10:
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
        if self.y+height>((margin+height)*n+10+margin) :
            self.x = koo[0]
            self.y = koo[1]
            self.action = False
           
    def mesto(self):# запись положения объектов в список грид             
        self.column = self.x // (width + margin)
        self.row = self.y // (height + margin)            
        grid[self.row][self.column] = 1
class Stop(Sprite):    
    def funtion (self):# функция движения точно в клетку
        mp = pygame.mouse.get_pos()# получ коорд мышки        
        self.x = (mp[0]// (width + margin))*(width + margin)+margin# коорд. клетки где находится мышь
        self.y = (mp[1] // (height + margin))*(height + margin)+margin
        self.column = self.x // (width + margin)# координ. в списке грид
        self.row = self.y // (height + margin)
        grid[ koo[1] // (height + margin)][ koo[0]// (width + margin)] =0# старой клетке = 0
        if  grid[self.row][self.column] ==1 : # если клетка куда переместили занята
            self.x = koo[0]# откат на обратные координаты
            self.y = koo[1]
            self.znak = self.x, self.y

        cxz = self.x, self.y
        znaki_stop.append(cxz)
class Pryamo(Sprite):
    def funtion (self):# функция движения точно в клетку
        mp = pygame.mouse.get_pos()# получ коорд мышки        
        self.x = (mp[0]// (width + margin))*(width + margin)+margin# коорд. клетки где находится мышь
        self.y = (mp[1] // (height + margin))*(height + margin)+margin
        self.column = self.x // (width + margin)# координ. в списке грид
        self.row = self.y // (height + margin)
        grid[ koo[1] // (height + margin)][ koo[0]// (width + margin)] =0# старой клетке = 0
        if  grid[self.row][self.column] ==1 : # если клетка куда переместили занята
            self.x = koo[0]# откат на обратные координаты
            self.y = koo[1]
            self.znak = self.x, self.y

        cxz = self.x, self.y
        znaki_pryamo.append(cxz)
class Parking(Sprite):
    def funtion (self):# функция движения точно в клетку
        mp = pygame.mouse.get_pos()# получ коорд мышки        
        self.x = (mp[0]// (width + margin))*(width + margin)+margin# коорд. клетки где находится мышь
        self.y = (mp[1] // (height + margin))*(height + margin)+margin
        self.column = self.x // (width + margin)# координ. в списке грид
        self.row = self.y // (height + margin)
        grid[ koo[1] // (height + margin)][ koo[0]// (width + margin)] =0# старой клетке = 0
        if  grid[self.row][self.column] ==1 : # если клетка куда переместили занята
            self.x = koo[0]# откат на обратные координаты
            self.y = koo[1]
            self.znak = self.x, self.y

        cxz = self.x, self.y
        znaki_park.append(cxz)
class Peshehod(Sprite):
    def funtion (self):# функция движения точно в клетку
        mp = pygame.mouse.get_pos()# получ коорд мышки        
        self.x = (mp[0]// (width + margin))*(width + margin)+margin# коорд. клетки где находится мышь
        self.y = (mp[1] // (height + margin))*(height + margin)+margin
        self.column = self.x // (width + margin)# координ. в списке грид
        self.row = self.y // (height + margin)
        grid[ koo[1] // (height + margin)][ koo[0]// (width + margin)] =0# старой клетке = 0
        if  grid[self.row][self.column] ==1 : # если клетка куда переместили занята
            self.x = koo[0]# откат на обратные координаты
            self.y = koo[1]
            self.znak = self.x, self.y

        cxz = self.x, self.y
        znaki_peshehod.append(cxz)
hero1 = Stop(0, 0,('res/4.png'))
hero2 = Stop(70, 0 ,('res/4.png'))
hero3 = Stop(105, 0 ,('res/4.png'))
hero4 = Stop(35, 0 ,('res/4.png'))
hero5 = Pryamo(0, 35,('res/5.png'))
hero6 = Pryamo(70, 35,('res/5.png'))
hero7 = Pryamo(105, 35,('res/5.png'))
hero8 = Pryamo(35, 35,('res/5.png'))
hero9 =  Parking(0, 70,('res/6.png'))
hero10 = Parking(70, 70,('res/6.png'))
hero11 = Parking(105, 70,('res/6.png'))
hero12 = Parking(35, 70,('res/6.png'))
hero13 = Peshehod(0, 105,('res/7_1.png'))
hero14 = Peshehod(70, 105,('res/7_1.png'))
hero15 = Peshehod(105, 105,('res/7_1.png'))
hero16 = Peshehod(35, 105,('res/7_1.png'))
hero17 = Peshehod(0, 140,('res/7_2.png'))
hero18 = Peshehod(70, 140,('res/7_2.png'))
hero19 = Peshehod(105, 140,('res/7_2.png'))
hero20 = Peshehod(35, 140,('res/7_2.png'))



class Cars:
    def __init__(self,x,y,filename):
        self.position = pygame.math.Vector2(window.get_rect().center)  
        self.direction = pygame.math.Vector2(5, 0)
        self.car = pygame.image.load(filename)
        all_car.append(self)
        self.position.x = 595
        x = list.pop()
        self.position.y = x
        if x == 175 or x == 455 or x == 735:
            self.direction.rotate_ip(-180)
    def borders(self):
        # границы
        if self.position.x >= WIDTH:
            self.position.x = 0
        elif self.position.x <= 0:
            self.position.x = WIDTH
        elif self.position.y >= HEIGHT:
            self.position.y = 0
        elif self.position.y <= 0:
            self.position.y = HEIGHT

    def turn(self):
        self.plus90 = True
        self.minus90 = True
        x = random.randint(0,2)
        y = random.randint(0,1)
        # полные перекрестки
        if self.position in prv_left:
            if x == 1:
                self.plus90 = False
                self.position.x -= 35
            if x == 2:   
                self.minus90 = False 
                self.position.x -= 70
        if self.position in prv_up:
            if x == 1:
                self.plus90 = False
                self.position.y +=35
            if x == 2: 
                self.minus90 = False
                self.position.y +=70
        if self.position in prv_right:
            if x == 1:
                self.plus90 = False
                self.position.x +=35
            if x == 2: 
                self.minus90 = False
                self.position.x += 70
        if self.position in prv_down:
            if x == 1: 
                self.plus90 = False
                self.position.y -= 35
            if x == 2: 
                self.minus90 = False
                self.position.y -=70

        # неполные перекрестки
        if self.position in neprv_1:
            if y == 1:
                self.plus90 = False
                self.position.x -= 35
        if self.position in neprv_1_2:
            if y == 0:
                self.minus90 = False
                self.position.y -=70
            if y == 1:
                self.plus90 = False
                self.position.y -= 35                
        if self.position in neprv_2:
            if y == 1:
                self.minus90 = False
                self.position.x -= 70
        if self.position in neprv_1_3:
            if y == 0:
                self.plus90 = False
                self.position.y += 35
            if y == 1:
                self.minus90 = False
                self.position.y += 70
        if self.position in neprv_1_4:
            if y == 1:
                self.minus90 = False
                self.position.x += 70
        if self.position in neprv_3_1:
            if y == 1:
                self.minus90 = False
                self.position.y += 70
        if self.position in neprv_3_2:
            if y == 1:
                self.plus90 = False
                self.position.y -= 35
        if self.position in neprv_3_3:
            if y == 0: 
                self.minus90 = False
                self.position.x -= 70
            if y == 1:
                self.plus90 = False
                self.position.x -= 35
        if self.position in neprv_3_4:
            if y == 0:
                self.plus90 = False
                self.position.x += 35
            if y == 1:
                self.minus90 = False
                self.position.x += 70
        if self.position in neprv_3_5:
            if y == 1:
                self.plus90 = False
                self.position.y += 35
        if self.position in neprv_3_6:
            if y == 1:
                self.minus90 = False
                self.position.y -= 70

        if self.plus90 == False:
            self.direction.rotate_ip(90)
            self.plus90 = True
        if self.minus90 == False:
            self.direction.rotate_ip(-90)
            self.minus90 = True
        if self.plus90 and self.minus90 == True:
            self.position += self.direction   


    def regulation(self):
        if self.position in swet_left:
            if STOP_right == False:
                None
            if STOP_right == True:
                self.position -= self.direction
        if self.position in swet_right:
            if STOP_left == False:
                None
            if STOP_left == True:
                self.position -= self.direction

    def znaki(self):
        if self.position in znaki_stop:
            print('стоп')
        if self.position in znaki_peshehod:
            for _ in range(2):
                self.position -= self.direction
        if self.position in znaki_park:
            print('парковка')
        if self.position in znaki_pryamo:
            print('прямо')
    def rendering(self):
        angle = self.direction.angle_to((1, 0))
        self.rotated_car = pygame.transform.rotate(self.car, angle)
        screen.blit(self.rotated_car, self.rotated_car.get_rect( topleft = (round(self.position.x), round(self.position.y))))
        self.turn()
        self.borders()
        self.regulation()
        self.znaki()

car1 = Cars( 0, 0, ("res/1.png"))
car2 = Cars( 0, 0, ("res/2.png"))   
car3 = Cars( 0, 0, ("res/1.png"))
car4 = Cars( 0, 0, ("res/2.png"))
car5 = Cars( 0, 0, ("res/2.png"))
car6 = Cars( 0, 0, ("res/1.png"))
car7 = Cars( 0, 0, ("res/2.png"))   
car8 = Cars( 0, 0, ("res/1.png"))
car9 = Cars( 0, 0, ("res/2.png"))
car10 = Cars( 0, 0, ("res/2.png"))


class Regulationr(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.spritesr = []
        self.spritesr.append(pygame.image.load('1.png'))
        self.spritesr.append(pygame.image.load('3.png'))
        self.spritesr.append(pygame.image.load('2.png'))
        self.current_sprite = 2
        self.image = self.spritesr[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self,speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.spritesr):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.spritesr[int(self.current_sprite)]    
        self.regulation()
    def regulation(self):
        global STOP_right 
        if self.current_sprite >= 0 and self.current_sprite < 1:
            STOP_right = False
        if self.current_sprite >= 1 and self.current_sprite < 2:
            STOP_right = False
        if self.current_sprite >= 2 and self.current_sprite < 3:
            STOP_right = True
class Regulationl(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.spritesl = []
        self.spritesl.append(pygame.image.load('1.png'))
        self.spritesl.append(pygame.image.load('2.png'))
        self.spritesl.append(pygame.image.load('3.png'))
        self.current_sprite = 0
        self.image = self.spritesl[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self,speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.spritesl):
            self.current_sprite = 0
            self.attack_animation = False
        self.image = self.spritesl[int(self.current_sprite)]    
        self.regulation()
    def regulation(self):
        global STOP_left 
        if self.current_sprite >= 0 and self.current_sprite < 1:
            STOP_left = False
        if self.current_sprite >= 1 and self.current_sprite < 2:
            STOP_left = True
        if self.current_sprite >= 2 and self.current_sprite < 3:
            STOP_left = False
moving_sprites_right = pygame.sprite.Group()
pl1 = Regulationr(70, 525)
pl2 = Regulationr(350, 525)
pl3 = Regulationr(735, 525)
pl4 = Regulationr(1015, 525)
pl5 = Regulationr(1015, 245)
pl6 = Regulationr(735, 245)
pl7 = Regulationr(350, 245)
pl8 = Regulationr(70, 245)
pl9 = Regulationr(175, 420)
pl10= Regulationr(455, 420)
pl11= Regulationr(840, 420)
pl12= Regulationr(1120, 420)
pl13= Regulationr(1120, 140)
pl14= Regulationr(840, 140)
pl15= Regulationr(455, 140)
pl16= Regulationr(175, 140)
moving_sprites_right.add(pl1, pl2, pl3, pl4, pl5, pl6, pl7, pl8, pl9, pl10, pl11, pl12, pl13, pl14, pl15, pl16)

moving_sprites_left = pygame.sprite.Group()
pl1 = Regulationl(175, 525)
pl2 = Regulationl(70, 420)
pl3 = Regulationl(350, 420)
pl4 = Regulationl(455, 525)
pl5 = Regulationl(735, 420)
pl6 = Regulationl(840, 525)
pl7 = Regulationl(1015, 420)
pl8 = Regulationl(1120, 525)
pl9 = Regulationl(1015, 140)
pl10= Regulationl(1120, 245)
pl11= Regulationl(735, 140)
pl12= Regulationl(840, 245)
pl13= Regulationl(350, 140)
pl14= Regulationl(455, 245)
pl15= Regulationl(175, 245)
pl16= Regulationl(70,140)
moving_sprites_left.add(pl1, pl2, pl3, pl4, pl5, pl6, pl7, pl8, pl9, pl10, pl11, pl12, pl13, pl14, pl15, pl16) 

# Цикл игры
In_game = True
while In_game:
    # Ввод  процесса (события)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            In_game = False

    if event.type == pygame.MOUSEBUTTONDOWN and event.button ==1:                                        
                mp = pygame.mouse.get_pos()
                for i in all_s :# захват объекта
                    i.bum()
        
    if event.type == pygame.MOUSEBUTTONUP and event.button ==1: # если отпущена лкм         
                for i in all_s:
                    if i.action ==True:
                        i.funtion()# перемещение объекта точно в клетку

                for i in all_s :
                    i.action = False# движение запрещено
                
                for i in all_s:# запись положения объекта в список grid
                    i.mesto() # запись положения объектов в список грид
                koor = []# список координат разницы между обьуктом и мышкой
                koo = []# обнуление списка захвачен. объекта
    for i in all_s:
            if i.action == True:
                i.mouv()# перемещение объекта мышкой    

    for i in all_s:# отображаем все объекты
        i.render()

    for s in all_s:
        s.render
    for e in all_car:
        e.rendering()
    # После отрисовки всего, обновляем экран
    clock.tick(FPS)
    window.blit(screen, (0,0)) 
    screen.blit(map2, (0, 0))
    moving_sprites_right.draw(screen)
    moving_sprites_right.update(0.005)
    moving_sprites_left.draw(screen)
    moving_sprites_left.update(0.005)
    pygame.display.flip()
    pygame
pygame.quit()