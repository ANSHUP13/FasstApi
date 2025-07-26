from pydantic import BaseModel, EmailStr, Field
from typing import Dict, List, Optional


class Person1(BaseModel):
    hobbies: List[str] = [] 

class Person2(BaseModel):
    hobbies: List[str] = []


p1 = Person2()
p2 = Person2()
p1.hobbies.append("Reading")
print(p1.hobbies)  # Output: ['Reading']
print(p2.hobbies)  # Output: []
p2.hobbies.append("Writing")
print(p1.hobbies)  # Output: ['Reading']
print(p2.hobbies)  # Output: ['Writing']


from dataclasses import dataclass, field

@dataclass
class MyClass:
    items: list = field(default_factory =list)  # BAD practice

a = MyClass()
b = MyClass()

a.items.append(1)
print(a.items)  # 😱 Output: [1] — b was also affected!

