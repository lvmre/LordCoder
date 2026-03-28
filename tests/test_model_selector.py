"""Tests for LordCoder model selection helpers."""

import io
import shutil
import unittest
from pathlib import Path
from uuid import uuid4

from lordcoder.model_selector import (
    ModelSelection,
    choose_model,
    detect_provider,
    get_ollama_model_name,
    prepare_runtime_files,
    read_saved_model,
    render_effective_config,
)


def make_workspace_temp_dir() -> Path:
    """Create a temp directory inside the workspace to avoid system temp restrictions."""
    root = Path(".test-temp") / f"model-selector-{uuid4().hex}"
    root.mkdir(parents=True, exist_ok=False)
    return root


class TestConfigRendering(unittest.TestCase):
    """Tests for effective config generation."""

    def test_render_effective_config_replaces_existing_model(self) -> None:
        base = "model: ollama/old\nsystem-prompt: |\n  hello\n"
        rendered = render_effective_config(base, "anthropic/claude-3-7-sonnet")
        self.assertEqual(
            rendered,
            "model: anthropic/claude-3-7-sonnet\nsystem-prompt: |\n  hello\n",
        )

    def test_render_effective_config_injects_missing_model(self) -> None:
        base = "system-prompt: |\n  hello\n"
        rendered = render_effective_config(base, "openai/gpt-5")
        self.assertEqual(rendered, "model: openai/gpt-5\nsystem-prompt: |\n  hello\n")

    def test_render_effective_config_preserves_remaining_content(self) -> None:
        base = (
            "model: ollama/old\r\n"
            "\r\n"
            "system-prompt: |\r\n"
            "  line one\r\n"
            "  line two\r\n"
            "auto-commits: true\r\n"
        )
        rendered = render_effective_config(base, "ollama/qwen2.5-coder:7b")
        self.assertEqual(
            rendered,
            (
                "model: ollama/qwen2.5-coder:7b\r\n"
                "\r\n"
                "system-prompt: |\r\n"
                "  line one\r\n"
                "  line two\r\n"
                "auto-commits: true\r\n"
            ),
        )


class TestProviderHelpers(unittest.TestCase):
    """Tests for provider detection helpers."""

    def test_detect_provider(self) -> None:
        self.assertEqual(detect_provider("ollama/qwen2.5-coder:14b"), "ollama")
        self.assertEqual(detect_provider("openai/gpt-5"), "openai")

    def test_get_ollama_model_name(self) -> None:
        self.assertEqual(get_ollama_model_name("ollama/qwen2.5-coder:32b"), "qwen2.5-coder:32b")
        self.assertIsNone(get_ollama_model_name("openai/gpt-5"))

    def test_model_selection_properties(self) -> None:
        selection = ModelSelection("ollama/qwen2.5-coder:14b")
        self.assertTrue(selection.is_ollama)
        self.assertEqual(selection.ollama_model, "qwen2.5-coder:14b")
        self.assertEqual(selection.provider, "ollama")


class TestSelectionFlow(unittest.TestCase):
    """Tests for interactive selection and persistence."""

    def test_choose_model_keeps_saved_model(self) -> None:
        self.assertEqual(
            choose_model("openai/gpt-5", input_func=lambda _: ""),
            "openai/gpt-5",
        )

    def test_choose_model_allows_custom_entry(self) -> None:
        answers = iter(["c", "4", "anthropic/claude-3-7-sonnet"])
        chosen = choose_model("openai/gpt-5", input_func=lambda _: next(answers))
        self.assertEqual(chosen, "anthropic/claude-3-7-sonnet")

    def test_prepare_runtime_files_persists_state_and_writes_effective_config(self) -> None:
        root = make_workspace_temp_dir()
        try:
            (root / "lordcoder.yml").write_text(
                "model: ollama/original\nsystem-prompt: |\n  test\n",
                encoding="utf-8",
            )

            output = io.StringIO()
            selection = prepare_runtime_files(
                root,
                input_func=lambda _: "2",
                print_func=lambda *args, **kwargs: print(*args, **kwargs, file=output),
            )

            self.assertEqual(selection.model, "ollama/qwen2.5-coder:14b")
            self.assertEqual(
                read_saved_model(root / ".lordcoder-model"),
                "ollama/qwen2.5-coder:14b",
            )
            self.assertEqual(
                (root / "lordcoder.effective.yml").read_text(encoding="utf-8"),
                "model: ollama/qwen2.5-coder:14b\nsystem-prompt: |\n  test\n",
            )
        finally:
            shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
