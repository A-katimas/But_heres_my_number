# But_heres_my_number
so call me maybe
*This project has been created as part of the 42 curriculum by jtardieu*

# Call-Me-Maybe

<table>
  <tr>
    <td>
      <img src="https://media1.tenor.com/m/Ih_cmy7Dv_IAAAAC/fail.gif"width="200">
    </td>
    <td align="center">
      <h2>But_heres_my_number</h2>
    </td>
	<td>
      <img src="https://media1.tenor.com/m/dWm2kuG5WXAAAAAd/neuvillette-genshin.gif" width="200">
    </td>
  </tr>
</table>

## Description

call me maybe is a project using LLM the principle is to know how to make a prompt and be able to use the information it generates to implement it in a json


## 🚀 Quick Start

```bash
make run
```

## ⚙️ How to Run

| Command | What it does |
|---------|-------------|
| `make run` | run the projet |
| `make install` | install venv without runing |
| `make clean` | 🧹 Remove tempory files |
| `make fclean` | 🗑️ Remove everything (including .venv) |
| `make lint` | 🔄 look the norme in normal used |
| `make strict-lint` | 🔄 look the norme in strict mod |

## 📋 Parameters Explained

this program must have two json files included in the data/input folder with both file name specify in the subject
| Folders_Name |how to implement | what it does|
|--------------|-----------------|-------------|
| function_calling_tests.json | [ {"prompt" : "\<insert your prompt>"} ] | it will put your prompt as it goes into the machine|
| functions_definition.json | [ {"name" : "\<enter name>", "description" : "\<insert descrition>", "parameters" : {\<put all your parameter with like a json>},"return" :  { \<put you'r returns>} } ] | has the machine to know what to return |


