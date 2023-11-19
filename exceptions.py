class BadEnchantmentLevel(Exception):
    pass
class ItemDoubleDefinition(Exception):
    pass
class ItemBadDefinition(Exception):
    pass
class IngredientBadDefinition(Exception):
    pass
class IngredientQuantityBadDefinition(Exception):
    pass
class UndefinedIngredient(Exception):
    pass
class UndefinedItem(Exception):
    pass
class EnchantDoubleDefinition(Exception):
    pass
class ExceptionFileExecuted(Exception):
    pass

if __name__=="__main__":
    raise ExceptionFileExecuted