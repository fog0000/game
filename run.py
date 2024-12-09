import sys
from implements import Basic, Block, Paddle, Ball
import config

import pygame
from pygame.locals import QUIT, Rect, K_ESCAPE, K_SPACE


pygame.init()
pygame.key.set_repeat(3, 3)
surface = pygame.display.set_mode(config.display_dimension)

fps_clock = pygame.time.Clock()

paddle = Paddle()
ball1 = Ball()
BLOCKS = []
ITEMS = []
BALLS = [ball1]
life = config.life
start = False


def create_blocks():
    for i in range(config.num_blocks[0]):
        for j in range(config.num_blocks[1]):
            x = config.margin[0] + i * (config.block_size[0] + config.spacing[0])
            y = (
                config.margin[1]
                + config.scoreboard_height
                + j * (config.block_size[1] + config.spacing[1])
            )
            color_index = j % len(config.colors)
            color = config.colors[color_index]
            block = Block(color, (x, y))
            BLOCKS.append(block)


def tick():
    global life
    global BLOCKS
    global ITEMS
    global BALLS
    global paddle
    global ball1
    global start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:  # ESC 키가 눌렸을 때
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:  # space키가 눌려지만 start 변수가 True로 바뀌며 게임 시작
                for ball in BALLS:
                    ball.start = True
            paddle.move_paddle(event)

    for ball in BALLS:
        if not ball.start:                           # 공이 아직 시작하지 않은 경우 Paddle에 고정
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top
        else:                                        # 공이 발사된 경우 이동
            ball.move()

        ball.collide_block(BLOCKS, ITEMS)   # ITEMS 전달 추가
        ball.collide_paddle(paddle)
        ball.hit_wall()
        if ball.alive() == False:
            BALLS.remove(ball)

     # 아이템 처리
    for item in ITEMS[:]:                  
        item.move()                                          # 아이템 이동
        if item.rect.colliderect(paddle.rect):               # Paddle과 충돌
            if item.color == config.red_item_color:
                new_ball = Ball()
                new_ball.rect.centerx = paddle.rect.centerx
                new_ball.rect.bottom = paddle.rect.top
                new_ball.start = True
                BALLS.append(new_ball)
            ITEMS.remove(item)                               # Paddle에 닿으면 아이템 제거
        elif item.rect.top > config.display_dimension[1]:    # 화면 아래로 사라지면
            ITEMS.remove(item)


def main():
    global life
    global BLOCKS
    global ITEMS
    global BALLS
    global paddle
    global ball1
    global start
    my_font = pygame.font.SysFont(None, 50)
    mess_clear = my_font.render("Cleared!", True, config.colors[2])
    mess_over = my_font.render("Game Over!", True, config.colors[2])
    create_blocks()

    while True:
        tick()
        surface.fill((0, 0, 0))
        paddle.draw(surface)

        for block in BLOCKS:
            block.draw(surface)

         # 아이템 그리기
        for item in ITEMS:
            item.draw(surface)

        cur_score = config.num_blocks[0] * config.num_blocks[1] - len(BLOCKS)

        score_txt = my_font.render(f"Score : {cur_score * 10}", True, config.colors[2])
        life_font = my_font.render(f"Life: {life}", True, config.colors[0])

        surface.blit(score_txt, config.score_pos)
        surface.blit(life_font, config.life_pos)

        if len(BALLS) == 0:
            if life > 1:
                life -= 1
                ball1 = Ball()
                BALLS = [ball1]
                start = False
            else:
                surface.blit(mess_over, (200, 300))
        elif all(block.alive == False for block in BLOCKS):
            surface.blit(mess_clear, (200, 400))
        else:
            for ball in BALLS:
                if start == True:
                    ball.move()
                ball.draw(surface)
            for block in BLOCKS:
                block.draw(surface)

        pygame.display.update()
        fps_clock.tick(config.fps)


if __name__ == "__main__":
    main()
