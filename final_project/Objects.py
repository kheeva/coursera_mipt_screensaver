from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display):
        pass


class Interactive(ABC):
    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):
    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):
    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Effect(Hero):
    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


# FIXME
# add classes
class Berserk(Effect):
    def apply_effect(self):
        self.stats["strength"] += 4
        self.stats["endurance"] += 4
        self.stats["intelligence"] -= 4
        self.calc_max_HP()
        return self


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2
        self.calc_max_HP()
        return self


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 2
        self.stats["endurance"] -= 2
        self.stats["intelligence"] -= 2
        self.stats["luck"] -= 2
        self.calc_max_HP()
        return self


class Holy(Effect):
    def apply_effect(self):
        self.stats["intelligence"] += 1000
        return self


class Enemy(Creature):
    def __init__(self, icon, stats, xp, position, action):
        super().__init__(icon, stats, position)
        self.icon = icon
        self.stats = stats
        self.xp = xp
        self.position = position
        self.action = action

    def interact(self, engine, hero):
        if self.action is not None:
            self.action(engine, hero)

        self.fight(engine, hero)

    def fight(self, engine, hero):
        impact_force = ((self.stats['strength'] + self.stats['endurance']) // 2) * (
            random.randint(1, self.stats['luck']))

        hero.hp -= impact_force

        if hero.hp <= 0:
            engine.notify('You lose!')
            engine.game_process = False
        else:
            hero.exp += self.xp
            engine.notify(f'Got {self.xp} XP.')

            is_enough_exp = len([i for i in hero.level_up()]) > 0
            if is_enough_exp:
                engine.notify('Level up!')
