class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:3f} ч.; '
                f'Дистанция: {self.distance:3f} км; '
                f'Ср. скорость: {self.speed:3f} км/ч; '
                f'Потрачено ккал: {self.calories:3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        M_IN_KM = 1000
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    '''Тренировка: бег.'''
    training_type = 'RUN'

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        M_IN_KM = 1000
        calories = ((coeff_calorie_1 * self.get_mean_speed()
                    - coeff_calorie_2) * self.weight / M_IN_KM
                    * self.duration * 60)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    training_type = 'WLK'
    '''Получаем высоту спортсмена'''
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
        coeff_calorie_3 = 0.035
        coeff_cal_4 = 2
        coeff_calorie_5 = 0.029
        calories = (coeff_calorie_3 * self.weight
                    + (self.get_mean_speed() ** coeff_cal_4 // self.height)
                    * coeff_calorie_5 * self.weight) * self.duration * 60
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    training_type = 'SWM'

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        M_IN_KM = 1000
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_6 = 1.1
        coeff_calorie_4 = 2
        calories = ((self.get_mean_speed() + coeff_calorie_6)
                    * coeff_calorie_4 * self.weight)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_1 = {'RUN': Running, 'SWM': Swimming, 'WLK': SportsWalking}
    return dict_1[workout_type](*data)


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
