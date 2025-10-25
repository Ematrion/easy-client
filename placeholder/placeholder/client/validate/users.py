from pydantic import BaseModel, EmailStr
from datetime import datetime

class CompanyModel(BaseModel):
	name: str
	catchPhrase: str
	bs: str

class GeoModel(BaseModel):
	lat: datetime
	lng: datetime | str

class AddressModel(BaseModel):
	geo: GeoModel
	street: str
	suite: str
	city: str
	zipcode: str

class Users(BaseModel):
	company: CompanyModel
	address: AddressModel
	id: int
	name: str
	username: str
	email: EmailStr
	phone: str
	website: str