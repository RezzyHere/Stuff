import pygame
import random
import sys

# Inisialisasi Pygame
pygame.init()

# template warna
White = (255, 255, 255)
Black = (0, 0, 0)

#Variabel variabel
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
BIRD_JUMP = -10
BULLET_SPEED = 10
PIPE_SPEED = 5
PIPE_GAP = 200
ENEMY_WIDTH, ENEMY_HEIGHT = 80, 80  # Musuh lebih besar
BIRD_WIDTH, BIRD_HEIGHT = 70, 70    # Burung lebih besar

# Setup window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Final Project")
clock = pygame.time.Clock()

# Load semua gambar
bird_img = pygame.image.load("hero2.png").convert_alpha()
enemy_img = pygame.image.load("cyborg2.png").convert_alpha()
bullet_img = pygame.image.load("bullet.png").convert_alpha()
game_over_img = pygame.image.load("game-over_1.png").convert_alpha()

# Scale semua gambar
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))  
enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))  
bullet_img = pygame.transform.scale(bullet_img, (30, 15))  # Peluru disesuaikan
game_over_img = pygame.transform.scale(game_over_img, (WIDTH, HEIGHT))  

# Kelas Burung
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect(center=(100, HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Batas burug
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def jump(self):
        self.velocity = BIRD_JUMP

# Kelas Pipa
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, height, inverted=False):
        super().__init__()
        self.image = pygame.Surface((50, height))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.inverted = inverted
        self.passed = False  # Untuk menandai apakah pipa sudah dilewati

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

# Kelas Musuh
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.x -= PIPE_SPEED
        if self.rect.right < 0:
            self.kill()

# Kelas Peluru
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.x += BULLET_SPEED
        if self.rect.left > WIDTH:
            self.kill()

#  menampilkan layar game over
def game_over(score):
    screen.blit(game_over_img, (0, 0))  # Gambar game over memenuhi layar
    font = pygame.font.SysFont("Arial", 50)
    score_text = font.render(f"Score: {score}", True, Black)
    screen.blit(score_text, (WIDTH // 2 - 100, HEIGHT // 2 + 3))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

# Main game loop
def main():
    bird = Bird()
    all_sprites = pygame.sprite.Group(bird)
    pipes = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    pipe_timer = 0
    score = 0
    running = True
    while running:
        clock.tick(FPS)
        pipe_timer += 1

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    bird.jump()
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(bird.rect.centerx, bird.rect.centery)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

        # generate pipa dan musuh
        if pipe_timer % 100 == 0:
            pipe_height = random.randint(100, 400)
            pipe_top = Pipe(WIDTH, 0, pipe_height, inverted=True)
            pipe_bottom = Pipe(WIDTH, pipe_height + PIPE_GAP, HEIGHT - pipe_height - PIPE_GAP)
            enemy = Enemy(WIDTH, pipe_height + PIPE_GAP // 2 - ENEMY_HEIGHT // 2)
            all_sprites.add(pipe_top, pipe_bottom, enemy)
            pipes.add(pipe_top, pipe_bottom)
            enemies.add(enemy)


        all_sprites.update()

        # tabrakan burung dengan pipa atau musuh
        if pygame.sprite.spritecollide(bird, pipes, False) or pygame.sprite.spritecollide(bird, enemies, False):
            game_over(score)

        # peluru
        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollide(bullet, enemies, True)
            if enemy_hit:
                bullet.kill()

        # cek burung melewati pipa
        for pipe in pipes:
            if not pipe.passed and pipe.rect.right < bird.rect.left:
                pipe.passed = True
                score += 1

        # render
        screen.fill(White)
        all_sprites.draw(screen)

        # tampilkan skor
        font = pygame.font.SysFont("Arial", 36)
        score_text = font.render(f"Score: {score}", True, Black)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()