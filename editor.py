import pygame
import pygame_gui
import json
import os
from life_game import game_of_life_step
from map_util import save_map, load_map, get_map_files, save_window, load_window

def map_editor():
    """地图编辑器"""
    pygame.init()
    pygame.display.set_caption("Map Editor")
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()

    icon = pygame.image.load("assets/icon.png")
    pygame.display.set_icon(icon)

    manager = pygame_gui.UIManager((960, 720))

    GRID_SIZE = 20
    CELL_SIZE = 25
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    target_grid = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    brush_type = 1  # 默认刷子类型
    brush_types = {
        1: "Add Cell",
        2: "Remove Cell",
        3: "Set Required",
        4: "Set Prohibited",
        5: "Clear Requirement"
    }

    # 创建按钮
    save_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (120, 40)),
                                               text="Save",
                                               manager=manager)
    load_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 120), (120, 40)),
                                               text="Load",
                                               manager=manager)
    exit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 190), (120, 40)),
                                               text="Exit",
                                               manager=manager)
    brush_prev_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 260), (50, 40)),
                                                     text="<",
                                                     manager=manager)
    brush_next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((120, 260), (50, 40)),
                                                     text=">",
                                                     manager=manager)

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((13, 27, 42))

        # 绘制网格
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE + 250, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 将网格右移
                color = (0, 255, 0) if grid[y][x] == 1 else (40, 40, 40)
                pygame.draw.rect(screen, color, rect)

                # 绘制目标状态
                if target_grid[y][x] != -1:
                    target_color = (0, 0, 255) if target_grid[y][x] == 1 else (255, 0, 0)
                    pygame.draw.circle(screen, target_color, rect.center, CELL_SIZE // 4)

                pygame.draw.rect(screen, (30, 30, 30), rect, 1)

        # 显示当前刷子类型
        font = pygame.font.Font(None, 24)
        brush_text = font.render(f"Brush Type: {brush_types[brush_type]}", True, (255, 255, 255))
        screen.blit(brush_text, (50, 310))

        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit"

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == save_button:
                        save_window(manager, grid, target_grid)
                    elif event.ui_element == load_button:
                        load_window(manager, grid, target_grid)
                    elif event.ui_element == exit_button:
                        return "menu"
                    elif event.ui_element == brush_prev_button:
                        brush_type = max(1, brush_type - 1)
                    elif event.ui_element == brush_next_button:
                        brush_type = min(len(brush_types), brush_type + 1)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 250 <= mouse_pos[0] < 250 + GRID_SIZE * CELL_SIZE and 0 <= mouse_pos[1] < GRID_SIZE * CELL_SIZE:
                    x = (mouse_pos[0] - 250) // CELL_SIZE
                    y = mouse_pos[1] // CELL_SIZE
                    if brush_type == 1:
                        grid[y][x] = 1
                    elif brush_type == 2:
                        grid[y][x] = 0
                    elif brush_type == 3:
                        target_grid[y][x] = 1
                    elif brush_type == 4:
                        target_grid[y][x] = 0
                    elif brush_type == 5:
                        target_grid[y][x] = -1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    brush_type = max(1, brush_type - 1)  # 切换到上一个刷子
                elif event.key == pygame.K_RIGHT:
                    brush_type = min(len(brush_types), brush_type + 1)  # 切换到下一个刷子

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()
    return "exit"


