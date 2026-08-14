import json
from llm_sdk import Small_LLM_Model
from parthing import Parseurjson


class LlmUsed:
    def __init__(
        self,
        model: Small_LLM_Model,
        data: Parseurjson,
        prompt: str = "",
        maxtoken: int = 50,
    ):
        self.model = model
        self.data = data
        self.prompt = prompt
        self.max_token = maxtoken

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

        for fn in self.data.function_define.root:

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
            '- Valid type values are EXACTLY: "integer", "string" or "number". '
            'Never use "str", "int", "float" , or any other type name.',
            "- Use this exact format:",
            '  "function": "<function_name>"\n'
            + '  "arguments": { "<param_name>": <value>, ... }\n',
            "}",
            f"Question: {question}",
            'Answer: {"prompt": "' + question + '",',
        ]

        return "\n".join(lines)

    def use_prompt(self, promptquest: str) -> str:

        built_prompt = self.build_prompt(promptquest)
        print("Hey, I just met you, and this is crazy")

        prompt_json = json.dumps(promptquest)  # échappe correctement " et \
        llm_start = '{"prompt": \n' + prompt_json + '\n, "function": '
        input_ids = self.model.encode(built_prompt + llm_start)[0].tolist()

        print("Token IDs de départ :", input_ids)
        print("Texte décodé (vérif) :", self.model.decode(input_ids))

        llm_input = self.model.encode(llm_start)[0].tolist()

        # first bracket dans built_prompt
        brace_depth = 1
        started = True

        for step in range(self.max_token):
            logits = self.model.get_logits_from_input_ids(input_ids)
            # print(llm_input, model

            # on prend la meilleur posibiliter
            next_token_id = max(range(len(logits)), key=lambda i: logits[i])

            input_ids.append(next_token_id)
            llm_input.append(next_token_id)

            piece = self.model.decode([next_token_id])

            # capte si bracket
            for ch in piece:
                if ch == "{":
                    brace_depth += 1
                    started = True
                elif ch == "}":
                    brace_depth -= 1

            print(piece, end="", flush=True)

            if started and brace_depth <= 0:
                print(f"[STOP] JSON complet détecté après {step + 1} tokens")
                break

        print("\n--- Résultat final ---")
        print(self.model.decode(input_ids))
        text = self.model.decode(llm_input)
        return text[: text.rfind("}") + 1]

    def launch(self) -> str:
        if self.prompt:
            result = self.use_prompt(self.prompt)

        else:
            self.prompt = self.data.function_call.root
            result = ",\n".join(
                self.use_prompt(llm_result.prompt)
                for llm_result in self.prompt
            )
            result = "[" + result + "]"
        return result
