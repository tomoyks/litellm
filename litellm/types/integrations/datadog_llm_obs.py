"""
Payloads for Datadog LLM Observability Service (LLMObs)

API Reference: https://docs.datadoghq.com/llm_observability/setup/api/?tab=example#api-standards
"""
from typing import Any, Dict, List, Literal, Optional, Union

from typing_extensions import TypedDict

from litellm.types.integrations.custom_logger import StandardCustomLoggerInitParams


class DDPrompt(TypedDict, total=False):
    """
    Datadog LLM Observability Prompt object.

    A Prompt object contains the information needed to render a prompt template.
    This enables prompt tracking and versioning in Datadog LLM Observability.

    Reference: https://docs.datadoghq.com/llm_observability/setup/api/

    Attributes:
        id: The unique identifier of the prompt. Should be unique per ml_app.
        version: User-defined version tag for the prompt.
        template: A string template for the prompt (defaults to "user" role).
        chat_template: A list of message dicts with role and content/template.
        variables: A dictionary of variables used to render the prompt template.
        tags: Optional tags to associate with the prompt run.
        rag_context_variables: Variable key names containing ground truth context info.
        rag_query_variables: Variable key names containing query information for LLM calls.
    """

    id: str
    version: str
    template: str
    chat_template: Union[List[Dict[str, str]], List[Dict[str, Any]]]
    variables: Dict[str, str]
    tags: Dict[str, str]
    rag_context_variables: List[str]
    rag_query_variables: List[str]


class InputMeta(TypedDict, total=False):
    messages: List[
        Dict[str, Any]  # changed to fit with tool calls
    ]  # Relevant Issue: https://github.com/BerriAI/litellm/issues/9494
    value: str
    prompt: DDPrompt  # Prompt template information for prompt tracking


class OutputMeta(TypedDict):
    messages: List[Any]


class DDLLMObsError(TypedDict, total=False):
    """Error information on the span according to DD LLM Obs API spec"""

    message: str  # The error message
    stack: Optional[str]  # The stack trace
    type: Optional[str]  # The error type


class Meta(TypedDict, total=False):
    # The span kind: "agent", "workflow", "llm", "tool", "task", "embedding", or "retrieval".
    kind: Literal["llm", "tool", "task", "embedding", "retrieval"]
    input: InputMeta  # The span's input information.
    output: OutputMeta  # The span's output information.
    metadata: Dict[str, Any]
    error: Optional[DDLLMObsError]  # Error information on the span


class LLMMetrics(TypedDict, total=False):
    input_tokens: float
    output_tokens: float
    total_tokens: float
    time_to_first_token: float
    time_per_output_token: float
    total_cost: float


class LLMObsPayload(TypedDict, total=False):
    parent_id: str
    trace_id: str
    apm_id: str
    span_id: str
    name: str
    meta: Meta
    start_ns: int
    duration: int
    metrics: LLMMetrics
    tags: List
    status: Literal["ok", "error"]  # Error status ("ok" or "error"). Defaults to "ok".


class DDSpanAttributes(TypedDict):
    ml_app: str
    tags: List[str]
    spans: List[LLMObsPayload]


class DDIntakePayload(TypedDict):
    type: str
    attributes: DDSpanAttributes


class DatadogLLMObsInitParams(StandardCustomLoggerInitParams):
    """
    Params for initializing a DatadogLLMObs logger on litellm
    """

    pass


class DDLLMObsLatencyMetrics(TypedDict, total=False):
    time_to_first_token_ms: float
    litellm_overhead_time_ms: float
    guardrail_overhead_time_ms: float


class DDLLMObsSpendMetrics(TypedDict, total=False):
    response_cost: float
    user_api_key_spend: float
    user_api_key_max_budget: float
    user_api_key_budget_reset_at: str
