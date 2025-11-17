class PracticeNumerator:

    __i = 0

    def get_next_practice_number(self):
        self.__i += 1
        return self.__i

    def clear(self):
        self.__i = 0