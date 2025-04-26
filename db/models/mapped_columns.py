from typing import Annotated
from sqlalchemy import BigInteger, DateTime, String, text, Float
from sqlalchemy.orm import mapped_column

# Определение столбцов без использования Annotated
intpk = Annotated[
    int,
    mapped_column(primary_key=True)
]
floatp = mapped_column(Float)
unique_big_int = mapped_column(BigInteger, unique=True)
created_at = mapped_column(DateTime(timezone=True), server_default=text("TIMEZONE('Europe/Moscow', NOW())"))

# Для строковых столбцов с ограничениями
str_3 = mapped_column(String(3))
str_32 = mapped_column(String(32))
str_140 = mapped_column(String(140))
str_240 = mapped_column(String(240))
