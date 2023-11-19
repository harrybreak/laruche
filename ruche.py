from economy import *

'''
CODE SOURCE DU BOT BERNARD TAONPIE    
'''

# Listes opérateurs
operateurs:list = []
operateursNom:list = []

# Les bibliothèques
from math import *
import discord

# Le token secret :)
token:str = ""

# La fonction de load/reload
def loadbdd() -> bool:
    global token
    global operateurs
    global operateursNom
    fichier = open("token.txt", "r")
    token = fichier.readline()
    fichier.close()
    admin = open("operator.txt", "r")
    for line in admin.readlines():
        try:
            line = line.split(',',2)
            operateurs.append(int(line[1][:-1]))
            operateursNom.append(line[0])
        except Exception:
            return False
    admin.close()
    return True

# Elle retourne False ou True selon si l'exécution échoue ou non
def savebdd() -> bool:
    admin = open("operator.txt", "w")
    try:
        for i in range(len(operateurs)):
            admin.write(operateursNom[i]+","+str(operateurs[i])+"\n")
    except Exception:
        return False
    admin.close()
    return True

# La fonction de tentative d'envoi sur un channel privé
async def sendto(message:discord.Message, content:str) -> bool:
    try:
        await message.author.send(content)
        return True
    except discord.Forbidden:
        await message.channel.send(content)
        return True
    except AttributeError:
        return False

# La fonction de tentative de suppression de message
async def trydelmsg(message:discord.Message) -> bool:
    try:
        await message.delete()
        return True
    except discord.Forbidden:
        return False

