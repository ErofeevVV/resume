"""
Служба аренды транспортных средств
"""


class Vehicle:
    def __init__(self, vin, make, model, daily_rate):
        self.vin = str(vin)
        self.make = make
        self.model = model
        self.daily_rate = daily_rate
        self.available = True

    def start_rental(self):
        if self.available:
            self.available = False
            return True
        return False

    def end_rental(self):
        self.available = True
        return True

    def __str__(self):
        status = 'Доступен' if self.available else 'Не доступен'
        return f'{self.make} {self.model} (VIN: {self.vin}) - {status}'


class Car(Vehicle):
    def __init__(self, vin, make, model, daily_rate, passenger_capacity):
        super().__init__(vin, make, model, daily_rate)
        self.passenger_capacity = passenger_capacity

    def __str__(self):
        return f'Автомобиль: {super().__str__()} - Количество пассажиров {self.passenger_capacity}'


class Motorcycle(Vehicle):
    def __init__(self, vin, make, model, daily_rate, engine_size):
        super().__init__(vin, make, model, daily_rate)
        self.engine_size = engine_size

    def __str__(self):
        return f'Мотоцикл: {super().__str__()} - {self.engine_size} СС'


class Rental:
    def __init__(self, rental_id, vehicle, customer_name, days):
        self.rental_id = rental_id
        self.vehicle = vehicle
        self.customer_name = customer_name
        self.days = days
        self.is_active = True

    def calculate_cost(self):
        return self.vehicle.daily_rate * self.days

    def end_rental(self):
        if self.is_active:
            self.is_active = False
            self.vehicle.end_rental()
            return True
        return False

    def __str__(self):
        status = 'Available' if self.is_active else 'Not Available'
        return f'Rental {self.rental_id}: {self.vehicle.make} {self.vehicle.model} for {self.customer_name} - {status}'


class RentalAgency:
    def __init__(self, name):
        self.name = name
        self.vehicles = {}
        self.rentals = {}
        self.next_rental_id = 1

    def add_vehicle(self, vehicle):
        self.vehicles[vehicle.vin] = vehicle

    def rent_vehicle(self, vin, customer_name, days):
        vehicle = self.vehicles.get(vin)
        if vehicle and self.vehicles:
            if vehicle.start_rental():
                rental_id = f'R{self.next_rental_id}'
                rental = Rental(rental_id, vehicle, customer_name, days)
                self.rentals[rental_id] = rental
                self.next_rental_id += 1
                return rental_id
        return None

    def return_vehicle(self, rental_id):
        rental = self.rentals.get(rental_id)
        if rental and rental.is_active:
            return rental.end_rental()
        return False

    def available_vehicles(self):
        return [vehicle for vehicle in self.vehicles.values() if vehicle.available]


def main():
    print('Добро пожаловать в Transport Rental Agency')
    agency = RentalAgency('Transport Rental Agency')

    agency.add_vehicle(Car('VIN001', 'Nissan', 'Almera', 50, 5))
    agency.add_vehicle(Car('VIN002', 'Honda', 'Civic', 45, 4))
    agency.add_vehicle(Motorcycle('VIN003', 'Yamaha', 'MT-07', 30, 689))
    agency.add_vehicle(Motorcycle('VIN004', 'Harley-Davidson', 'Iron 883', 40, 883))

    while True:
        print('\n Выберите действие:')
        print('1 - Показать доступный транспорт')
        print('2 - Арендовать транспорт')
        print('3 - Завершить аренду')
        print('4 - Выйти')

        choice = input('Введите номер действия: ')

        if choice == '1':
            available = agency.available_vehicles()
            if not available:
                print('Нет доступных транспортных средств')
            else:
                print('\n Доступный транспорт: ')
                for v in available:
                    print(f'- {v}')

        elif choice == '2':
            vin = input('Введите VIN транспорта: ').strip()
            name = input('Введите ваше имя: ').strip()
            try:
                days = int(input('Введите количество дней аренды: '))
            except ValueError:
                print('Ошибка: введите корректное число!')
                continue

            rental_id = agency.rent_vehicle(vin, name, days)
            if rental_id:
                cost = agency.rentals[rental_id].calculate_cost()
                print(f'Аренда прошла успешно! ID аренды: {rental_id}')
                print(f'Стоимость: ${cost}')
            else:
                print('Транспорт не найден или уже арендован!')

        elif choice == '3':
            rental_id = input('Введите ID аренды: ').strip()
            if agency.return_vehicle(rental_id):
                print('Аренда завершена!')
            else:
                print('Ошибка: аренда не найдена или уже завершена!')

        elif choice == '4':
            print('До свидания!')
            break

        else:
            print('Неверный выбор: выберете действие от 1 дло 4!')


if __name__ == '__main__':
    main()
