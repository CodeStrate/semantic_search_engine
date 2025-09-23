from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

class QnAModel(BaseModel):
    query: str = Field(..., description="User's query to the System")
    k: int = Field(default=5, description="Number of k Chunks to retrieve as an answer")
    mode: Literal["baseline", "hybrid-bm25"] = Field(default="baseline", description="Mode of chunk retrieval (base retrieve or hybrid-bm25 reranking)")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example" : {
                "query" : "What is Machinery Regulation?",
                "k" : 5,
                "mode" : "baseline"
            }
    })
