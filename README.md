# Yighlo – YouTube Summary & Notes Generator

Yighlo analyzes information from a YouTube video or short (title, description, and transcript) and creates a file with clear, organized notes in **Markdown** format.

Everything works directly from the console with an interactive interpreter:

```
python main.py
```

Then you'll see:

```
Yighlo >
```

From there you can execute commands like:

```
Yighlo > help
Yighlo > openai <key>
Yighlo > start <url> [Options...]
```

---

## 📌 How it works

1. Start the program with Python.
2. Configure your OpenAI **API Key**.
3. Run `start <url>` with the YouTube video URL.
4. The system retrieves:
   - Title
   - Description
   - Transcript (if available)
5. With that information, it generates organized output with key points, ideas, and useful notes.
6. Creates a `.md` file inside the `output/` folder.

---

## 🔑 Getting your OpenAI API Key

To use this program, you need a valid API key.

1. 👉 [Get API Key](https://platform.openai.com/settings/organization/api-keys)  
2. Create a new key.
3. Copy it.
4. Inside the console, type:

```
openai <your_api_key_here>
```

---

## 🧰 Available commands

### Interactive CLI

| Command | Example | Explanation |
|--------|---------|-------------|
| `help` or `?` | `help` | Shows all commands. |
| `openai <key>` | `openai sk-1234...` | Sets the API key. **Required** before starting. |
| `start <url> [options...]` | `start https://youtu.be/abc123 level=0` | Analyzes the specified video. |
| `exit` | `exit` | Exit the console. |

---

## 📌 `start` parameters

> **`<>`** = required  
> **`[]`** = optional


| Parameter | Values | Example | Description |
|----------|----------|----------|-------------|
| `<url>` | - | `https://youtu.be/abc123` | YouTube video URL. |
| `[lang]` | `es` = Spanish<br>`en` = English | `lang=es` | Forces output in a specific language. **Default: en** |
| `[level]` | `0` = Weak<br>`1` = Strong | `level=0` | Allows saving some tokens. **Default: 1**
| `[model]` | [Model list](https://platform.openai.com/docs/models) | `model=gpt-5` | ChatGPT model ID to use. **Default: gpt-5-mini** |
| `[max_tokens]` | Your preference as an integer | `max_tokens=5000` | Maximum tokens allowed in output. Does not affect quality in *nano* or *mini* models. **Default: 10000**

Complete example:

```
start https://youtu.be/abc123 lang=es model=gpt-5.1 level=0
```

---

## 📄 Generated output

The console creates a `.md` file inside the `output/` folder with the video title containing the following information:

- Summary
- Key points
- Highlights
- Ideas for creators
- Related video ideas

---

## 🚀 Quick start

1. Install dependencies, you can run the `install_req.cmd` file or enter the following command:

```
pip install -r requirements.txt
```

2. Run:

```
python main.py
```

3. Configure OpenAI:

```
Yighlo > openai <key>
```

4. Analyze video:

```
Yighlo > start <url>
```

---