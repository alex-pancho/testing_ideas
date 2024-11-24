"""
Написати клас EndlessAray, який підтримує наступний інтерфейс і забезпечує ефективну роботу для 
описаних сценаріїв:
Методи:

    set(index: int, value: Any)
    Задає значення value для конкретного ключа index. Якщо для цього індексу вже було 
    встановлене значення, воно оновлюється.

    get(index: int) -> Any
    Повертає значення, пов'язане з ключем index. Якщо значення для цього індексу не 
    встановлене, повертає None, або останнє значення, встановлене методом set_all.

    set_all(value: Any)
    Встановлює значення value для всіх ключів. Це значення буде повертатися методом get 
    для будь-якого ключа, поки для нього не буде явно викликано метод set.

    ТЕСТИ:
    a = EndlessAray()
    a.set(1, "a")
    a.get(1) # a
    a.get(1000) # None

    a.set_all("b")
    a.set(2, "c")

    a.get(1) # b
    a.get(2) # c
    a.get(1000000000000000000000000) # b
"""

class EndlessAray():

    def __init__(self):
        self.array = {}
        self.all = None


    def set(self, index, value):
        self.array[index] = value


    def get(self, index):
        """if not exist - None"""
        return self.array.get(index, self.all)


    def set_all(self, value):
        """set all index to val"""
        self.all = value
        for index in self.array:
            self.set(index, value)

if __name__ == "__main__":
    pass
