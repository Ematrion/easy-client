
# CodeBase

## Features
- logs
- errors handling


---

## Improvements
- create imports for generated class
- checks redundant Pydantic models builds from different endpoints
- use sqlparse.KEYWORDS to filter sematnic sql protected words
(https://github.com/andialbrecht/sqlparse/blob/master/sqlparse/keywords.py) 


---

# Commands

## commands.validate

under construction
- add class builder
- care about EmailStr Annotatted or type
- deal with dict/list with recursion ? car about naming clash
- detect Enum
- Implement a validation proof-test with % of failed data point




---

# Testing:

## Pytest

## Tutorial APIs
https://jsonplaceholder.typicode.com
https://dummyjson.com 



---

# External tool

## SI-LLM
A data-aware schema inference based on LLM. No readm nor distribuiotn atm

papre link: https://www.arxiv.org/pdf/2509.04632
github: https://github.com/PierreWoL/SILLM/tree/master