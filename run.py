import os
from candfans_client.models.timeline import PostType
from candfans_client.models.search import CreatorTerm
from candfans_client.client import CandFansClient, AnonymousCandFansClient
from candfans_client.async_client import AsyncAnonymousCandFansClient, AsyncCandFansClient


def main():
    # client = CandFansClient(
    #     email=os.getenv('CANDFANS_EMAIL'),
    #     password=os.getenv('CANDFANS_PASSWORD'),
    #     debug=True
    # )
    client = AnonymousCandFansClient(debug=False)
    # res = client.get_followed(1025744)
    # print(len(list(res)))
    res = client.get_users('koma_showcase')
    # print(res)
    res = client.get_timeline(res.user.id, post_types=[PostType.LIMITED_ACCESS_ITEM], max_page=1)
    post = list(res)[0]
    print(post.attachment_length, post.title)
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
    # backnumber = client.get_sales_backnumber('2024-01')
    # print(backnumber.total_price, len(backnumber.sales))
    # res = client.get_follows(1025744)
    # print(len(list(res)))
    # res = client.get_followed(1025744)
    # print(len(list(res)))
    # res = client.get_user_mine()
    # print(res.model_dump_json(indent=4))
    # res = client.get_creator_ranking(start_page=1, max_page=1, per_page=10, terms=CreatorTerm.TOTALY)
    # for x in res: print(x.rank, x.username)
    # res = client.get_trend_new_commers()
    # for x in res: print(x.user_id, x.username)


async def async_main():
    anonymous_client = AsyncAnonymousCandFansClient(debug=False)
    client = AsyncCandFansClient(
        email=os.getenv('CANDFANS_EMAIL'),
        password=os.getenv('CANDFANS_PASSWORD'),
        debug=True
    )
    await client.login()
    # res = anonymous_client.get_followed(1025744)
    # print(len(list(res)))
    res = await anonymous_client.get_users('hamayoko333')
    # print(resnymous_client.get_users('hamayoko333')
    # print(res)
    # cnt = 0
    # async for r in anonymous_client.get_timeline(res.user.id, post_types=[PostType.PUBLIC_ITEM]):
    #     print(r)
    #     cnt += 1
    #     if cnt > 5:
    #         break
    async for r in client.get_creator_ranking(max_page=1, per_page=10, terms=CreatorTerm.TOTALY):
        print(r.rank, r.username)


if __name__ == "__main__":
    # import asyncio
    # asyncio.run(async_main())
    main()
