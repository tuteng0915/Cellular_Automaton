# setting.py
import pygame
import pygame_gui
from ui_element import Button

def settings_screen():
    """设置页面"""
    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    pygame.display.set_caption("Settings")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((960, 720))

    # 创建滑块和按钮
    grid_size_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((100, 200), (760, 40)),
        start_value=20,
        value_range=(10, 50),
        manager=manager
    )
    speed_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((100, 300), (760, 40)),
        start_value=1.0,
        value_range=(0.1, 5.0),
        manager=manager
    )
    back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((430, 500), (100, 50)),
        text="Back",
        manager=manager
    )

    running = True
    grid_size = 20
    update_speed = 1.0

    while running:
        time_delta = clock.tick(60) / 1000.0
        screen.fill((13, 27, 42))

        # 绘制文本
        font = pygame.font.Font(None, 36)
        grid_size_text = font.render(f"Grid Size: {int(grid_size)}", True, (255, 255, 255))
        speed_text = font.render(f"Update Speed: {update_speed:.1f}", True, (255, 255, 255))
        screen.blit(grid_size_text, (100, 160))
        screen.blit(speed_text, (100, 260))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "exit", {"grid_size": int(grid_size), "update_speed": update_speed}
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == back_button:
                        return "menu", {"grid_size": int(grid_size), "update_speed": update_speed}
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == grid_size_slider:
                        grid_size = event.value
                    elif event.ui_element == speed_slider:
                        update_speed = event.value

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()
    return "exit", {"grid_size": int(grid_size), "update_speed": update_speed}
