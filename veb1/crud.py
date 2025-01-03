from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import uvicorn
from datetime import datetime

class CakeItem(BaseModel):
    id: int
    name: str
    description: str
    image_url: str

class Feedback(BaseModel):
    id: int
    name: str
    comment: str

class Booking(BaseModel):
    id: int
    name: str
    date: str = Field(..., example="2023-12-25")
    time: str = Field(..., example="18:00")
    number_of_people: int

    @field_validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v

    @field_validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Time must be in HH:MM format')
        return v

class Contact(BaseModel):
    address: str
    phone: str
    email: str

class User(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None

class Order(BaseModel):
    id: int
    user_id: int
    cake_ids: List[int]
    total_price: float
    order_date: str = Field(..., example="2023-12-25")

    @field_validator('order_date')
    def validate_order_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Order date must be in YYYY-MM-DD format')
        return v

CAKE_DB = [
    CakeItem(id=1, name="Шоколадный торт", description="Шоколадный торт — это классика кондитерского искусства. Он сочетает в себе нежный вкус шоколада и мягкую текстуру бисквита.", image_url="c-cake.jpg"),
    CakeItem(id=2, name="Ванильный торт", description="Ванильный торт — это воплощение классической элегантности. Его нежный вкус и аромат ванили делают его идеальным для любого случая.", image_url="v-cake.jpg"),
    CakeItem(id=3, name="Фруктовый торт", description="Фруктовый торт — это свежий и легкий десерт, идеально подходящий для летних дней.", image_url="f-cake.jpg"),
    CakeItem(id=4, name="Чизкейк", description="Чизкейк — это нежный и кремовый десерт, который покорил сердца миллионов людей по всему миру.", image_url="chizkeik.jpg"),
    CakeItem(id=5, name="Тирамису", description="Тирамису — это итальянский десерт, который сочетает в себе кофе, маскарпоне и савоярди.", image_url="tt-cake.jpg"),
    CakeItem(id=6, name="Макарон", description="Макарон — это французское печенье, которое состоит из двух меренг с начинкой между ними.", image_url="m.jpg"),
]

FEEDBACK_DB = [
    Feedback(id=1, name="Анна Иванова", comment="Отличные торты, особенно шоколадный!"),
    Feedback(id=2, name="Иван Петров", comment="Ванильный торт был просто восхитителен!"),
]

BOOKING_DB = [
    Booking(id=1, name="Мария Сидорова", date="2023-12-25", time="18:00", number_of_people=4),
    Booking(id=2, name="Дмитрий Кузнецов", date="2023-12-26", time="19:00", number_of_people=2),
]

CONTACT_DB = Contact(
    address="ул. Профсоюзов, 8, г. Сургут",
    phone="8(945) 426-89-27",
    email="info@pokofeyku.com"
)

USER_DB = [
    User(id=1, name="Алексей Петров", email="alex@example.com", phone="123-456-7890"),
    User(id=2, name="Мария Иванова", email="maria@example.com", phone="987-654-3210"),
]

ORDER_DB = [
    Order(id=1, user_id=1, cake_ids=[1, 2], total_price=50.0, order_date="2023-12-25"),
    Order(id=2, user_id=2, cake_ids=[3], total_price=30.0, order_date="2023-12-26"),
]

app = FastAPI()

# CRUD для CakeItem
@app.get("/cakes/", response_model=List[CakeItem])
def read_cakes():
    return CAKE_DB

@app.get("/cakes/{id}", response_model=CakeItem)
def read_cake_item(id: int):
    for item in CAKE_DB:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.post("/cakes/", response_model=CakeItem)
def create_cake_item(item: CakeItem):
    for existing_item in CAKE_DB:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Торт с таким ID уже существует")
    CAKE_DB.append(item)
    return item

@app.put("/cakes/{id}", response_model=CakeItem)
def update_cake_item(id: int, item: CakeItem):
    for index, existing_item in enumerate(CAKE_DB):
        if existing_item.id == id:
            CAKE_DB[index] = item
            return item
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.delete("/cakes/{id}", response_model=dict)
def delete_cake_item(id: int):
    for index, item in enumerate(CAKE_DB):
        if item.id == id:
            del CAKE_DB[index]
            return {"message": "Торт успешно удален"}
    raise HTTPException(status_code=404, detail="Торт не найден")

# CRUD для Feedback
@app.get("/feedback/", response_model=List[Feedback])
def read_feedback():
    return FEEDBACK_DB

@app.get("/feedback/{id}", response_model=Feedback)
def read_feedback_item(id: int):
    for feedback in FEEDBACK_DB:
        if feedback.id == id:
            return feedback
    raise HTTPException(status_code=404, detail="Отзыв не найден")

@app.post("/feedback/", response_model=Feedback)
def create_feedback_item(feedback: Feedback):
    for existing_feedback in FEEDBACK_DB:
        if existing_feedback.id == feedback.id:
            raise HTTPException(status_code=400, detail="Отзыв с таким ID уже существует")
    FEEDBACK_DB.append(feedback)
    return feedback

@app.put("/feedback/{id}", response_model=Feedback)
def update_feedback_item(id: int, feedback: Feedback):
    for index, existing_feedback in enumerate(FEEDBACK_DB):
        if existing_feedback.id == id:
            FEEDBACK_DB[index] = feedback
            return feedback
    raise HTTPException(status_code=404, detail="Отзыв не найден")

@app.delete("/feedback/{id}", response_model=dict)
def delete_feedback_item(id: int):
    for index, feedback in enumerate(FEEDBACK_DB):
        if feedback.id == id:
            del FEEDBACK_DB[index]
            return {"message": "Отзыв успешно удален"}
    raise HTTPException(status_code=404, detail="Отзыв не найден")

# CRUD для Booking
@app.get("/bookings/", response_model=List[Booking])
def read_bookings():
    return BOOKING_DB

@app.get("/bookings/{id}", response_model=Booking)
def read_booking_item(id: int):
    for booking in BOOKING_DB:
        if booking.id == id:
            return booking
    raise HTTPException(status_code=404, detail="Бронирование не найдено")

@app.post("/bookings/", response_model=Booking)
def create_booking_item(booking: Booking):
    for existing_booking in BOOKING_DB:
        if existing_booking.id == booking.id:
            raise HTTPException(status_code=400, detail="Бронирование с таким ID уже существует")
    BOOKING_DB.append(booking)
    return booking

@app.put("/bookings/{id}", response_model=Booking)
def update_booking_item(id: int, booking: Booking):
    for index, existing_booking in enumerate(BOOKING_DB):
        if existing_booking.id == id:
            BOOKING_DB[index] = booking
            return booking
    raise HTTPException(status_code=404, detail="Бронирование не найдено")

@app.delete("/bookings/{id}", response_model=dict)
def delete_booking_item(id: int):
    for index, booking in enumerate(BOOKING_DB):
        if booking.id == id:
            del BOOKING_DB[index]
            return {"message": "Бронирование успешно удалено"}
    raise HTTPException(status_code=404, detail="Бронирование не найдено")

# CRUD для User
@app.get("/users/", response_model=List[User])
def read_users():
    return USER_DB

@app.get("/users/{id}", response_model=User)
def read_user_item(id: int):
    for user in USER_DB:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.post("/users/", response_model=User)
def create_user_item(user: User):
    for existing_user in USER_DB:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="Пользователь с таким ID уже существует")
    USER_DB.append(user)
    return user

