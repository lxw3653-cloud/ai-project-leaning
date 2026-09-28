"""AI 相关接口：聊天问答、笔记总结。"""

from fastapi import APIRouter, HTTPException

from app.ai.client import AiServiceError
from app.ai.service import answer_question, summarize_notes
from app.schemas.ai import ChatRequest, ChatResponse, SummarizeRequest, SummarizeResponse

router = APIRouter(tags=["ai"])


@router.post("/ai/chat", response_model=ChatResponse, summary="AI 问答")
async def chat(payload: ChatRequest) -> ChatResponse:
    try:
        answer = await answer_question(
            question=payload.question,
            history=[message.model_dump() for message in payload.history],
        )
    except AiServiceError as error:
        # AiServiceError 里的 message 已经是能直接给用户看的话
        raise HTTPException(status_code=error.status_code, detail=error.message) from error

    return ChatResponse(answer=answer)


@router.post("/ai/summarize", response_model=SummarizeResponse, summary="AI 笔记总结")
async def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    try:
        summary, key_points = await summarize_notes(payload.content)
    except AiServiceError as error:
        # 和 /ai/chat 用同一套错误处理，前端拿到的提示文案也一致
        raise HTTPException(status_code=error.status_code, detail=error.message) from error

    return SummarizeResponse(summary=summary, key_points=key_points)
