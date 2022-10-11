# pygame は、ビデオゲームを製作するために設計されたクロスプラットフォームのPythonモジュール集。
import pygame
import random
import math

# 初期化
pygame.init()

# 画面を作成する。画面の縦横の大きさを設定。
screen = pygame.display.set_mode((800, 600))
# 画面の名前
pygame.display.set_caption('Invaders Game')

# プレイヤーの画像を表示。
playerImg = pygame.image.load('player.png')
# 画像を表示させる座標を設定。
playerX, playerY = 370, 480
playerX_change = 0

# 敵の画像を表示。
enemyImg = pygame.image.load('enemy.png')
# 敵の画像の初期位置をランダムにする。
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
# 敵が移動する座標幅について設定する。
enemyX_change, enemyY_change = 4, 40

# 銃弾の画像を表示。
bulletImg = pygame.image.load('bullet.png')
# 銃弾の画像を表示させる初期座標を設定。
bulletX, bulletY = 0, 480
bulletX_change, bulletY_change = 0, 3
# 銃弾を打った状態を「fire」、銃弾を打つ準備をしている状態を「ready」とする。
# 初期は銃弾を打つ準備をしている状態「ready」とする。
bullet_state = 'ready'

# スコア
score_value = 0

# プレイヤーの画像の座標に関する関数。
def player(x, y):
    screen.blit(playerImg, (x, y))

# 敵の画像の座標に関する関数。
def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# 銃弾の画像の座標に関する関数。
def fire_bullet(x, y):
    global bullet_state
    # 銃弾を打った状態「fire」とする。
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

#　敵と銃弾が当たったかを判定する関数。
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # 敵と銃弾の距離。
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    # 敵と銃弾の距離が27未満の場合、銃弾が敵に当たったとする。
    if distance < 27:
        return True
    else:
        return False

# ずっと表示し続けるために。
running = True
while running:
    # 背景色の設定。画面を黒で上書きする(リセット)。
    screen.fill((0, 0, 0))

    # イベント(操作)情報を取り続ける。
    for event in pygame.event.get():
        # 画面閉じるを押した場合。
        if event.type == pygame.QUIT:
            # 画面表示を止める。
            running = False

        # 何かキーを押した場合。
        if event.type == pygame.KEYDOWN:
            # 左矢印キーを押した場合。
            if event.key == pygame.K_LEFT:
                # プレーヤーの画像を右に-1.5移動する。
                playerX_change = -1.5
            # 右矢印キーを押した場合。
            if event.key == pygame.K_RIGHT:
                # プレーヤーの画像を右に1.5移動する。
                playerX_change = 1.5
            # スペースキーを押した場合。
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # 手がキーから離れた場合。
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # x座標の変化量を0にリセットする。
                playerX_change = 0
                
    # プレーヤーの画像の座標を更新する。
    playerX += playerX_change
    # プレーヤーが左端まできた場合。
    if playerX <= 0:
        # 左端で止まる。
        playerX = 0
    # プレーヤーが右端まできた場合。
    elif playerX >= 736:
        # 右端で止まる。
        playerX = 736

    # 敵画像が下まで来た場合。
    if enemyY > 440:
        # ゲーム終了。
        break
    # 敵が移動する。
    enemyX += enemyX_change
    if enemyX <= 0: #左端に来たら
        # 右に移動方向を変換する。
        enemyX_change = 4
        enemyY += enemyY_change
    elif enemyX >=736: #右端に来たら
        # 左に移動方向を変換する。
        enemyX_change = -4
        enemyY += enemyY_change
    
    # 敵と銃弾が当たったかの関数を呼び出す。
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    # 銃弾が敵に当たった場合。
    if collision:
        # 敵を初期位置に戻す。
        bulletY = 480
        # 銃弾を準備状態にする。
        bullet_state = 'ready'
        # スコアを更新する。
        score_value += 1
        # 敵の位置をランダムで決定する。
        enemyX = random.randint(0, 736)
        enemyY = random.randint(50, 150)

    # 銃弾の動きについての処理。
    # 銃弾が敵に衝突せず、画面上端に行った場合。
    if bulletY <=0:
        # 銃弾を初期位置に戻す。
        bulletY = 480
        # 銃弾を準備状態にする。
        bullet_state = 'ready'

    # 銃弾を発射した場合。
    if bullet_state is 'fire':
        #　銃弾の画像を表示させる。
        fire_bullet(bulletX, bulletY)
        # 銃弾を移動させる。
        bulletY -= bulletY_change  

    # スコア
    # フォントの作成。Noneはデフォルトのfreesansbold.ttf
    font = pygame.font.SysFont(None, 32)
    # テキストを描画したSurfaceの作成
    score = font.render(f"Score : {str(score_value)}", True, (255,255,255))
    # スコアを表示する座標の設定。
    screen.blit(score, (20,50))

    # プレーヤーを指定した座標に表示させる。
    player(playerX, playerY)
    # 敵を指定した座標に表示させる。
    enemy(enemyX, enemyY)

    # スクリーン上の変更点を更新する。
    pygame.display.update()