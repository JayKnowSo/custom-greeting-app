from pydantic import BaseModel, computed_field
from typing import Optional

class SessionModel(BaseModel):
    # Simply define your fields and types here
    name: str
    greetings: int
    number: int
    farewell: str
    id: Optional[int] = None

    # This property calculates the result of greetings * number
    @computed_field
    @property
    def result(self) -> int:
        return self.greetings * self.number
    
# ... your other tests (test_greet, test_session_model_bad, etc.)

def test_session_model_serialization():
    """
    Verifies that SessionModel can be created from a dict 
    and that @computed_field 'result' is included in exports.
    """
    # 1. Setup raw input data
    data = {
        "name": "Alice",
        "greetings": 3,
        "number": 5,
        "farewell": "Goodbye",
        "id": 101
    }
    
    # 2. Initialize model
    session = SessionModel(**data)
    
    # 3. Test that the model exports the computed 'result' field
    # .model_dump() is the Pydantic v2 way to get a dictionary
    serialized_dict = session.model_dump()
    
    assert "result" in serialized_dict
    assert serialized_dict["result"] == 15
    assert serialized_dict["name"] == "Alice"
    print("Serialization test passed: 'result' is included in output.")


   