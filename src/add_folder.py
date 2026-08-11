import json
from parthing import parth_llm_ouput, define_function
from use_terminal.color import color


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

    def parth_folders(self) -> dict | None:
        parser = parth_llm_ouput(self.data_input)
        result = parser.put_in_dict()

        if result is None:
            print("la")
            return None

        matching_fn = next(
            (
                fn
                for fn in self.known_functions
                if fn.name == result["function"]
            ),
            None,
        )

        if matching_fn is None:
            print(f"[ERREUR] Fonction inconnue : '{result['function']}'")
            return None

        if not result["prompt"][0]:
            print(
                color(
                    f"[ERREUR] no prompt return ",
                    200,
                    150,
                    50,
                )
            )
            return None

        # if result["returns"]["type"] != matching_fn.returns.type:
        #     print(
        #         color(
        #             f"[ERREUR] Type de retour incohérent : le LLM a dit ",
        #             200,
        #             150,
        #             50,
        #         ),
        #         f"'{result['returns']['type']}', attendu "
        #         f"'{matching_fn.returns.type}' pour {result['function']}",
        #     )
        #     return None

        return result

    def generate(self) -> None:
        parsed = self.parth_folders()

        if parsed is None:
            print(f"[ABANDON] Écriture annulée, sortie du LLM invalide.")
            return

        with open(self.name_output, "w+", encoding="utf-8") as file:
            json.dump(parsed, file, indent=2, ensure_ascii=False)

        print(color(f"[OK] llm has good job {self.name_output}", 100, 230, 70))
