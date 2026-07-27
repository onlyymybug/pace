from typing import Any
from pathlib import Path

from .constants import NA

_RUNTIME_TOKENIZER: Any = None


def _format_prompt_for_runtime(
    prompt: str,
    decoder_model: str,
    system_prompt: str,
) -> str:
    if decoder_model not in {
        "qwen2_5-0_5b",
        "qwen2_5-1_5b_instruct",
        "qwen2_5-3b_instruct",
    }:
        return prompt

    formatted_prompt = ""
    if system_prompt:
        formatted_prompt += f"<|im_start|>system\n{system_prompt}<|im_end|>\n"
    return (
        formatted_prompt
        + f"<|im_start|>user\n{prompt}<|im_end|>\n"
        + "<|im_start|>assistant\n"
    )

def _get_runtime_tokenizer(tokenizer_path: Path, tokenizer_config_path: Path | None = None) -> Any:
    global _RUNTIME_TOKENIZER
    if _RUNTIME_TOKENIZER is not None:
        return _RUNTIME_TOKENIZER

    if not tokenizer_path.exists():
        raise FileNotFoundError(f"Tokenizer file not found: {tokenizer_path}")

    try:
        from pytorch_tokenizers import get_tokenizer
    except ImportError as exc:
        raise RuntimeError(
            "Cannot import pytorch_tokenizers. Run with the same Python environment "
            "used for ExecuTorch llama inference, for example `.venv/bin/python "
            "two_week_task/run_w1_streaming.py`, or set dynamic_max_seq_len=false."
        ) from exc

    if tokenizer_config_path is not None and tokenizer_config_path.exists():
        _RUNTIME_TOKENIZER = get_tokenizer(str(tokenizer_path), str(tokenizer_config_path))
    else:
        _RUNTIME_TOKENIZER = get_tokenizer(str(tokenizer_path))
    return _RUNTIME_TOKENIZER

def count_prompt_tokens(
    prompt: str,
    tokenizer_path: Path,
    tokenizer_config_path: Path | None,
    decoder_model: str,
    system_prompt: str = "",
) -> int:
    tokenizer = _get_runtime_tokenizer(tokenizer_path, tokenizer_config_path)
    formatted_prompt = _format_prompt_for_runtime(
        prompt,
        decoder_model,
        system_prompt,
    )
    return len(tokenizer.encode(formatted_prompt, bos=True, eos=False))

def resolve_run_max_seq_len(
    *,
    runner_cfg: dict[str, Any],
    paths: Any,
    prompt: str,
    budget: int,
    dynamic_max_seq_len: bool,
    max_seq_len_cap: int,
) -> tuple[int, Any]:
    if not dynamic_max_seq_len:
        return int(runner_cfg["max_seq_len"]), NA
    
    prompt_tokens = count_prompt_tokens(
        prompt=prompt,
        tokenizer_path=paths.tokenizer_path,
        tokenizer_config_path=paths.tokenizer_config_path,
        decoder_model=str(runner_cfg["decoder_model"]),
        system_prompt=str(runner_cfg.get("system_prompt", "")),
    )
    max_seq_len = prompt_tokens + budget
    if max_seq_len > max_seq_len_cap:
        raise ValueError(
            f"prompt_tokens + budget = {max_seq_len}, larger than max_seq_len_cap={max_seq_len_cap}. "
            "Use a smaller budget/sample or increase max_seq_len_cap if the PTE supports it."
        )
    return max_seq_len, prompt_tokens
