from anthropic import Anthropic
import os

def get_response(system_prompt, messages, model, temp=0.0, max_tok=1250):
    """
    Get the response from the Anthropic API.

    Parameters:
    - system_prompt: String, the system prompt to use
    - messages: List of Dict, the messages to use
    - model: String, the model to use (opus or haiku)
    - temp: Float, the temperature to use for the generation process (default is 0)
    - max_tok: Integer, the maximum number of tokens to generate (default is 1000)

    Returns:
    - response: String, the response from the API
    """
    client = Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    kwargs = {
        "model": 'claude-3-opus-20240229' if model == 'opus' else 'claude-3-haiku-20240307',
        "max_tokens": max_tok,
        "temperature": temp,
        "system": system_prompt,
        "messages": messages
    }

    message = client.messages.create(**kwargs)
    return message.content[0].text
