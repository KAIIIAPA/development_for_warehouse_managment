from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.models.schemas import CreateProduct
from src.backend.models.models import Product
from src.database import get_async_session

router = APIRouter(prefix='/products', tags=['products'])


@router.post('/')
async def post_product(create_product: CreateProduct, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Product).values(**create_product.dict())
    try:
        await session.execute(stmt)
        await session.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Товар добавлен',
        }
    except:
        return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail='Товар с таким именем уже существует'
                )


@router.get('/')
async def get_products(session: AsyncSession = Depends(get_async_session)):
    query = select(Product).order_by(Product.id)
    products = await session.execute(query)
    return products.scalars().all()


@router.get('/{id}')
async def get_product_for_id(product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).filter(Product.id == product_id)
    product_ = await session.execute(query)
    result = product_.scalars().fetchall()
    if not result:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товара с данным id не существует'
        )
    else:
        return result


@router.put('/{id}')
async def get_product_for_id(product_id: int, update_product_model: CreateProduct,
                             session: AsyncSession = Depends(get_async_session)):
    query1 = select(Product).filter(Product.id == product_id)
    product_1 = await session.execute(query1)
    result_1 = product_1.scalars().fetchall()
    if not result_1:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товара с данным id не существует'
        )

    await session.execute(update(Product).where(Product.id == product_id).values(name=update_product_model.name,
                                                                                 description=update_product_model.description,
                                                                                 price=update_product_model.price,
                                                                                 quantity_on_hand=update_product_model.quantity_on_hand))
    await session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Товар обновлен'
    }


@router.delete('/{id}')
async def delete_product(product_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Product).filter(Product.id == product_id)
    product_ = await session.execute(query)
    result = product_.scalars().fetchall()
    if not result:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Товара с данным id не существует'
        )
    else:
        await session.execute(delete(Product).where(Product.id == product_id))
        await session.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Товар удален'
        }