from fastapi import FastAPI
from pydantic import BaseModel
import sqlalchemy
import pandas as pd
import json


class DoltReq(BaseModel):
    username: str
    password: str
    action: str
    query: str | None = None

engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:secret2@0.0.0.0:3307/edb")

app = FastAPI()

@app.post("/query/")
async def create_item(item: DoltReq):
    if (await authenticated(item)):
        # match only works in python 3.10 and above, so might need to rework as if, elif, else...
        match item.action:
            # if the user is going to make a query:
            case "query":
                if item.query:
                    try:
                        return {"authentication" : await authenticated(item), "value" : await query_table(item.query)}
                    except:
                        return {"authentication" : await authenticated(item), "value" : "Bad query, could not complete request."}
                else:
                    return {"authentication" : await authenticated(item), "value" : "No query string provided, could not complete request."}
            # for authentication checks, no query needed
            case "auth":
                try:
                    return {"authentication" : await authenticated(item), "value" : "Authentication completed."}
                except:
                    return {"authentication" : await authenticated(item), "value" : "Credentials not accepted."}
            # for any other non-matching action
            case _:
                return {"authentication" : await authenticated(item), "value" : "Invalid action."}
    else:
        return {"authentication" : await authenticated(item), "value" : "Credentials not accepted."}

    
async def query_table(query):
    table = pd.read_sql(query, engine)
    return table.to_json()
    
async def authenticated(item):
    user = item.username
    query = f"SELECT password FROM users WHERE username='{user}'"
    pword = pd.read_sql(query, engine).values.ravel()[0]
    auth = item.password
    return pword==auth