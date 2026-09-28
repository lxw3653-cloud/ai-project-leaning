"""与大模型服务通信的唯一出口。

所有 AI 请求都从这里发出：超时、上游错误、返回内容解析都在这一层处理完，
业务代码只需要关心「拿到回答」或者「拿到一句能展示给用户的话」。
"""

import logging

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class AiServiceError(Exception):
    """调用 AI 服务失败。

    message 是整理好的、可以直接展示给用户的说明；
    status_code 是这次请求要返回给前端的 HTTP 状态码。
    """

    def __init__(self, message: str, *, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


async def chat_completion(messages: list[dict[str, str]]) -> str:
    """调用一次聊天补全接口，返回模型回答的纯文本。

    使用 OpenAI 兼容协议，因此换服务商只需要改配置里的 base_url 和 model。
    """
    settings = get_settings()

    if not settings.ai_api_key.strip():
        raise AiServiceError(
            "还没有配置 AI 的 API Key，请在 backend/.env 中设置 AI_API_KEY 后重启后端",
            status_code=503,
        )

    url = f"{settings.ai_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.ai_model,
        "messages": messages,
        "stream": False,
    }
    headers = {"Authorization": f"Bearer {settings.ai_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=settings.ai_timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
    except httpx.TimeoutException as exc:
        raise AiServiceError(
            f"AI 服务响应超时（超过 {settings.ai_timeout:g} 秒），请稍后重试或把问题写短一些",
            status_code=504,
        ) from exc
    except httpx.HTTPError as exc:
        # 连不上、DNS 解析失败、连接被断开等
        logger.warning("调用 AI 服务失败：%s", exc)
        raise AiServiceError(
            "无法连接 AI 服务，请检查网络，以及 .env 里的 AI_BASE_URL 是否正确",
            status_code=502,
        ) from exc

    if response.status_code in (401, 403):
        raise AiServiceError(
            "AI 服务拒绝了这次请求：API Key 无效或没有权限，请检查 .env 里的 AI_API_KEY",
            status_code=502,
        )

    if response.status_code == 429:
        raise AiServiceError(
            "AI 服务提示请求过于频繁或额度不足，请稍后再试",
            status_code=502,
        )

    if response.status_code >= 400:
        # 上游的具体报错写进日志方便排查，但不直接透给前端
        logger.warning(
            "AI 服务返回错误：HTTP %s %s",
            response.status_code,
            response.text[:500],
        )
        raise AiServiceError(
            f"AI 服务返回错误（HTTP {response.status_code}），详细信息请看后端日志",
            status_code=502,
        )

    try:
        data = response.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        logger.warning("无法解析 AI 服务返回：%s", response.text[:500])
        raise AiServiceError("AI 服务返回的内容无法解析，请稍后重试", status_code=502) from exc

    answer = (content or "").strip()
    if not answer:
        raise AiServiceError("AI 服务返回了空内容，请重试", status_code=502)

    return answer
