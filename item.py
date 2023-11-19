from enchant import *

class Item:
    def __init__(self, name:str, price:float = 0.0):
        self.name:str = name
        self.price:float = price
        self.ingredients:dict[Item,float] = dict()
    def isRaw(self) -> bool:
        return len(self.ingredients) <= 0
    def makeRaw(self, price:float = 0.0):
        self.ingredients.clear()
        self.price = price
    def isFree(self) -> bool:
        return self.price <= 0
    def updatePrice(self, new_price:float = -1.0):
        if not(self.isRaw):
            self.price = 0.0
            for item,number in self.ingredients.items():
                item.updatePrice()
                self.price += number * item.price
        else:
            self.price = new_price if new_price >= 0.0 else self.price
    def addMaterial(self, item, q:float):
        self.ingredients[item] = q
        self.price += q * item.price
    def getPrice(self, enchants:dict = {}) -> float:
        self.updatePrice()
        price = self.price
        for enchant,level in enchants.items():
            price += enchant.getPrice(level)
        return price
    def __str__(self) -> str:
        string = self.name
        if self.isRaw():
            string += " is an ingredient " + str(self.price) + " EOs worth\n"
        else:
            string += " is an item " + str(self.price) + " EOs worth made of:\n"
            for item,number in self.ingredients.items():
                string += " - " + str(number) + " " + item.name + "\n"
        return string

if __name__=="__main__":
    raise ExceptionFileExecuted