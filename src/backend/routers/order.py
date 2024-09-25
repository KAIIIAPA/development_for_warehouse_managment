from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.backend.models.schemas import CreateOrder, OrderStatusEnum
from src.backend.models.models import Product, OrderItem, Order
from src.database import get_async_session

router = APIRouter(prefix='/orders', tags=['orders'])


@router.post('/')
async def post_orders(create_order: CreateOrder, session: AsyncSession = Depends(get_async_session)):
    await session.execute(insert(Order).values())
    orders = (await session.scalars(select(Order))).fetchall()
    last_order_id = 0
    for order in orders:
        if order.id > last_order_id:
            last_order_id = order.id
    if len((await session.scalars(select(Product).where(Product.id == create_order.product_id))).fetchall()) == 0:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Товар с данным id не существует'
        )
    else:
        prods = (await session.scalars(select(Product).where(Product.id == create_order.product_id))).first()
        print(prods)
        print(prods.quantity_on_hand)
        if prods.quantity_on_hand < create_order.quantity:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Количество товара в заказе превышает количество имеющегося товара на складе')
        else:
            await session.execute(insert(OrderItem).values(product_id=create_order.product_id,
                                                           order_id=last_order_id, quantity=create_order.quantity))
            prods.quantity_on_hand = prods.quantity_on_hand - create_order.quantity
            await session.commit()
            return {
                'status_code': status.HTTP_201_CREATED,
                'transaction': 'Заказ добавлен',
            }


@router.get('/')
async def get_orders(session: AsyncSession = Depends(get_async_session)):
    query = select(Order).order_by(Order.id)
    orders = await session.execute(query)
    return orders.scalars().all()


@router.get('/{id}')
async def get_order_for_id(order_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Order).filter(Order.id == order_id)
    order_ = await session.execute(query)
    result = order_.scalars().fetchall()
    if not result:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого заказа не существует'
        )
    else:
        item_order = (await session.scalars(select(OrderItem).where(OrderItem.order_id == order_id))).all()
        order = result
        return 'Заказ: ', order, 'Элементы заказа :', item_order


@router.patch('/{id}/status')
async def get_product_for_id(order_id: int, model_name: OrderStatusEnum, session: AsyncSession = Depends(get_async_session)):
    query = select(Order).filter(Order.id == order_id)
    order_ = await session.execute(query)
    result = order_.scalars().fetchall()
    if not result:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Такого заказа не существует'
        )
    else:
        await session.execute(update(Order).where(Order.id == order_id).values(status=model_name.value))
        await session.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Статус заказа обновлен'
        }
