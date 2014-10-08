import pygame
from pygame.locals import *

low_keys = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]


class KeyLogger :
    def __init__(self, width, height, mode) :
        self.text_field = pygame.Rect(0, 0, width, height)
        self.text = ""                                          # actual user input
        self.placeholder = ""                                   # placeholder for rendering for passwords, masks password with *
        self.surface = pygame.Surface((width, height))
        self.robC = pygame.font.Font('assets/robotoCondens.ttf', 14)
        self.mode = mode

    def get_input(self, focus) :
        color = (40, 40, 40)
        if focus :
            color = (80, 80, 80)
            for event in pygame.event.get(KEYDOWN) :
                key_name = str(pygame.key.name(event.key))
                if key_name in low_keys :
                    if pygame.key.get_mods() == 4097 : # if user pressed shift key
                        self.text += key_name.upper()
                    else :
                        self.text += key_name

                elif key_name == "backspace" : # character deletion
                    new_text = ""
                    for i in range(0, len(self.text) -1) :
                        new_text += self.text[i]
                    self.text = new_text

        if self.mode == "password" :    # mask the password NOW
            self.placeholder = self.mode + ": " + "*" * len(self.text)
        else :
            self.placeholder = self.mode + ": " + self.text

        pygame.draw.rect(self.surface, color, self.text_field) # render and return
        text_input = self.robC.render(self.placeholder, True, (255, 255, 255), color)
        self.surface.blit(text_input, self.text_field)
        return self.text, self.surface