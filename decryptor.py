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
        self.cipher = self.common.divide_bytes_into_grids(cipher)
#         self.keygen.pg(self.round_keys)
#         g = [[0x04,0xe0, 0x48, 0x28],[0x66,0xcb,0xf8,0x06],[0x81,0x19,0xd3,0x26],[0xe5,0x9a,0x7a,0x4c]]
#         self.common.pg([g])
#         self.common.pg([self.step_inv_mix_columns(g)])
        
    def step_inv_sbox(self, grid):
        size = 4
        inverted_grid = [[self.common.lookup_inv_sbox(grid[i][j]) for j in range(size)] for i in range(size)]
        return inverted_grid
    
    def step_add_round_key(self, grid, round_key):
        new_grid = [[grid[i][j] ^ round_key[i][j] for j in range(len(grid))] for i in range(len(grid))]
        return new_grid
    
    def step_inv_shift_rows(self, grid):
        size = 4
        new_grid = [self.common.rotate_bytes_left(grid[i], size-i) for i in range(len(grid))]
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
    def decrypt_block(self, grid):
        '''
        xpandkey128(key);

addroundkey(data,key,10);
rev_shiftrows(data);
rev_subbytes(data); 

for(int i = 9; i>= 1; i--) { 
    addroundkey(data,key,i);
    rev_mixColumn(data);
    rev_shiftrows(data);
    rev_subbytes(data); 
}

addroundkey(data,key,0);
'''
#         print "Now decrypting the block"
#         self.common.pg([grid])
        grid = self.step_add_round_key(grid, self.round_keys[-1])
        grid = self.step_inv_shift_rows(grid)
        grid = self.step_inv_sbox(grid)
        
        number_of_rounds = 9
        for r in range(number_of_rounds):
            grid = self.step_add_round_key(grid, self.round_keys[number_of_rounds - r])
            grid = self.step_inv_mix_columns(grid)
            grid = self.step_inv_shift_rows(grid)
            grid = self.step_inv_sbox(grid)
        grid = self.step_add_round_key(grid, self.round_keys[0])
#         print "to"
#         self.common.pg([grid])
        return grid
    
    def decrypt(self):
#         print "BEFORE:"
#         self.common.pg(self.cipher)
        decrypted_cipher = []
        for grid in self.cipher:
            decrypted_block = self.decrypt_block(grid)
            decrypted_cipher.append(decrypted_block)
#         print "AFTER:"
#         self.common.pg(decrypted_cipher)
        plaintext = self.get_plaintext(decrypted_cipher)
        return plaintext
    def get_plaintext(self, decrypted_cipher):
        plaintext = ""
        
        for grid in decrypted_cipher:
            size = len(grid)
            plaintext_grid = [ "".join( [ chr (grid[i][j]) for i in range(len(grid))]) for j in range(len(grid))]
            plaintext_grid = "".join(plaintext_grid)
            plaintext += plaintext_grid
        return plaintext      
        
                                                                                       

import base64
cipher = map(ord, base64.decodestring(open('c07.txt').read()))
# cipher = cipher[:16]
# cipher = base64.encodestring("".join(map(chr,cipher)))
key = "YELLOW SUBMARINE"
key = map(ord, key)

# cipher = [57, 2, 220, 25, 37, 220, 17, 106, 132, 9, 133, 11, 29, 251, 151, 50]
# key = [43, 40, 171, 9, 126, 174, 247, 207, 21, 210, 21, 79, 22, 166, 136, 60]


decryptor = AES_Decryptor(cipher,key)
print decryptor.decrypt()










