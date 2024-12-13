from fastapi import FastAPI
from routes import user


app = FastAPI(
    tittle="test1",
    debug=True
)


@app.get("/healthcheck", status_code=200, tags=["default"])
def healthcheck():
    return "OK"


app.include_router(user, prefix="/user", tags=["CRUD Users"])
