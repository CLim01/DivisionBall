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

# 케릭터 이동 방향
character_to_x = 0

# 이동속도
character_speed = 1

# 무기
weapon = pygame.image.load(os.path.join(image_path,'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한 번에 여러발  발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 2

# 공 만들기 ( 4개의 크기 따로 처리 )
ball_images = [
    pygame.image.load(os.path.join(image_path,'ball.png')),
    pygame.image.load(os.path.join(image_path,'ball2.png')),
    pygame.image.load(os.path.join(image_path,'ball3.png')),
    pygame.image.load(os.path.join(image_path,'ball4.png'))
]

# 공의 크기에 따라 다른 최초 속도
ball_speed_y = [-18,-15,-12,-9]

# 공들
balls = []

balls.append({
    'pos_x' : 50,
    'pos_y' : 50,
    'img_idx' : 0,
    'to_x' : 3,
    'to_y' : -6,
    'init_spd_y' : ball_speed_y[0]
})

# 사라질 무기와 공
weapon_to_remove = -1
ball_to_remove = -1

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(30)
    # print('fps :'+str(clock.get_fps()))

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = (character_x_pos + character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 케릭터 위치 정의
    character_x_pos += character_to_x * dt

    # 가로 경계
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 튕겨 나옴
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val['to_x'] = ball_val['to_x'] * -1\

        # 세로 위치
        if ball_pos_y >= screen_height - ground_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        else:
            ball_val['to_y'] += 0.5

        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']


    # 4. 출돌 처리

    # 케릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 케릭터 충돌
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기 충돌
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx
                
                if ball_img_idx != 3:
                    # 현재 공 크기 정보
                    ball_width = ball_size[0]
                    ball_height = ball_size[1]
                    
                    #나누어진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]


                    balls.append({
                        'pos_x' : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y' : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        'img_idx' : ball_img_idx + 1,
                        'to_x' : -3,
                        'to_y' : -6,
                        'init_spd_y' : ball_speed_y[ball_img_idx + 1]
                        })

                    balls.append({
                        'pos_x' : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y' : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        'img_idx' : ball_img_idx + 1,
                        'to_x' : 3,
                        'to_y' : -6,
                        'init_spd_y' : ball_speed_y[ball_img_idx + 1]
                        })


                break

    # 충돌된 공과 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 5. 화면에 그리기

    screen.blit(sky, (0,0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))


    screen.blit(ground, (0,screen_height - ground_height))
    screen.blit(character, (character_x_pos,character_y_pos))


    # 타이머

    # 시간, True, 글자 색상 

    pygame.display.update() # 게임화면 다시 그리기

# pygame 종료
pygame.quit()
