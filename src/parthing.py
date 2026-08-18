import json
import sys
from typing import Any, Literal
from pydantic import BaseModel, RootModel, ValidationError
from src.use_terminal.color import color

# ---------------------------------------------------------------------------
# Modèles pour functions_definition.json
# ---------------------------------------------------------------------------


class ParamSpec(BaseModel):
    type: Literal["integer", "string", "number", "bool"]


class LLMFunctionCall(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]


class define_function(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParamSpec]
    returns: ParamSpec


class all_functions(RootModel[list[define_function]]):
    root: list[define_function]


class define_prompt(BaseModel):
    prompt: str


class all_prompts(RootModel[list[define_prompt]]):
    root: list[define_prompt]


class Parseurjson:
    def __init__(
        self,
        function_call: str = "data/input/function_calling_tests.json",
        function_define: str = "data/input/functions_definition.json",
    ):
        self.function_call: all_prompts = self.validate_or_stop(
            all_prompts, self.readjson(function_call), source=function_call
        )
        self.function_define: all_functions = self.validate_or_stop(
            all_functions,
            self.readjson(function_define),
            source=function_define,
        )

    def readjson(self, folders: str) -> Any:
        """allows you to read a json"""
        try:
            with open(folders, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERREUR] Impossible de lire le fichier : {folders}")
            print(e)
            sys.exit(1)

    def validate_or_stop(
        self, model: type[RootModel[Any]], data: list[Any], source: str
    ) -> Any:
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
        """print all call function in json"""
        for i, prompt in enumerate(self.function_call.root):
            print(f"Prompt {i}: {prompt.prompt}")

    def print_function_define(self) -> None:
        """print all define function in json"""
        for i, function in enumerate(self.function_define.root):
            print(
                f"Function {i}: {function.name} - {function.description} "
                f"parameters: {function.parameters} ",
                f"-> returns: {function.returns.type}",
            )


class parth_llm_ouput:
    def __init__(self, llm_raw_output: str):
        self.llm_raw_output = llm_raw_output

    def extract_json(self) -> str:
        """Extrait la sous-chaîne { ... } dans le texte brut, au cas où
        le modèle aurait généré du texte parasite avant/après (fréquent
        tant qu'il n'y a pas de constrained decoding)."""
        if self.llm_raw_output == "[]":
            return "[]"
        start = self.llm_raw_output.find("{")
        end = self.llm_raw_output.rfind("}")
        if start == -1 or end == -1 or end < start:
            raise ValueError("Aucun objet JSON trouvé dans la sortie du LLM.")
        return "[\n" + self.llm_raw_output[start:end + 1] + "\n]"

    def put_in_dict(self) -> list[LLMFunctionCall] | None:
        """put all data in the input json to a dict to use them easly"""
        try:
            raw_json = self.extract_json()
        except ValueError as e:
            print(color(f"[ERREUR] {e}", 230, 70, 70))
            return None

        try:
            print(raw_json)
            data = json.loads(raw_json)
        except json.JSONDecodeError as e:
            print(
                color(
                    f"[ERREUR] JSON invalide généré par le LLM : {e}",
                    200,
                    100,
                    70,
                )
            )
            print(f"Contenu brut : {raw_json!r}")
            return None

        try:
            print(data)
            validated = [
                LLMFunctionCall.model_validate(function_call)
                for function_call in data
            ]
        except ValidationError as e:
            print(
                color(f"[ERREUR] Structure JSON invalide : {e}", 255, 150, 100)
            )
            return None

        return validated
