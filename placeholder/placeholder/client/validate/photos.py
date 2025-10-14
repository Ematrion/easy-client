from pydantic import BaseModel, HttpUrl

class Photos(BaseModel):
	albumId: int
	id: int
	title: str
	url: HttpUrl
	thumbnailUrl: HttpUrl