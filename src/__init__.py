from src import chara_sheet, images
import random, os

class Game():
    def __init__(self):
        self.party_deck = Deck()
        self.stage_deck = Deck()
        self.player = None
        self.stage = 1

    def game_start(self):
        '''Takes self. calls self.game_loop().'''
        ## Prep
        for hero in chara_sheet.heros:
            self.party_deck.cards.append(Chara(hero))
        ## Input
        CastleScene = Scene(images=[images.castle_image], text=["Welcome to Card World!"], menu=[
            "Start Game",
            "Quit"
        ]).show()
        ## Response
        if CastleScene.menu_selection == "Start Game":
            self.game_loop()
        elif CastleScene.menu_selection == "Quit":
            quit()

    def game_loop(self):
        '''Takes self. Continues until force quite.'''
        # Logic No Inputs
        self.player = None
        while self.player == None:
            self.select_chara()

            self.build_stage()

            self.play_stage()

            self.stage_conditions()

            self.game_over()

    def stage_conditions(self):
        '''Takes self. Modifies player, stage_deck. Returns self.'''
        # Scene for each to transition
        if self.player.hp <= 0:
            print(f'\n{self.player.name} has been defeated')
            self.party_deck.cards.pop(self.party_deck.cards.index(self.player))
            self.player = None
            input()

        elif len(self.stage_deck.cards) == 0:
            Scene.clear()
            input("Stage Complete")
            self.stage += 1
            self.player = None

        return self

    def build_stage(self, size: int=10):
        '''Takes self. Modifies self.stage_deck. Returns self'''
        if len(self.stage_deck.cards) == 0:
            n = 1
            while n <= size:
                if n % 4 == 0:
                    self.stage_deck.cards.append(Event('Respite', 'Rest and restore some health', rester))
                else:
                    self.stage_deck.cards.append(Chara(random.choice(chara_sheet.mobs)))
                n += 1
        return self

    def play_stage(self):
        '''Takes self. Returns self'''
        # Logic
        # Scenes
        while len(self.stage_deck.cards) > 0 and self.player.hp > 0:
            ## Prep
            DrawStart = Scene(text=[
                f'Player CPs: {self.player.cp}',
                f'Cards in Stage: {len(self.stage_deck.cards)}',
                'You draw a card...'
                ]
                ).cards_to_images([self.player], 'battle').show()
            ## Input
            card = self.stage_deck.draw_top()
            ## Response
            if isinstance(card, Chara):
                enemy = card
                MonasterDraw = Scene().cards_to_images([enemy], 'desc').show()
                self.player.hp, enemy.hp = self.battle_phase(self.player, enemy)
            elif isinstance(card, Event):
                # Remove to scnee function
                input(f'\nYou drew an Event: {card.name}, {card.desc}')
                card.activate(self)
            
            self.camp()

        return self   
    
    def camp(self):
        '''Takes self. Modifies self.player. Returns self.'''
        while self.player.cp > 0:
            ## Prep
            CampScene = Scene(images=[images.camp_image], text=[f"{self.player.name} has {self.player.cp} CPs to spend."],
                              menu=self.player.chara_stats())
            CampScene.menu.append("Leave Camp")
            ## Input
            CampScene.show()
            ## Response
            if CampScene.menu_selection == "Leave Camp":
                break
            tmp = CampScene.menu_selection[0].replace(' ', '_').lower() # Player Stat = player_stat
            # print(tmp)
            for key, value in vars(self.player).items():
                # print(key, value)
                if key == tmp or value == tmp.capitalize():
                    self.player.increase_stat(key)
                    self.player.cp -= 1
                    if value == tmp.capitalize():
                        key = value
                    CampScene.text = [f'You upgraded {key.capitalize()}\nYou have {self.player.cp} CP reamining.']
                    CampScene.show()
                    break
            # input()
        return self    
    
    def double_battle(self, player, enemy):
        # Unused, nothing goes here.
        while player.hp > 0 and enemy.hp > 0:
            players = [player, enemy]
            first_player = None
            second_player = None
            if player.speed > enemy.speed:
                first_player = players.pop(player)
            else:
                first_player = players.pop(enemy)
            second_player = players.pop()

            enemy_selections = [enemy.shield, enemy.scroll, enemy.sword]
            enemy_input = random.choice(enemy_selections)

            if first_player is player:
                player_input = None
                while player_input is None:
                    # Call Battle scene with moves menu
                    pass

            else:
                # Call Battle scene showing enemy move and move menu for response
                pass


    def battle_phase(self, player, enemy):
        while player.hp > 0 and enemy.hp > 0:
            # Input
            player_input = None
            while player_input is None:
                BattleScene = Scene(menu=player.chara_moves()).cards_to_images(cards=[player, enemy], data='battle').show()
                for key, value in vars(self.player).items():
                    if value == BattleScene.menu_selection[0]: # Takes first index of tuple
                        player_input = key[-1] # Takes last character of string either 1,2,3

            # Logic
            inputs = ['1', '2', '3']
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
                ## Instant damage for testing
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
                    draw()

        if enemy.hp <= 0:
            player.cp += enemy.cp
            input(f'\nYou defeated {enemy.name}. You earned {enemy.cp} CPs')

        return player.hp, enemy.hp
    
    def select_chara(self):
        '''Takes self. Modifies self.party_deck and self.player. Returns self.'''
        selected = None
        while selected == None:
            ## Prep
            chara_menu = []
            for card in self.party_deck.cards:
                chara_menu.append(f'{card.name}, {card.desc}')
            ## Input
            CharaSelect = Scene(menu=chara_menu).cards_to_images(self.party_deck.cards).show()
            ## Response
            for card in self.party_deck.cards:
                if card.name in CharaSelect.menu_selection:
                    selected = card

        self.player = selected
        return self

    def game_over(self):
        '''Takes self. Return to game_start() or quit. Returns self.'''
        if len(self.party_deck.cards) == 0:
            # Scene. Choose restart or quit
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
        
        return self


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
    def __init__(self, name: str, desc: str):
        self.name = name 
        self.desc = desc
    def read(self):
        print(f'{self.name}\n{self.desc}')


