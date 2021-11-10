from dataclasses import dataclass
from typing import ClassVar, Union, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # Тип тренировки
    duration: float  # Длительность
    distance: float  # Дистанция
    speed: float  # Ср. скорость
    calories: float  # Потрачено ккал

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int  # шаг - бег, ходьба; гребок - плавание.
    duration: float  # длительность тренировки.
    weight: float  # вес спортсмена.

    LEN_STEP: ClassVar[float] = 0.65  # расстояние одного шага
    M_IN_KM: ClassVar[int] = 1000  # константа перевода метров в километры.
    coeff_calorie_1: ClassVar[Union[int, float]] = 18  # Коэф-т для расчета
    coeff_calorie_2: ClassVar[Union[int, float]] = 20  # Коэф-т для расчета
    coeff_calorie_3: ClassVar[Union[int, float]] = 60  # Коэф-т для расчета

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

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
        return ((self.coeff_calorie_1
                * self.get_mean_speed()
                - self.coeff_calorie_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.coeff_calorie_3)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float  # Рост спортсмена

    coeff_calorie_1: ClassVar[Union[int, float]] = 0.035  # Коэф-т для расчета
    coeff_calorie_2: ClassVar[Union[int, float]] = 0.029  # Коэф-т для расчета

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() ** 2 // self.height
                * self.coeff_calorie_2 * self.weight
                + self.coeff_calorie_1 * self.weight)
                * self.duration * self.coeff_calorie_3)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float  # длина бассейна
    count_pool: float  # количество проплытых бассейнов

    LEN_STEP: ClassVar[float] = 1.38  # расстояние одного гребка
    coeff_calorie_1: ClassVar[Union[int, float]] = 1.1  # Коэф-т для расчета
    coeff_calorie_2: ClassVar[Union[int, float]] = 2  # Коэф-т для расчета

    def get_mean_speed(self):
        """Метод возвращает значение средней
        скорости движения во время тренировки"""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self):
        """Метод возвращает число потраченных колорий"""
        return ((self.get_mean_speed()
                + self.coeff_calorie_1)
                * self.weight
                * self.coeff_calorie_2)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    dict_class = {'SWM': (Swimming, 5),
                  'RUN': (Running, 3),
                  'WLK': (SportsWalking, 4)}

    if workout_type not in dict_class:
        raise TypeError('Неизвестный тип тренировки')

    if len(data) != dict_class[workout_type][1]:
        raise ValueError('Ошибка размера пакета данных')

    return dict_class[workout_type][0](*data)


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
