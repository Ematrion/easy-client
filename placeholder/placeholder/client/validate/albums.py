from pydantic import BaseModel

class Albums(BaseModel):
	userId: int
	id: int
	title: str