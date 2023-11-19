from item import *
from enchant import *

class Economy:
    def __init__(self, filename:str):
        self.items:dict[str,Item] = {}
        # Parsing file
        tokens:list[list[str]] = []
        file = open(filename, "r")
        for line in file.readlines():
            # We can comment with symbol '#'
            # We can write empty lines
            if line[0] == '#' or len(line) < 2:
                continue
            tokens.append([])
            line = line.split(',')
            for x in line:
                tokens[-1].append(x)
            tokens[-1][-1] = tokens[-1][-1][:-1]
        file.close()
        # Parsing tokens
        for line in tokens:
            price:float = 0.0
            if line[0] in self.items.keys():
                # If the item has multiple definition : raise a specific error
                raise ItemDoubleDefinition(f"{line[0]} has multiple definition")
            self.items[line[0]] = Item(line[0])
            try:
                price = float(line[1])
                self.items[line[0]].price = price
            except IndexError:
                # If the user just put one string without any ',' : raise a specific error
                raise ItemBadDefinition(f"{line[0]} has a bad definition : missing price or ingredients argument")
            except ValueError:
                # If the second argument is not a number, this item is not raw :
                for ingredient in line[1:]:
                    ing = ingredient.split(":")
                    if len(ing) != 2:
                        raise IngredientBadDefinition(f"Ingredient of {line[0]} has a bad definition")
                    try:
                        self.items[line[0]].addMaterial(self.items[ing[0]], float(ing[1]))
                    except ValueError:
                        raise IngredientQuantityBadDefinition(f"Ingredient {ing[0]}'s quantity of item {line[0]} has a bad definition")
                    except KeyError:
                        raise UndefinedIngredient(f"Ingredient {ing[0]} is not defined")
    def item(self, itemname:str) -> Item:
        try:
            return self.items[itemname]
        except KeyError:
            raise UndefinedItem(f"{itemname} is not defined in the economy")
    def __str__(self) -> str:
        string = ""
        for item in self.items.values():
            string += str(item)
        return string

economy:Economy = Economy("items.txt")

if __name__=="__main__":
    print("A Diamond Pickaxe with enchantments Efficiency 3, Unbreaking 3 and Fortune 2 costs :")
    print(economy.item("Diamond Pickaxe").getPrice({enchantments["ef"]:3 , enchantments["un"]:3 , enchantments["fo"]:2}))