from fastapi import FastAPI, status
from qna_model import QnAModel

app = FastAPI(title="Mini-QnA System")

@app.post("/ask", status_code=status.HTTP_200_OK)
async def ask_qna(payload: QnAModel):
    pass