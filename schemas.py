from pydantic import Field, BaseModel, model_validator, ConfigDict


class User(BaseModel):
    id: int
    name: str
    lastname: str
    dni: str
    phone: str | None = None
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    name: str
    lastname: str
    dni: str
    phone: str | None
    email: str


class UpdateUser(BaseModel):
    name: str | None
    lastname: str | None
    dni: str | None
    phone: str | None
    email: str | None


# {
#     "name": "algo",
#     "lastname": "perez",
#     "dni": "00-000-000",
#     "email": "sarasa@gmail.com"
# }


# {
#     "email": "saras@gmail.com"
# }