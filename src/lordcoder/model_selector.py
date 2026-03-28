"""
Model selection and effective config rendering for LordCoder.

This module provides a small interactive CLI used by the Windows launchers to
pick an Aider-compatible model, persist that choice, and generate a runtime
configuration file with the selected model injected.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional


DEFAULT_MODEL = "ollama/qwen2.5-coder:14b"
MODEL_PRESETS = [
    "ollama/qwen2.5-coder:7b",
    "ollama/qwen2.5-coder:14b",
    "ollama/qwen2.5-coder:32b",
]


@dataclass(frozen=True)
class ModelSelection:
    """A selected model plus derived provider information."""

    model: str

    @property
    def provider(self) -> str:
        """Return the provider prefix for the model string."""
        return self.model.split("/", 1)[0] if "/" in self.model else "unknown"

    @property
    def is_ollama(self) -> bool:
        """Return whether the selected model is an Ollama model."""
        return self.provider == "ollama"

    @property
    def ollama_model(self) -> Optional[str]:
        """Return the raw Ollama model name when applicable."""
        if not self.is_ollama or "/" not in self.model:
            return None
        return self.model.split("/", 1)[1]


def read_saved_model(state_path: Path) -> Optional[str]:
    """Read a persisted model choice if it exists."""
    if not state_path.exists():
        return None

    saved = state_path.read_text(encoding="utf-8").strip()
    return saved or None


def write_saved_model(state_path: Path, model: str) -> None:
    """Persist the selected model string."""
    state_path.write_text(f"{model}\n", encoding="utf-8")


def detect_provider(model: str) -> str:
    """Return the provider prefix for a model string."""
    return ModelSelection(model).provider


def get_ollama_model_name(model: str) -> Optional[str]:
    """Return the raw Ollama model name from an Aider model string."""
    return ModelSelection(model).ollama_model


def render_effective_config(base_config: str, model: str) -> str:
    """
    Render an effective config with the selected model injected.

    The implementation only replaces or injects the top-level `model:` entry and
    preserves the rest of the config verbatim.
    """

    lines = base_config.splitlines(keepends=True)

    for index, line in enumerate(lines):
        if line.startswith("model:"):
            newline = "\r\n" if line.endswith("\r\n") else "\n"
            lines[index] = f"model: {model}{newline}"
            return "".join(lines)

    prefix = f"model: {model}\n"
    if lines and lines[0].endswith("\r\n"):
        prefix = prefix.replace("\n", "\r\n")
    return prefix + "".join(lines)


def write_effective_config(base_config_path: Path, effective_config_path: Path, model: str) -> str:
    """Create the runtime config file and return its contents."""
    base_config = base_config_path.read_text(encoding="utf-8")
    rendered = render_effective_config(base_config, model)
    effective_config_path.write_text(rendered, encoding="utf-8")
    return rendered


def _prompt_choice(
    prompt: str,
    valid_choices: Iterable[str],
    input_func: Callable[[str], str] = input,
) -> str:
    """Prompt until a valid choice is entered."""
    allowed = {choice.lower(): choice for choice in valid_choices}

    while True:
        response = input_func(prompt).strip().lower()
        if response in allowed:
            return allowed[response]
        print("Please enter one of:", ", ".join(valid_choices))


def choose_model(
    saved_model: Optional[str],
    input_func: Callable[[str], str] = input,
    print_func: Callable[..., None] = print,
) -> str:
    """Run the interactive model selection flow."""
    if saved_model:
        print_func(f"Current saved model: {saved_model}")
        keep = _prompt_choice(
            "Press Enter to keep it, or type C to change it: ",
            ["", "c"],
            input_func=input_func,
        )
        if keep == "":
            return saved_model

    print_func("Select a model for LordCoder:")
    for index, preset in enumerate(MODEL_PRESETS, start=1):
        print_func(f"  {index}. {preset}")
    print_func(f"  {len(MODEL_PRESETS) + 1}. Enter a custom model")

    valid_choices = [str(index) for index in range(1, len(MODEL_PRESETS) + 2)]
    choice = _prompt_choice("Choose a number: ", valid_choices, input_func=input_func)

    if choice == str(len(MODEL_PRESETS) + 1):
        while True:
            custom_model = input_func("Enter the full Aider model string: ").strip()
            if custom_model:
                return custom_model
            print_func("Model cannot be empty.")

    return MODEL_PRESETS[int(choice) - 1]


def prepare_runtime_files(
    project_root: Path,
    input_func: Callable[[str], str] = input,
    print_func: Callable[..., None] = print,
) -> ModelSelection:
    """Select a model, persist it, and render the effective config."""
    state_path = project_root / ".lordcoder-model"
    base_config_path = project_root / "lordcoder.yml"
    effective_config_path = project_root / "lordcoder.effective.yml"

    selected_model = choose_model(
        saved_model=read_saved_model(state_path),
        input_func=input_func,
        print_func=print_func,
    )
    write_saved_model(state_path, selected_model)
    write_effective_config(base_config_path, effective_config_path, selected_model)
    return ModelSelection(selected_model)


def _emit_batch_output(selection: ModelSelection, project_root: Path) -> None:
    """Print key/value output that batch scripts can parse."""
    effective_config_path = project_root / "lordcoder.effective.yml"
    print(f"MODEL={selection.model}")
    print(f"PROVIDER={selection.provider}")
    print(f"EFFECTIVE_CONFIG={effective_config_path}")
    if selection.ollama_model:
        print(f"OLLAMA_MODEL={selection.ollama_model}")


def main() -> int:
    """CLI entrypoint for the model selector helper."""
    project_root = Path.cwd()
    selection = prepare_runtime_files(project_root)
    _emit_batch_output(selection, project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
