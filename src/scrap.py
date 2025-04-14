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
clothing_categorie = ['top', 'bottom', 'feet']
clothing_fastener = ['button', 'stitch', 'zipper']
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

    def add(self, clothing):
        attr = f'{clothing.layer}_{clothing.categorie}'
        for a in vars(self):
            if str(a) == str(attr):
                if getattr(self, a) == None:
                    setattr(self, a, clothing.name)
                    return 1
                return 0
    def remove(self):
        pass
    def stats(self):
        if self.under_bottom == None and self.outer_bottom == None:
            print("Player is bottomless")
        if self.under_top == None and self.outer_top == None:
            print("Player is topless")
        if self.under_feet == None and self.outer_feet == None:
            print("Player is barefoot")


def create_deck():
    deck = Deck()
    n = 24
    while n > 0:
        clothing_card = Clothing(
            "Clothing",
            "Description",
            "Image",
            random.choice(clothing_layers),
            random.choice(clothing_categorie),
            random.choice(clothing_fastener)
        )
        deck.stack.append(clothing_card)
        # print(clothing_card)
        # print(deck.stack)
        n -= 1
    x = 16
    while x > 0:
        action_card = Action(
            "Action",
            "Descriptions",
            "Image",
            random.choice(clothing_fastener)
        )
        deck.stack.append(action_card)
        # print(action_card)
        x -= 1

    deck.shuffle()

    # print(deck.stack)

    return deck

def test_hand():
    deck = create_deck()
    hand = []
    n = 10
    while n > 0:
        hand.append(deck.draw_top())
        n -= 1
    player = Player("Harper")
    def auto_add_clothing():
        for card in hand:
            if card.type == 'Clothing':
                if player.add(card) == 1:
                    hand.pop(hand.index(card))
                # print(card.type,card.layer, card.categorie, card.fastener)
    auto_add_clothing()
    full = False
    while not full and len(deck.stack) > 0:
        if all(getattr(player, attr) is not None for attr in vars(player)) == False:
            hand.append(deck.draw_top())
            auto_add_clothing()
        else:
            full = True



    print(json.dumps(vars(player), indent=2))
    for card in hand:
        print(card.type, card.fastener)
    player.stats()

    print(len(deck.stack))

test_hand()

# class Parent:
#     def __init__(self, class_name):
#         print(f"Parent class initialized by: {class_name}")

# class Child(Parent):
#     def __init__(self):
#         super().__init__(self.__class__.__name__)
#         print("Child class initialized")

# obj = Child()