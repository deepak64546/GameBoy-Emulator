from ..cartridge import Cartridge

class MBC1(Cartridge):
    def UpdateCache(self):
        self.OFF0 = (self.BANKSEL2 << 19) & ((self.NBANKS << 14) - 1) if self.BANKMODE else 0
        self.OFFN = ((self.BANKSEL2 << 19) | (self.BANKSEL << 14)) & ((self.NBANKS << 14) - 1)
        self.OFFR = ((self.BANKSEL2 & (self.NRAM - 1)) << 13) if self.BANKMODE else 0
    
    def OnWriteROM(self, address, data):
        case = (address >> 13) & 3
        
        if case == 0:   # RAME
            self.RAMENA = (data & 0x0F) == 0x0A
        elif case == 1: # ROMB
            self.BANKSEL = (data & 0x1F)
            if not self.BANKSEL:
                self.BANKSEL = 1
        elif case == 2: # SEL2
            self.BANKSEL2 = data & 3
        elif case == 3: # MODE
            self.BANKMODE = not not (data & 1)
        
        self.UpdateCache()
    