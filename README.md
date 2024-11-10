# Repo of Derivation Prompting

![derivation_prompting](imgs/derivation_prompting.png)

Official implementation for the paper [Derivation Prompting: A Logic-Based Method for
Improving Retrieval-Augmented Generation](#) with code, data and prompts.

**Note:** The main prompt, few-shot examples and corpus used in this work are all in Spanish due to the nature of the project. However, the code can be easily adapted to other languages.

## Setup
To set up the project, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/nsuruguay05/derivation-prompting.git
    cd derivation-prompting
    ```

2. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Add the Anthropic API key:**

    Create a `.env` file in the root directory and add your API key:

    ```bash
    ANTHROPIC_API_KEY=your_api_key_here
    ```

4. **Run the application:**

    ```bash
    python run.py --question "Your question here"
    ```

## Arguments
- `--question` (required): The question to generate an answer for.
- `--save_tree` (optional, default: `True`): Whether to save the derivation tree to a JSON file.
- `--retrieval_method` (optional, default: `'bi_encoder'`): The retrieval method to use (`'bi_encoder'` or `'cross_encoder'`).
- `--model` (optional, default: `'opus'`): The model to use for answer generation (`'opus'` or `'haiku'`).
- `--temperature` (optional, default: `0.0`): The temperature for the language model sampling.

## Example Usage

```bash
python run.py --question "¿Cómo me inscribo a un curso?" --model "haiku" --temperature 0.7
```

## Visualizing the Derivation Tree
After generating an answer, a derivation tree is saved as derivation_tree.json. To visualize this tree:

1. **Ensure derivation_tree.json is present**

   This file is created when you run the run.py script with the `--save_tree` flag enabled (default is `True`).

2. **Open visualize_derivation.html in a browser**

   Directly opening the file might cause cross-origin issues. Instead, start a local HTTP server:

   ```bash
   python -m http.server 8000
   ```

   This command starts a server on port 8000.

3. **Access the visualization**

   Navigate to `http://localhost:8000/visualization/visualize_derivation.html` in your web browser.

Now you can interactively explore the derivation tree generated from your question.

## Citation

The paper was accepted at the Iberamia'2024 conference. We will update this section with the citation once the proceedings are published.