from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "aaaaa"}


@app.get("/users/{id}")
async def read_item(id: int):
    return {"item_id": id}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]





### items respoonse


from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item