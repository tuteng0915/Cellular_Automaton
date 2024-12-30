# menu.py
import pygame
from ui_element import Button

def menu_screen():
    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption("Main Menu")

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    clock = pygame.time.Clock()

    # 定义按钮
    start_button = Button((360, 300), "Start Game", (0, 255, 0))
    editor_button = Button((360, 400), "Map Editor", (0, 255, 0))
    settings_button = Button((360, 500), "Settings", (0, 255, 0))
    exit_button = Button((360, 600), "Exit", (0, 255, 0))

    running = True
    while running:
        screen.fill((10, 24, 15))

        # 绘制按钮
        start_button.draw(screen)
        editor_button.draw(screen)
        settings_button.draw(screen)
        exit_button.draw(screen)

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked():
                    return "game"  # 进入游戏关卡选择
                if editor_button.is_clicked():
                    return "editor"  # 进入地图编辑器
                if settings_button.is_clicked():
                    return "settings"  # 进入设置
                if exit_button.is_clicked():
                    return "exit"  # 退出程序

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
