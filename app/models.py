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
