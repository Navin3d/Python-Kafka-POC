from pydantic import BaseModel, EmailStr
from typing import Literal


class Coordinates(BaseModel):
    lat: float
    lng: float


class Address(BaseModel):
    address: str
    city: str
    state: str
    stateCode: str
    postalCode: str
    coordinates: Coordinates
    country: str


class Hair(BaseModel):
    color: str
    type: str


class Bank(BaseModel):
    cardExpire: str
    cardNumber: str
    cardType: str
    currency: str
    iban: str


class Company(BaseModel):
    department: str
    name: str
    title: str
    address: Address


class Crypto(BaseModel):
    coin: str
    wallet: str
    network: str


class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    maidenName: str
    age: int
    gender: str
    email: EmailStr
    phone: str
    username: str
    password: str
    birthDate: str
    image: str
    bloodGroup: str
    height: float
    weight: float
    eyeColor: str
    hair: Hair
    ip: str
    address: Address
    macAddress: str
    university: str
    bank: Bank
    company: Company
    ein: str
    ssn: str
    userAgent: str
    crypto: Crypto
    role: Literal["admin", "user", "moderator"]
