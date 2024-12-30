import pygame
import numpy as np
import json
import os
import pygame_gui

from settings import *
from life_game import game_of_life_step, check_target
from map_util import load_level

def game_screen():
    """游戏主屏幕"""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Screen")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    # 加载关卡
    level_data = load_level("assets/maps/level1.json")
    grid_size = level_data["grid_size"]
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    target_grid = [[2 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # 将关卡数据对齐到 GRID_SIZE 的中心
    offset = (GRID_SIZE - grid_size) // 2
    for y in range(grid_size):
        for x in range(grid_size):
            grid[y + offset][x + offset] = level_data["cells"][y][x]
            target_grid[y + offset][x + offset] = level_data["target"][y][x]

    CELL_SIZE = 10
    grid_width = GRID_SIZE * CELL_SIZE
    grid_height = GRID_SIZE * CELL_SIZE
    start_x = SCREEN_WIDTH - grid_width
    start_y = (SCREEN_HEIGHT - grid_height) // 2

    # UI 按钮
    toggle_target_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 60), (150, 40)),
        text="Toggle Target",
        manager=manager
    )
    run_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 120), (150, 40)),
        text="Run",
        manager=manager
    )
    exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((0, 180), (150, 40)),
        text="Exit",
        manager=manager
    )

    running = True
    show_target = True
    auto_run = False

    drawing = False
    
    FPS_run = 20
    FPS_draw = 120


    while running:
        fps = FPS_run if auto_run else FPS_draw

        time_delta = clock.tick(fps) / 1000.0
        screen.fill(BG_COLOR)

        # 绘制网格
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(start_x + x * CELL_SIZE, start_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = (0, 255, 0) if grid[y][x] == 1 else (40, 40, 40)
                pygame.draw.rect(screen, color, rect)

                if show_target and target_grid[y][x] != 2:
                    target_color = (0, 0, 255) if target_grid[y][x] == 1 else (255, 0, 0)
                    pygame.draw.circle(screen, target_color, rect.center, CELL_SIZE // 4)

                pygame.draw.rect(screen, (30, 30, 30), rect, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "menu"
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == toggle_target_button:
                        show_target = not show_target
                    elif event.ui_element == run_button:
                        auto_run = not auto_run
                        run_button.set_text("Stop" if auto_run else "Run")
                    elif event.ui_element == exit_button:
                        running = False
                        return "menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_x <= mouse_pos[0] < start_x + grid_width and start_y <= mouse_pos[1] < start_y + grid_height:
                    x = (mouse_pos[0] - start_x) // CELL_SIZE
                    y = (mouse_pos[1] - start_y) // CELL_SIZE
                    grid[y][x] = 1 - grid[y][x]  # 切换细胞状态
                    drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

            if event.type == pygame.MOUSEMOTION and drawing:
                mouse_pos = pygame.mouse.get_pos()
                if start_x <= mouse_pos[0] < start_x + grid_width and start_y <= mouse_pos[1] < start_y + grid_height:
                    x = (mouse_pos[0] - start_x) // CELL_SIZE
                    y = (mouse_pos[1] - start_y) // CELL_SIZE
                    grid[y][x] = 1  # 确保拖动绘制时设置为活细胞

            manager.process_events(event)

        if auto_run:
            grid = game_of_life_step(grid, True)

        # if check_target(grid, target_grid):
        #     print("Level Complete!")
        #     return "menu"

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    return "exit"