import google.generativeai as palm
from discord.ext import commands
import yaml

with open("creds.yaml", 'r') as creds:
    credentials = yaml.safe_load(creds)
    bot_token = credentials['bot_token']
    palm_key = credentials['palm_key']
    
palm.configure(api_key = palm_key)

defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 2000,
    'stop_sequences': [],
    'safety_settings': [{"category": "HARM_CATEGORY_DEROGATORY", "threshold": 3},
                        {"category": "HARM_CATEGORY_TOXICITY", "threshold": 3},
                        {"category": "HARM_CATEGORY_VIOLENCE", "threshold": 3},
                        {"category": "HARM_CATEGORY_SEXUAL", "threshold": 3},
                        {"category": "HARM_CATEGORY_MEDICAL", "threshold": 3},
                        {"category": "HARM_CATEGORY_DANGEROUS", "threshold": 3}],
    }

client = commands.Bot()


def split_responses(response):
    sentences = []
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
        if sections[index] == "":
            sections[index] += sentence
        elif len(sections[index] + sentence) < 2000:
            sections[index] += sentence
        elif len(sections[index] + sentence) > 2000:
            index += 1
            sections.append(sentence)
    
    return sections


@client.slash_command(name = "text", description = "Text prompt with PaLM AI")
async def text(context, prompt: str):
    await context.defer()
    
    print(f"Username: {context.author.name} ({str(context.author.id)})")
    print("Prompt: " + prompt)
    
    try:
        response = palm.generate_text(**defaults, prompt = prompt).result
        
        if response is None:
            print("Text | No Response Available\n")
            await context.respond("No Response Available")
        
        elif len(response) > 2000:
            print("Response: " + response + "\n")
            sections = split_responses(response)
            for section in sections:
                await context.respond(section)
        
        else:
            print("Response: " + response + "\n")
            await context.respond(response)
    
    except (Exception,):
        print("\033[31mERROR\033[0m")
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
    