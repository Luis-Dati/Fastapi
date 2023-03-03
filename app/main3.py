from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#from models import User
from uuid import uuid4,UUID

app=FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel

# định nghĩa database
class User(BaseModel):
	id:Optional[str]
	#Thay thế giá trị của key _id trong mongodb
	name: str
	clas: str
	roles: str

from datetime import date
from pymongo import MongoClient

from dotenv import dotenv_values
config = dotenv_values(".env")

client = MongoClient(config.get("DATABASE_CONNECT_URL"))
database=client.UserList
#UserList: tên của 1 database từ mongo
#Database là một container vật lý cho các collection
#gán giá trị đang có của UserList cho biến "database" 

collection=database.user
#collection có thể được hiểu là 1 bảng lưu trữ các document 
#trong các database có thể có nhiều collection
#tạo 1 collection mới tên là user và gán nó cho biến "collection"

async def get_one(id):
	#document là 1 object trong collection
	#tìm trong collection, 1 object có key name=giá trị của biến "name",
	#rồi gán cho biến document
	document=collection.find_one({"id":id})
	return document

async def get_all():
	users=[]
	#lấy hết dữ liệu trong collection và gán cho cursor
	cursor=collection.find({})
	for document in cursor:
		#lặp qua tất cả các object trong cursor
		#biến document lần lượt nhận các giá trị là 1 object trong cursor
		users.append(User(**document))
		#thêm 1 document vào mảng users
	return users

async def create(user):
	#lấy dữ liệu biến user gán cho document
	document=user
	result=collection.insert_one(document)
	#thêm dữ liệu từ biến document vào bảng collection
	#insert_many: thêm từ 2 object mới trở lên vào collection
	return document

async def remove(id):
	#xóa object nào có key id=id đã cho
	collection.delete_one({"id":id})
	#delete_many({}): xóa hết tất cả object
	return True

	#update giá trị của 1 cặp key-value
	#collection.update_one({1 key-value của object cần target}.{"$set":{key-value cần thay đổi/thêm vào}})

	#count số document trong 1 collection
	#count=collection.count_documents({có thể điền cặp key-value nếu cần target đến 1 số document cụ thể})
#logic data
# if date.today().weekday()==0:
# 	collection.delete_many({})

@app.get("/")
async def root():
	return "Hello World"

@app.get("/api/users")
async def fetch_get():
	response=await get_all()
	#gọi đến hàm get_all trong file database.py rồi gán kết quả cho response
	return response
	#trả lại biến response khi gọi đến đường dẫn này

@app.get("/api/users/{id}",response_model=User)
async def fetch_get_id(id):
	response=await get_one(id)
	return response
	
@app.post("/api/users",response_model=User)
async def fetch_post(user: User):
	response=await create(user.dict())
	return response

@app.delete("/api/users/{id}")
async def fetch_del(id):
	response=await remove(id)
	return response







