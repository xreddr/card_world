from src import chara_sheet
from texttable import Texttable
import random

class Game():
    def __init__(self):
        self.party_deck = Deck()
        self.stage_deck = Deck()

    def game_start(self):
        n = 1
        while n <= 10:
            if n % 4 == 0:
                self.stage_deck.cards.append(Event('Respite', 'Rest and restore some health', restore))
            else:
                self.stage_deck.cards.append(Chara('Zombie', 'Undead', 25, 25, 8, 8, 8, 8, 1))
            n += 1
        self.party_deck.cards.append(Chara('Harper', 'Girl', 100, 100, 10, 10, 10, 10, 0))
        self.party_deck.cards.append(Chara('Alexa', 'Girl', 100, 100, 10, 10, 10, 10, 0))

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
            player = self.play_stage(player, self.stage_deck.cards)


            if player.hp <= 0:
                print(f'\n{player.name} has been defeated')
                self.party_deck.cards.pop(self.party_deck.cards.index(player))
                player = None

        # Epilogue, Replay
        print("The End")
        self.game_over()

    def play_stage(self, player, stage):
        while len(stage) > 0 and player.hp > 0:
            print(f'\nPlayer CPs: {player.cp}')
            print(f'Cards in Stage: {len(stage)}')
            input('You draw a card...')
            card = stage[0]
            if isinstance(card, Chara):
                enemy = card
                print(f'\nYou drew a Monster {enemy.name}!')
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
                p_card = Texttable()
                p_card.add_rows([[f'{player.name} HP: {player.hp}', f'{enemy.name} HP: {enemy.hp}'],
                                 [f'SHDL:{player.shield} SCRL:{player.scroll} SWRD:{player.sword}', f'SHDL:{enemy.shield} SCRL:{enemy.scroll} SWRD:{enemy.sword}']])
                print()
                print(p_card.draw())
                inputs = ['1', '2', '3']
                print("1) Shield")
                print('2) Scroll')
                print('3) Sword')
                entry = input("Select a number:")
                if entry in inputs:
                    player_input = entry

            com_entry = random.choice(inputs)
            if com_entry == '1':
                com_stat = enemy.shield
            elif com_entry == '2':
                com_stat = enemy.scroll
            elif com_entry == '3':
                com_stat = enemy.sword

            def take_damage(player_stat, com_stat):
                if com_stat >= player_stat:
                    hit= com_stat
                elif com_stat < player_stat:
                    hit = com_stat - (player_stat - com_stat)
                player.hp  -= hit
                print(f'\nYou took {hit} points of damage!')

            def give_damage(player_stat, com_stat):
                if player_stat >= com_stat:
                    hit = player_stat
                elif player_stat < com_stat:
                    hit = player_stat - (com_stat - player_stat)
                enemy.hp -= hit
                print(f'\nYou gave {enemy.name} {hit} points of damage!')

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
                player_stat = player.sword
                if com_entry == '1':
                    take_damage(player_stat, com_stat)
                if com_entry == '2':
                    give_damage(player_stat, com_stat)                     
                if com_entry == '3':
                    print("\nDraw!")

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
    def __init__(self, name, desc, hp, sp, shield, scroll, sword, speed, cp):
        super().__init__(name, desc)
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.sp = sp
        self.shield = shield
        self.scroll = scroll
        self.sword = sword
        self.speed = speed
        self.cp = cp

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
