class Player:
    def __init__(self, deaths, current_boss, new_game, total_deaths):
        self.dead = False
        self.deaths = deaths
        self.current_boss = current_boss
        self.new_game = new_game
        self.total_deaths = total_deaths
