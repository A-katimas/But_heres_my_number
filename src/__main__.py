from parthing import Parseurjson
from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]
from add_folder import Add_Folders
from llm_used import LlmUsed
from argparse import Namespace, ArgumentParser


def inputpath() -> Namespace:
    """creates an argument parther"""
    parth = ArgumentParser(exit_on_error=False)
    parth.add_argument(
        "--functions_definition",
        help="file with function",
        default="data/input/functions_definition.json",
        required=False,
    )
    parth.add_argument(
        "--input",
        help="the input",
        default="data/input/function_calling_tests.json",
        required=False,
    )
    parth.add_argument(
        "--output",
        help="file for output",
        default="data/output/function_calling_results.json",
        required=False,
    )
    return parth.parse_args()


def main() -> None:
    try:
        arg = inputpath()
        model = Small_LLM_Model()
        pars = Parseurjson(arg.input, arg.functions_definition)
        pars.print_function_call()
        pars.print_function_define()

        usedllm = LlmUsed(model, pars)
        result = usedllm.launch()

        final = Add_Folders(
            arg.output,
            result,
            known_functions=pars.function_define.root,
        )
        final.generate()

    except Exception as e:
        print(e, "occured in intialisation")


if __name__ == "__main__":
    main()
