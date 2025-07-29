# app/exceptions.py
from fastapi import  status

class UsernameAlreadyExists(Exception):
   pass

class EmailAlreadyExists(Exception):
   pass

class UserOrPasswordError(Exception):
   pass