'''
Created on 11-Mar-2017

@author: murtraja
'''

        
        
class AES_Decryptor:
    '''
    this class deals with decrypting 128 bit AES in ECB
    mode, the input is cipher text(ord format) and key(ord format)
    '''
    def __init__(self, cipher, key):
        self.cipher_text = cipher
        self.key=key
        self.round_key_arrays = []
        self.make_arrays()
        self.step_shift_rows(self.state_array[0])
        
    def step_inv_sbox(self, grid):
        size = 4
        inverted_grid = [[self.lookup_sbox(grid[i][j]) for j in range(size)] for i in range(size)]
        return inverted_grid
    
    def step_add_round_key(self, grid, round_key):
        new_grid = [[grid[i][j] ^ round_key[i][j] for j in range(len(grid))] for i in range(len(grid))]
        return new_grid
    
    def step_shift_rows(self, grid):
        new_grid = [self.rotate_byte_left(grid[i], i) for i in range(len(grid))]
        return new_grid

import base64
cipher = map(ord, base64.decodestring(open('c07.txt').read()))
key = "YELLOW_SUBMARINE"
key = map(ord, key)
decryptor = AES_Decryptor(cipher,key)
decryptor.make_arrays()









