from typing import Any
import json
import time

from application.models import ModelFactory
from application.prompt_management import PromptRepository
from application.domain.llm_request import LLMRequest
from application.domain.llm_response import LLMResponse
from application.services.tool_registry import ToolRegistry


class LLMOrchestrator:
    """
    Core orchestration layer:
    - selects model
    - builds prompt
    - calls LLM
    - optionally executes tools
    """

    def __init__(self, model_factory: ModelFactory, prompt_repo: PromptRepository):
        self.model_factory = model_factory
        self.prompt_repo = prompt_repo
        self.tools = ToolRegistry()

    async def process_request(
        self,
        request_type: str,
        input_text: str,
        **kwargs
    ) -> LLMResponse:

        model = self._get_model(request_type)
        prompt = self._format_prompt(request_type, input_text, **kwargs)

        llm_request = LLMRequest(
            prompt=prompt,
            model=model.model_name,
            max_tokens=kwargs.get("max_tokens", 100),
            temperature=kwargs.get("temperature", 0.7),
            top_p=kwargs.get("top_p", 1.0),
        )

        generated_text = await model.generate(
            prompt=llm_request.prompt,
            max_tokens=llm_request.max_tokens,
            temperature=llm_request.temperature,
        )

        # -----------------------------
        # TOOL EXECUTION LAYER
        # -----------------------------
        try:
            data = json.loads(generated_text)

            if isinstance(data, dict) and "tool" in data:
                tool_name = data["tool"]
                params = data.get("params", {})

                result = self.tools.execute(tool_name, params)

                return LLMResponse(
                    id=f"tool-{int(time.time())}",
                    object="tool_execution",
                    created=int(time.time()),
                    model=model.model_name,
                    choices=[{
                        "text": f"Tool executed: {tool_name} → {result}",
                        "index": 0,
                        "logprobs": None,
                        "finish_reason": "tool"
                    }],
                    usage={}
                )

        except Exception:
            # If parsing fails, fall back to normal text response
            pass

        return LLMResponse(
            id=f"response-{int(time.time())}",
            object="text_completion",
            created=int(time.time()),
            model=model.model_name,
            choices=[{
                "text": generated_text,
                "index": 0,
                "logprobs": None,
                "finish_reason": "length"
            }],
            usage={
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": len(generated_text.split()),
                "total_tokens": len(prompt.split()) + len(generated_text.split())
            }
        )

    def _get_model(self, request_type: str) -> Any:
        if request_type in ["translate", "summarize"]:
            return self.model_factory.get_model("gpt-3.5-turbo")

        if request_type in ["code_generation", "complex_reasoning"]:
            return self.model_factory.get_model("gpt-4")

        return self.model_factory.get_model("gpt-3.5-turbo")

    def _format_prompt(
        self,
        request_type: str,
        input_text: str,
        **kwargs
    ) -> str:

        prompt_template = self.prompt_repo.get_prompt(request_type)

        if not prompt_template:
            raise ValueError(f"No prompt template found for: {request_type}")

        return prompt_template.format(
            input_text=input_text,
            **kwargs
        )