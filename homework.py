from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str  # Тип тренировки
    duration: float  # Длительность
    distance: float  # Дистанция
    speed: float  # Ср. скорость
    calories: float  # Потрачено ккал

    def get_message(self) -> str:
        temp = (f'Тип тренировки: {self.training_type};' +
                f' Длительность: {self.duration:.3f} ч.;' +
                f' Дистанция: {self.distance:.3f} км;' +
                f' Ср. скорость: {self.speed:.3f} км/ч;' +
                f' Потрачено ккал: {self.calories:.3f}.')
        return temp


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int  # шаг - бег, ходьба; гребок - плавание.
    duration: float  # длительность тренировки.
    weight: float  # вес спортсмена.

    LEN_STEP = 0.65  # расстояние, которое преодалевает спортсмен.
    M_IN_KM = 1000  # константа перевода метров в километры.
    coeff_calorie_1 = 18  # Очень хочеться сделать все атрибуты
    coeff_calorie_2 = 20  # приватными, но pytest не разрешает :(
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    coeff_calorie_6 = 1.1
    coeff_calorie_7 = 2

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


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float  # Рост спортсмена

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        temp1 = (self.coeff_calorie_3 * self.weight)
        temp = (self.get_mean_speed() ** 2) // self.height
        temp = temp1 + temp * self.coeff_calorie_4 * self.weight
        return temp * self.duration * 60


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float  # длина бассейна
    count_pool: float  # количество проплытых бассейнов

    LEN_STEP = 1.38

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

    dict_class = {'SWM': (Swimming, 5),
                  'RUN': (Running, 3),
                  'WLK': (SportsWalking, 4)}

    if workout_type in dict_class:  # Проверяем соответствие типа тренеровки и
        if len(data) == dict_class[workout_type][1]:  # размер пакета данных
            return dict_class[workout_type][0](*data)
        else:
            raise ValueError('Ошибка размера пакета данных')
    else:
        raise TypeError('Неизвестный тип тренировки')


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