def isNumber(string:str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False

print("==========================================================")
print("Lecture des données dans la base de données ...")
loadbdd()
print("==========================================================")
print("Configuration du bot...")
# Configuration du reboot du bot
instance_intents = discord.Intents.default()
instance_intents.members = True

# Reboot du bot
client:discord.Client = discord.Client(intents=instance_intents)
@client.event
async def on_ready():
    data = discord.Game("Ministre de l'Economie de La Ruche")
    await client.change_presence(activity = data)
    print("==========================================================")
    print("Le bot est connecté !")
    
@client.event
async def on_message(message:discord.Message):
    '''
    COMMAND SECTION
    '''
    if message.content.startswith("&"):
        if message.content.split()[0] == "&prix":
            tokens = message.content.split()[1:]
            try:
                index:int = 0
                itemname:str = ""
                while index < len(tokens) and not(isNumber(tokens[index])):
                    itemname += tokens[index] + " "
                    index += 1
                itemname = itemname[:-1]
                if index >= len(tokens):
                    # Neither quantity nor enchant provided
                    price:float = economy.item(itemname).getPrice()
                    await message.channel.send(f'__Prix minimal :__ **{price:9.2f} EOs**')
                else:
                    quantity:int = int(tokens[index])
                    if index + 1 == len(tokens):
                        price:float = quantity * economy.item(itemname).getPrice()
                        await message.channel.send(f'__Prix minimal :__ **{price:9.2f} EOs**')
                    else:
                        # Both quantity and enchantment provided
                        enchants:dict = {}
                        index += 1
                        while index < len(tokens):
                            code:str = tokens[index]
                            index += 1
                            niveau:int = int(tokens[index])
                            index += 1
                            enchants[enchantments[code]] = niveau
                        price:float = quantity * economy.item(itemname).getPrice(enchants)
                        await message.channel.send(f'__Prix minimal :__ **{price:9.2f} EOs**')
            except BadEnchantmentLevel as e:
                await message.channel.send(str(e))
            except ItemDoubleDefinition as e:
                await message.channel.send(str(e))
            except ItemBadDefinition as e:
                await message.channel.send(str(e))
            except IngredientBadDefinition as e:
                await message.channel.send(str(e))
            except IngredientQuantityBadDefinition as e:
                await message.channel.send(str(e))
            except UndefinedIngredient as e:
                await message.channel.send(str(e))
            except UndefinedItem as e:
                await message.channel.send(str(e))
            except EnchantDoubleDefinition as e:
                await message.channel.send(str(e))
            except ExceptionFileExecuted as e:
                await message.channel.send(str(e))
            except Exception as e:
                await message.channel.send("**Erreur de syntaxe !** Tapez ``&aide prix`` pour obtenir de l'aide.")
                print(e)
        if message.content.split()[0] == "&cmds":
            information = "__Les commandes d'administration :__\n"
            information += "``&upg`` : donner des droits\n"
            information += "``&dwng``: retirer des droits\n"
            information += "``&save``: sauvegarder la base de données\n"
            information += "``&kill``: éteindre le bot\n"
            information += "``&test``: lancer l'exécution de déboggage\n"
            information += "__Les commandes d'utilisation :__\n"
            information += "``&prix``: connaître le prix d'un item\n"
            information += "``&cmds``: vous venez de le faire :D\n"
            information += "``&aide``: obtenir de l'aide\n"
            information += "``&info``: voir plus d'information\n"
            await sendto(message, information)
        elif message.content.split()[0] == "&aide":
            information = ""
            if len(message.content.split()) > 1 and message.content.split()[1] == "prix":
                information += "__**Utiliser la commande**__ ``&prix`` \n\n"
                information += "``&prix <nom complet de l'item> [quantité] [enchantements]``\n\n"
                information += "__**Exemple :**__\n\n"
                information += "``&prix Netherite Pickaxe 1 ef 5 me 1 un 3 fo 3``\n\n"
                information += "Dans l'exemple ci-dessus, il est demandé le prix d'**1 pioche en netherite** enchantée :\n"
                information += " + **Efficacité** (*ef*) **V** (*5*)\n"
                information += " + **Raccomodage** (*me*) **I** (*1*)\n"
                information += " + **Solidité** (*un*) III (*3*)\n"
                information += " + **Fortune** (*fo*) III (*3*)\n\n"
                information += "De manière générale, voici les principales modalités de ``&prix`` :\n"
                information += " + Le __nom__ de l'item doit être donné en **anglais** et en **entier** (y compris les espaces).\n"
                information += " + La quantité (en nombre entier) doit être donné après le nom de l'item\n"
                information += " + Chaque enchantement est donné sous la forme ``<code> <niveau>``"
                information += "où **code** est le code de l'enchantement (voir paragraphe suivant)\n"
                information += " + Chaque enchantement est séparé par un espace\n"
                information += " + La quantité et les enchantements sont optionnels\n\n"
                information += "__**Le code d'un enchantement :**__\n"
                information += "Le code d'un enchantement est composé de ses deux premières lettres du nom en anglais.\n"
                information += "Exemple : **Chatîment** --> ``sm`` (car *Smite* en anglais)\n"
                information += "**Si** l'enchantement est composé de plusieurs mots, le code est alors\n"
                information += "composé des deux principales initiales.\n"
                information += "Exemple : **Fléau des Arthropodes** --> ``ba`` (car *Bane of Arthropods* en anglais)\n"
                information += "**Exception** pour les enchantements suivants :\n"
                information += " + **Swift Sneak** : ``sw``\n"
                information += " + **Soul Speed** : ``so``\n"
                information += " + **Loyalty** : ``loy``\n"
                information += " + **Looting** : ``loo``\n"
            else:
                information += "__Je suis Bernard Taonpie, Ministre de l'Economie de La Ruche :__\n"
                information += "Vous pouvez consulter les commandes disponibles avec ``&cmds``\n"
                information += "Pour en savoir plus la commande ``&prix``, tapez ``&aide prix``\n"
                information += "Pour en savoir plus sur moi : ``&info``\n"
            await sendto(message, information)
        elif message.content.split()[0] == "&info":
            information = "__**Bernard Taonpie**__\n"
            information += "Je suis open source ! Vous pouvez contribuer au projet si vous le souhaitez!\n"
            information += "Compétences nécessaires : **Python3.10**, le module **Discordpy** et **Git**.\n"
            information += "__Source code :__ https://github.com/harrybreak/laruche\n"
            information += "__Version :__ alpha-20.11.23\n"
            information += "__Programmé par :__\n"
            information += " + HarryBreak\n"
            await sendto(message, information)
        elif message.content.split()[0] == "&upg":
            if message.author.id in operateurs:
                contenu = message.content.split()
                if len(contenu) == 1 or (len(contenu) == 2 and contenu[1] == "help"):
                    information = "Voici la liste des opérateurs:\n"
                    for i in operateursNom:
                        information += "+ " + str(i) + "\n"
                    information += "Pour augmenter des utilisateurs, suivez cette commande de leur @pseudo."
                    await message.author.send(information)
                elif len(contenu) > 1 and len(message.mentions) == 0:
                    await message.author.send("**Erreur d'identification** ! Impossible d'augmenter les utilisateurs indiqués !")
                else:
                    information = "Les utilisateurs suivants sont dorénavant des opérateurs :\n"
                    for i in message.mentions:
                        if not(i.id in operateurs):
                            operateurs.append(i.id)
                        if not(i.name in operateursNom):
                            operateursNom.append(i.name)
                            information += "+ " + i.name + "\n"
                    await message.author.send(information)
            else:
                await message.author.send("**Erreur de permission** ! Cette opération nécessite une élévation.")
        elif message.content.split()[0] == "&dwng":
            if message.author.id in operateurs:
                contenu = message.content.split()
                if len(contenu) == 1 or (len(contenu) == 2 and contenu[1] == "help"):
                    await message.author.send("Pour retirer les privilèges d'opérateur de plusieurs utilisateurs, suivez cette commande de leur @pseudo")
                elif len(contenu) > 1 and len(message.mentions) == 0:
                    await message.author.send("**Erreur d'identification** ! Impossible d'identifier les utilisateurs indiqués !")
                else:
                    information = "Les utilisateurs suivants ne jouissent dorénavant plus des privilèges d'opérateur :\n"
                    for i in message.mentions:
                        try:
                            operateurs.remove(i.id)
                            operateursNom.remove(i.name)
                        except ValueError:
                            information += "+ " + i.name + "  *(était déjà dépourvu des privilèges)*" + "\n"
                        else:
                            information += "+ " + i.name + "\n"
                    information += "Pour leur redonner accès aux fonctions d'opérateur, utilisez la commande ``&upg``."
                    await message.author.send(information)
            else:
                await message.author.send("**Erreur de permission** ! Cette opération nécessite une élévation.")
        ## KILL COMMAND
        elif message.content.split()[0] == "&kill":
            if message.author.id in operateurs:
                await message.author.send("**FERMETURE D'URGENCE DANS 5 SECONDES**")
                await client.close()
            else:
                await message.author.send("**Erreur de permission** ! Cette opération nécessite une élévation.")
        ## TEST COMMAND
        elif message.content.split()[0] == "&test":
            if message.author.id in operateurs:
                await sendto(message, "what are you branling?")
            else:
                await message.author.send("**Erreur de permission** ! Cette opération nécessite une élévation.")
        ## SAVE COMMAND
        elif message.content.split()[0] == "&save":
            if message.author.id in operateurs:
                if savebdd():
                    await message.author.send("Base de donnée sauvegardée !")
                else:
                    await message.author.send("**Echec de la sauvegarde !**")
            else:
                await message.author.send("**Erreur de permission** ! Cette opération nécessite une élévation.")
        ## UNRECOGNIZED COMMAND
        else:
            pass
    '''
    END OF COMMAND SECTION
    '''
        

# Run le client
client.run(token)

# Lors de l'exécution du client
print("==========================================================")
print("Sauvegarde de la base de données en cours ...")
savebdd()
print("Sauvegarde terminée avec succès !")
print("Le bot a bien été déconnecté !")