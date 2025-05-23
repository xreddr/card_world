import random
import json

class Card(object):
    def __init__(self, name, type, desc, image):
        self.name = name
        self.type = type
        self.desc = desc
        self.image = image

class Deck(object):
    def __init__(self):
        self.stack = []
    def draw_top(self):
        return self.stack.pop(0)
    def draw_bottom(self):
        return self.stack.pop()
    def shuffle(self):
        return random.shuffle(self.stack)

class Clothing(Card):
    def __init__(self, name, desc, image, layer, categorie, fastener):
        super().__init__(name, self.__class__.__name__, desc, image)
        self.layer = layer
        self.categorie = categorie
        self.fastener = fastener

    def remove(self):
        pass

    def add(self):
        pass

    def wear(self):
        pass
clothing_layers = ['under', 'outer']
clothing_categories = ['top', 'bottom', 'feet']
items = {
"under_top_items" : ['bra', 'bralet', 'beater', 'pasties'],
"under_bottom_items" : ['panties', 'boxers', 'thong', 'booty shorts'],
"under_feet_items" : ['ankle socks', 'knee socks', 'crew socks'],
"outer_top_items" : ['blouse', 'shirt', 'polo', 'hoodie'],
"outer_bottom_items" : ['shorts', 'skirt', 'pants', 'leggings'],
"outer_feet_items" : ['shoes', 'sneakers', 'loafers', 'sandals'],
}
clothing_fasteners = ['button', 'stitch', 'zipper']
clothing_sets = ['School', 'Casual', 'Sexy', 'Smart']

def create_clothing_set():
    set = random.choice(clothing_sets)
    clothing_set = []
    for layer in clothing_layers:
        for cat in clothing_categories:
            item_name = f'{layer}_{cat}_items'
            clothing_set.append(Clothing(f'{set} {random.choice(items[item_name])}',
                                         "Description",
                                         "Image",
                                         layer,
                                         cat,
                                         random.choice(clothing_fasteners)
                                         ))
    # for item in clothing_set:
    #     print(vars(item))

    return clothing_set

class Action(Card):
    def __init__(self, name, desc, image, fastener):
        super().__init__(name, self.__class__.__name__, desc, image)
        self.fastener = fastener

class Player(object):
    def __init__(self, name):
        self.name = name
        self.under_top = None
        self.under_bottom = None
        self.under_feet = None
        self.outer_top = None
        self.outer_bottom = None
        self.outer_feet = None
        self.deck = Deck()
        self.hand = []

    def add(self, clothing):
        attr = f'{clothing.layer}_{clothing.categorie}'
        for a in vars(self):
            if str(a) == str(attr):
                if getattr(self, a) == None:
                    setattr(self, a, clothing)
                    return 1
                return 0
    def remove(self):
        pass
    def stats(self):
        stats = []
        if self.under_bottom == None and self.outer_bottom == None:
            print("Player is bottomless")
            stats.append('bottomless')
        if self.under_top == None and self.outer_top == None:
            print("Player is topless")
            stats.append('topless')
        if self.under_feet == None and self.outer_feet == None:
            print("Player is barefoot")
            stats.append('barefoot')

        return stats
    def show_outfit(self):
        for var in vars(self):
                if "_" in var:
                    if getattr(self, var) == None:
                        print(f'{var}: {getattr(self, var)}')
                    else:
                        print(f'{var}: {getattr(self, var).name} {getattr(self, var).fastener}')


def create_deck():
    deck = Deck()
    clo_cards = 24
    act_cards = 16
    set_cards = create_clothing_set()
    for card in set_cards:
        deck.stack.append(card)
        deck.stack.append(card)
    while len(deck.stack) < clo_cards:
        clothing_card = Clothing(
            "Clothing",
            "Description",
            "Image",
            random.choice(clothing_layers),
            random.choice(clothing_categories),
            random.choice(clothing_fasteners)
        )
        deck.stack.append(clothing_card)

    x = 0
    while x < act_cards:
        action_card = Action(
            "Action",
            "Descriptions",
            "Image",
            random.choice(clothing_fasteners)
        )
        deck.stack.append(action_card)
        x += 1

    deck.shuffle()

    print(len(deck.stack))
    return deck


class Game():
    def __init__(self):
        self.player = Player('Harper')
        self.ai = Player('Alexa')
    
    def loop(self):
        self.gen_decks()
        self.draw_outfits()
        input()
        self.turn_loop()

    def turn_loop(self):
        while True:
            self.play_turn(self.player, self.ai)
            self.player_stats()
            input()
            self.play_turn(self.ai, self.player)
            self.player_stats()
            x = input()
            if x == "x":
                exit()
            self.player.hand.append(self.player.deck.draw_top())
            self.ai.hand.append(self.ai.deck.draw_top())

    def gen_decks(self):
        self.player.deck = create_deck()
        self.ai.deck = create_deck()

    def draw_outfits(self):
        players = [self.player, self.ai]
        for player in players:

            n = 6
            for card in player.deck.stack:
                if n > 0:
                    if card.type == "Clothing":
                        if player.add(card) == 1:
                            player.deck.stack.pop(player.deck.stack.index(card))
                        n -= 1
                    else:
                        pass

            stats = player.stats()
            if 'bottomless' in stats:
                for card in player.deck.stack:
                    if card.type == "Clothing" and card.categorie == 'bottom':
                        if player.add(card) == 1:
                            player.deck.stack.pop(player.deck.stack.index(card))
            if 'topless' in stats:
                for card in player.deck.stack:
                    if card.type == "Clothing" and card.categorie == 'top':
                        if player.add(card) == 1:
                            player.deck.stack.pop(player.deck.stack.index(card))


            while len(player.hand) < 5:
                player.hand.append(player.deck.draw_top())



            print(len(player.deck.stack))

        self.player_stats()

    def player_stats(self):
        players = [self.player, self.ai]
        for player in players:
            player.show_outfit()
            self.show_hand(player)
            player.stats()
            print()

    def show_hand(self, player):
        for card in player.hand:
            if card.type == "Clothing":
                print(card.name, card.layer, card.categorie, card.fastener)
            else:
                print(card.name, card.fastener)

    def play_turn(self, player, player2):
        for card in player.hand:
            if card.type == "Clothing":
                if player.add(card) == 1:
                    player.hand.pop(player.hand.index(card))
            if card.type == "Action":
                for var in vars(player2):
                    if '_' in var:
                        # print(var)
                        attr = getattr(player2, var)
                        # print(var, attr)
                        if attr is not None:
                            if attr.fastener == card.fastener:
                                print(f"{attr.name}'s {attr.fastener} has been removed by {card.name}'s {card.fastener}")
                                setattr(player2, var, None)
                                player.hand.pop(player.hand.index(card))
                                break
                        else:
                            continue

Session = Game()
Session.loop()