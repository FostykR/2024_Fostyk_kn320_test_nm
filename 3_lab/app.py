# спочатку йдуть імпорти бібліотек
from game.sword import Swords
from random import randint 
# опис функціоналу програми у вигляді функцій 

# виконання всієї програми
if __name__ == "__main__":
    print("Start game")
    c = Swords.create_random_rarity("Катана")
    # Робимо динамічний атрибут, який буде вказувати, кому належить даний меч
    c.player = input("Enter the name of the first player:")
    print(f"Гравець {c.player} отримує Меч:", c.info)

    d = Swords.create_random_rarity("Шпага")
    d.player = input("Enter the name of the second player:")
    print(f"Гравець {d.player} отримує Меч:", d.info)

    # Дозволимо гравцю впливати на те як ми будемо змагатись на отриманих мечах
    c.player_buff = input(f"{c.player} enter 1 for attack buff, 2 for vitality buff, or skip it: ")
    d.player_buff = input(f"{d.player} enter 1 for attack buff, 2 for vitality buff, or skip it: ")

    for pb in [c, d]:
        if pb.player_buff == "1": # Ця перевірка нам потрібна, щоб визначити, чи гравці ввели правильні значення
            print(f"{pb.player} Damage buff applied")
            pb.get_baff_damage(randint(2, 5)) 
        elif pb.player_buff == "2":
            print(f"{pb.player} Vitality buff applied")
            pb.get_baff_vitality(randint(6, 12)) 
        else:
            print("An invalid value was entered, so no buffs were applied")
       # меч старіє/зношується від використання, тому накладаємо випадковий негативний ефект
        print( pb.aging(), pb.info)
    
    # емулюємо як ми користуємось нашим мечем та ми проводимо бої де його міцність зменшується через атак
    # Перший хід робить 1 гравець
    while c.vitality > 0 and d.vitality > 0:
        print("Start round")
        c.attack(d)
        print(f"{c.player} з {c.name} атакував {d.player} з {d.name}")
        d.attack(c)
        print(f"У відповідь {d.player} з {d.name} атакував {c.player} з {c.name}")
        print(f"Закінчилась дія бафу: {c.expired_buff()} ||||| {d.expired_buff()}")
        print(f"<<<<< {c.name} {c.vitality} |||| {d.name} {d.vitality} >>>>>")
        print(f"Починаємо відновлення мечів: {c.repair()} |||| {d.repair()}")
        print(f"<<<<< {c.name} {c.vitality} |||| {d.name} {d.vitality} >>>>>")

    if c.vitality > 0 and c.vitality >= d.vitality:
        print(f"Гравець {c.player} переміг над {d.player}")
    else:
        print(f"Гравець {d.player} переміг над {c.player}")

    print("End game")
