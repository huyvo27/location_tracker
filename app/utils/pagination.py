from typing import Any, Generic, List, Sequence, Type, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(50, ge=1, le=1000)


class Metadata(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int


class PaginatedData(BaseModel, Generic[T]):
    items: Sequence[T]
    metadata: Metadata


async def paginate(
    db: AsyncSession,
    stmt: Any,
    params: PaginationParams,
    schema: Type[BaseModel],
) -> PaginatedData:
    """Paginate the results of a SQLAlchemy statement.
    Args:
        db (AsyncSession): Database session.
        stmt (Any): SQLAlchemy statement to paginate.
        params (PaginationParams): Pagination parameters.
        schema (Type[BaseModel]): Pydantic schema for the response items.
    Returns:
        PaginatedData: Paginated response containing items and metadata.
    Example:
        paginated_data = await paginate(
                                        db=db,
                                        stmt=my_stmt,
                                        params=PaginationParams(page=1,
                                        page_size=10),
                                        schema=MySchema
                                    )
    """

    total_result = await db.execute(select(func.count()).select_from(stmt.subquery()))

    total = total_result.scalar_one()

    paginated_stmt = stmt.offset((params.page - 1) * params.page_size).limit(
        params.page_size
    )
    result = await db.execute(paginated_stmt)
    items = result.scalars().all()

    metadata = Metadata(
        page=params.page,
        page_size=params.page_size,
        total_items=total,
        total_pages=(total + params.page_size - 1) // params.page_size,
    )

    return PaginatedData[schema](items=items, metadata=metadata)


def paginate_without_stmt(
    items: List,
    schema: Type[BaseModel],
) -> PaginatedData:
    """Paginate the results.
    Args:
        items (List): items.
        schema (Type[BaseModel]): Pydantic schema for the response items.
    Returns:
        PaginatedData: Paginated response containing items and metadata.
    Example:
        paginated_data = paginate(
                                    items=items
                                    schema=MySchema
                                )
    """
    metadata = Metadata(
        page=1, page_size=len(items), total_items=len(items), total_pages=1
    )

    return PaginatedData[schema](items=items, metadata=metadata)
