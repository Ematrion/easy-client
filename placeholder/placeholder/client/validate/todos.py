from pydantic import BaseModel

class Todos(BaseModel):
	userId: int
	id: int
	title: str
	completed: bool