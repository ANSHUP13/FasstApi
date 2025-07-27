from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, computed_field
from typing import List, Literal, Optional, Annotated
from pprint import pprint


class Person(BaseModel):
    id: Annotated[str, Field(..., description="Unique identifier for the person", example="p001")]
    name: Annotated[str, Field(min_length=1, max_length=50)]
    age: Annotated[int, Field(ge=0, le=120)]  # age must be between 0 and 120
    weight: Annotated[float, Field(gt=0, description= 'weight should be in Kgs')]  # weight must be greater than 0
    height: Annotated[float, Field(gt=0, description= 'height should be in mts')]  # height must be greater than 0
    gender: Annotated[Literal['male','female','other'], Field(default='other')]  #
    email: EmailStr
    contact: str = Field(default='', description="Contact number in string format")
    address: Optional[str] = None
    hobbies: Optional[List[str]] = Field(default_factory=list, max_length=5)  # max 5 hobbies allowed
    # instantiate a new list for each instance similar to hobbies: Optional[List[str]] = [] 


    # mode = 'before' means that the value passed to the validator is the raw value before any type conversion
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value):
        domain = value.split('@')[-1]
        # Ensure the email domain is 'example.com'
        # You can change 'example.com' to any domain you want to validate against
        if domain != 'gmail.com':
            raise ValueError('Email must be from example.com domain')
        return value

    @model_validator(mode='after')
    @classmethod
    def validate_contact(cls, model):
        if ((model.age < 18 or model.age > 60) and (model.contact == '')):
            raise ValueError('Contact number must be present for persons under 18 and over 60 years old')    
        return model
    
    @computed_field
    @property
    def is_adult(self) -> bool:
        return self.age >= 18
    
    @computed_field
    @property
    def is_senior(self) -> bool:
        return self.age >= 60
    
    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height) ** 2) if self.height else 0.0
    

class Update_Person(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[Literal['male', 'female', 'other']] = None
