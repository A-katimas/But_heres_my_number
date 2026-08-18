import json
from parthing import parth_llm_ouput, define_function, LLMFunctionCall
from src.use_terminal.color import color
from typing import Any


class MyEncoder(json.JSONEncoder):
    def default(self, o: object) -> Any:
        if isinstance(o, LLMFunctionCall):
            return o.model_dump()
        return super().default(o)


class Add_Folders:
    def __init__(
        self,
        name_output: str,
        data_input: str,
        known_functions: list[define_function] | None = None,
    ):
        self.name_output = name_output
        self.data_input = data_input
        self.known_functions = known_functions or []

    def convert_parameters(
        self,
        call: LLMFunctionCall,
        function: define_function,
    ) -> bool:
        """Convertit les paramètres selon la définition de la fonction."""

        for param_name, param_value in call.parameters.items():
            param_spec = function.parameters.get(param_name)

            if param_spec is None:
                print(
                    color(
                        f"[ERREUR] Paramètre inconnu : {param_name}",
                        200,
                        80,
                        80,
                    )
                )
                return False

            try:
                if param_spec.type == "integer":
                    call.parameters[param_name] = int(param_value)

                elif param_spec.type == "number":
                    call.parameters[param_name] = float(param_value)

                elif param_spec.type == "string":
                    call.parameters[param_name] = str(param_value)

                else:
                    print(
                        color(
                            f"[ERREUR] Type inconnu : {param_spec.type}",
                            200,
                            80,
                            80,
                        )
                    )
                    return False

            except (ValueError, TypeError):
                print(
                    color(
                        f"[ERREUR] Impossible de convertir "
                        f"{param_name}={param_value!r} "
                        f"en {param_spec.type}",
                        200,
                        80,
                        80,
                    )
                )
                return False

        return True

    def parth_folders(self) -> list[LLMFunctionCall] | None:
        parser = parth_llm_ouput(self.data_input)
        result: list[LLMFunctionCall] | None = parser.put_in_dict()

        if result is None:
            return None

        for call in result:
            function = next(
                (
                    func
                    for func in self.known_functions
                    if func.name == call.name
                ),
                None,
            )

            if function is None:
                print(
                    color(
                        f"[ERREUR] Fonction inconnue : {call.name}",
                        40,
                        100,
                        150,
                    )
                )
                return None

            if not call.prompt:
                print(
                    color(
                        "[ERREUR] no prompt return",
                        200,
                        150,
                        50,
                    )
                )
                return None

            if not self.convert_parameters(call, function):
                return None

        return result

    def generate(self) -> None:
        parsed = self.parth_folders()

        if parsed is None:
            print(
                color(
                    "[ABANDON] Écriture annulée, sortie du LLM invalide.",
                    170,
                    130,
                    60,
                )
            )
            return

        print(f"\n\n{parsed}\n\n", flush=True)
        with open(self.name_output, "w+", encoding="utf-8") as file:
            json.dump(
                parsed, file, indent=2, ensure_ascii=False, cls=MyEncoder
            )

        print(color(f"[OK] llm has good job {self.name_output}", 100, 230, 70))
