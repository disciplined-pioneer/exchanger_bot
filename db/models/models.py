from datetime import datetime, timedelta
from typing import TypeVar, Generic, Sequence

from typing import Optional, List
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, case, desc, JSON, func 

from sqlalchemy.orm import Mapped, selectinload, load_only
from sqlalchemy.sql import select, update as sqlalchemy_update

from db.models.mapped_columns import *
from core.psql import async_db_session, Base


T = TypeVar("T")


class ModelAdmin(Generic[T]):
    
    class DoesNotExists(Exception):
        pass

    @classmethod
    async def create(cls, **kwargs) -> T:
        """
        # Создает новый объект и возвращает его.
        :param kwargs: Поля и значения для объекта.
        :return: Созданный объект.
        """

        async with async_db_session() as session:
            obj = cls(**kwargs)
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj

    @classmethod
    async def add(cls, **kwargs) -> None:
        """
        # Создает новый объект.
        :param kwargs: Поля и значения для объекта.
        """

        async with async_db_session() as session:
            session.add(cls(**kwargs))
            await session.commit()

    async def update(self, **kwargs) -> None:
        """
        # Обновляет текущий объект.
        :param kwargs: Поля и значения, которые надо поменять.
        """

        async with async_db_session() as session:
            await session.execute(
                sqlalchemy_update(self.__class__), [{"id": self.id, **kwargs}]
            )
            await session.commit()

    async def delete(self) -> None:
        """
        # Удаляет объект.
        """
        async with async_db_session() as session:
            await session.delete(self)
            await session.commit()

    @classmethod
    async def get(cls, select_in_load: str | None = None, **kwargs) -> T:
        """
        # Возвращает одну запись, которая удовлетворяет введенным параметрам.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Объект или вызовет исключение DoesNotExists.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with async_db_session() as session:
                results = await session.execute(query)
                (result,) = results.one()
                return result
        except NoResultFound:
            return None

    @classmethod
    async def filter(cls, select_in_load: str | None = None, **kwargs) -> Sequence[T]:
        """
        # Возвращает все записи, которые удовлетворяют фильтру.

        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения.
        :return: Перечень записей.
        """

        params = [getattr(cls, key) == val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        try:
            async with async_db_session() as session:
                results = await session.execute(query)
                return results.scalars().all()
        except NoResultFound:
            return ()

    @classmethod
    async def all(
            cls, select_in_load: str = None, values: list[str] = None
    ) -> Sequence[T]:
        """
        # Получает все записи.

        :param select_in_load: Загрузить сразу связанную модель.
        :param values: Список полей, которые надо вернуть, если нет, то все (default None).
        """

        if values and isinstance(values, list):
            # Определенные поля
            values = [getattr(cls, val) for val in values if isinstance(val, str)]
            query = select(cls).options(load_only(*values))
        else:
            # Все поля
            query = select(cls)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        async with async_db_session() as session:
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def exclude(cls, select_in_load: str | None = None, **kwargs) -> Sequence[T]:
        """
        # Возвращает все записи, которые не удовлетворяют фильтру (то есть, исключает значения).
        :param select_in_load: Загрузить сразу связанную модель.
        :param kwargs: Поля и значения для исключения.
        :return: Перечень записей.
        """
        # Строим условия для исключения (не равно)
        params = [getattr(cls, key) != val for key, val in kwargs.items()]
        query = select(cls).where(*params)

        if select_in_load:
            query.options(selectinload(getattr(cls, select_in_load)))

        async with async_db_session() as session:
            result = await session.execute(query)
            return result.scalars().all()

# Хранение списка всех пользователей
class Users(Base, ModelAdmin):
    
    __tablename__ = 'users'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    role: Mapped[str]

    @classmethod
    async def get_allowed_tg_ids(cls) -> list[int]:
        """
        Возвращает список tg_id всех пользователей, у которых роль не 'ban'.
        """
        async with async_db_session() as session:
            result = await session.execute(
                select(cls.tg_id).where(cls.role != 'ban')
            )
            return [row.tg_id for row in result]


# Хранение списка всех партнёров
class Partners(Base, ModelAdmin):
    
    __tablename__ = 'partners'

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    name: Mapped[str]
    active_pairs: Mapped[dict] = mapped_column(JSON)

    @classmethod
    async def get_ids_by_from_and_platform(cls, from_currency: str, platform: str) -> List[int]:
        """
        Возвращает список ID партнёров, у которых в active_pairs есть указанные 'from' и 'platform'.
        """
        async with async_db_session() as session:
            result = await session.execute(select(cls))
            partners = result.scalars().all()

            matching_ids = []
            for partner in partners:
                for pair in partner.active_pairs:
                    if pair.get("from") == from_currency and pair.get("platform") == platform:
                        matching_ids.append(partner.tg_id)
                        break

            return matching_ids
    

# Хранение всех ставок
class Rates(Base, ModelAdmin):
    
    __tablename__ = 'rates'

    id: Mapped[intpk]
    from_currency: Mapped[str]
    to_currency: Mapped[str]

    rate: Mapped[float] = mapped_column(Float)
    platform: Mapped[str]
    limits: Mapped[str]
    partner_id: Mapped[int] = mapped_column(BigInteger)
    date: Mapped[datetime]

    @classmethod
    async def get_latest_rate(
        cls,
        from_currency: str,
        to_currency: str,
        platform: str,
        partner_id: int
    ) -> Optional["Rates"]:
        
        """Выозвращает последний (самый новый) курс обмена """

        async with async_db_session() as session:
            result = await session.execute(
                select(cls)
                .where(
                    cls.from_currency == from_currency,
                    cls.to_currency == to_currency,
                    cls.platform == platform,
                    cls.partner_id == partner_id
                )
                .order_by(desc(cls.date))
                .limit(1)
            )
            return result.scalar_one_or_none()


# Хранение всех обменов
class Exchanges(Base, ModelAdmin):
    
    __tablename__ = 'exchanges'

    id: Mapped[intpk]
    client_id: Mapped[int] = mapped_column(BigInteger)
    partner_id: Mapped[int] = mapped_column(BigInteger)

    from_currency: Mapped[str]
    to_currency: Mapped[str]

    amout_from: Mapped[float] = mapped_column(Float)
    amout_to: Mapped[float] = mapped_column(Float)

    platform: Mapped[str]
    state: Mapped[str]

    created_at: Mapped[datetime]
    update_at: Mapped[datetime]

    payment_check: Mapped[str]
    state_completed = "COMPLETED"

    @classmethod
    async def get_cny_sales_summary(cls) -> dict:
        """
        Возвращает сумму проданных CNY (amout_from, где to_currency == 'CNY') за день, неделю и месяц
        для завершённых обменов.
        """
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        start_of_week = start_of_day - timedelta(days=start_of_day.weekday())  # Понедельник
        start_of_month = datetime(now.year, now.month, 1)

        async with async_db_session() as session:
            result = await session.execute(
                select(
                    func.sum(
                        case((cls.created_at >= start_of_day, cls.amout_from), else_=0.0)
                    ).label("day_sum"),
                    func.sum(
                        case((cls.created_at >= start_of_week, cls.amout_from), else_=0.0)
                    ).label("week_sum"),
                    func.sum(
                        case((cls.created_at >= start_of_month, cls.amout_from), else_=0.0)
                    ).label("month_sum"),
                ).where(
                    cls.to_currency == "CNY",
                    cls.state == cls.state_completed
                )
            )

            row = result.first()
            return {
                "day": row.day_sum or 0.0,
                "week": row.week_sum or 0.0,
                "month": row.month_sum or 0.0,
            }

    @classmethod
    async def get_amout_to_current_month(cls) -> float:
        """
        Возвращает сумму amout_to за текущий месяц для завершённых обменов.
        """
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        next_month = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)

        async with async_db_session() as session:
            result = await session.execute(
                select(func.sum(cls.amout_to))
                .where(
                    cls.created_at >= start_of_month,
                    cls.created_at < next_month,
                    cls.state == cls.state_completed
                )
            )
            total = result.scalar()
            return total or 0.0

    @classmethod
    async def get_amout_from_for_month(cls, from_currency: str) -> float:
        """
        Получает сумму amout_from для указанной валюты за текущий месяц для завершённых обменов.
        """
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)

        async with async_db_session() as session:
            result = await session.execute(
                select(func.sum(cls.amout_from))
                .where(
                    cls.from_currency == from_currency,
                    cls.created_at >= start_of_month,
                    cls.state == cls.state_completed
                )
            )
            total_amount = result.scalar()
            return total_amount or 0.0

    @classmethod
    async def get_deal_count_by_partner(cls, partner_id: int) -> int:
        """
        Возвращает количество завершённых сделок с данным партнёром.
        """
        async with async_db_session() as session:
            result = await session.execute(
                select(func.count())
                .where(
                    cls.partner_id == partner_id,
                    cls.state == cls.state_completed
                )
            )
            count = result.scalar()
            return count or 0


# Хранение комиссий
class Commissions(Base, ModelAdmin):
    
    __tablename__ = 'commissions'

    id: Mapped[intpk]
    date: Mapped[datetime]
    commissions = mapped_column(Float)


    @classmethod
    async def get_monthly_commission_sum(cls) -> float:
        """
        Возвращает сумму всех комиссий за текущий месяц.
        """
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        next_month = datetime(now.year + 1, 1, 1) if now.month == 12 else datetime(now.year, now.month + 1, 1)

        async with async_db_session() as session:
            result = await session.execute(
                select(func.sum(cls.commissions))
                .where(cls.date >= start_of_month, cls.date < next_month)
            )
            total = result.scalar()
            return total or 0.0


