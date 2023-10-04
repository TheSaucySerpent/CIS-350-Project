#Currently only needed as a parent to weapons, doesn't do anything.

class Item:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

class HealthPack(Item):
    #Amount we want to heal
    amount = 50;
    def __init__(self, amount, owner):
        self.heal(amount)
class AmmoPack(Item):
    #Amount of ammo we want to add
    amount = 1;
    def __init__(self,amount,owner):
        self.addAmmo(amount)
