from pydantic import BaseModel, EmailStr

class Comments(BaseModel):
	postId: int
	id: int
	name: str
	email: EmailStr
	body: str