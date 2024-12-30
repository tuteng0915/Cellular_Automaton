import json
import pygame_gui
import pygame


def load_level(filename):
    """加载关卡文件"""
    with open(filename, 'r') as f:
        return json.load(f)
    
def save_map(grid, target_grid, filename="custom_map.json"):
    """保存地图"""
    with open(filename, 'w') as f:
        json.dump({"max_size": len(grid), "grid_size": len([row for row in grid if any(row)]), "cells": grid, "target": target_grid}, f)

def load_map(filename="custom_map.json"):
    """加载地图"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Map file not found.")
        return None

def get_map_files(folder="assets/maps"):
    """获取 maps 文件夹中的所有 JSON 文件"""
    try:
        return [f for f in os.listdir(folder) if f.endswith(".json")]
    except FileNotFoundError:
        print(f"Folder {folder} not found.")
        return []

def save_window(manager, grid, target_grid):
    """弹出保存地图的窗口"""
    window = pygame_gui.windows.UIFileDialog(
        rect=pygame.Rect((300, 150), (400, 300)),
        manager=manager,
        window_title="Save Map",
        initial_file_path="assets/maps/"
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    save_map(grid, target_grid, event.text)
                    print(f"Map saved to {event.text}")
                    return
                elif event.user_type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == window:
                    print("Save window closed")
                    return

        time_delta = pygame.time.Clock().tick(60) / 1000.0
        manager.update(time_delta)
        manager.draw_ui(pygame.display.get_surface())
        pygame.display.flip()


def load_window(manager, grid, target_grid):
    """弹出加载地图的窗口"""
    window = pygame_gui.windows.UIFileDialog(
        rect=pygame.Rect((300, 150), (400, 300)),
        manager=manager,
        window_title="Load Map",
        initial_file_path="assets/maps/"
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            manager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
                    loaded_map = load_map(event.text)
                    if loaded_map:
                        grid_size = len(loaded_map["cells"])
                        for y in range(grid_size):
                            for x in range(grid_size):
                                grid[y][x] = loaded_map["cells"][y][x]
                                target_grid[y][x] = loaded_map["target"][y][x]
                        print(f"Map loaded from {event.text}")
                    return
                elif event.user_type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == window:
                    print("Load window closed")
                    return

        time_delta = pygame.time.Clock().tick(60) / 1000.0
        manager.update(time_delta)
        manager.draw_ui(pygame.display.get_surface())
        pygame.display.flip()



