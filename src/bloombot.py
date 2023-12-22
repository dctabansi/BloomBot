import google.generativeai as genai
from discord.ext import commands
import yaml
import re


with open("creds.yaml", 'r') as creds:
    credentials = yaml.safe_load(creds)
    bot_token = credentials['bot_token']
    genai_key = credentials['palm_key']

genai.configure(api_key = genai_key)

generation_config = genai.GenerationConfig(
    temperature = 0.9,
    top_p = 1,
    top_k = 1,
    max_output_tokens = 2048
)

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

model = genai.GenerativeModel(
    model_name = "gemini-pro",
    generation_config = generation_config,
    safety_settings = safety_settings
)

client = commands.Bot()


def split_responses(response):
    sentences = re.split('(?<! [A-Z])\\.(?= [A-Z])', response)
    current_sentence = ""
    sections = [""]
    
    for word in response.split():
        if word[-1] in [".", "!", "?"]:
            sentences.append(current_sentence + word)
            current_sentence = ""
        else:
            current_sentence += word + " "
    
    index = 0
    for sentence in sentences:
        new_sentence = " " + sentence if sections[index] else sentence
        if len(sections[index] + new_sentence) <= 2000:
            sections[index] += new_sentence
        else:
            index += 1
            sections.append(sentence)
    
    return sections


@client.slash_command(name = "text", description = "Text prompt with Gemini Pro")
async def text(context, prompt: str):
    await context.defer()
    
    print(f"Username: {context.author.name} ({str(context.author.id)})")
    print("Prompt: " + prompt)
    
    try:
        response = model.generate_content(contents = prompt).text
        
        if response is None:
            print("Text | No Response Available\n")
            await context.respond("No Response Available")
        
        elif len(response) > 2000:
            print("Response: " + response + "\n")
            sections = split_responses(response)
            for section in sections:
                await context.respond(section.strip())
        
        else:
            print("Response: " + response + "\n")
            await context.respond(response)
    
    except Exception as e:
        print(f"\033[31mERROR: {e}\033[0m")
        await context.respond("An error has occurred. Please try again.")


@client.slash_command(name = "chat", description = "Chat prompt with PaLM AI")
async def chat(context, prompt: str):
    print("Prompt: " + prompt)
    
    print("Chat | Not Yet Implemented")
    await context.respond("Not Yet Implemented")


@client.slash_command(name = "data", description = "Data prompt with PaLM AI")
async def data(context, prompt: str):
    print("Prompt: " + prompt)
    
    print("Data | Not Yet Implemented")
    await context.respond("Not Yet Implemented")


if __name__ == "__main__":
    print("\nRunning...\n"
          "Log:\n")
    client.run(bot_token)
    print("\nProgram Stopped Successfully\n")
