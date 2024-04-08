from random import choice, randint
from typing import Any
class SwordBonus: 
    """Описує функціонал бонусів"""
    count = 0

    def __init__(self) -> None:
        SwordBonus.count += 1

    @staticmethod
    def bonus_poison(item) -> str:
        """Накладення отрути, шкода +1"""
        if SwordBonus.__check_obj(item):
            item.damage += 1
            return f"Застосовано бонус отрути до {item.name}"

    @staticmethod
    def bonus_confusion(item) -> str:
        """Накладення конфузії, шкода +2"""
        if SwordBonus.__check_obj(item):
            item.damage += 2
            return f"Застосовано бонус спантеличеність до {item.name}"
        
    @staticmethod
    def bonus_berserk(item) -> str:
        """Ефект берсерка, шкода +10"""
        if SwordBonus.__check_obj(item):
            item.damage += 10
            return f"Застосовано бонус Берсерка {item.name}"

    @staticmethod
    def bonus_strength(item) -> str:
        """Накладення міцності, витривалість +5"""
        if SwordBonus.__check_obj(item): 
            item.vitality += 5
            return f"Застосовано бонус сили. до {item.name}"
        
    @staticmethod
    def bonus_invincible(item) -> str:
        """Накладення незламності, витривалість +15"""
        if SwordBonus.__check_obj(item): 
            item.vitality += 15
            return f"Застосовано бонус незламності {item.name}"
        
    @staticmethod
    def _nothing(item) -> str:
        """Пустий бонус для мечів з низькою якістю"""
        if SwordBonus.__check_obj(item):
            return f"Меч {item.name} має занизьку рідкісність!"
    
    @staticmethod
    def list_bonus_methods() -> list:
        """"""
        return [method for method in dir(SwordBonus) if callable(getattr(SwordBonus, method)) and method.startswith("bonus_")]

    @staticmethod
    def __check_obj(obj: Any) -> bool:
        """Реалізували приватний метод, який перевіряє, чи ми працюємо з правильним об'єктом"""
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
    who_has_buff = [] #Ця класова змінна відслідковує на які об'єкт накладено баф
    # Це мапа, яка вказує коефіцієнт збільшення атрибутів відносно Рідкісності предмету
    rarity_map = {"Basic": 1, "White": 2, "Green": 3, "Blue": 5, "Yellow": 7, "Epic": 9, "Legendary": 10}


    def __init__(self, name:str, rarity:str, damage:int, vitality:int, bonus: callable) -> None: 
        """Конструктор для створення об'єкту Меч.
        name: поля для імені;
        rarity: рідкість предмету;
        damage: к-сть урону, дамагу
        vitality: к-сть витривалості
        bonus: необов'язковий аргумент;
        """
        # Атрибути об'єкта, які можна змінювати
        self.name = name
        self.rarity = rarity
        self.damage = damage
        self.vitality = vitality
        self.bonus = bonus.__doc__ # тут ми просто будемо знати, що бонус був застосований до нашого об'єкту
        bonus(self) # тут ми застосовуємо бонус до нашого поточного обєкту

        self.buff_damage = 0
        self.buff_vitality = 0
        self.debuff = list()

    @classmethod
    def create_from_rarity(cls, name:str, rarity:str):
        """Цей конструктор використовується, коли отримується меч з крафту"""
        bonus_list = SwordBonus.list_bonus_methods()
        bonus = SwordBonus._nothing
        if rarity in list(cls.rarity_map.keys())[-3:]:
            bonus = getattr(SwordBonus, choice(bonus_list))

        if rarity in cls.rarity_map.keys():
            return cls(name, rarity, damage=3*cls.rarity_map[rarity], vitality=5*cls.rarity_map[rarity], bonus = bonus)
        raise AttributeError(f"Неправильно задано рідкісність предмету, повинно бути один з {list(cls.rarity_map.keys())}")

    @classmethod
    def create_random_rarity(cls, name:str):
        """Тут ми випадково вибили меч з Боса"""
        rarity = choice(list(cls.rarity_map.keys()))
        return cls.create_from_rarity(name, rarity)

    def get_baff_damage(self, damage:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладений баф"
        self.buff_damage = damage
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут дамагу +{damage}"
    
    def get_baff_vitality(self, vitality:int) -> str:
        if self.__hash__ in Swords.who_has_buff:
            return f"На меч {self.name} вже накладений баф"
        self.vitality += vitality
        self.buff_vitality = vitality
        Swords.who_has_buff.append(self.__hash__)
        return f"Накладено баф на {self.name} який додає атрибут витривалості +{vitality}, загальна витривалість: {self.vitality}"
    
    def expired_buff(self) -> str:
        Swords.who_has_buff.remove(self.__hash__)
        if self.buff_damage > 0:
            self.buff_damage = 0
            return "Дія бафу дамагу - завершена!"
        if self.buff_vitality > 0:
            self.vitality -= self.buff_vitality
            self.buff_vitality = 0
            return "Дія бафу витривалості - завершена!"
        return "На мечі відсутній баф"
    
    def aging(self):
        """Даний метод реалізує процес старіння меча"""
        if Swords.negative_effects("ржавіння"):
            self.debuff.append("ржавіння")
        if Swords.negative_effects("затуплення"):
            self.debuff.append("затуплення")
        if Swords.negative_effects("тріщина"):
            self.debuff.append("тріщина")
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
        """Метод для парирування, тут в нас присутній баг, ми не можемо зменшувати властивість health
        """
        self.vitality -= damage
        return self.vitality
    
    @staticmethod
    def negative_effects(name:str) -> int:
        """Визначаємо чи меч випадковим чином отримав якийсь негативний ефект"""
        r = randint(0, 4)
        if r > 2:
            print(f"Меч отримав негативний ефект {name}, повертаємо дебаф на 1")
            return True
        return False

    @property
    def get_name(self) -> str:
        """"Повертає значення імені, яке змінювати уже не можна. Ця властивість лише для читання"""
        return self.name
    
    @property
    def info(self) -> str:
        """Виводить інформацію про об'єкт"""
        return f"""<<<<< Статистика для {self.name} >>>>>
Назва: {self.get_name}!
Рідкість: {self.rarity}.
Дамаг: + {self.hit}
Витривалість: + {self.health}
Бонус: {self.bonus}
Накладені Бафи: Дамаг {self.buff_damage} та Витривалість {self.buff_vitality}
Накладені Дебафи: {self.debuff}
>>>>>\n"""
        
    @property
    def hit(self):
        """Property яка визначає загальне значення нанесення шкоди"""
        return self.damage + self.buff_damage
    
    @property
    def health(self):
        """Property яка визначає загальну витривалість"""
        return self.vitality
