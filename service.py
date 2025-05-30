from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3

import jwt

import datetime

import requests

from pathlib import Path

async def get_roles(db: Session):


    query = db.query(models.Roles)







    roles_all = query.all()
    roles_all = [new_data.to_dict() for new_data in roles_all] if roles_all else roles_all
    res = {
        'roles_all': roles_all,
    }
    return res

async def get_roles_role_id(db: Session, role_id: int):

    roles_one = db.query(models.Roles).filter(models.Roles.role_id == role_id).first() 
    roles_one = roles_one.to_dict() if roles_one else roles_one

    res = {
        'roles_one': roles_one,
    }
    return res

async def put_roles_role_id(db: Session, role_id: int, role_name: str):

    roles_edited_record = db.query(models.Roles).filter(models.Roles.role_id == role_id).first()
    for key, value in {'role_id': role_id, 'role_name': role_name}.items():
          setattr(roles_edited_record, key, value)
    db.commit()
    db.refresh(roles_edited_record)
    roles_edited_record = roles_edited_record.to_dict() 

    res = {
        'roles_edited_record': roles_edited_record,
    }
    return res

async def delete_roles_role_id(db: Session, role_id: int):

    roles_deleted = None
    record_to_delete = db.query(models.Roles).filter(models.Roles.role_id == role_id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        roles_deleted = record_to_delete.to_dict() 

    res = {
        'roles_deleted': roles_deleted,
    }
    return res

async def get_users(db: Session):


    query = db.query(models.Users)







    users_all = query.all()
    users_all = [new_data.to_dict() for new_data in users_all] if users_all else users_all
    res = {
        'users_all': users_all,
    }
    return res

async def get_users_user_id(db: Session, user_id: int):

    users_one = db.query(models.Users).filter(models.Users.user_id == user_id).first() 
    users_one = users_one.to_dict() if users_one else users_one

    res = {
        'users_one': users_one,
    }
    return res

async def put_users_user_id(db: Session, user_id: int, username: str, email: str, role_id: int):

    users_edited_record = db.query(models.Users).filter(models.Users.user_id == user_id).first()
    for key, value in {'email': email, 'role_id': role_id, 'user_id': user_id, 'username': username}.items():
          setattr(users_edited_record, key, value)
    db.commit()
    db.refresh(users_edited_record)
    users_edited_record = users_edited_record.to_dict() 

    res = {
        'users_edited_record': users_edited_record,
    }
    return res

async def delete_users_user_id(db: Session, user_id: int):

    users_deleted = None
    record_to_delete = db.query(models.Users).filter(models.Users.user_id == user_id).first()

    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict() 

    res = {
        'users_deleted': users_deleted,
    }
    return res

async def post_users(db: Session, raw_data: schemas.PostUsers , request: Request):
    user_id:int = raw_data.user_id
    username:str = raw_data.username
    email:str = raw_data.email
    role_id:int = raw_data.role_id
    page:int = raw_data.page
    limit:int = raw_data.limit

    header_authorization:str = request.headers.get('header-authorization')


    record_to_be_added = {'email': email, 'role_id': role_id, 'user_id': user_id, 'username': username}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    users_inserted_record = new_users.to_dict()



    query = db.query(models.Users, models.Roles)
        
    query = query.join(models.Roles,
                
        and_(
            models.Users.role_id ==models.Roles.role_id
        
        )
                       )


    query = query.order_by(models.Users.user_id.asc())


    query = query.limit(limit)



    user_roles = query.all()
    user_roles = [
        {
            "user_roles_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
            "user_roles_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
        }
        for s1, s2 in user_roles
    ] if user_roles else user_roles


    query = db.query(models.Users, models.Roles)
        
    query = query.join(models.Roles,
                
        and_(
            models.Users.user_id ==models.Roles.role_id
        
        )
                       )


    query = query.order_by(models.Users.user_id.asc())


    query = query.limit(limit)



    user_left_join_records = query.all()
    user_left_join_records = [
        {
            "user_left_join_records_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
            "user_left_join_records_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
        }
        for s1, s2 in user_left_join_records
    ] if user_left_join_records else user_left_join_records


    headers = {'authorization': header_authorization}
    auth=('', '')
    payload = {'workspace_name': username, 'workspace_description': username}
    apiResponse = requests.post(
        'https://cc1fbde45ead-in-south-01.backstract.io/sigma/api/v1/workspace/create',
        headers=headers,
        json=payload if 'raw' == 'raw' else None
    )
    user_craete_workspace = apiResponse.json() if 'dict' in ['dict', 'list'] else apiResponse.text
    res = {
        'users_inserted_record': users_inserted_record,
        'user_roles': user_roles,
        'user_left_join_records': user_left_join_records,
        'fdkjshgdg': user_craete_workspace,
    }
    return res

async def post_roles(db: Session, raw_data: schemas.PostRoles):
    role_id:int = raw_data.role_id
    role_name:str = raw_data.role_name


    record_to_be_added = {'role_id': role_id, 'role_name': role_name}
    new_roles = models.Roles(**record_to_be_added)
    db.add(new_roles)
    db.commit()
    db.refresh(new_roles)
    roles_inserted_record = new_roles.to_dict()



    headers = {}
    auth=('', '')
    payload = {'userId': role_name}
    apiResponse = requests.post(
        'https://jsonplaceholder.typicode.com/posts',
        headers=headers,
        json=payload if 'raw' == 'raw' else None
    )
    sdfgjcfxhd = apiResponse.json() if 'dict' in ['dict', 'list'] else apiResponse.text


    headers = {}
    auth=('', '')
    payload = {}
    apiResponse = requests.get(
        'https://jsonplaceholder.typicode.com/todos/1',
        headers=headers,
        json=payload if 'params' == 'raw' else None
    )
    sdgfsh = apiResponse.json() if 'dict' in ['dict', 'list'] else apiResponse.text


    jhgjdf = aliased(models.Roles)
    query = db.query(models.Users, jhgjdf)
        
    query = query.join(jhgjdf,
                
        and_(
            models.Users.username !=jhgjdf.email
        
        )
                       )


    query = query.order_by(models.Users.user_id.desc())


    query = query.limit(role_id)



    jhbhbkjdfhdf = query.all()
    jhbhbkjdfhdf = [
        {
            "jhbhbkjdfhdf_1": s1.to_dict() if hasattr(s1, "to_dict") else s1.__dict__,
            "jhbhbkjdfhdf_2": s2.to_dict() if hasattr(s2, "to_dict") else s2.__dict__,
        }
        for s1, s2 in jhbhbkjdfhdf
    ] if jhbhbkjdfhdf else jhbhbkjdfhdf
    res = {
        'roles_inserted_record': roles_inserted_record,
        'mbgdfn': sdfgjcfxhd,
        'kfjdhk': sdgfsh,
        'ndsvghdf': jhbhbkjdfhdf,
    }
    return res

