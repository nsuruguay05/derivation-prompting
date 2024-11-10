import pandas as pd

from src.claude import get_response
from src.retrieval import retrieve, chunks
from prompts.whole_derivation import system_message, user_message

def create_messages(question, retrieval_model):
    """
    Create the user and assistant messages for the derivation process from the few-shot examples and the question.
    
    Parameters:
    - question: String, the question to derive the answer for
    - retrieval_model: String, the retrieval model to use (Dict or CrossEncoder)

    Returns:
    - messages: List of Dict, the user and assistant messages
    - references: List of Dict, the references used to derive the answer
    """
    messages = []
    # Load Few-Shot examples
    df = pd.read_csv("prompts/few_shot_examples.csv")
    examples = [row['derivación'] for _, row in df.iterrows()]

    # Create examples messages
    for i in range(len(df)):
        example_text = "Hipótesis:"
        for idx, reference in enumerate(df["extractos"].iloc[i].split()):
            example_text += f'\n\n{idx + 1}. {chunks[int(reference)]["chunk"]}'
        example_text += f'\n\nPregunta de usuario:\n\n{df["pregunta"].iloc[i]}'
        messages.append({"role": "user", "content": example_text})
        messages.append({"role": "assistant", "content": examples[i]})

    # Retrieve references for new message
    references = retrieve(question, retrieval_model)

    # Create hypothesis string
    hypothesis = ''
    for i in range(len(references)):
        hypothesis += f'{str(i+1)}. {references[i]["chunk"].strip()}\n\n'

    # Create messages list
    messages.append(
        {"role": "user", "content": user_message.format(hypothesis=hypothesis, message=question)}
    )

    return messages, references

def create_answer(question, model, retrieval_model, temperature=0):
    """
    Create the answer for a given question using the specified model and retrieval model.

    Parameters:
    - question: String, the question to derive the answer for
    - model: String, the Anthropic model to use (opus or haiku)
    - retrieval_model: Dict or CrossEncoder, the retrieval model to use
    - temperature: Float, the temperature to use for the generation process (default is 0)

    Returns:
    - answer: String, the answer to the question
    - references: List of Dict, the references used to derive the answer
    - tree: Dict, the derivation tree
    """
    messages, references = create_messages(question, retrieval_model)
    answer = get_response(system_message, messages, model, temp=temperature)

    # Parse the answer
    steps_text = [e for e in answer.split("\n\n") if not e.startswith("Nueva hipótesis:")]
    steps_text_fixed = []

    for i in range(len(steps_text)):
        # Skip broken steps
        if len(steps_text_fixed) > 0 and is_ending_final_answer(steps_text_fixed[-1]) and not is_starting_rule(steps_text[i]):
            continue
        # Concatenate steps if not starting a new rule
        if is_starting_rule(steps_text[i]):
            steps_text_fixed.append(steps_text[i])
        elif len(steps_text_fixed) > 0:
            steps_text_fixed[-1] += "\n\n" + steps_text[i]

    steps_text = steps_text_fixed
    steps = []

    for step_text in steps_text:
        parts = step_text.split("|")
        if len(parts) >= 3:
            steps.append({"rule": parts[0].strip(), "hipotesis": parts[1].strip(), "conclusion": parts[2].strip()})
        else:
            steps.append({"rule": None, "hipotesis": None, "conclusion": "|".join(parts).strip()})

    # If no steps could be parsed, return the answer as the final answer with a NoInfo rule
    if len(steps) == 0:
        return answer, get_tree([{"rule": "NoInfo", "hipotesis": "-1", "conclusion": answer}], references)
    return steps[-1]["conclusion"], get_tree(steps, references)

def is_starting_rule(message):
    """Check if the message is the start of a new derivation rule."""
    return message.startswith("Extract") or message.startswith("Concat") or message.startswith("Instantiate") or message.startswith("Compose") or message.startswith("Refine") or message.startswith("NoInfo")

def is_ending_final_answer(message):
    """Check if the message ends with the final answer decision."""
    return message.endswith("Es respuesta final") or message.endswith("No es respuesta final")

### FUNCTIONS TO CREATE THE DERIVATION TREE ###

def get_hips(hip_str):
    """Parse the hypothesis string into a list of integers."""
    if hip_str.strip() == "" or hip_str.strip() == "-":
        return []
    elems = hip_str.split(",")
    elems = [elem for elem in elems if elem != "NoInfo"]

    # Parse the elements, considering that they can be references (numbers) of previous steps (letters)
    try:
        return [int(elem.strip()) if ord(elem.strip()[-1]) < ord("a") else ord(elem.strip()) - ord("a") + 4 for elem in elems]
    except Exception as e:
        raise ValueError(f"Error parsing hypothesis: {hip_str}") from e

def reference_to_html(reference):
    """Convert a reference to an HTML link."""
    return f"<a href='{reference['source']}' target='_blank'>{reference['source']}</a>"

def get_tree(steps, refs):
    """
    Create the derivation tree from the steps and references.

    Parameters:
    - steps: List of Dict, the steps of the derivation
    - refs: List of Dict, the references used in the derivation

    Returns:
    - tree: Dict, the derivation tree
    """

    def build_tree_from_step(step_index):
        step = steps[step_index]
        node = {
            "text": step["conclusion"],
            "rule": f'[{step["rule"]}]',
            "children": []
        }

        if "-1" not in step["hipotesis"]:
            for hip in get_hips(step["hipotesis"]):
                if hip <= len(refs):
                    # This is a reference
                    ref_node = {
                        "text": reference_to_html(refs[hip - 1]),
                        "rule": None,
                        "children": None
                    }
                    node["children"].append(ref_node)
                else:
                    # This is a previous step
                    prev_step_index = hip - len(refs) - 1
                    child_node = build_tree_from_step(prev_step_index)
                    node["children"].append(child_node)
        else:
            node["children"] = None

        return node

    return build_tree_from_step(len(steps) - 1)
