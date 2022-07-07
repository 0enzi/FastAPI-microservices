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

@app.post('/products')
def create(product: Product):
    return product.save()


