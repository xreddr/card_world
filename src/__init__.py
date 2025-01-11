from src import chara_sheet
from texttable import Texttable
import random

class Game():
    def __init__(self):
        self.party_deck = Deck()
        self.stage_deck = Deck()
        self.player = None

    def game_start(self):
        for hero in chara_sheet.heros:
            self.party_deck.cards.append(Chara(hero))
        # self.party_deck.cards.append(Chara(chara_sheet.harper))
        # self.party_deck.cards.append(Chara(chara_sheet.alexa))

        print(self.party_deck.cards[0].name)
        for card in self.stage_deck.cards:
            print(card.name, self.stage_deck.cards.index(card))
        self.game_loop()

    def game_loop(self):
        self.player = None
        while self.player == None:
            self.select_chara()

            self.build_stage()

            self.play_stage()

            if self.player.hp <= 0:
                print(f'\n{self.player.name} has been defeated')
                self.party_deck.cards.pop(self.party_deck.cards.index(self.player))
                self.player = None

            if len(self.stage_deck.cards) == 0:
                for card in self.party_deck.cards:
                    print(card.read())
                input("Stage Complete")
                self.player = None

    def build_stage(self):
        if len(self.stage_deck.cards) == 0:
            n = 1
            while n <= 10:
                if n % 4 == 0:
                    self.stage_deck.cards.append(Event('Respite', 'Rest and restore some health', rester))
                else:
                    self.stage_deck.cards.append(Chara(random.choice(chara_sheet.mobs)))
                n += 1
        return self

    def play_stage(self):
        while len(self.stage_deck.cards) > 0 and self.player.hp > 0:
            self.camp()
            print(f'\nPlayer CPs: {self.player.cp}')
            print(f'Cards in Stage: {len(self.stage_deck.cards)}')
            input('You draw a card...')
            card = self.stage_deck.cards[0]
            if isinstance(card, Chara):
                enemy = card
                input(f'\nYou drew a Monster: {enemy.name}, {enemy.desc}!')
                self.player.hp, enemy.hp = self.battle_phase(self.player, enemy)
                if enemy.hp <= 0:
                    self.stage_deck.cards.pop(self.stage_deck.cards.index(card))
            elif isinstance(card, Event):
                input(f'\nYou drew an Event: {card.name}, {card.desc}')
                card.activate(self)
                self.stage_deck.cards.pop(self.stage_deck.cards.index(card))

        return self   
    
    def camp(self):
        while self.player.cp > 0:
            print(f"\n{self.player.name} has {self.player.cp} CPs to spend.")
            print(f"1) {self.player.shield['name']}: {self.player.shield['stat']}")
            print(f"2) {self.player.scroll['name']}: {self.player.scroll['stat']}")
            print(f"3) {self.player.sword['name']}: {self.player.sword['stat']}")
            print(f"4) None for now")
            raw = input('Select a stat to increase')
            raw_int = int(raw)
            if raw_int == 1:
                self.player.cp -= 1
                self.player.shield['stat'] += 1
            elif raw_int == 2:
                self.player.cp -= 1
                self.player.scroll['stat'] += 1
            elif raw_int == 3:
                self.player.cp -= 1
                self.player.sword['stat'] += 1
            elif raw_int == 4:
                break
        print(f"{self.player.shield['name']}: {self.player.shield['stat']}")
        print(f"{self.player.scroll['name']}: {self.player.scroll['stat']}")
        print(f"{self.player.sword['name']}: {self.player.sword['stat']}")
        return self    

    def battle_phase(self, player, enemy):
        while player.hp > 0 and enemy.hp > 0:
            player_input = None
            while player_input is None:
                battle_grid = Texttable()
                battle_grid.add_rows([
                    [player.name, enemy.name],
                    [f'HP: {player.hp}/{player.max_hp}', f'HP: {enemy.hp}/{enemy.max_hp}']
                    ])
                # print(battle_grid.draw())
                self.print_cards([player, enemy])
                inputs = ['1', '2', '3']
                print(f"1) {player.shield['name']}: {player.shield['stat']}")
                print(f'2) {player.scroll["name"]}: {player.scroll["stat"]}')
                print(f'3) {player.sword["name"]}: {player.sword["stat"]}')
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
                    hit = com_stat - (round((player_stat - com_stat)/2))
                if hit <= 0:
                    hit = 1
                player.hp  -= hit
                input(f'\nYou took {hit} points of damage!')

            def give_damage(player_stat, com_stat):
                if player_stat >= com_stat:
                    hit = player_stat
                elif player_stat < com_stat:
                    hit = player_stat - (round((com_stat - player_stat)/2))
                if hit <= 0:
                    hit = 1
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

        return player.hp, enemy.hp
    
    def select_chara(self):
        # Console Interface Menu
        selected = None
        if len(self.party_deck.cards) == 0:
            self.game_over()
        deck = self.party_deck.cards
        while selected == None:
            self.print_cards(self.party_deck.cards)
            print(f'\nSelect Your Character')
            for i in range(len(deck)):
                print(f'{i+1}) {deck[i].name}, {deck[i].desc}')
            selection = input('Choose an option by number')
            try:
                selection = int(selection)
                if selection-1 in range(len(deck)):
                    selected = deck[selection-1]
                    self.player = selected
            except ValueError:
                pass

        return self
    
    def print_cards(self, cards=list):
        card_names = []
        card_hps = []
        card_sps = []
        card_speeds = []
        card_move1s = []
        card_move2s = []
        card_move3s = []
        for card in cards:
            card_names.append(card.name)
            card_hps.append(f'HP: {(card.hp, card.max_hp)}')
            card_sps.append(f'SP: {(card.sp, card.max_sp)}')
            card_speeds.append(f'Speed: {card.speed}')
            card_move1s.append(f'{card.shield["name"]}: {card.shield["stat"]}')
            card_move2s.append(f'{card.scroll["name"]}: {card.scroll["stat"]}')
            card_move3s.append(f'{card.sword["name"]}: {card.sword["stat"]}')
        sheet = Texttable()
        sheet.add_rows([card_names, card_hps, card_sps, card_speeds, card_move1s, card_move2s, card_move3s])
        print(sheet.draw())

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
        self.sp = chara_sheet['sp']
        self.max_sp = chara_sheet['sp']
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

def rester(self):
    self.player.hp += 10
    input(f'\n{self.player.name} has restored 10 hp!')


