from llm_sdk import Small_LLM_Model
from parthing import Parseurjson
from add_folder import Add_Folders
import json


def simple_prompt(
    model: Small_LLM_Model, prompt: str, max_new_tokens: int, promptquest: str
) -> str:

    print("Hey, I just met you, and this is crazy")
    # llm_start = '{"prompt": \n"' + promptquest + '"\n, "function": '
    prompt_json = json.dumps(promptquest)  # échappe correctement " et \
    llm_start = '{"prompt": \n' + prompt_json + '\n, "function": '
    input_ids = model.encode(prompt + llm_start)[0].tolist()

    print("Token IDs de départ :", input_ids)
    print("Texte décodé (vérif) :", model.decode(input_ids))

    llm_input = model.encode(llm_start)[0].tolist()

    brace_depth = 1
    started = True  # on n'a pas encore vu la première "{"

    for step in range(max_new_tokens):
        logits = model.get_logits_from_input_ids(input_ids)
        # print(llm_input, model)
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

        print(piece, end="", flush=True)

        # dès que le JSON est complet (on a ouvert puis refermé toutes les accolades)
        if started and brace_depth <= 0:
            print(f"[STOP] JSON complet détecté après {step + 1} tokens")
            break

    print("\n--- Résultat final ---")
    print(model.decode(input_ids))
    text = model.decode(llm_input)
    return text[: text.rfind("}") + 1]


def posible_token(logits: list[float], model: Small_LLM_Model):
    for i in logits:
        print(model.encode(i))


def all_try(
    model: Small_LLM_Model,
    pars: Parseurjson,
    prompt: list[str] | str,
) -> str:
    if isinstance(prompt, str):
        result = simple_prompt(model, pars.build_prompt(prompt), 50, prompt)

    else:
        # for i in prompt:
        #    result.append(
        #        simple_prompt(
        #            model,
        #            pars.build_prompt(i.prompt),
        #            50,
        #            i.prompt,
        #        )
        #    )
        result = ",\n".join(
            simple_prompt(
                model,
                pars.build_prompt(llm_result.prompt),
                50,
                llm_result.prompt,
            )
            for llm_result in prompt
        )
        result = "[" + result + "]"
    return result


def main() -> None:
    model = Small_LLM_Model()
    pars = Parseurjson()
    pars.print_function_call()
    pars.print_function_define()

    all_prompt = pars.function_call.root
    prompt = "combien font 5+4"
    result = all_try(model, pars, prompt)

    final = Add_Folders(
        "data/output/finalfunc.json",
        result,
        known_functions=pars.function_define.root,
    )
    final.generate()


if __name__ == "__main__":
    main()
