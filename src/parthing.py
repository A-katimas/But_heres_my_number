import json
import sys
from typing import Any
from pydantic import BaseModel, RootModel, ValidationError
from use_terminal.color import color

# ---------------------------------------------------------------------------
# Modèles pour functions_definition.json
# ---------------------------------------------------------------------------


class ParamSpec(BaseModel):
    type: str


class define_function(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParamSpec]
    returns: ParamSpec


class all_functions(RootModel):
    root: list[define_function]


class define_prompt(BaseModel):
    prompt: str


class all_prompts(RootModel):
    root: list[define_prompt]


class Parseurjson:
    def __init__(
        self,
        function_call: str = "data/input/function_calling_tests.json",
        function_define: str = "data/input/functions_definition.json",
    ):
        self.function_call = self.validate_or_stop(
            all_prompts, self.readjson(function_call), source=function_call
        )
        self.function_define = self.validate_or_stop(
            all_functions,
            self.readjson(function_define),
            source=function_define,
        )

    def readjson(self, folders: str) -> Any:
        try:
            with open(folders, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERREUR] Impossible de lire le fichier : {folders}")
            print(e)
            sys.exit(1)

    def validate_or_stop(
        self, model: type[RootModel], data: list[Any], source: str
    ) -> RootModel:
        """Valide tout le fichier d'un coup. Si une seule entrée est invalide,
        affiche un message clair et arrête le programme."""
        try:
            return model.model_validate(data)
        except ValidationError as e:
            print(
                color(
                    f"[ERREUR] Validation échouée pour le fichier : {source}",
                    255,
                    100,
                    100,
                )
            )
            print(e)
            sys.exit(1)

    def print_function_call(self) -> None:
        for i, prompt in enumerate(self.function_call.root):
            print(f"Prompt {i}: {prompt.prompt}")

    def print_function_define(self) -> None:
        for i, function in enumerate(self.function_define.root):
            print(
                f"Function {i}: {function.name} - {function.description} "
                f"parameters: {function.parameters} ",
                f"-> returns: {function.returns.type}",
            )

    def build_prompt(self, question: str) -> str:
        """
        functions: liste de dicts au format
            {
                "name": "fn_add_numbers",
                "description": "Add two numbers together and return their sum.",
                "parameters": {"a": "number", "b": "number"}
            }
        question: le prompt utilisateur (ex: "What is 265 + 345?")
        """

        lines = [
            "You are a function-calling assistant.",
            "Your job is to select the single most appropriate function "
            "for the user's question and extract its arguments.",
            "",
            "Available functions:",
            "",
        ]

        for fn in self.function_define.root:
            lines.append(f"- {fn.name}")
            lines.append(f"  description: {fn.description}")
            params = fn.parameters
            if params:
                lines.append(f"  parameters: {params}")
            else:
                lines.append("  parameters: none")
            lines.append("")

        lines += [
            "Rules:",
            "- Choose exactly ONE function from the list above.",
            "- Respond with ONLY a valid JSON object, nothing else.",
            "- Do not add explanations, comments, or extra text.",
            "- Use this exact format:",
            "{",
            '  "function": "<function_name>",',
            '  "arguments": { "<param_name>": <value>, ... }',
            "}",
            "",
            f"Question: {question}",
            "Answer:",
        ]

        return "\n".join(lines)
