from abc import ABC, abstractmethod


class Hero:
    def __init__(self):
        self.positive_effects = []
        self.negative_effects = []

        self.stats = {
            "HP": 128,
            "MP": 42,
            "SP": 100,

            "Strength": 15,
            "Perception": 4,
            "Endurance": 8,
            "Charisma": 2,
            "Intelligence": 3,
            "Agility": 8,
            "Luck": 1
        }

    def get_positive_effects(self):
        return self.positive_effects.copy()

    def get_negative_effects(self):
        return self.negative_effects.copy()

    def get_stats(self):
        return self.stats.copy()


class AbstractEffect(Hero, ABC):
    def __init__(self, base):
        self.base = base

    def get_stats(self):
        pass

    def get_positive_effects(self):
        pass

    def get_negative_effects(self):
        pass


class AbstractPositive(AbstractEffect):
    def get_positive_effects(self):
        self.base.get_positive_effects()


class Berserk(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['berserk']


class Blessing(AbstractPositive):
    def get_positive_effects(self):
        return self.base.get_positive_effects() + ['blessing']


hero = Hero()
berserk = Berserk(hero)
blessing = Blessing(berserk)
print(hero.get_positive_effects())
print(berserk.get_positive_effects())
print(blessing.get_positive_effects())

blessing.base = blessing.base.base

print(hero.get_positive_effects())
print(berserk.get_positive_effects())
print(blessing.get_positive_effects())