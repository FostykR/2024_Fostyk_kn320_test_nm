# спочатку йдуть імпорти бібліотек
from game.sword import Swords
from random import randint
# опис функціоналу програми у вигляді функцій

# виконання всієї програми
if __name__ == "__main__":
    print("Старт гри:")
    c = Swords.create_random_rarity("Катана")
    # Робими динамічний атрибут який буде вказувати кому належить даний меч
    c.player = input("Введіть імя першого гравця: ")
    print(f"Гравець {c.player} отримує Меч:", c.info)
    
    d = Swords.create_random_rarity("Шпага")
    d.player = input("Введіть імя другого гравця: ")
    print(f"Гравець {d.player} отримує Меч:", d.info)

    # Дозволимо гравцю впливати на те як ми будемо змагатись на отриманих мечах
    c.player_buff = input(f"{c.player} ведіть 1 для бафу на атаку, 2 для бафу на міцності, будь-яка кнопка щоб пропустити: ")
    d.player_buff = input(f"{d.player} ведіть 1 для бафу на атаку, 2 для бафу на міцності, будь-яка кнопка щоб пропустити: ")
    
    for pb in [c, d]:
        if pb.player_buff == "1": # Ця перевірка нам потрібна щоб визначити чи гравці ввели правильні значення
            print(f"{pb.player} застосував баф на нанесення шкоди:")
            pb.get_buff_damag(randint(2, 5))
        elif pb.player_buff == "2":
            print(f"{pb.player} застосував баф на міцність:")
            pb.get_buff_vitality(randint(6, 12))
        else:
            print("Введено не коректне значення, тому ніяких бафів не застосовано!")
        # меч старіє/зношується від використання, тому накладаємо випадковий негативний ефект
        print(pb.aging(), pb.info)

    # емулюємо як ми користуємось нашим мечем та проводимо бої де його міцність зменшується через атаки
    # Перший хід за першим гравцем
    while c.vitality > 0 and d.vitality > 0:
        print("Новий раунд:")
        c.attack(d)
        print(f"{c.player} з {c.name} атакував {d.player} з {d.name}")
        d.attack(c)
        print(f"Зворотньо {d.player} з {d.name} атакував {c.player} з {c.name}")
        print(f"Закінчилась дія бафу: {c.expired_buff()} ||||| {d.expired_buff()}")
        print(f"<<<<< {c.name} {c.vitality} ||||| {d.name} {d.vitality} >>>>>>")
        print(f"Починаємо ремонтувати мечі: {c.repair()} ||||| {d.repair()}")
        print(f"<<<<< {c.name} {c.vitality} ||||| {d.name} {d.vitality} >>>>>>")

    if c.vitality > 0 and c.vitality >= d.vitality:
        print(f"Гравець {c.player} переміг над {d.player}")
    else:
        print(f"Гравець {d.player} переміг над {c.player}")

    print("Завершення гри")
