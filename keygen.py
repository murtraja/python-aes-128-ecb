'''
Created on 15-Mar-2017

@author: murtraja
'''
from common import Common_Operations

class Round_Key_Generator:
    '''
    given a key, this generates
    all the required keys for the
    rounds
    '''
    def __init__(self, key):
        # the key is in grid/block form
        self.key = key
        self.common = Common_Operations()
        
    def generate_key(self, previous_key, round_number):
        size = len(previous_key)
        last_column = [previous_key[i][size-1] for i in range(size)]
        
        
        # now move one element up
        last_column_rotated = self.common.rotate_bytes_left(last_column)
        
        # now replace every value with its inv_sbox value
        last_column_sub = map(self.common.lookup_sbox, last_column_rotated)
        
        # now perform the xor
        first_column = [previous_key[i][0] for i in range(size)]
        
        constant_xor = [0 for _ in range(size)]
        constant_xor[0] = self.common.rcon(round_number)
        
        last_column_xored = self.common.get_xor(last_column_sub, self.common.get_xor(first_column, constant_xor))
        
        new_key = [last_column_xored]
        
        for i in range(1, size):
            previous_column_new_key = new_key[-1]
            previous_column_previous_key = [previous_key[j][i] for j in range(size)]
            
            new_column_new_key = self.common.get_xor(previous_column_new_key, previous_column_previous_key)
            new_key.append(new_column_new_key)
        
        return [[new_key[i][j] for i in range(size)] for j in range(size)]

def pg(grid):
    pad = 2**8
    for row in grid:
        if type(row) is list:
            for col in row:
                print hex(col+pad)[3:],
        else:
            print hex(row+pad)[3:],
        print ""
previous_key = [[43, 40, 171, 9], [126, 174, 247, 207], [21, 210, 21, 79], [22, 166, 136, 60]]
round_number = 1
keygen = Round_Key_Generator(previous_key)
for r in range(1,11):
    new_key = keygen.generate_key(previous_key, r)
    pg(new_key)
    print "---end---",r
    previous_key = new_key
            
            
            
                  