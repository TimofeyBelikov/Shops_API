from mongoengine import Document, StringField, ListField, FloatField, ReferenceField, DictField, EmbeddedDocument, EmbeddedDocumentField
from pydantic import BaseModel
from typing import Union, Any, Optional, List, Dict


class Product(Document):
    name = StringField(required=True, max_length=200)
    # Каждый тип товара может относиться к классам
    type = StringField(choices=['econom', 'standard', 'premium'], required=True)
    # У каждого товара может быть разное число параметров
    attributes = DictField()
    # Каждый товар имеет базовую и оптовую це ну
    base_price = FloatField(required=True)
    wholesale_price = FloatField(required=True)
    # Каждый тип товара облагается пошлиной 
    tax = FloatField(required=True)

class Stand(Document):
    name = StringField(required=True, max_length=200)
    # В каждой стойке находится несколько товаров
    products = ListField(ReferenceField(Product))

# В каждом магазине есть программа лояльности для покупателей
class LoyaltyProgram(EmbeddedDocument):
    level = StringField(choices=['base', 'silver', 'gold'])
    discount = FloatField(required=True)

class Store(Document):
    name = StringField(required=True, max_length=200)
    stands = ListField(ReferenceField(Stand))
    loyaltyProgram = EmbeddedDocumentField(LoyaltyProgram)


# Для API

class ProductIn(BaseModel):
    name: str
    type: str
    attributes: Optional[Dict[str, str]]
    base_price: float
    wholesale_price: float
    tax: float
    # prices: Dict[str, Dict[str, float]]

class StandIn(BaseModel):
    name: str
    products: List[ProductIn] = []

class LoyaltyProgramIn(BaseModel):
    level: str
    discount: float

class StoreIn(BaseModel):
    name: str
    loyaltyProgram: LoyaltyProgramIn
    stands: List[StandIn] = []