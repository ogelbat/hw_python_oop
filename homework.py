from dataclasses import dataclass


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        temp = (f'Тип тренировки: {self.training_type};' +
                f' Длительность: {self.duration:.3f} ч.;' +
                f' Дистанция: {self.distance:.3f} км;' +
                f' Ср. скорость: {self.speed:.3f} км/ч;' +
                f' Потрачено ккал: {self.calories:.3f}.')
        return temp


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # расстояние, которое преодалевает спортсмен.
    M_IN_KM = 1000  # константа перевода метров в километры.
    coeff_calorie_1 = 18  # Очень хочеться сделать все атрибуты
    coeff_calorie_2 = 20  # приватными, но pytest не разрешает :(
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    coeff_calorie_6 = 1.1
    coeff_calorie_7 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action  # шаг - бег, ходьба; гребок - плавание.
        self.duration = duration  # длительность тренировки.
        self.weight = weight  # вес спортсмена.

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.' % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        temp = self.coeff_calorie_1 * self.get_mean_speed()
        temp2 = temp - self.coeff_calorie_2
        return temp2 * self.weight / self.M_IN_KM * self.duration * 60


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        temp1 = (self.coeff_calorie_3 * self.weight)
        temp = (self.get_mean_speed() ** 2) // self.height
        temp = temp1 + temp * self.coeff_calorie_4 * self.weight
        return temp * self.duration * 60


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длина бассейна
        self.count_pool = count_pool  # количество проплытых бассейнов

    def get_mean_speed(self):
        """Метод возвращает значение средней
        скорости движения во время тренировки"""
        temp = self.length_pool * self.count_pool
        return temp / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        """Метод возвращает число потраченных колорий"""
        temp = (self.get_mean_speed() + self.coeff_calorie_6) * self.weight
        return temp * self.coeff_calorie_7


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(*data)

    if workout_type == 'RUN':
        return Running(*data)

    if workout_type == 'WLK':
        return SportsWalking(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
