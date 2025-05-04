import src
from src import Game as StartGame
from src import scene

def main():
    Play = src.Game()
    Play.game_start()

Game = StartGame()
# Scene = StartScene()
Scene = scene.Scene()

def play_game():
    Game.game_start()

if __name__ == '__main__':
    main()