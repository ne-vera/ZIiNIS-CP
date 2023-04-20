class Grain:
    def __init__(self, key, iv):
        self.INITCLOCKS = 160
        self.NFSR = [0] * 80
        self.LFSR = [0] * 80
        self.NFTable = [
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,0,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,1,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,1,
            1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,0,0,1,0,0,1,0,1,1,1,1,1,0,1,1,1,1,
            0,1,0,0,1,0,1,1,1,1,1,0,0,0,0,1,0,1,0,0,1,0,1,1,1,1,1,0,1,1,1,1,
            1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,0,1,1,0,1,0,0,0,1,0,0,1,0,1,1,1,0,1,1,1,0,1,0,
            0,1,0,0,1,0,1,1,1,1,1,0,0,0,0,1,1,0,1,1,0,1,0,0,0,0,0,1,0,0,0,0,
            1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,1,0,0,0,0,0,1,1,1,1,1,
            0,1,0,0,1,0,0,0,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,
            1,0,1,1,0,1,1,1,0,1,0,0,1,0,0,0,1,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,
            1,0,1,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,1,1,0,1,1,0,0,
            0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,0,0,1,0,0,1,0,0,0,1,1,1,0,1,1,0,0,
            1,0,1,1,0,1,1,1,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0,1,1,1,0,0,1,
            0,1,0,0,1,0,0,0,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,1,0,1,0,0,0,1,1,0,
            1,0,1,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,1,1,0,1,1,0,0,
            1,0,1,1,0,1,1,1,0,0,0,1,1,1,0,1,0,1,0,0,1,0,0,0,1,1,1,0,0,0,1,1
        ]
        self.boolTable = [0,0,1,1,0,0,1,0,0,1,1,0,1,1,0,1,1,1,0,0,1,0,1,1,0,1,1,0,0,1,0,0]
        self.keysize = 80
        self.ivsize = 64

        # Convert string key 00000000 to [k1, k2, k3]
        key = [key[i:i + 2] for i in range(0, len(key), 2)]
        self.key = [int(i, 16) for i in key]
        
        # Convert string iv 00000 to [iv1, iv2]
        iv = [iv[i:i + 2] for i in range(0, len(iv), 2)]
        self.iv = [int(i, 16) for i in iv]
        
        # ivsetup, load registers
        for i in range(self.ivsize//8):
            for j in range(8):
                self.NFSR[i * 8 + j] = (self.key[i] >> j) & 1
                self.LFSR[i * 8 + j] = (self.iv[i] >> j) & 1
        for i in range(self.ivsize//8, self.keysize//8):
            for j in range(8):
                self.NFSR[i * 8 + j] = (self.key[i] >> j) & 1
                self.LFSR[i * 8 + j] = 1
        
        for i in range(self.INITCLOCKS):
            outbit = self.keystream()
            self.LFSR[79] ^= outbit
            self.NFSR[79] ^= outbit
    
    def N(self, i):
        return self.NFSR[80 - i]

    def L(self, i):
        return self.LFSR[80 - i]

    def keystream(self):
        X0 = self.LFSR[3]
        X1 = self.LFSR[25]
        X2 = self.LFSR[46]
        X3 = self.LFSR[64]
        X4 = self.NFSR[63]
    
        # Calculate feedback and output bits
        outbit = self.N(79)^self.N(78)^self.N(76)^self.N(70)^self.N(49)^self.N(37)^self.N(24)^self.boolTable[(X4<<4) | (X3<<3) | (X2<<2) | (X1<<1) | X0]
        NBit = self.L(80)^self.N(18)^self.N(66)^self.N(80)^self.NFTable[(self.N(17)<<9) | (self.N(20)<<8) | (self.N(28)<<7) | (self.N(35)<<6) | (self.N(43)<<5) | (self.N(47)<<4) | (self.N(52)<<3) | (self.N(59)<<2) | (self.N(65)<<1) | self.N(71)]
        LBit = self.L(18)^self.L(29)^self.L(42)^self.L(57)^self.L(67)^self.L(80)

        # Update register
        for i in range(1, self.keysize):
            self.NFSR[i - 1] = self.NFSR[i]
            self.LFSR[i - 1] = self.LFSR[i]

        
        self.NFSR[self.keysize - 1] = NBit
        self.LFSR[self.keysize - 1] = LBit        

        return outbit

    def keystream_bytes(self, msglen):
        keystream = [0] * msglen
        for i in range(msglen):
            for j in range(8):
                outbit = self.keystream()
                outbit <<= j
                keystream[i] = keystream[i] | outbit
        return keystream

    def encrypt(self, msg):
        keystream = self.keystream_bytes(len(msg))
        
        cipher = [x^y for x,y in zip(msg, keystream)]

        return cipher
    
    def decrypt(self, msg):
        keystream = self.keystream_bytes(len(msg))
        
        plain = [x^y for x,y in zip(msg, keystream)]

        return plain



#grain = Grain('80000000000000000000', '0000000000000000')

#print grain.keystream_bytes(2)