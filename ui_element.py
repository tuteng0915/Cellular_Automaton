import pygame

class Button:
    def __init__(self, position, text, color, size=(200, 50), hover_color=(79, 255, 143)):
        self.rect = pygame.Rect(position, size)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def is_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]


class TextInput:
    def __init__(self, position, label, width=150, height=40, font_size=24):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.color = (200, 200, 200)
        self.text = ""
        self.label = label  # 输入框的标签
        self.font = pygame.font.SysFont("Arial", font_size)
        self.active = False

    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查鼠标是否点击在文本框内
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self, screen):
        """绘制文本框"""
        # 绘制标签
        label_surface = self.font.render(self.label, True, (255, 255, 255))
        screen.blit(label_surface, (self.rect.x - label_surface.get_width() - 10, self.rect.y + 5))

        # 绘制文本框
        pygame.draw.rect(screen, self.color, self.rect, 2 if self.active else 1)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        """获取当前输入的文本"""
        return self.text

    def clear(self):
        """清空输入框"""
        self.text = ""
