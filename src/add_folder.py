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

    def parth_folders(self) -> Any | None:
        parser = parth_llm_ouput(self.data_input)
        result = parser.put_in_dict()

        if result is None:
            return None

        func_name_list = [func.name for func in self.known_functions]

        if not all([func_call.name in func_name_list for func_call in result]):
            print(
                color("unknow function name", 40, 100, 150),
                [
                    call.function
                    for call in result
                    if call.function not in func_name_list
                ],
            )
            return None

        if not all(call.prompt for call in result):
            print(
                color(
                    "[ERREUR] no prompt return ",
                    200,
                    150,
                    50,
                )
            )
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
