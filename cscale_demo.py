#!/usr/bin/env python
import os

class Cuboid:
    def __init__(self):
        # things we need
        self.field = None
        self.legal = '.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


    def populate_from_string(self, field):
        fields = field.split('\n')
        if not fields:
            raise TypeError('no fields')
        if not fields[0]:
            raise TypeError('empty first row')

        # the first row contains the canonical amount of columns
        # for my purposes anyway
        x_len = len(fields[0])
        if x_len % 2 == 0:
            raise TypeError('x length even')
        y_len = len(fields)
        if y_len % 2 == 0:
            raise TypeError('y length even')

        container = []
        for f in fields:
            if len(f) != x_len: # safe at this point
                raise TypeError('uneven row lengths')
            if any(map(f, lambda x: x in self.legal)): # throw out bad strings
                raise TypeError('bad characters in input')
            container.append(f)
        self.field = container


    @property
    def x(self):
        return len(self.field[0]) if self.field and self.field[0] else None


    @property
    def y(self):
        return len(self.field) if self.field else None


    def __repr__(self):
        # python representation to make this easier later
        return '\n'.join(self.field)
    

    def decrement_symbol(symbol):
        # gonna use the ascii representation here and patch the odd ones
        # followed up on stack overflow and the interactive python to figure
        # out the rest
        if symbol not in legal:
            raise TypeError # this should be taken care of above, but...
        elif symbol == '.':
            return '.' # identity
        elif symbol == 'a':
            return '*' # would be `, note that it is not in self.legal
        elif symbol == 'A':
            return 'z' # would be @
        else:
            return str(unichr(ord(symbol) - 1))
            

    def fall(self):
        # decrement every mine on the field
        container = []
        for f in self.field:
            container.append(''.join(map(decrement_symbol, f)))
        self.field = container


    def move(self, direction):
        # when you move the ship in whatever direction, what you're really changing is the
        # shape of the view you have of the field
        # constrained by the odd number of rows and columns, we need to add two
        # rows or columns from one side and remove two on the other side
        # but only if there are no mines there
        # classic 2d video game thing
        if not direction:
            raise TypeError('no direction to move')
        elif direction == 'north':
            blank = '.' * self.x

            # check the two at the bottom if they exist
            if self.y >= 3:
                if self.field[-2] == blank and self.field[-1] == blank:
                    self.field = self.field[:-2] # cut them if they are blank
                else:
                    # add the two at the top if i didn't cut anything or had only 1 row
                    self.field = [blank, blank] + self.field
            else:
                self.field = [blank, blank] + self.field
        elif direction == 'south':
            blank = '.' * self.x

            # check the two at the top if they exist
            if self.y >= 3:
                if self.field[0] == blank and self.field[1] == blank:
                    self.field = self.field[2:] # cut them if they are blank
                else:
                    # add the two at the bottom if i didn't cut anything or had only 1 row
                    self.field = self.field + [blank, blank]
            else:
                self.field = self.field + [blank, blank]
        elif direction == 'east':
            # check the first two characters of each line to see if they are blank
            if self.y >= 3:
                if all(map(lambda f: f[:2] == '..', self.field)):
                    container = []
                    for f in self.field:
                        container.append(f[2:]) # works on strings
                else:
                    container = []
                    for f in self.field:
                        container.append(f + '..')
            else:
                container = []
                for f in self.field:
                    container.append(f + '..')
        elif direction == 'west':
            # check the last two characters of each line to see if they are blank
            if self.y >= 3:
                if all(map(lambda f: f[-2:] == '..', self.field)):
                    container = []
                    for f in self.field:
                        container.append(f[:-2]) # works on strings
                else:
                    container = []
                    for f in self.field:
                        container.append('..' + f)
            else:
                container = []
                for f in self.field:
                    container.append('..' + f)
        else:
            raise TypeError('invalid direction operation')

    def projectile_scan(self, letter):
        # this just overwrites places with periods if they exist
        # abuse of python slicing here because strings are immutable
        if not letter:
            raise TypeError('no projectile scan type')
        elif letter == 'alpha':
            # x pattern centered on ship but not including it
            if self.x > 3 and self.y > 3:
                center_x, center_y = (self.x / 2, self.y / 2)
                container = []
                for i, f in enumerate(self.fields):
                    if i == center_y - 1:
                        f = f[:center_x - 1] + '.' + f[center_x:]
                        f = f[:center_x + 1] + '.' + f[center_x + 2:]
                    elif i == center_y + 1:
                        f = f[:center_x - 1] + '.' + f[center_x:]
                        f = f[:center_x + 1] + '.' + f[center_x + 2:]
                    container.append(f)
                self.field = container
        elif letter == 'beta':
            # + pattern centered on ship but not including it
            if self.x > 3 and self.y > 3:
                center_x, center_y = (self.x / 2, self.y / 2)
                container = []
                for i, f in enumerate(self.fields):
                    if i == center_y - 1:
                        f = f[:center_x] + '.' + f[center_x + 1:]
                    elif i == center_y:
                        f = f[:center_x - 1] + '.' + f[center_x:]
                        f = f[:center_x + 1] + '.' + f[center_x + 2:]
                    elif i == center_y + 1:
                        f = f[:center_x] + '.' + f[center_x + 1:]
                    container.append(f)
                self.field = container
        elif letter == 'gamma':
            # ship and the two  left and right
            if self.x > 3 and self.y > 3:
                center_x, center_y = (self.x / 2, self.y / 2)
                container = []
                for i, f in enumerate(self.fields):
                    if i == center_y:
                        f = f[:center_x - 1] + '...' + f[center_x + 2]
                    container.append(f)
            else:
                # degenerate case
                self.field = ['.']
        elif letter == 'delta':
            # ship and the two above and below
            if self.x > 3 and self.y > 3:
                center_x, center_y = (self.x / 2, self.y / 2)
                container = []
                for i, f in enumerate(self.fields):
                    if i == center_y - 1:
                        f = f[:center_x] + '.' + f[center_x + 1:]
                    elif i == center_y:
                        f = f[:center_x] + '.' + f[center_x + 1:]
                    elif i == center_y + 1:
                        f = f[:center_x] + '.' + f[center_x + 1:]
                    container.append(f)
            else:
                # degenerate case
                self.field = ['.']
        else:
            raise TypeError('invalid projectile scan type')


