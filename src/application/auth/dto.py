from dataclasses import dataclass

@dataclass
class AuthResultDTO:
    status: str
    message: str
    access_token: str

@dataclass
class AuthProfileResultDTO:
    status: str
    message: str

@dataclass
class AuthPostResultDTO:
    status: str
    message: str