@app.put("/users/{id}", response_model=User)
def update_user_item(id: int, user: User):
    for index, existing_user in enumerate(USER_DB):
        if existing_user.id == id:
            USER_DB[index] = user
            return user
    raise HTTPException(status_code=404, detail="Пользователь не найден")

@app.delete("/users/{id}", response_model=dict)
def delete_user_item(id: int):
    for index, user in enumerate(USER_DB):
        if user.id == id:
            del USER_DB[index]
            return {"message": "Пользователь успешно удален"}
    raise HTTPException(status_code=404, detail="Пользователь не найден")

# CRUD для Order
@app.get("/orders/", response_model=List[Order])
def read_orders():
    return ORDER_DB

@app.get("/orders/{id}", response_model=Order)
def read_order_item(id: int):
    for order in ORDER_DB:
        if order.id == id:
            return order
    raise HTTPException(status_code=404, detail="Заказ не найден")

@app.post("/orders/", response_model=Order)
def create_order_item(order: Order):
    for existing_order in ORDER_DB:
        if existing_order.id == order.id:
            raise HTTPException(status_code=400, detail="Заказ с таким ID уже существует")
    ORDER_DB.append(order)
    return order

@app.put("/orders/{id}", response_model=Order)
def update_order_item(id: int, order: Order):
    for index, existing_order in enumerate(ORDER_DB):
        if existing_order.id == id:
            ORDER_DB[index] = order
            return order
    raise HTTPException(status_code=404, detail="Заказ не найден")

@app.delete("/orders/{id}", response_model=dict)
def delete_order_item(id: int):
    for index, order in enumerate(ORDER_DB):
        if order.id == id:
            del ORDER_DB[index]
            return {"message": "Заказ успешно удален"}
    raise HTTPException(status_code=404, detail="Заказ не найден")

@app.get("/contact/", response_model=Contact)
def read_contact():
    return CONTACT_DB

if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)