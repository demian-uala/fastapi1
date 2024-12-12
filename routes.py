from fastapi import APIRouter, HTTPException
from schemas import User, CreateUser, UpdateUser
from models import Users
from deps import SQLSession, Config
from sqlalchemy import select
from google.cloud import bigquery
from config import get_settings


user = APIRouter()


@user.post("", status_code=201)
async def create(
    db: SQLSession,
    obj_in: CreateUser
) -> User:
    db_obj = Users(**obj_in.model_dump())
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@user.get("/all", status_code=200)
async def get_all(
    *, 
    db: SQLSession,
    skip: int = 0,
    limit: int = 100
) -> list[User]:
    query = await db.scalars(
        select(
            Users
        ).order_by(
            Users.created_at.desc()
        ).limit(limit).offset(skip)
    )
    return query.unique().all()


@user.get("/{id}", status_code=200)
async def get(
    *,
    db: SQLSession, 
    id: int
) -> User:
    query = await db.get(Users, id)
    if not query:
        raise HTTPException(
            status_code=404,
            detail=f"ID {id} not found"
        )
    return query


@user.patch("/{id}", status_code=200)
async def update(
    *,
    db: SQLSession,
    id: int,
    obj_in: UpdateUser
) -> User:
    db_obj = await get(db=db, id=id)
    update_data = obj_in.model_dump(exclude_unset=True)
    for field, value in db_obj:
        if field in update_data:
            setattr(db_obj, field, update_data[field])

    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj


@user.delete("/{id}", status_code=200)
async def delete(
    *, 
    db: SQLSession, 
    id: int
) -> User:
    query = await get(db=db, id=id)
    await db.delete(query)
    await db.commit()
    return query

import pandas


@user.patch("/migrate", status_code=200)
async def migrate(
    *, 
    db: SQLSession, 
    config: Config
):
    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        autodetect=True,
    )

    users_records = await get_all(db=db, limit=10000)
    records = [u.model_dump() for u in users_records]
    df = pandas.DataFrame(
        records,
        columns=records[0].keys()
    )

    table_id = f"{config.PROJECT_ID}.{config.DATASET}.{config.TABLE}"

    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
