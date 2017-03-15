'''
Created on 13-Mar-2017

@author: murtraja
'''
import itertools
class Common_Operations:
    '''
    this class contains all those operations which the encryption
    as well as decryption algorithms will use
    '''
    def __init__(self):
        self.inv_sbox = self.make_sbox("aes_inv_sbox.txt")
        self.sbox = self.make_sbox('aes_sbox.txt')
        self.rcon_values = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
        
    def make_sbox(self, file_name):
        with open(file_name) as sbox_file:
            space_separated = " ".join(sbox_file.read().split('\n'))
            sbox = [int(x, 16) for x in space_separated.split(' ')]
        return sbox
    
    def rotate_bytes_left(self, input_bytes, rotation_factor = 1):
        length = len(input_bytes)
        rotated_bytes = [input_bytes[(i+rotation_factor)%length] for i in range(length)]
        return rotated_bytes

    def rcon(self, i):
        return self.rcon_values[i]
    
    def lookup_inv_sbox(self, lookup_byte):
        sub_byte = self.inv_sbox[lookup_byte]
        return sub_byte
    
    def lookup_sbox(self, lookup_byte):
        sub_byte = self.sbox[lookup_byte]
        return sub_byte
    
    def divide_bytes_into_grids(self, input_bytes):
        block_row_size = 4
        block_total_size = block_row_size*block_row_size
        '''
        B B    B B    B B
        B B    B B    B B are grids
                
        B B
        B B is a block
        
        B B is the row in that block        
        
        '''
        grids = []
        for block in [input_bytes[i:i+block_total_size] for i in range(0,len(input_bytes),block_total_size)]:
            rows = []
            # now convert this block array to proper grid
            for row in [block[i:i+block_row_size] for i in range(0, len(block), block_row_size)]:
                rows.append(row)
            grids.append(rows)
        return grids
    
    def get_xor(self, array1, array2):
        # both arrays have bytes
        if len(array1) > len(array2):
            big_array = array1
            small_array = array2
        else:
            big_array = array2
            small_array = array1
        
        xored = [value1^value2 for (value1, value2) in zip(big_array, itertools.cycle(small_array))]
        
        return xored
        