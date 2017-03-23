'''
Created on 11-Mar-2017

@author: murtraja
'''

import common
import keygen
        
        
class AES_Decryptor:
    '''
    this class deals with decrypting 128 bit AES in ECB
    mode, the input is cipher text(ord format) and key(ord format)
    '''
    def __init__(self, cipher, key):
        self.cipher_text = cipher
        self.common = common.Common_Operations()
        self.key=self.common.divide_bytes_into_grids(key)[0]
        self.keygen = keygen.Round_Key_Generator()
        self.round_keys = self.keygen.get_round_keys(self.key)
#         self.keygen.pg(self.round_keys)
        g = [[0x04,0xe0, 0x48, 0x28],[0x66,0xcb,0xf8,0x06],[0x81,0x19,0xd3,0x26],[0xe5,0x9a,0x7a,0x4c]]
        self.common.pg([g])
        self.common.pg([self.step_inv_mix_columns(g)])
        
    def step_inv_sbox(self, grid):
        size = 4
        inverted_grid = [[self.lookup_sbox(grid[i][j]) for j in range(size)] for i in range(size)]
        return inverted_grid
    
    def step_add_round_key(self, grid, round_key):
        new_grid = [[grid[i][j] ^ round_key[i][j] for j in range(len(grid))] for i in range(len(grid))]
        return new_grid
    
    def step_inv_shift_rows(self, grid):
        size = 4
        new_grid = [self.rotate_byte_left(grid[i], size-1-i) for i in range(len(grid))]
        return new_grid
    
    def step_inv_mix_columns(self, grid):
        columns = [[grid[i][j] for i in range(len(grid))] for j in range(len(grid[0]))]
        matrix = self.common.make_matrix_for_mixcolumns([14,11,13,9])
        new_columns = []
        for column in columns:
            new_column = self.common.multiply_matrix_for_mixcolumns(matrix, column)
            new_columns.append(new_column)
        new_grid = [[new_columns[i][j] for i in range(len(new_column))] for j in range(len(new_columns[0]))]
        return new_grid
                                                                                       

import base64
cipher = map(ord, base64.decodestring(open('c07.txt').read()))
key = "YELLOW_SUBMARINE"
key = map(ord, key)
decryptor = AES_Decryptor(cipher,key)










