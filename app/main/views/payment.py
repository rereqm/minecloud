import yoomoney
from datetime import datetime


class Payment:
    def __init__(self, token, secret_key, account_id) -> None:
        self.token = str(token)
        self.secret_key = str(secret_key)
        self.account_id = str(account_id)

    # Выставление счёта, возвращает URL для оплаты
    def quickpay(self, sum: float, label, successURL=None) -> str:
        sum = float(sum)
        label = str(label)

        payment = yoomoney.Quickpay(
            receiver=self.account_id,
            quickpay_form="shop",
            targets="Оплата сервера Minecloud",
            paymentType="SB",
            sum=sum,
            label=label,
            successURL=successURL
        )

        return payment.redirected_url

    def check_payment(self, label) -> bool:
        label = str(label)

        client = yoomoney.Client(self.token)
        history = client.operation_history(
            label=label,
            type="deposition",
            records=100,
            from_date=datetime(2023, 5, 1)
        )

        for operation in history.operations:
            if operation.status == 'success':
                return True

        return False