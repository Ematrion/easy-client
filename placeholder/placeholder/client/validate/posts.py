from pydantic import BaseModel

class Posts(BaseModel):
	userId: int
	id: int
	title: str
	body: str