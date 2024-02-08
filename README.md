# candfans-client
非公式のCandfansのAPI Clientです。なんの保証もありません。

# install
https://pypi.org/project/candfans-client/

## pip
```bash
pip install candfans-client
```

## poetry

```bash
poetry add candfans-client
```

# example

## init and login
初期化時にログインを行います。

```python
from candfans_client.client import CandFansClient

client = CandFansClient(
    email='YOUR_EMAIL',
    password='YOUR_PASSWORD',
)
```

## get_sales
指定月の売上のサマリーを取得します。

```python
sales = client.get_sales('2023-11')
print(sales[0].subscribe_sum)
```

## get_sales_history
指定月の売上の履歴を取得します。

```python
histories = client.get_sales_history('2023-11')
print(len(histories))
print(histories[0])
```

## get_sales_purchase_post
指定月の単体販売の詳細を取得します。

```python
purchase = client.get_sales_purchase_post('2023-11')
print(purchase.total_price, len(purchase.sales))
```

## get_sales_subscribe
指定月のサブスクの詳細を取得します。

```python
subscribe = client.get_sales_subscribe('2023-11')
print(subscribe.total_price, len(subscribe.sales))
```

## get_sales_chip
指定月のチップの詳細を取得します。

```python
chip = client.get_sales_chip('2023-11')
print(chip.total_price, len(chip.sales))
```

## get_sales_backnumber
指定月のバックナンバーの売上の詳細を取得します。

```python
backnumber = client.get_sales_backnumber('2023-11')
print(backnumber.total_price, len(backnumber.sales))
```

# contribution

## test

```
poetry run python -m unittest discover -s tests/
```