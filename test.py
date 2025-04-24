import asyncio
from db.crud.base import init_postgres
from db.models.models import ExchangeRate

async def main():

    await init_postgres()

    await ExchangeRate.create(usd_alipay=0.0,
                              usd_wechat=0.0,
                              rub_alipay=0.0,
                              rub_wechat=0.0)

    result = await ExchangeRate.get(id=1)
    print(result.usd_alipay, result.usd_wechat, result.rub_alipay, result.rub_wechat)

    
    

if __name__ == "__main__":
    asyncio.run(main())