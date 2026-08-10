from typing import Any


class parth_llm_ouput:
    def __init__(self, llm_folders_input: str):
        self.llm_input = llm_folders_input
        pass

    def put_in_dict(self) -> Any:
        pass


class Add_Folders:
    def __init__(
        self,
        name_output: str,
        data_input: str,
    ):
        self.name_output = name_output
        self.data_input = data_input

    def parth_folders(self) -> None:
        from parthing import parth_llm_ouput

        parth_llm_ouput(self.name_output)

        pass

    def generate(self) -> None:
        with open(self.name_output, "w+", encoding="utf-8") as file:
            file.write(self.data_input)
        pass
