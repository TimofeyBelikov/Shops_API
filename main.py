from typing import Union, Any
from fastapi_redis_session import setSession
import redis
from fastapi import FastAPI, HTTPException
import logging
import aioredis
import conf
from pydantic import BaseModel
from common import *
from conf import *
from logger import *
from pymongo import MongoClient
from mongoengine import connect, DoesNotExist
from models import *
from routers import store, product, stand

app = FastAPI()
app.include_router(product.router)
app.include_router(store.router)
app.include_router(stand.router)

connect(db='shoplab', host='localhost', port=27017, username='root', password='password')

MONGO_CLIENT = MongoClient('mongodb://root:password@localhost:27017')
MONGO_DB = MONGO_CLIENT['stores']

@app.post('/stores/')
def create_store(store_data : StoreIn):
    print('create store', store_data)
    loyalty_program = LoyaltyProgram(**store_data.loyaltyProgram.dict())
    stands = []
    # Если есть стенды, то добавим их
    for stand_data in store_data.stands:
        products = []
        for product_data in stand_data.products:
            product = Product(**product_data.dict()).save()
            products.append(product)
        stand = Stand(name=stand_data.name, products=products).save()
        stands.append(stand)
    # Создаём объект магазина
    store = Store(name=store_data.name, stands=stands, loyaltyProgram=loyalty_program)
    store.save()
    return {"message": "Магазин создан", "store_id": str(store.id)}

# Список всех магазинов
@app.get('/stores/')
def get_stores():
    try:
        stores = Store.objects.all()
    except Exception:
        raise HTTPException(status_code=404, detail="Возникла ошибка")
    stores_data = []
    print(stores)
    for store in stores:
        store_data = {
            "id": str(store.id),
            "name": store.name,
            "loyaltyProgram": store.loyaltyProgram.to_mongo() if store.loyaltyProgram else None,
            "stands": [
                {
                    "id": str(stand.id),
                    "name": stand.name,
                    "products": [
                        {
                            "id": str(product.id),
                            "name": product.name,
                            "type": product.type,
                            "attributes": product.attributes,
                            "base_price": product.base_price,
                            "wholesale_price": product.wholesale_price,
                            "tax": product.tax,
                            # "prices": product.prices,
                        }
                        for product in stand.products
                    ]
                }
                for stand in store.stands
            ]
        }
        stores_data.append(store_data)

    return stores_data

# Конкретный магазин по ID
@app.get('/stores/{store_id}/')
def get_store(store_id: str):
    try:
        store = Store.objects.get(id=store_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    store_data = {
        "id": str(store.id),
        "name": store.name,
        "loyaltyProgram": store.loyaltyProgram.to_mongo(),
        "stands": [
            {
                "name": stand.name,
                "id": str(stand.id),
                "products": [
                    {
                        "name": product.name,
                        "type": product.type,
                        "attributes": product.attributes,
                        "base_price": product.base_price,
                        "wholesale_price": product.wholesale_price,
                        "tax": product.tax,
                        # "prices": product.prices,
                    }
                    for product in stand.products
                ]
            }
            for stand in store.stands
        ]
    }
    return store_data


# Конкретный стенд по ID
@app.get('/stand/{stand_id}/')
def get_stand(stand_id: str):
    try:
        stand = Stand.objects.get(id=stand_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Стенд не найден")
    stand_data = {
        "id": str(stand.id),
        "name": stand.name,
        "products": [
            {
                "name": product.name,
                "type": product.type,
                "attributes": product.attributes,
                "base_price": product.base_price,
                "wholesale_price": product.wholesale_price,
                "tax": product.tax,
                # "prices": product.prices,
            }
            for product in stand.products
        ]
    }
    return stand_data

@app.post("/stands/{store_id}/")
def add_stand(store_id: str, stand_data: StandIn):
    try:
        print('try post stand')
        store = Store.objects.get(id=store_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Магазин не найден")
    
    products = []
    for product_data in stand_data.products:
        product = Product(**product_data.dict()).save()
        products.append(product)

    stand = Stand(name=stand_data.name, products=products).save()
    store.update(push__stands=stand)

    return {"message": "Stand added successfully", "stand_id": str(stand.id)}

@app.get('/healthcheck/')
def _healthcheck():
    return {'health': 'ok'}
