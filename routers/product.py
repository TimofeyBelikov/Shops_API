from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from models import Store, LoyaltyProgram, Stand, Product, ProductIn
from mongoengine import DoesNotExist

router = APIRouter()

# Добавление товаров на стойку
@router.post("/stands/{stand_id}/products/")
def add_product(stand_id: str, product_data: ProductIn):
    try:
        stand = Stand.objects.get(id=stand_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Стойка не найдена")
    
    product = Product(**product_data.dict()).save()
    stand.update(push__products=product)

    return {"message": "Товар добавлен", "product_id": str(product.id)}

@router.patch("/stands/{stand_id}/products/{product_id}")
def update_product(stand_id: str, product_id: str, product : ProductIn):
    try:
        product = Product.objects.get(id=product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Товар не найден")
    # Обновление продукта