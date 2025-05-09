import openai

openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # Qwen:0.5b

async def query_llm(prompt: str):
    response = await openai.ChatCompletion.acreate(
        model="qwen:0.5b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def query_llm_sync(prompt: str):
    import asyncio
    return asyncio.run(query_llm(prompt))
