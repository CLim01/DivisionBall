import os
import pygame
######################################################################################################

# 기본 초기화
pygame.init() 

# 화면 크기
screen_width = 640 # 가로
screen_height = 480 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption('Monster Ball')

# FPS
clock = pygame.time.Clock()
######################################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트)
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path,'images')

# 배경
sky = pygame.image.load(os.path.join(image_path,'sky.png'))

ground = pygame.image.load(os.path.join(image_path,'ground.png'))
ground_size = ground.get_rect().size
ground_height = ground_size[1]

# 케릭터 이미지

character = pygame.image.load(os.path.join(image_path,'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - ground_height

# 이동할 좌표

# 이동속도

# 적

# 폰트 정의

# 촐 플레이 타임

# 시작 시간

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60)
    # print('fps :'+str(clock.get_fps()))

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 3. 게임 케릭터 위치 정의

    # 가로 경계

    # 세로 경계

    # 4. 출돌 처리

    # 충동 처리

    # 충돌 체크

    # 5. 화면에 그리기

    screen.blit(sky, (0,0))

    screen.blit(ground, (0,screen_height - ground_height))

    screen.blit(character, (character_x_pos,character_y_pos))

    # 타이머

    # 시간, True, 글자 색상 

    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()
