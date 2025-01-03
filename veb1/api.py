
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

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
    date: str
    time: str
    number_of_people: int

class Contact(BaseModel):
    address: str
    phone: str
    email: str

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

app = FastAPI()

@app.get("/cakes/")
def read_cakes():
    return CAKE_DB

@app.get("/cakes/{id}")
def read_cake_item(id: int):
    for item in CAKE_DB:
        if item.id == id:
            return item
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.post("/cakes/")
def create_cake_item(item: CakeItem):
    for existing_item in CAKE_DB:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Торт с таким ID уже существует")
    CAKE_DB.append(item)
    return item

@app.delete("/cakes/{id}")
def delete_cake_item(id: int):
    for index, item in enumerate(CAKE_DB):
        if item.id == id:
            del CAKE_DB[index]
            return {"message": "Торт успешно удален"}
    raise HTTPException(status_code=404, detail="Торт не найден")

@app.get("/feedback/")
def read_feedback():
    return FEEDBACK_DB

@app.get("/feedback/{id}")
def read_feedback_item(id: int):
    for feedback in FEEDBACK_DB:
        if feedback.id == id:
            return feedback
    raise HTTPException(status_code=404, detail="Отзыв не найден")

@app.post("/feedback/")
def create_feedback_item(feedback: Feedback):
    for existing_feedback in FEEDBACK_DB:
        if existing_feedback.id == feedback.id:
            raise HTTPException(status_code=400, detail="Отзыв с таким ID уже существует")
    FEEDBACK_DB.append(feedback)
    return feedback

@app.delete("/feedback/{id}")
def delete_feedback_item(id: int):
    for index, feedback in enumerate(FEEDBACK_DB):
        if feedback.id == id:
            del FEEDBACK_DB[index]
            return {"message": "Отзыв успешно удален"}
    raise HTTPException(status_code=404, detail="Отзыв не найден")

@app.get("/bookings/")
def read_bookings():
    return BOOKING_DB

@app.get("/bookings/{id}")
def read_booking_item(id: int):
    for booking in BOOKING_DB:
        if booking.id == id:
            return booking
    raise HTTPException(status_code=404, detail="Бронирование не найдено")

@app.post("/bookings/")
def create_booking_item(booking: Booking):
    for existing_booking in BOOKING_DB:
        if existing_booking.id == booking.id:
            raise HTTPException(status_code=400, detail="Бронирование с таким ID уже существует")
    BOOKING_DB.append(booking)
    return booking

@app.delete("/bookings/{id}")
def delete_booking_item(id: int):
    for index, booking in enumerate(BOOKING_DB):
        if booking.id == id:
            del BOOKING_DB[index]
            return {"message": "Бронирование успешно удалено"}
    raise HTTPException(status_code=404, detail="Бронирование не найдено")

@app.get("/contact/")
def read_contact():
    return CONTACT_DB

if name == "main":
    uvicorn.run(app, host='127.0.0.1', port=8000)