class Chara(Card):
    def __init__(self, chara_sheet: dict):
        super().__init__(chara_sheet['name'], chara_sheet['desc'])
        self.name = chara_sheet['name']
        self.hp = chara_sheet['hp']
        self.max_hp = chara_sheet['hp']
        self.sp = chara_sheet['sp']
        self.max_sp = chara_sheet['sp']
        self.speed = chara_sheet['speed']
        self.shield = chara_sheet['shield']
        self.scroll = chara_sheet['scroll']
        self.sword = chara_sheet['sword']
        self.move1 = chara_sheet['move1']
        self.move2 = chara_sheet['move2']
        self.move3 = chara_sheet['move3']
        self.cp = chara_sheet['cp']
        self.image = chara_sheet['image']

    def chara_moves(self):
        '''Takes self. Returns list[tuple(str, int)].'''
        moves = [(self.move1, self.shield),
                 (self.move2, self.scroll),
                 (self.move3, self.sword)
                 ]

        return moves
    
    def chara_stats(self):
        '''Takes self. Returns list[tuple(str, int)].'''
        stats = [('Max HP', self.max_hp),
                 ('Max SP', self.max_sp),
                 ('Speed', self.speed),
                 ]
        for stat in self.chara_moves():
            stats.append(stat)
        # stats.append(self.chara_moves())

        return stats
    
    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp > 0:
            self.hp = 0

        return self
    
    def heal(self, amount: int):
        if (self.hp + amount) > self.max_hp:
            self.hp = self.max_hp
        else:
            self.hp += amount
        
        return self
    
    def increase_stat(self, attr: str):
        if attr == 'move1':
            attr = 'shield'
        elif attr == 'move2':
            attr = 'scroll'
        elif attr == 'move3':
            attr = 'sword'
        value = getattr(self, attr)
        setattr(self, attr, value + 1)

        return self


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
    self.player.heal(10)
    input(f'\n{self.player.name} has restored 10 hp!')
    
    return self


