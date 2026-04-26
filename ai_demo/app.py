from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# 配置 DeepSeek API
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 读取本地知识库
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

@app.route("/ask", methods=["POST"])
def ask():
    # 1. 获取用户问题
    question = request.json.get("question", "")

    # 2. 拼接Prompt：知识 + 用户问题
    prompt = f"""你是一个招聘助手。请根据以下参考资料回答用户问题。
如果资料中没有答案，请如实说不知道。

参考资料：
{knowledge}

用户问题：{question}

请回答："""

    # 3. 调用大模型API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # 4. 提取并返回答案
    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
