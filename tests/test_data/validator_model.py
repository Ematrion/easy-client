from pydantic import BaseModel, EmailStr
from enum import StrEnum
from datetime import datetime

class Best_playerModel(BaseModel):
	id: str
	name: str
	score: int

class ScoresModel(BaseModel):
	Red Dragons: int
	Blue Phoenix: int

class MatchesItems(BaseModel):
	teams: list
	best_player: dict
	scores: dict
	match_id: str
	date: datetime

class PlayersItemsRole(StrEnum):
	SNIPER = 'sniper'
	ASSAULT = 'assault'
	SCOUT = 'scout'
	TANK = 'tank'
	SUPPORT = 'support'

class PlayersItems(BaseModel):
	id: str
	name: str
	role: PlayersItemsRole
	email: EmailStr

class CoachModelName(StrEnum):
	COACH_A = 'Coach A'
	COACH_B = 'Coach B'

class CoachModel(BaseModel):
	name: CoachModelName
	experience_years: int

class TeamsItemsName(StrEnum):
	RED_DRAGONS = 'Red Dragons'
	BLUE_PHOENIX = 'Blue Phoenix'

class TeamsItems(BaseModel):
	players: list
	coach: dict
	name: TeamsItemsName

class ValidatorLocation(StrEnum):
	BERLIN = 'Berlin'
	TOKYO = 'Tokyo'
	LOS_ANGELES = 'Los Angeles'
	NEW_YORK = 'New York'
	SYDNEY = 'Sydney'
	SEOUL = 'Seoul'
	LONDON = 'London'
	SHANGHAI = 'Shanghai'
	TORONTO = 'Toronto'
	PARIS = 'Paris'

class Validator(BaseModel):
	matches: list
	teams: list
	tournament: str
	location: ValidatorLocation
	date: datetime