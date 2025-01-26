import src
from src import Game as StartGame, Scene as StartScene

def main():
    Play = src.Game()
    Play.game_start()

Game = StartGame()
Scene = StartScene()

def play_game():
    Game.game_start()

if __name__ == '__main__':
    main()