import asyncio
from db.crud.base import init_postgres
from db.models.models import ExchangeRate

async def main():

    await init_postgres()

    
    

if __name__ == "__main__":
    asyncio.run(main())