import json
from llm_sdk import Small_LLM_Model
from parthing import Parseurjson
from use_terminal.color import chose_color
from typing import Literal


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
        self.all_func_name: list = [e.name for e in data.function_define.root]

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
        print(self.all_func_name)
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
            '- If say asterisks replace it with "*"'
            "- Use this exact format:",
            '  "name": "<function_name>"\n'
            + '  "arguments": { "<param_name>": <value>, ... }\n',
            "}",
            f"Question: {question}",
            'Answer: {"prompt": "' + question + '",',
        ]

        return "\n".join(lines)

    def autocomplete_func(self, texte: str) -> str | None:
        """Retourne la fonction complète si une seule correspond."""
        resultats = [f for f in self.all_func_name if f.startswith(texte)]

        if len(resultats) == 1:
            return resultats[0]

        return None

    def complete_function(
        self,
        function_text: str,
        input_ids: list[int],
        llm_input: list[int],
    ) -> tuple[str, Literal[False]] | tuple[str, Literal[True]]:
        """
        Complète automatiquement une fonction lorsqu'une seule
        possibilité existe.

        Retourne :
            function_text, completed
        """

        function_complete = self.autocomplete_func(function_text)

        if function_complete is None:
            return function_text, False

        remaining = function_complete[len(function_text) :]

        if not remaining:
            return function_text, True

        remaining += '", "arguments": '
        completion_tokens = self.model.encode(remaining)[0].tolist()

        input_ids.extend(completion_tokens)
        llm_input.extend(completion_tokens)

        print(chose_color(remaining, 4), end="", flush=True)

        return function_complete, True

    def use_prompt(self, promptquest: str) -> str:

        built_prompt = self.build_prompt(promptquest)
        print(chose_color("Hey, I just met you, and this is crazy", 11))

        prompt_json = json.dumps(promptquest)  # échappe correctement " et \
        llm_start = '{"prompt": \n' + prompt_json + '\n, "name": '
        input_ids = self.model.encode(built_prompt + llm_start)[0].tolist()
        print("Texte décodé (vérif) :", self.model.decode(input_ids))

        llm_input = self.model.encode(llm_start)[0].tolist()

        # first bracket dans built_prompt
        brace_depth = 1
        started = True

        # if in funcomplit
        function_text = ""
        in_function = True
        for step in range(self.max_token):
            logits = self.model.get_logits_from_input_ids(input_ids)

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

            # capte func
            if in_function:

                function_text += piece

                if not any(c in piece for c in ['"', "}", ","]):
                    function_text, completed = self.complete_function(
                        function_text,
                        input_ids,
                        llm_input,
                    )

                    if completed:
                        in_function = False

                else:
                    function_text = ""

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
