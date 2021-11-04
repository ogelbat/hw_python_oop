class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

        def get_message(self):
            temp = f'Тип тренировки: {self.training_type:.3}; Длительность: {self.duration:.3} ч.;'
            f' Дистанция: {self.distance:.3} км; Ср. скорость: {self.speed:.3} км/ч; Потрачено ккал: {self.calories:.3}'
            return temp



class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action       # шаг - бег, ходьба; гребок - плавание.
        self.duration = duration   # длительность тренировки.
        self.weight = weight       # вес спортсмена.
        self.M_IN_KM = 1000        # константа.
        self.LEN_STEP = 0.65       # расстояние, которое спортсмен преодалевает за один шаг или гребок.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        temp = (coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
        temp = temp * self.weight / self.M_IN_KM * self.duration
        return temp


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.M_IN_KM = 1000        # константа.
        self.LEN_STEP = 0.65       # расстояние, которое спортсмен преодалевает за один шаг или гребок.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035
        self.height = 0.029
        temp = self.get_mean_speed() ** 2 // self.height
        temp = (coeff_calorie_1 * self.weight + temp * self.height * self.weight) * self.duration
        return temp


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool,
                 count_pool
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool   # длина бассейна
        self.count_pool = count_pool     # количество проплытых бассейнов
        self.LEN_STEP = 1.38
        self.M_IN_KM = 1000

    def get_mean_speed(self):
        """Метод возвращает значение средней скорости движения во время тренироветод возвращает значение средней скорости движения во время тренировки"""
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        """Метод возвращает число потраченных колорий"""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    pass


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

