import pygame

class Timer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
        self.paused = False
    def start(self):
        if not self.running:
            self.start_time = pygame.time.get_ticks()
            self.running = True
    def stop(self):
        if self.running:
            self.elapsed_time += pygame.time.get_ticks() - self.start_time
            self.running = False
            self.paused = True
    def play(self):
        if self.paused:
            self.start_time = self.elapsed_time
            self.running = True
    def reset(self):
        self.start_time = 0
        self.elapsed_time = 0
        self.running = False
    def get_time(self):
        if self.running:
            return pygame.time.get_ticks() - self.start_time
        else:
            return self.elapsed_time
    def get_formatted_time(self):
        total_milliseconds = self.get_time()
        minutes = total_milliseconds // 60000
        seconds = (total_milliseconds % 60000) // 1000
        milliseconds = total_milliseconds % 1000
        return f'Time: {minutes:02}:{seconds:02}:{milliseconds:03}'