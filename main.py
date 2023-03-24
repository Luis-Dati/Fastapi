from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from deta import Deta
from models import User

deta = Deta("c01ys6dpyyz_heJs9zCra6bQpGjvevHgBCocD8dR7Xgt")
db = deta.Base("Base")

app = FastAPI()

origins=[
	"https://luis-dati.github.io/Jsondata/res.html",
	"http://localhost:8000",
	"http://localhost:8080"
]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
async def root():
	return {"Hello World!"}

@app.get("/user")
async def get_all():
	res=db.fetch()
	respone=res.items
	return respone

@app.post("/user",response_model=User)
async def post_one(user: User):
	respone=db.put(user.dict())
	return respone

@app.delete("/user/{key}")
async def delete_one(key):
	respone=db.delete(key)
	return respone










