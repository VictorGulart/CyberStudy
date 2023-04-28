# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from random import randint
import numpy as np


class PlayFair:
    def __init__(self, kw=None):
        '''  '''
        self.__kw = None
        self.set_kw(kw)
        
            
    def get_kw(self):
        ''' Getting the kw'''
        return self.__kw
    
    def set_kw(self, val):
        ''' Set the kw '''
        if val is None:
            self.__kw = None 
        else:
            self.__kw = self.rm_duplicate(val.upper(), {})
            
    
    #### PLAYFAIR CIPHER ####
    def rm_duplicate(self, word, memo={}) -> list:
        new_word = []
        for l in word:
            if l not in memo:
                memo[l] = l
                new_word.append(l)
        return new_word
    
    def get_grid(self):
        ''' 
            Get a 5x5 grid with the keyword
        '''
        if self.__kw is None:
            raise TypeError("Keyword can not be None")

        lst = list('ABCDEFGHIKLMNOPQRSTUVWXYZ')
        clean_lst = self.rm_duplicate(lst, memo={l:l for l in self.__kw})
        grid = list(self.__kw) + clean_lst
        
        return np.array(grid).reshape((5,5))
    
    def get_right(self, pos):
        ''' Substitute the letter in the same row '''
        if pos[1][0] == self.grid.shape[1]-1: # is it on the edge
            # first letter of this row
            return self.grid[pos[0][0]][0]
        else:
            return self.grid[pos[0][0]][pos[1][0]+1]
    
    def get_down(self, pos):
        ''' Substitute the letter in the same column but below'''
        if (pos[0][0]) == self.grid.shape[0]-1:
            # first letter of this column
            return self.grid[0][pos[1][0]]
        else:
            return self.grid[pos[0][0]+1][pos[1][0]]
    
    def get_left(self, pos):
        ''' Substitute for a letter to the left in the same row'''
        if pos[1][0] == 0: # is it on the edge
            # get last letter of this row
            return self.grid[pos[0][0]][-1]
        else:
            return self.grid[pos[0][0]][pos[1][0]-1]
    
    def get_up(self, pos):
        ''' Substitute for a letter above it, in the same column '''
        if (pos[0][0]) == 0:
            # last letter of this column
            return self.grid[self.grid.shape[0]-1][pos[1][0]]
        else:
            return self.grid[pos[0][0]-1][pos[1][0]]
    
    def get_from_rect(self, x_pos, y_pos):
        row_distance = x_pos[1][0] - y_pos[1][0]
        # go back or forward
        x = self.grid[x_pos[0][0]][x_pos[1][0] - row_distance]
        y = self.grid[y_pos[0][0]][y_pos[1][0] + row_distance]
        return x, y
        
    def en_substitute(self, pair) -> str:
        '''
            Substitutes the values of the pair 
            of characters with 
        '''
        x, y = pair
        
        # Get the x and y position of the two characters
        # in the grid 
        
        x_pos = np.where(self.grid == x)
        y_pos = np.where(self.grid == y)
        
        # replace row
        if x_pos[0][0] == y_pos[0][0]: # rows are the same
            x = self.get_right(x_pos)
            y = self.get_right(y_pos)    
            
        # replace column
        elif x_pos[1][0] == y_pos[1][0]:
            x = self.get_down(x_pos)
            y = self.get_down(y_pos)
            
        # replace rectangle
        else:
            x, y = self.get_from_rect(x_pos, y_pos)
        return f'{x}{y}'
    
    def de_substitute(self, pair) -> str:
        
        x, y = pair
        
        # Get the x and y position of the two characters
        # in the grid 
        
        x_pos = np.where(self.grid == x)
        y_pos = np.where(self.grid == y)
        
        # replace row
        if x_pos[0][0] == y_pos[0][0]: # rows are the same
            x = self.get_left(x_pos)
            y = self.get_left(y_pos)    
            
        # replace column
        elif x_pos[1][0] == y_pos[1][0]:
            x = self.get_up(x_pos)
            y = self.get_up(y_pos)
            
        # replace rectangle
        else:
            x, y = self.get_from_rect(x_pos, y_pos)
            
        return f'{x}{y}'
        
    def encrypt(self, plaintext):
        if not self.__kw:
            raise TypeError("Keyword cannot be None")

        self.grid = self.get_grid()
        
        if plaintext == "":
            return f"The plaintext is empty {self.__kw}"
        
        print("\n\nEncryption Process")
        print(f'Plaintext: {plaintext}')
        cipher_text = ""
        plaintext = plaintext.replace('j', 'i')
        plaintext = plaintext.replace(' ', '')
        plaintext = plaintext.upper()
        
        idx = 0 # index to keep track where we parsing the plaintext
        
        # Iterate over plaintext
        while idx <= len(plaintext)-1:
            if (idx+1 > len(plaintext)-1):
                pair = (plaintext[idx], "X")
                
            # two characters are the same
            elif ( plaintext[idx] == plaintext[idx+1] ):
                pair = (plaintext[idx], "X")
                idx += 1
            
            # different characters
            elif ( plaintext[idx] != plaintext[idx+1]):
                pair = (plaintext[idx], plaintext[idx+1])
                idx += 2
            else:
                raise ValueError("Wrong iteration of the characters")
            cipher_text += self.en_substitute(pair)
        return cipher_text
    
    def decrypt(self, cipher_text, kw=None):
        '''
            Decryption of a cipher text doing the reverse 
            of the Playfair cipher encryption
        '''
        print("\n\nDecryption Process")
        print(f'Cipher Text: {cipher_text}')
        
        if kw is not None:
            self.set_kw(kw)
        elif not self.__kw:
            raise TypeError(f'Keyword cannot be {type(self.__kw)}')
            
        
        
        idx = 0 # index to keep track where we parsing the plaintext
        self.grid = self.get_grid()
                
        # Iterate over plaintext
        plaintext = ""
        
        for idx in range(0, len(cipher_text), 2):
            # get x and y
            x, y = cipher_text[idx], cipher_text[idx+1]
            
            # swap letters
            plaintext += self.de_substitute((x,y))
        return plaintext
        

pf = PlayFair()
pf.set_kw("holy")
cipher_text = pf.encrypt("Hello")
print(pf.grid)
print(f'cipher_text: {cipher_text}')

pf2 = PlayFair("holy")
plaintext = pf2.decrypt("YBYWYL")
print(f'plaintext is {plaintext}')