if __name__ == '__main__':
    # running out of time, let's make this quick and dirty
    field_string = open(os.path.join(sys.path[0], 'field'), 'r').read()
    script_string = open(os.path.join(sys.path[0], 'script'), 'r').read()

    cuboid = Cuboid()
    cuboid.populate_from_string(field_string)

    for script_line in script_string.splitlines():
        print ' '.join(['Step', str(i + 1), '\n'])
        print ''.join([str(cuboid), '\n'])
        print ''.join([script_line, '\n'])
        for command in script_line.split(' '):
            cuboid.transform(command)
            if command in ['alpha', 'beta', 'gamma', 'delta']:
                shots_fired_delta = shots_fired_delta + 5
            if command in ['north', 'south', 'east', 'west']:
                movement_delta = movement_delta + 2

            # look for interrupt-based clear conditions
            f_string = ''.join(cuboid.field)
            if all(map(lambda x: x is '.', f_string)):
                # everything is clear
                if i != len(script_string) - 1:
                    steps_remaining = True
                break
            elif all(map(lambda x: x is '*', f_string)):
                # we found a mine
                found_mine = True
                break
        cuboid.fall()

    # look for remaining mines
    if all(map(lambda x: x is '*', f_string)):
        found_mine = True

    # count up the score
    if found_mine: # conditions 1 & 2
        score = 0
        result = 'fail'
    elif steps_remaining: # condition 3
        score = 1
        result = 'fail'
    else:
        # this could all be on one line, but for clarity
        score = 10 * cuboid.initial_mines
        score = score - min(shots_fired_delta, 5 * cuboid.initial_mines)
        score = score - min(movement_delta, 3 * cuboid.initial_mines)
        result = 'pass'

    print ''.join([result, ' (', str(score), ')'])
