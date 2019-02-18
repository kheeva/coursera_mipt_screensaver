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
        self.effect_stats = {}

    def get_stats(self):
        return self._merge_stats(self.base.get_stats(), self.effect_stats)

    @abstractmethod
    def get_positive_effects(self):
        pass

    @abstractmethod
    def get_negative_effects(self):
        pass

    def _merge_stats(self, dict_1, dict_2):
        return {key: dict_1.get(key, 0) + dict_2.get(key, 0)
                for key in set(dict_1) | set(dict_2)}


class AbstractPositive(AbstractEffect):
    @abstractmethod
    def __init__(self, base):
        super().__init__(base)

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [self.__class__.__name__]

    def get_negative_effects(self):
        return self.base.get_negative_effects()

class AbstractNegative(AbstractEffect):
    @abstractmethod
    def __init__(self, base):
        super().__init__(base)

    def get_positive_effects(self):
        return self.base.get_positive_effects()

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [self.__class__.__name__]


class Berserk(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)
        self.effect_stats = {
            "HP": 50,

            "Strength": 7,
            "Perception": -3,
            "Endurance": 7,
            "Charisma": -3,
            "Intelligence": -3,
            "Agility": 7,
            "Luck": 7
        }


class Blessing(AbstractPositive):
    def __init__(self, base):
        super().__init__(base)
        self.effect_stats = {
            "Strength": 2,
            "Perception": 2,
            "Endurance": 2,
            "Charisma": 2,
            "Intelligence": 2,
            "Agility": 2,
            "Luck": 2
        }


class Weakness(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.effect_stats = {
            "Strength": -4,
            "Endurance": -4,
            "Agility": -4,
        }


class EvilEye(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.effect_stats = {
            "Luck": -10,
        }


class Curse(AbstractNegative):
    def __init__(self, base):
        super().__init__(base)
        self.effect_stats = {
            "Strength": -2,
            "Perception": -2,
            "Endurance": -2,
            "Charisma": -2,
            "Intelligence": -2,
            "Agility": -2,
            "Luck": -2
        }



hero = Hero()
print(hero.get_stats(), hero.get_negative_effects(), hero.get_positive_effects())

berserk = Berserk(hero)
print(berserk.get_stats(), berserk.get_negative_effects(), berserk.get_positive_effects())

blessing = Blessing(berserk)
print(blessing.get_stats(), blessing.get_negative_effects(), blessing.get_positive_effects())

weakness = Weakness(blessing)
print(weakness.get_stats(), weakness.get_negative_effects(), weakness.get_positive_effects())

weakness.base.base = weakness.base.base.base

weakness = Weakness(blessing)
print(weakness.get_stats(), weakness.get_negative_effects(), weakness.get_positive_effects())
