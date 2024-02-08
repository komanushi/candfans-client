import os
from candfans_client.client import CandFansClient


def main():
    client = CandFansClient(
        email=os.getenv('CANDFANS_EMAIL'),
        password=os.getenv('CANDFANS_PASSWORD'),
        debug=True
    )
    # histories = client.get_sales_history('2023-11')
    # print(len(histories))
    # print(histories[0])
    # sales = client.get_sales('2023-11')
    # print(sales[0].subscribe_sum)
    # purchase = client.get_sales_purchase_post('2023-12')
    # print(purchase.total_price, len(purchase.sales))
    # subscribe = client.get_sales_subscribe('2023-11')
    # print(subscribe.total_price, len(subscribe.sales))
    # chip = client.get_sales_chip('2023-11')
    # print(chip.total_price, len(chip.sales))
    backnumber = client.get_sales_backnumber('2024-01')
    print(backnumber.total_price, len(backnumber.sales))


if __name__ == "__main__":
    main()
