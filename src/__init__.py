from src import chara_sheet
import random

class Game():
    def __init__(self):
        self.party_deck = []
        self.stage_deck = []

    def game_start(self):
        n = 1
        while n <= 10:
            if n % 4 == 0:
                self.stage_deck.append(Event('Respite', 'Rest and restore some health', restore))
            else:
                self.stage_deck.append(Chara('Zombie', 'Undead', 25, 25, 8, 8, 8, 8, 1))
            n += 1
        self.party_deck.append(Chara('Harper', 'Girl', 100, 100, 10, 10, 10, 10, 0))
        print(self.party_deck[0].name)
        for card in self.stage_deck:
            print(card.name, self.stage_deck.index(card))
        self.game_loop()

    def game_loop(self):
        # Select Chara from party deck
        player = self.party_deck[0]

        # Draw cards from stage deck
        while len(self.stage_deck) > 0 and player.hp > 0:
            for card in self.stage_deck:
                # Draw phase
                print(f'\nCards left in stage: {len(self.stage_deck)}')
                input("You draw a card...")
                # for card in self.stage_deck:
                #     print(card.name)

                if isinstance(card, Chara):
                    # Enter battle phase
                    enemy = card
                    print(f'\nYou encountered a {card.name}!')
                    while enemy.hp > 0 and player.hp > 0:
                        player.hp, enemy.hp = self.battle_phase(player, enemy)
                        if enemy.hp <=0:
                            player.cp += enemy.cp
                            input(f'\n{player.name} has defeted {enemy.name}')
                        elif player.hp <= 0:
                            input(f"\n{player.name} has fallen")

                elif isinstance(card, Event):
                    # Event 
                    print(f'\n{card.desc}')
                    card.activate(player, 10)

                self.stage_deck.pop(self.stage_deck.index(card))

            if player.hp > 0:
                print("Congrats!")

        # Epilogue, Replay
        print("The End")

    def battle_phase(self, player, enemy):
            print(f'Player HP: {player.hp}, Enemy HP: {enemy.hp}')
            player_input = None
            while player_input is None:
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
                player_stat = player.shield
                if com_entry == '1':
                    print("\nDraw!")
                if com_entry == '2':
                    take_damage(player_stat, com_stat)
                if com_entry == '3':
                    give_damage(player_stat, com_stat)

            if player_input == '2':
                player_stat = player.scroll
                if com_entry == '1':
                    give_damage(player_stat, com_stat)                     
                if com_entry == '2':
                    print("\nDraw!")
                if com_entry == '3':
                    take_damage(player_stat, com_stat)

            if player_input == '3':
                player_stat = player.sword
                if com_entry == '1':
                    take_damage(player_stat, com_stat)
                if com_entry == '2':
                    give_damage(player_stat, com_stat)                     
                if com_entry == '3':
                    print("\nDraw!")
            
            return player.hp, enemy.hp
            

class Deck(object):
    def __init__(self):
        self.cards = []

class Card(object):
    def __init__(self, name, desc):
        self.name = name 
        self.desc = desc

class Chara(Card):
    def __init__(self, name, desc, hp, sp, shield, scroll, sword, speed, cp):
        super().__init__(name, desc)
        self.name = name
        self.hp = hp
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


