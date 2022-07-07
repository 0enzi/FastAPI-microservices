from math import prod
from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)
redis = get_redis_connection(
    host='redis-17738.c300.eu-central-1-1.ec2.cloud.redislabs.com',
    port=17738,
    password='aGruUThkX5g2WcwWIdwjlozBxV9SRHo2')


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

@app.get('/products')
def all():
    return Product.all_pks()

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity

    }

@app.post('/products')
def create(product: Product):
    return Product.save()

@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/product/{pk}')
def delete(pk: str):
    return Product.delete(pk)


