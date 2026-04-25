# 基于 Flask + 大模型 API 的简易 RAG 问答系统

## 项目简介

本项目是一个**轻量级 RAG（检索增强生成）问答系统 Demo**，基于 Flask + 大模型 API 实现。

用于：

* 快速验证大模型 API 调用流程
* 理解 RAG 基本原理
* 搭建最小可运行 AI 后端服务

---

## 系统架构

```text
用户请求
   ↓
Flask API 接收
   ↓
构造 Prompt（拼接知识库）
   ↓
调用大模型 API
   ↓
返回答案
```

---

## 技术栈

* Python
* Flask
* OpenAI / DeepSeek API
* Prompt Engineering

---

## 项目结构

```
├── ai_demo/
│ ├── app.py # Flask服务
│ ├── knowledge.txt # 本地知识库
├── README.md
```

---

## 知识库示例

```text
周勋毕业于南京工业大学。
周勋掌握Python和Java开发。
周勋有RAG项目经验。
```

---

##  核心代码（简化）

```python
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="your_api_key")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")

    # 读取知识库
    with open("knowledge.txt", "r", encoding="utf-8") as f:
        knowledge = f.read()

    # 构造Prompt
    prompt = f"""
    参考资料：
    {knowledge}

    用户问题：
    {question}

    请基于参考资料回答：
    """

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})
```

---

## 运行方式

```bash
python app.py
```

测试接口：

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body ([System.Text.Encoding]::UTF8.GetBytes('{"question":"周勋毕业于哪所大学？"}'))
```


##  项目局限性

该 Demo 为教学/验证版本，存在以下问题：

### 无真正检索（伪RAG）

* 直接把整个 knowledge.txt 拼进 Prompt
* ❌ 无向量检索
* ❌ 无 Top-K

---

### Prompt 容易失控

* 模型可能忽略上下文
* 容易出现幻觉

---

### 无工程化能力

* ❌ 无工作流编排
* ❌ 无多节点处理
* ❌ 无可视化调试

---

##  遇到的关键问题 & 解决方案

### OpenAI / API 402 错误

**问题：**

```text
Insufficient Balance
```

**原因：**
API余额不足

**解决：**

* 更换本地模型（Ollama）
* 或充值API

---

**Windows PowerShell 中文乱码问题**

在 PowerShell 中直接传 JSON 字符串时，服务端可能收到乱码：

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"周勋毕业于哪所大学？"}'
```

```text
??????????
```

### 原因

* PowerShell 默认编码不是 UTF-8
* 中文 JSON 在传输过程中被错误编码

---

### 解决方案一

```powershell
$body = @{
    question = "周勋毕业于哪所大学？"
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://127.0.0.1:5000/ask" `
  -Method POST `
  -ContentType "application/json; charset=utf-8" `
  -Body $body
```

---

### 解决方案二（底层方式）

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body ([System.Text.Encoding]::UTF8.GetBytes('{"question":"周勋毕业于哪所大学？"}'))
```

解决后正确回答：
```text
根据参考资料,周勋毕业于南京工业大学。
```
<img width="1256" height="469" alt="屏幕截图 2026-04-25 234401" src="https://github.com/user-attachments/assets/c4cd1a68-2e86-4f8a-9484-6ad00cb9c90c" />

---

## 项目收获

* 理解 LLM API 调用流程
* 掌握基础 Prompt 设计
* 初步理解 RAG 思路

---

## 后续升级方向

本项目已升级为：

**Dify + 本地大模型 RAG 系统（工程化版本）**

