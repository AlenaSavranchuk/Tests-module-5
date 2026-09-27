import random


class DataGenerator:

    @staticmethod
    def get_credit_data():
        # Генерируем кредит строго в рамках правил бэка (от 5000 до 8000, чтобы депозит покрыл его)
        credit_amount = random.randrange(5000, 8000, 500)

        # Депозит делаем больше кредита, но не превышая верхний лимит бэка в 9000
        deposit_amount = credit_amount + random.randrange(500, 1000, 500)

        # Если депозит случайно вылетел за 9000, жестко фиксируем его на границе
        if deposit_amount > 9000:
            deposit_amount = 9000
            # Срезаем кредит, чтобы он гарантированно был меньше или равен депозиту
            credit_amount = 7000

        term_months = random.randint(3, 24)

        return {
            "deposit_amount": deposit_amount,
            "credit_amount": credit_amount,
            "term_months": term_months
        }

    @staticmethod
    def get_invalid_amount():
        # генерирует невалидную сумму
        import random
        return random.randint(-1000, 100)

