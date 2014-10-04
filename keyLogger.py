import pygame
from pygame.locals import *

low_keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


class KeyLogger :
    def __init__(self, width, height) :
        self.text_field = pygame.Rect(0, 0, width, height)
        self.text = ""
        self.surface = pygame.Surface((width, height))
        self.robC = pygame.font.Font('assets/robotoCondens.ttf', 14)

    def getinput(self) :
        for event in pygame.event.get(KEYDOWN) :
            key_name = str(pygame.key.name(event.key))
            if key_name in low_keys :
                self.text += key_name

            elif key_name == "backspace" :
                new_text = ""
                for i in range(0, len(self.text) -1) :
                    new_text += self.text[i]
                self.text = new_text

        pygame.draw.rect(self.surface, (40, 40, 40), self.text_field)
        text_input = self.robC.render(self.text, True, (255, 255, 255), (40, 40, 40))
        self.surface.blit(text_input, self.text_field)
        return self.text, self.surface