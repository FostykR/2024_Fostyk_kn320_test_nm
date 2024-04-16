from random import choice, randint
from typing import Any

class SwordBonus:
    """Описує функціонал бонусів"""
    count = 0

    def __init__(self) -> None:
        SwordBonus.count += 1

    @staticmethod
    def bonus_poison(item) -> str:
        """Накладення отрути, шкода +1 і втрата 2 витривалості"""
        if SwordBonus.__check_obj(item):
            item.damag += 1
            item.vitality -= 2
            return f"Застосовано бонус отрути {item.name}, нанесено шкоду та зменшено витривалість"
    
    @staticmethod
    def bonus_confusion(item) -> str:
        """Накладення конфузії, шкода +2"""
        if SwordBonus.__check_obj(item):
            item.damag += 2
            return f"Застосовано бонус спантеличеність {item.name}"
    
    @staticmethod
    def bonus_berserk(item) -> str:
        """Ефукт Берсерка, шкода +10"""
        if SwordBonus.__check_obj(item):
            item.damag += 10
            return f"Застосовано бонус Берсерка {item.name}"
    
    @staticmethod
    def bonus_strength(item) -> str:
        """Накладення міцності, міцність +5"""
        if SwordBonus.__check_obj(item):
            item.vitality += 5
            return f"Застосовано бонус сили до {item.name}"
        
    @staticmethod
    def bonus_invincible(item) -> str:
        """Накладення ефект Незламності, міцність +15"""
        if SwordBonus.__check_obj(item):
            item.vitality += 15
            return f"Застосовано бонус сили до {item.name}"
    
    @staticmethod
    def _nothing(item) -> str:
        """Пустий бонус для мечів з низькою якістю"""
        if SwordBonus.__check_obj(item):
            return f"Меч {item.name} має занизьку рідкісність!"
    
    @staticmethod
    def list_bonus_methods() -> list:
        """Знаходимо методи що надають бонуси, вони будуть починатись з bonus_, та повертаємо їх список"""
        return [method for method in dir(SwordBonus) if callable(getattr(SwordBonus, method)) and method.startswith("bonus_")]

    @staticmethod
    def __check_obj(obj: Any) -> bool:
        """Реалізували приватний метод який перевіряє чи ми працюємо з правильним обєктом"""
        if isinstance(obj, Swords):
            return True
        raise ValueError(f"Неможливо застосувати бонус до класу {type(obj)}")
    
    def __str__(self) -> str:
        """Представлення об'єкта у вигляді рядка, Це буде викликатись коли застосовуємо функцію прінт"""
        return f"Клас SwordBonus: реалізує функціонал бонусів, поточний обєкт має хеш {self.__hash__()}"

    def __repr__(self) -> str:
        """Канонічне представлення об'єкту"""
        return f"SwordBonus()"
    
    def __len__(self) -> int:
        """Застосування методу довжини поверне кількість бонусів які реалізовані в даному класі"""
        return len(SwordBonus.bonus_list())
  

