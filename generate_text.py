import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()

def openai_generate_text(api_key, prompt, context=None, model="gpt-4", temperature=0.7, max_tokens=100, stop=None):
    """
    Generates text based on a given prompt using the OpenAI API.

    Parameters:
    api_key (str): The API key for accessing the OpenAI API.
    prompt (str): The prompt to generate text from.
    context (str): Optional context to provide additional information for the text generation.
    model (str): The model to use for text generation (default is "gpt-4").
    temperature (float): Sampling temperature to control the creativity of the model (default is 0.7).
    max_tokens (int): The maximum number of tokens in the generated text (default is 100).
    stop (str or list): Optional stop sequence to end the generation.

    Returns:
    str: Text generated by the OpenAI API.
    """
    if context:
        prompt_content = f"Context: {context}\n\nPrompt: {prompt}"
    else:
        prompt_content = f"Prompt: {prompt}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt_content}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stop": stop
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json["choices"][0]["message"]["content"].strip()
        return generated_text
    else:
        return f"Error {response.status_code}: {response.text}"



def anthropic_generate_text(api_key, prompt, model="claude-3-5-sonnet-20240620", max_tokens=1024, temperature=0.7):
    """
    Generates text based on a given prompt using the Anthropic API.

    Parameters:
    api_key (str): The API key for accessing the Anthropic API.
    prompt (str): The prompt to generate text from.
    model (str): The model to use for text generation (default is "claude-3-5-sonnet-20240620").
    max_tokens (int): The maximum number of tokens in the generated response (default is 1024).
    temperature (float): Sampling temperature to control the creativity of the model (default is 0.7).

    Returns:
    str: Text generated by the Anthropic API.
    """
    url = "https://api.anthropic.com/v1/messages"
    
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        generated_text = response_json["content"][0]["text"].strip()
        return generated_text
    else:
        return f"Error {response.status_code}: {response.text}"


import requests
import json

def run_mistral(api_key, user_message, model="mistral-medium-latest"):
    url = "https://api.mistral.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7,
        "top_p": 1.0,
        "max_tokens": 512,
        "stream": False,
        "safe_prompt": False,
        "random_seed": 1337
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"].strip()
    else:
        return f"Error {response.status_code}: {response.text}"


def mistral_generate_text(api_key, prompt, model="mistral-medium-latest"):
    """
    Generates text based on a given prompt using the Mistral API.

    Parameters:
    api_key (str): The API key for accessing the Mistral API.
    prompt (str): The prompt to generate text from.
    model (str): The model to use for text generation (default is "mistral-medium-latest").

    Returns:
    str: Generated text from the Mistral API.
    """
    user_message = f"Generate text based on the following prompt:\n\n{prompt}"
    return run_mistral(api_key, user_message, model=model)
