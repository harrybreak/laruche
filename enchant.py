from exceptions import *

class Enchant:
    def __init__(self, name:str, maxlvl:int, price:float):
        self.name:str = name
        self.maxlvl:int = maxlvl
        self.price:float = price
    def getPrice(self, lvl:int) -> float:
        if lvl < 1:
            raise BadEnchantmentLevel(f"{lvl} is not valid for enchant's level")
        return self.price * (lvl/self.maxlvl)
    def __str__(self) -> str:
        return "Enchantment " + self.name + " has maximum level of " + str(self.maxlvl) + " " + str(self.price) + " worth\n"

class EnchantSet(dict):
    def __init__(self, filename:str):
        fichier = open(filename, "r")
        for line in fichier.readlines():
            line = line.split(',')
            if line[1] in self.keys():
                raise EnchantDoubleDefinition(f"{line[0]} has multiple definition")
            self[line[1]] = Enchant(line[0], int(line[2]), float(line[3][:-1]))
        fichier.close()

enchantments:EnchantSet = EnchantSet("enchants.txt")

if __name__=="__main__":
    raise ExceptionFileExecuted