class Swords:
    who_has_buff = [] # Ця класова змінна відслідковує на які обєкти зараз накладено баф
    # Це мапа яка вказує коефіцієнт збільшення атрибутів відносно Рідкісності предмету
    rarity_map = {"Basic": 1, "White": 2, "Green": 3, "Blue": 5, "Yellow": 7, "Epic": 9, "Legend": 10} 
    
    def __init__(self, name:str, rarity:str, damag:int, vitality:int, bonus: callable) -> None: # Це є свого роду конструктор
        """Конструктор для створення обєкту Меч.
        name: поля для імені;
        rarity: Рідкість предмету; 
        damag: Нанесення шкоди;
        vitality: Міцність предмету;
        bonus: необовязковий аргумент;
        """
        self.name = name # це є атрибути обєкта, їх можна змінювати після створення обєкту
        self.rarity = rarity
        self.damag = damag
        self.vitality = vitality
        self.bonus = bonus.__doc__ # тут ми просто будемо знати що за бонус був застосований до нашого обєкту
        bonus(self) # тут ми застосовуємо бонус до нашого поточного обєкту

        self.buff_damage = 0
        self.buff_vitality = 0
        self.debuff = list()

    @classmethod
    def create_from_rarity(cls, name:str, rarity:str):
        """Це конструктор використовуємо коли ми отримуємо меч з крафту"""
        bonus_list = SwordBonus.list_bonus_methods()
        bonus = SwordBonus._nothing
        if rarity in list(cls.rarity_map.keys())[-3:]:
            bonus = getattr(SwordBonus, choice(bonus_list))

        if rarity in cls.rarity_map.keys():
            return cls(name, rarity, damag=3*cls.rarity_map[rarity], vitality=5*cls.rarity_map[rarity], bonus = bonus)
        raise AttributeError(f"Неправильно задано рідкісність предмету, повинно бути один з {list(cls.rarity_map.keys())}")
    
    @classmethod
    def create_random_rarity(cls, name:str):
        """Тут ми випадково вибили меч з Боса"""
        rarity = choice(list(cls.rarity_map.keys()))
        return cls.create_from_rarity(name, rarity)
    
    def get_buff_damag(self, damag:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладено баф"
        self.buff_damage = damag
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут нанесення шкоди +{damag}"
    
    def get_buff_vitality(self, vitality:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладено баф"
        self.vitality += vitality
        self.buff_vitality = vitality
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут здоровя +{vitality}, загальне здоровя: {self.vitality}"
    
    def expired_buff(self) -> str:
        Swords.who_has_buff.remove(self.__hash__)
        if self.buff_damage > 0:
            self.buff_damage = 0
            return "Дія бафу на нанасення шкоди завершилась!"
        if self.buff_vitality > 0:
            self.vitality -= self.buff_vitality
            self.buff_vitality = 0
            return "Дія бафу на здоровя завершилась!"
        return "На мечі не має ніякого бафу!"
    
    def aging(self):
        """Даний метод реалізує процес старіння меча"""
        if Swords.negative_effects("ржавіння"):
            self.debuff.append("ржавіння")
        if Swords.negative_effects("затуплення"):
            self.debuff.append("затуплення")
        if Swords.negative_effects("трішина"):
            self.debuff.append("трішина")
        self.vitality -= len(self.debuff)
    
    def repair(self):
        """Метод реалізує відновлення міцності предмету під час ремонту"""
        if randint(0, 1):
            self.vitality += Swords.rarity_map[self.rarity]
            self.debuff = [] # Знімаємо всі дебафи
            return f"{self.name} відремонтовано та знято всі дебафи."
        return f"Не вийшло відремонтувати {self.name}"

    def attack(self, item = None) -> str:
        """Метод для атаки
        """
        if isinstance(item, Swords):
            item.vitality -= self.hit
            return f"Нанесено шкоду {self.hit} мечу {item.name}"
        if item is None:
            return "Ми промахнулись!"
        return f"Ми попали по сторонньому предмету {type(item)}"
        
    def parry(self, damage) -> int:
        """Метод для парирування, тут в нас є бага, ми не можемо зменшувати проперті health
        """
        self.vitality -= damage
        return self.vitality
    
    @staticmethod
    def negative_effects(name:str) -> int:
        """Визначаємо чи меч випадковим чином отримав якийсь негативний ефект"""
        r = randint(0, 4)
        if r > 2:
            print(f"Меч отримав негативнй ефект {name}, повертаємо дебаф на 1")
            return True
        return False
    
    @property 
    def get_name(self) -> str:
        """Повертає значення імені. І тут проперті змінювати не можна! Це моле лише для читання."""
        return self.name
    
    @property
    def info(self) -> str:
        """Проперті для читання, виводить інформацію про обєкт."""
        return f"""<<<<< Стати для {self.name} >>>>>
Назва: {self.get_name}
Рідкість: {self.rarity}
Дамаг: {self.hit}
Витривалість: {self.health}
Унікальна характеристика: {self.bonus}
Накладені Бафи: Дамаг {self.buff_damage} та Витривалість {self.buff_vitality}
Накладені Дебафи: {self.debuff}
>>>>>\n"""

    @property
    def hit(self):
        """Проперті яка визначає загальне значення нанесення шкоди"""
        return self.damag + self.buff_damage
    
    @property
    def health(self):
        """Проперті яка визначає всю витривалість ХП який має обєкт"""
        return self.vitality

    @property
    def rarity_info(self):
        """Властивість для виведення назви рідкісності меча та його поточного коефіцієнту"""
        return f"Рідкість: {self.rarity}, Коефіцієнт: {self.rarity_map[self.rarity]}"

