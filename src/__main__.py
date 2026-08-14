from llm_sdk import Small_LLM_Model
from parthing import Parseurjson
from add_folder import Add_Folders
from llm_used import LlmUsed


def main() -> None:
    model = Small_LLM_Model()
    pars = Parseurjson()

    pars.print_function_call()
    pars.print_function_define()

    usedllm = LlmUsed(model, pars)

    result = usedllm.launch()

    final = Add_Folders(
        "data/output/finalfunc.json",
        result,
        known_functions=pars.function_define.root,
    )
    final.generate()


if __name__ == "__main__":
    main()
