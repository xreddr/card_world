from src import chara_sheet
from texttable import Texttable
import random

class Game():
    def __init__(self):
        self.party_deck = Deck()
        self.stage_deck = Deck()

    def game_start(self):
        self.party_deck.cards.append(Chara(chara_sheet.harper))
        self.party_deck.cards.append(Chara(chara_sheet.alexa))

        print(self.party_deck.cards[0].name)
        for card in self.stage_deck.cards:
            print(card.name, self.stage_deck.cards.index(card))
        self.game_loop()

    def game_loop(self):
        player = None
        while player == None:
            # Select Player
            player = self.select_chara()

            # Play through stage deck
            self.build_stage()
            player = self.play_stage(player, self.stage_deck.cards)


            if player.hp <= 0:
                print(f'\n{player.name} has been defeated')
                self.party_deck.cards.pop(self.party_deck.cards.index(player))
                player = None

            if len(self.stage_deck.cards) == 0:
                for card in self.party_deck.cards:
                    print(card.read(), card.hp, card.cp)
                input("Stage Complete")
                player = None

        # Epilogue, Replay


    def build_stage(self):
        n = 1
        while n <= 10:
            if n % 4 == 0:
                self.stage_deck.cards.append(Event('Respite', 'Rest and restore some health', restore))
            else:
                self.stage_deck.cards.append(Chara(chara_sheet.zombie))
            n += 1
        return self

    def play_stage(self, player, stage):
        while len(stage) > 0 and player.hp > 0:
            print(f'\nPlayer CPs: {player.cp}')
            print(f'Cards in Stage: {len(stage)}')
            input('You draw a card...')
            card = stage[0]
            if isinstance(card, Chara):
                enemy = card
                print(f'\nYou drew a Monster: {enemy.name}, {enemy.desc}!')
                player.hp = self.battle_phase(player, enemy)
            elif isinstance(card, Event):
                print(f'\nYou drew an Event: {card.name}, {card.desc}')
                card.activate(player, 10)
            stage.pop(stage.index(card))

        return player   

    def battle_phase(self, player, enemy):
        while player.hp > 0 and enemy.hp > 0:
            player_input = None
            while player_input is None:
                battle_grid = Texttable()
                battle_grid.add_rows([
                    [player.name, enemy.name],
                    [f'HP: {player.hp}/{player.max_hp}', f'HP: {enemy.hp}/{enemy.max_hp}']
                    ])
                print(battle_grid.draw())
                inputs = ['1', '2', '3']
                print(f"1) {player.shield['name']}")
                print(f'2) {player.scroll["name"]}')
                print(f'3) {player.sword["name"]}')
                entry = input("Select a number:")
                if entry in inputs:
                    player_input = entry

            com_entry = random.choice(inputs)
            if com_entry == '1':
                com_stat = enemy.shield['stat']
            elif com_entry == '2':
                com_stat = enemy.scroll['stat']
            elif com_entry == '3':
                com_stat = enemy.sword['stat']

            def take_damage(player_stat, com_stat):
                if com_stat >= player_stat:
                    hit= com_stat
                elif com_stat < player_stat:
                    hit = com_stat - (player_stat - com_stat)
                player.hp  -= hit
                input(f'\nYou took {hit} points of damage!')

            def give_damage(player_stat, com_stat):
                if player_stat >= com_stat:
                    hit = player_stat
                elif player_stat < com_stat:
                    hit = player_stat - (com_stat - player_stat)
                enemy.hp -= hit
                input(f'\nYou gave {enemy.name} {hit} points of damage!')

            def draw():
                input(f'\nYour moves were evenly matched')

            if player_input == '1':
                enemy.hp -= 25
                # player_stat = player.shield
                # if com_entry == '1':
                #     print("\nDraw!")
                # if com_entry == '2':
                #     take_damage(player_stat, com_stat)
                # if com_entry == '3':
                #     give_damage(player_stat, com_stat)

            if player_input == '2':
                player.hp -= 50
                # player_stat = player.scroll
                # if com_entry == '1':
                #     give_damage(player_stat, com_stat)                     
                # if com_entry == '2':
                #     print("\nDraw!")
                # if com_entry == '3':
                #     take_damage(player_stat, com_stat)

            if player_input == '3':
                player_stat = player.sword['stat']
                if com_entry == '1':
                    take_damage(player_stat, com_stat)
                if com_entry == '2':
                    give_damage(player_stat, com_stat)                     
                if com_entry == '3':
                    draw()

        if enemy.hp <= 0:
            player.cp += enemy.cp
            input(f'\nYou defeated {enemy.name}. You earned {enemy.cp} CPs')

        return player.hp
    
    def select_chara(self):
        # Console Interface Menu
        selected = None
        if len(self.party_deck.cards) == 0:
            self.game_over()
        deck = self.party_deck.cards
        while selected == None:
            print(f'\nSelect Your Character')
            for i in range(len(deck)):
                print(f'{i+1}) {deck[i].name}, {deck[i].desc}')
            selection = input('Choose an option by number')
            try:
                selection = int(selection)
                if selection-1 in range(len(deck)):
                    selected = deck[selection-1]
            except ValueError:
                pass

        return selected
    
    def game_over(self):
        print(f'Your Party has Fallen')
        self.party_deck.cards.clear()
        self.stage_deck.cards.clear()
        print('1) Continue')
        print('2) Quit')
        selected = int(input('What will you do?'))
        if selected == 1:
            self.game_start()
        if selected == 2:
            quit()


class Deck(object):
    def __init__(self):
        self.cards = []
    def draw_top(self):
        return self.cards.pop(0)
    def draw_bottom(self):
        return self.cards.pop()
    def shuffle(self):
        return random.shuffle(self.cards)

class Card(object):
    def __init__(self, name, desc):
        self.name = name 
        self.desc = desc
    def read(self):
        print(f'{self.name}\n{self.desc}')

class Chara(Card):
    def __init__(self, chara_sheet):
        super().__init__(chara_sheet['name'], chara_sheet['desc'])
        self.name = chara_sheet['name']
        self.hp = chara_sheet['hp']
        self.max_hp = chara_sheet['hp']
        self.shield = {
            "name" : chara_sheet['moves']['shield']['name'], 
            "stat" : chara_sheet['moves']['shield']['stat']
            }
        self.scroll = {
            "name" : chara_sheet['moves']['scroll']['name'],
            "stat" : chara_sheet['moves']['scroll']['stat']
        }
        self.sword = {
            "name" : chara_sheet['moves']['sword']['name'],
            "stat" : chara_sheet['moves']['sword']['stat']
        }
        self.speed = chara_sheet['speed']
        self.cp = chara_sheet['cp']

class Event(Card):
    def __init__(self, name, desc, effect):
        super().__init__(name, desc)
        self.effect = effect
    def activate(self, *args, **kwargs):
        self.effect(*args, **kwargs)

def restore(player, amount):
    player.hp += amount
    input(f'\n{player.name} has restored {amount} hp!')
    return player.hp

