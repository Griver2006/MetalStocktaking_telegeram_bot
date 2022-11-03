import datetime

from data import db_session
from data.all_operations import AllOperations


dbs = db_session.create_session()


def add_to_all_operations(date, time, metal, quantity, price, amount, comment):
    # Создаём и записываем значения в AllOperations
    all_operations = AllOperations()
    all_operations.date = datetime.datetime.strptime(date.replace('.', '-'), "%Y-%m-%d").date()  # Записываем дату
    all_operations.time = datetime.datetime.strptime(time, "%H:%M:%S").time()  # Записываем время
    all_operations.metal = metal  # Записываем выбранный пользователем металл
    all_operations.quantity = quantity  # Записываем количество металла
    all_operations.price = price  # Записываем цену металла
    all_operations.sum = amount  # Записываем сумму металла
    all_operations.comment = comment  # Записываем комментарий
    dbs.add(all_operations)
    dbs.commit()