from dotenv import load_dotenv
import os, ctypes, sys
from openai import OpenAI, AuthenticationError, RateLimitError, InternalServerError

class highlights:
    def __init__(self, model="gpt-5-mini", lang="en", level=1,tokens=10000):
        self.fileenv = '.ako.env'
        self.key = None
        self.model = model
        self.lang = lang
        self.level = level
        self.tokens = tokens
        self.client = None
    def save_ak(self, key):
        try:
            self.key = key
            if self.key != None:
                if len(self.key) >= 111:
                    with open(self.fileenv, 'w', encoding="utf-8") as f:
                        f.write(f"API_KEY={self.key}\n")
                        if os.name == "nt":
                            FILE_ATTRIBUTE_HIDDEN = 0x02
                            ctypes.windll.kernel32.SetFileAttributesW(self.fileenv, FILE_ATTRIBUTE_HIDDEN)
                    if self.use_api() == True: print("API key saved successfully.")
                elif self.key == "" or self.key == None or self.key == []:
                    print("API key is empty.")
                else:
                    print("API key is too short.")
            else: print("Error saving API key.")
        except Exception as e:
            self.key = None
            print(f"Error: {e}")

    def use_api(self):
        try:
            if os.path.exists(self.fileenv):
                load_dotenv(self.fileenv, override=True)
                self.key = os.getenv("API_KEY")
                self.client = OpenAI(api_key=self.key)
                m = self.client.models.list()
                return True
            else:
                self.key = None
                print("API key not found. Use 'openai <key>' to set one.")
                return False
        except AuthenticationError as ae:
            self.key = None
            print(f"Authentication error: {ae}")
            return False
        except Exception as e:
            self.key = None
            print(f"Error: {e}")
            return False
    
    def get_highlights(self, title, desc, transcription):
        with open(rf".prompts/{self.lang}/{self.level}.txt", "r", encoding="utf-8") as r:
            prompt = r.read()
            prompt = prompt.replace("{YBzHoYH9uj0a1LLKOUh1}", f"\"{title}\"")
            prompt = prompt.replace("{200Dpehn&1102-_ad}", f"\"{desc}\"")
            prompt = prompt.replace("{t4sripc_&01-tses}", f"\"{transcription}\"")
        with open(rf".prompts/{self.lang}/st.txt", "r", encoding="utf-8") as r:
            sr = r.read()
        print("Using OpenAI API...")
        if self.use_api() == False: return False
        print("Generating highlights...")
        try:
            params = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": sr},
                    {"role": "user", "content": prompt}
                ]
            }
            if "nano" not in self.model.lower() or "mini" not in self.model.lower():
                params["max_completion_tokens"] = self.tokens
            response = self.client.chat.completions.create(**params)
            text = response.choices[0].message.content
            tokens_usage = response.usage.total_tokens
            return {
                "text": text,
                "tokens_usage": tokens_usage
            }
        except RateLimitError as rle:
            print(f"Rate limit error: {rle}")
            return False
        except InternalServerError as ise:
            print(f"Internal server error: {ise}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
