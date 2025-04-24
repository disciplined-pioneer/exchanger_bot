from sqlalchemy import Integer, BigInteger, DateTime, String, text
from sqlalchemy.orm import mapped_column

# Определение столбцов без использования Annotated
intpk = mapped_column(Integer, primary_key=True)
unique_big_int = mapped_column(BigInteger, unique=True)
created_at = mapped_column(DateTime(timezone=True), server_default=text("TIMEZONE('Europe/Moscow', NOW())"))

# Для строковых столбцов с ограничениями
str_3 = mapped_column(String(3))
str_32 = mapped_column(String(32))
str_140 = mapped_column(String(140))
str_240 = mapped_column(String(240))
