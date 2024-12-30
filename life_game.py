import numpy as np

def game_of_life_step(grid, wrap_edges=False):
    """计算生命游戏下一步。

    Args:
        grid (list of list): 当前网格状态。
        wrap_edges (bool): 是否启用边界循环。

    Returns:
        list of list: 更新后的网格。
    """
    grid = np.array(grid)
    grid_size = grid.shape[0]

    if wrap_edges:
        padded_grid = np.pad(grid, pad_width=1, mode='wrap')
    else:
        padded_grid = np.pad(grid, pad_width=1, mode='constant', constant_values=0)
    neighbors = sum(padded_grid[i:i + grid_size, j:j + grid_size]
                    for i in range(3) for j in range(3)
                    if (i, j) != (1, 1))

    new_grid = (neighbors == 3) | ((grid == 1) & (neighbors == 2))
    return new_grid.astype(int).tolist()

def check_target(grid, target):
    """检查是否完成目标"""
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if target[y][x] != 2 and grid[y][x] != target[y][x]:
                return False
    return True

