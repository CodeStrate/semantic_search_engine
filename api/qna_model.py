from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class QnAModel(BaseModel):
    query: str = Field(..., description="User's query to the System")
    k: int = Field(..., description="Number of k Chunks to retrieve as an answer", default=3)
    mode: Literal["baseline", "hybrid"] = Field(..., description="Mode of chunk retrieval (base retrieve or hybrid reranking)", default="baseline")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example" : {
                "query" : "What is Machinery Regulation?",
                "k" : 5,
                "mode" : "baseline"
            }
    })
