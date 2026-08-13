from llm_sdk import Small_LLM_Model
from parthing import Parseurjson
from add_folder import Add_Folders


def simple_prompt(
    model: Small_LLM_Model, prompt: str, max_new_tokens: int
) -> str:

    print("Hey, I just met you, and this is crazy")

    input_ids = model.encode(prompt)[0].tolist()
    print("Token IDs de départ :", input_ids)
    print("Texte décodé (vérif) :", model.decode(input_ids))

    llm_input = model.encode("")[0].tolist()

    brace_depth = 0
    started = False  # on n'a pas encore vu la première "{"

    for step in range(max_new_tokens):
        logits = model.get_logits_from_input_ids(input_ids)

        next_token_id = max(range(len(logits)), key=lambda i: logits[i])

        input_ids.append(next_token_id)
        llm_input.append(next_token_id)

        # on décode juste le nouveau token pour suivre l'évolution des accolades
        piece = model.decode([next_token_id])

        for ch in piece:
            if ch == "{":
                brace_depth += 1
                started = True
            elif ch == "}":
                brace_depth -= 1

        print(f"\ntexte partiel nb {step} = {model.decode(llm_input)!r}")

        # dès que le JSON est complet (on a ouvert puis refermé toutes les accolades)
        if started and brace_depth <= 0:
            print(f"[STOP] JSON complet détecté après {step + 1} tokens")
            break

    print("\n--- Résultat final ---")
    print(model.decode(input_ids))
    return model.decode(llm_input)


def main() -> None:
    model = Small_LLM_Model()
    pars = Parseurjson()
    pars.print_function_call()
    pars.print_function_define()

    result = simple_prompt(
        # model,
        # pars.build_prompt(pars.function_call.root[4].prompt),
        # 50,
        model,
        pars.build_prompt("4の2乗であること"),
        50,
    )
    final = Add_Folders(
        "data/output/finalfunc.json",
        result,
        known_functions=pars.function_define.root,
    )
    final.generate()


if __name__ == "__main__":
    main()