class Scene(object):
    def __init__(self, images: list[str] = None, text: list[str] = None, menu: list[str] = None) -> None:
        self.images = images
        self.text = text
        self.menu = menu
        self.menu_selection = None

    def clear(self=None):
        command = 'cls' if os.name in ('nt', 'dos') else 'clear'
        os.system(command)

    def show(self):
        '''Takes self. Returns self.'''
        self.clear()
        self.render_image()
        self.print_text()
        if self.menu:
            self.view_menu()
        else:
            input()

        return self
    
    def render_image(self):
        '''Takes self.image list of multiline str. Returns list[str].'''
        # Cocatonate lines of multiline str by index. Multiline strings appear side by side.
        display = []
        for i in range(len(list(self.images[0].splitlines()))):
            line = ''
            for image in self.images:
                img = list(image.splitlines())
                line = line + img[i]
            display.append(line)
            line= ''
        for line in display:
            ## Debug image size.
            # print(len(line))
            print(line)
        
        return display

    def print_text(self):
        '''Takes self. No return.'''
        if self.text:
            for line in self.text:
                print(line)

    def view_menu(self):
        '''Takes self. Modifies self.menu_selection. Returns self.'''
        while self.menu_selection is None:
            for i in range(len(self.menu)):
                n = i +1
                if type(self.menu[i]) == str:
                    print(f'{n}) {self.menu[i]}')
                elif type(self.menu[i]) == tuple:
                    print(f'{n}) {self.menu[i][0]} {self.menu[i][1]}')
            raw = input(f'Select option: ')
            try:
                selection = int(raw)
                if selection-1 in range(len(self.menu)):
                    self.menu_selection = self.menu[selection-1]
                    self.menu = []
                else:
                    self.show()
            except ValueError:
                self.show()

        return self

    def cards_to_images(self, cards: list[Card], data: str='stats'):
        '''Takes list of Card objects. data str 'stats'/'battle'/'desc'. Modifies self.images. Retruns self.'''
        card_images = []
        # Update to add lines to chara_images instead of new string images in chara_stats
        for card in cards:
            card_image = card.image
            if data == 'stats':
                stats = card.chara_stats()
                # print(stats)
                lines = [
                    f'{stats[0][0]}:{stats[0][1]} {stats[1][0]}:{stats[1][1]}',
                    f'{stats[2][0]}:{stats[2][1]} {stats[3][0]}:{stats[3][1]}',
                    f'{stats[4][0]}:{stats[4][1]} {stats[5][0]}:{stats[5][1]}'
                ]
            elif data == 'battle':
                lines = [
                    f'{card.name}',
                    f'HP:{card.hp}/{card.max_hp}',
                    f'SP:{card.sp}/{card.max_sp}'
                ]
            elif data == 'desc':
                desc1 = card.desc
                desc2 = ''
                if len(card.desc) > 20:
                    desc1 = card.desc[:20]
                    desc2 = card.desc[20:40]
                lines = [
                    f'{card.name}',
                    f'{desc1}',
                    f'{desc2}'
                ]
            for line in lines:
                print(line)
                dir = 'back'
                while len(line) <= 24:
                    if dir == 'back':
                        line += ' '
                        dir = 'front'
                    elif dir == 'front':
                        line = f' {line}'
                        dir = 'back'
                line = '▌' + line[1:-2] + '▐'
                card_image += f'\n{line}'
            card_image += f'\n▓▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▓'
            buffer = ''
            for i in range(20):
                buffer += '\n '
            card_images.append(buffer)
            card_images.append(card_image)
        self.images = card_images

        return self
