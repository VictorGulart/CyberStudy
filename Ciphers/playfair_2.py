import numpy as np
import string
import random

class PlayFair():
    
    def gen_bigrams(self, plaintext, null) -> str:
        bigram = ""
        
        i = 0
        while i < len(plaintext):
            
            if i == len(plaintext)-1 or plaintext[i] == plaintext[i+1]:
                bigram += plaintext[i].upper() + null
                i += 1
            else:
                bigram += plaintext[i:i+2]
                i += 2
            
        return bigram
    
    def substitution(self, plaintext, key, null):
        '''
            Applies the substituition of the Playfair cipher
            
            The method is separate from the encryption methods
            to avoid repetition. 
            
            So that the plaintext can be treated differently 
            depending on the ciphering method.
        '''
        
        # final cipher
        cipher_text = ""
        bigram = self.gen_bigrams(plaintext, null)
        
        for i in range(0, len(bigram), 2): # goes 2 by two
            
            # Gets the letters
            l1 = bigram[i]
            l2 = bigram[i+1]
            
            
            # Positions
            l1_pos = np.where(key == l1)
            l2_pos = np.where(key == l2)

            # print(f'L1: {l1} \t L2: {l2}')
            # print(f'L1 pos ({l1_pos[0][0]},{l1_pos[1][0]})\tL2 pos ({l2_pos[0][0]},{l2_pos[1][0]})')

            # Transformation
            if l1_pos[0][0] == l2_pos[0][0]: # same row
                cipher_text += key[l1_pos[0][0]][(l1_pos[1][0]+1) % len(key)] # move x position
                cipher_text += key[l2_pos[0][0]][(l2_pos[1][0]+1) % len(key)] # move x position
            
            elif l1_pos[1][0] == l2_pos[1][0]: # same column
                cipher_text += key[(l1_pos[0][0]+1) % len(key)][l1_pos[1][0]] # move y position
                cipher_text += key[(l2_pos[0][0]+1) % len(key)][l2_pos[1][0]] # move y position
                
            else: # different columns and rows
                cipher_text += key[l1_pos[0][0]][l2_pos[1][0]] # move x to l2_x position
                cipher_text += key[l2_pos[0][0]][l1_pos[1][0]] # move x to l1_x position
        
        return cipher_text
    
    def gen_key(self, keyword) -> list:
        ''' A key is generated from a keyword. It is a grid'''
        msg = "".join(dict.fromkeys(keyword.upper() + string.ascii_uppercase.replace("J", ""))) # create unique dictionary and joins it, keeps order
        key = [ list(msg[i:i+5]) for i in range(0, len(msg), 5)]
        
        return np.array(key).reshape((5,5))  
    
    def encrypt(self, plaintext, key) -> str:
        ''' 
            Algorightm to perform conventional Playfair cipher
        '''
        assert len(key)==5, "The key matrix must be (5x5)"
        # replace things 
        plaintext = plaintext.replace(" ", "")
        plaintext = plaintext.replace("J", "I")
        plaintext = plaintext.upper()

            
        return self.substitution(plaintext, key, "X")
    
    def decrypt(self, cipher_text, key) -> str:
        
        # assert len(key) == 5, "Key Matrix must be (5x5)"
        
        plaintext = ""
        for i in range(0, len(cipher_text), 2): # goes 2 by two
            
            # Gets the letters
            l1 = cipher_text[i]
            l2 = cipher_text[i+1]
            
            
            # Positions
            l1_pos = np.where(key == l1)
            l2_pos = np.where(key == l2)

            # print(f'L1: {l1} \t L2: {l2}')
            # print(f'L1 pos ({l1_pos[0][0]},{l1_pos[1][0]})\tL2 pos ({l2_pos[0][0]},{l2_pos[1][0]})')

            # Transformation
            if l1_pos[0][0] == l2_pos[0][0]: # same row
                plaintext += key[l1_pos[0][0]][(l1_pos[1][0]-1) % len(key)] # move x position
                plaintext += key[l2_pos[0][0]][(l2_pos[1][0]-1) % len(key)] # move x position
            
            elif l1_pos[1][0] == l2_pos[1][0]: # same column
                plaintext += key[(l1_pos[0][0]-1) % len(key)][l1_pos[1][0]] # move y position
                plaintext += key[(l2_pos[0][0]-1) % len(key)][l2_pos[1][0]] # move y position
                
            else: # different columns and rows
                plaintext += key[l1_pos[0][0]][l2_pos[1][0]] # move x to l2_x position
                plaintext += key[l2_pos[0][0]][l1_pos[1][0]] # move x to l1_x position
        
        return plaintext
    
    def nxn_gen_key(self, key, n, k2=None):
        ''' 
            Create a key matrix (nxn), where n>=10
            
            Base is 94 characters, hence matrix must be n>=10
        '''
        assert n>= 10, "Matrix size must be greater then or equal to (10x10)"
        base = [*string.ascii_lowercase, *string.digits, *string.ascii_uppercase, *string.punctuation]

        # Fill the base matrix until it fits the criteria
        counter = 0
        line = 1
        while len(base) != (n*n):
            if counter == 26: # using 26 because of the size of the alphabet
                line += 1
                counter = 0
            base.append( f'{string.ascii_lowercase[counter]}{line}')
            counter += 1

        # Clean the Keyword (k1) and create the permutation (k2)
        k1 = "".join(dict.fromkeys(key.replace(" ", "")))
        
        if not k2:
            k2= random.sample(range(0,n), n) # random permutation

        # Create the Key Matrix
        mx = np.array(list(dict.fromkeys(list(k1) + base))).reshape((n,n))

        # Permute and Transpose the Key Matric
        mx = mx[k2,:]
        mx= mx.T
    
        return mx
    
    def nxn_encrypt(self, plaintext, key):
        '''
            Method to perform (n x n) Playfair cipher
        '''
        assert key.shape[0] == key.shape[1], "Key Matrix must be square"
        
        # Remove spaces
        plaintext = plaintext.replace(" ", "")
        
        return self.substitution(plaintext, key, "^")

if __name__ == "__main__":
    # Using with normal playfair 5x5 grid
    pf = PlayFair()
    pf_key = pf.gen_key("holy")
    plaintext = "I will meet you there"
    pf_cipher = pf.encrypt(plaintext, pf_key)
    text_decrypted = pf.decrypt(pf_cipher, pf_key)
    print('Plaintext => ', plaintext)
    print('Cipher Text => ', pf_cipher)
    print('Decrypted Plaintext => ', text_decrypted)


    # NxN grid example
    k1 = "Cyber Security Is Key"
    k2 = [16, 8, 19, 1, 3, 0, 9, 14, 6, 17, 18, 2, 5, 15, 4, 11, 12, 7, 13, 10]
    n = 20

    # Key Matrix Generation
    nxn_key_matrix = pf.nxn_gen_key(k1, n, k2)

    # Plaintext and Cipher Text
    plaintext = "A cipher that can withstand cryptoanalysis."
    cipher  = pf.nxn_encrypt(plaintext, nxn_key_matrix)

    # Decryption of the Cipher Text
    text_decrypted = pf.decrypt(cipher, nxn_key_matrix)

    print('Plaintext => ', plaintext)
    print('Cipher Text => ', cipher)
    print('Decrypted plaintext => ', text_decrypted)
