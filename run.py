import os
from candfans.client import CandFansClient

def main():
    client = CandFansClient(
        email=os.getenv('CANDFANS_EMAIL'),
        password=os.getenv('CANDFANS_PASSWORD'),
        debug=True
    )
    histories = client.get_sales_history('2023-11')
    print(histories)


if __name__ == "__main__":
    main()