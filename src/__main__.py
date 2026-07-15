from llm_sdk import Small_LLM_Model
import json

def simple_prompt(prompt: str, max_new_tokens: int) -> None:
    print("Hey, I just met you, and this is crazy")

    # 1. Charger le modèle (télécharge Qwen3-0.6B au premier lancement)
    model = Small_LLM_Model()

    # 2. Encoder un prompt en une liste de token IDs
    input_ids = model.encode(prompt)[
        0
    ].tolist()  # encode() renvoie un Tensor 2D -> on récupère la liste
    print("Token IDs de départ :", input_ids)
    print("Texte décodé (vérif) :", model.decode(input_ids))

    # 3. Boucle de génération token par token (greedy, sans aucune contrainte)
    for step in range(max_new_tokens):
        # a. On demande les logits pour LE PROCHAIN token, étant donné la séquence actuelle
        logits = model.get_logits_from_input_ids(input_ids)

        # b. On choisit le token avec le score le plus élevé (greedy decoding)
        #    C'est ICI qu'on interviendrait pour faire du constrained decoding :
        #    on mettrait -inf sur les logits des tokens "invalides" AVANT ce max().
        next_token_id = max(range(len(logits)), key=lambda i: logits[i])

        # c. On ajoute le nouveau token à la séquence
        input_ids.append(next_token_id)

        # d. On regarde ce que ça donne en texte à chaque étape (debug pédagogique)
        print(
            f"Step {step}: token_id={next_token_id} -> texte partiel = {model.decode(input_ids)!r}"
        )

    print("\n--- Résultat final ---")
    print(model.decode(input_ids))


def main() -> None:
    readjson("data/input/function_calling_tests.json")
    #simple_prompt("What is the sum of 2 and 5? Answer:", 22)

def readjson(folders : str) -> None:
    with open(folders, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(data)

if __name__ == "__main__":
    main()
