import zipfile
import io
from openai import OpenAI
import json

API_KEY = "YOUR_API_KEY"

client = OpenAI(
    base_url="https://api.onlysq.ru/ai/openai",
    api_key=API_KEY,
)

response = client.chat.completions.create(
    model="pplx-gemini-3-flash", 
    messages=[
        {"role": "system", "content": """Role: Narrative Quest Designer.
Task: Create a branching text quest.
Output: ONLY a valid JSON array of objects. No intro/outro text.
Output raw JSON only, no markdown code blocks

Structure:
{
    "backgroundPrompt": "...",
    "nodes": [
        {
            "id": 1,
            "text": "Starting location description...",
            "buttons": [
                {"label": "Go North", "to": 2},
                {"label": "Search bushes", "to": 3}
            ]
        },
        ...
    ]
}

Constraints:
1. "to" MUST point to a valid "id" in the array.
2. Every path must lead to a valid node or an ending (empty buttons array).
3. Maximum 3-4 buttons per node.
4. "text" should be concise and atmospheric.
5. NO Markdown formatting, only raw JSON.
6. In background prompt add a english prompt for Flux image generator.
7. Text or buttons label should be in Russian.
"""},
        {"role": "user", "content": "Придумай большой квест с сюжетом"}
    ],
)

quest_data = response.choices[0].message.content
print(json.loads(quest_data)) # type: ignore

files = ['config.json', 'nodes.json']

buf = io.BytesIO()

with zipfile.ZipFile(buf, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
    for file in files:
        zf.writestr(file, open(f"res/{file}", "r", encoding="utf-8").read())

with open("quest.mnd", "wb") as f:
    f.write(b"MND_ZIP_")
    f.write(buf.getvalue())

print("Квест запакован")
with open("res/nodes.json", "r") as f:
    d = json.load(f)
    print(json.dumps(d, indent=4))