import os
'''
Decide image size in object setup
Card grid by card size? Resolution of small cards?
'''
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

    def cards_to_images(self, cards: list, data: str='stats'):
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