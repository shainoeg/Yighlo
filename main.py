import youtube, os, time
from datetime import datetime
from tzlocal import get_localzone
from highlights import highlights


def cls():
    os.system('cls')

def generate_markdown(data, url, title):
    md = f"""
# URL
- [@URL Video]({url})

{data}
"""
    now = datetime.now(get_localzone())
    if not os.path.exists("output"):
        os.makedirs("output")
    date = now.strftime('%Y-%m-%d %H-%M-%S')
    title = "".join(c for c in title if c not in "\\/:*?\"<>|")
    with open(f"output/{title}_{date}.md", "w",encoding="utf-8") as f:
        f.write(md)
    print(f"Markdown file saved as {title}_{date}.md")

def parse_cli_input(line):
    line = line.strip()
    if not line:
        return None, [],  {}
    parts = line.split(" ")
    command = parts[0]
    try:
        args = parts[1]
        options = {}
        for p in parts[1:]:
            if "=" in p:
                key, value = p.split("=", 1)
                if key not in options:
                    options[key] = value
    except Exception as e:
        print("Need an argument")
        args = ""
        options = {}
    return command, args, options

def main():
    cls()
    h = None
    debug = False

    print("Welcome to Yighlo CLI")
    print("======================")

    while True:
        del h
        h = highlights()
        line = input("Yighlo > ").strip()
        if line == "exit": break
        command, args, options = parse_cli_input(line)

        # --- HELP ---
        if command == "help" or command == "h" or command == "?":
            print("""
        List of Commands:
    help                            - Shows this help
    debug                           - Debug mode ON/OFF
    openai <key>                    - Saves an API key
    start <url> [OPTIONS...]        - Starts with a URL
    exit                            - Exits the program
    """)
            
        # --- DEBUG ---
        elif command == "debug":
            if debug == False:
                debug = True
                print(" * Debug mode ON")
            else:
                debug = False
                print(" * Debug mode OFF")

        # --- OPENAI KEY ---
        elif command == "openai":
            key = args
            h.save_ak(key)

        # --- START WITH URL ---
        elif command == "start":
            url = args
            if url == "":
                print("No URL provided.")
                continue
            else:
                lang = options.get("lang", "en")
                if lang not in ["en", "es"]:
                    print("Invalid language. Choose 'en' or 'es'.")
                    continue
                level = int(options.get("level", 1))
                if level not in [0, 1]:
                    print("Invalid level. Choose 0 or 1.")
                    continue
                model = options.get("model", "gpt-5-mini")
                max_tokens = int(options.get("max_tokens", 10000))

                info = youtube.yt(url, debug)
                h = highlights(model, lang, level, max_tokens)
                data = h.get_highlights(info.title, info.description, info.transcript)
                if data == False: continue
                else:
                    print("Generating file...")
                    generate_markdown(data["text"], url, info.title)
                    print(f"\nTokens used: {data['tokens_usage']}")

        # --- UNKNOWN COMMAND ---
        else:
            print("Unrecognized or incomplete command. Type 'help' or '?' to see the available commands.")

if __name__ == "__main__":
    main()