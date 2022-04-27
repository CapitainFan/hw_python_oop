from typing import List, Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        mess = ('Тип тренировки: {0}; '.format(self.training_type)
                + 'Длительность: {0:.3f} ч.; '.format(self.duration)
                + 'Дистанция: {0:.3f} км; '.format(self.distance)
                + 'Ср. скорость: {0:.3f} км/ч; '.format(self.speed)
                + 'Потрачено ккал: {0:.3f}.'.format(self.calories))
        return mess


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Вернуть информационное сообщение о выполненной тренировке."""
        raise NotImplementedError("Please Implement this method")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message1 = InfoMessage(self.__class__.__name__, self.duration,
                               self.get_distance(), self.get_mean_speed(),
                               self.get_spent_calories())
        return message1


class Running(Training):
    """Тренировка: бег."""
    COEFF_CALORIE_1: int = 18
    COEFF_CALORIE_2: int = 20
    VMIN: int = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2) * self.weight / self.M_IN_KM
                * (self.duration * self.VMIN))


class SportsWalking(Training):
    VMIN: int = 60

    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_3: float = 0.035
        coeff_cal_4: int = 2
        coeff_calorie_5: float = 0.029
        calories = (coeff_calorie_3 * self.weight
                    + (self.get_mean_speed() ** coeff_cal_4 // self.height)
                    * coeff_calorie_5
                    * self.weight) * self.duration * self.VMIN
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5: float = 1.1
    coeff_calorie_6: float = 2.0
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * Swimming.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: List[int]):
    """Прочитать данные полученные от датчиков."""
    read: dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    read_workout_type = read.get(workout_type)
    if read_workout_type is None:
        return print('Утебя ошибка в функции read_package')
    return read_workout_type(*data)


def main(training):
    """Главная функция."""
    try:
        info = training.show_training_info()
        print(info.get_message())
    except ValueError:
        print('Утебя ошибка в функции main')


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
