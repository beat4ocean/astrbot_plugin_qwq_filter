import re
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import LLMResponse
from openai.types.chat.chat_completion import ChatCompletion

@register("qwq-filter", "beat4ocean", "可选择是否过滤推理模型的思考内容", "1.0.0", 'https://github.com/beat4ocean/astrbot_plugin_qwq_filter')
class R1Filter(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.display_reasoning_text = self.config.get('display_reasoning_text', False)

    @filter.on_llm_response()
    async def resp(self, event: AstrMessageEvent, response: LLMResponse):
        if not self.display_reasoning_text:
            completion_text = response.completion_text
            # 适配 qwq 模型
            if r'' in completion_text or r'</details>' in completion_text:
                completion_text = re.sub(r'<details style=".*?" open>.*?</details>', '', completion_text, flags=re.DOTALL).strip()
                # 可能有单标签情况
                completion_text = completion_text.replace(r'<details>', '').replace(r'</details>', '').strip()
            response.completion_text = completion_text