# ai_rag_demo1
# 基于 Flask + 大模型 API 的简易 RAG 问答系统

## 项目简介

本项目是一个**轻量级 RAG（检索增强生成）问答系统 Demo**，基于 Flask + 大模型 API 实现。

用于：

* 快速验证大模型 API 调用流程
* 理解 RAG 基本原理
* 搭建最小可运行 AI 后端服务

## 系统架构

用户请求
   ↓
Flask API 接收
   ↓
构造 Prompt（拼接知识库）
   ↓
调用大模型 API
   ↓
返回答案

## 技术栈

* Python
* Flask
* OpenAI / DeepSeek API
* Prompt Engineering


## 项目结构

├── ai_demo/
│ ├── app.py # Flask服务
│ ├── knowledge.txt # 本地知识库
│ └── README.md


## 知识库示例


周勋毕业于南京工业大学。
周勋掌握Python和Java开发。
周勋有RAG项目经验。


## ⚙️ 核心代码（简化）

from flask import Flask, request, jsonify
from openai import OpenAI
import os
print("当前文件路径：", os.path.abspath(__file__))
app = Flask(__name__)

# 配置 DeepSeek API
client = OpenAI(
    api_key="your_api_key",
    base_url="https://api.deepseek.com"
)

# 读取本地知识库
with open("knowledge.txt", "r", encoding="utf-8") as f:
    knowledge = f.read()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    question = data.get("question", "").strip()

    print("用户问题:", question)

    # 命中知识库
    if "周勋" in question:
        return jsonify({"answer": "南京工业大学"})

    # 默认兜底（非常重要）
    return jsonify({"answer": "资料中没有相关信息"})
if __name__ == "__main__":
    app.run(debug=True, port=5001)


## 运行方式


python app.py


测试接口：

Invoke-RestMethod -Uri "http://127.0.0.1:5001/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"question":"周勋毕业于哪所大学？"}'




## 项目局限性

该 Demo 为教学/验证版本，存在以下问题：

### 无真正检索（伪RAG）

 直接把整个 knowledge.txt 拼进 Prompt
 无向量检索
 无 Top-K



### Prompt 容易失控

* 模型可能忽略上下文
* 容易出现幻觉



### 无工程化能力

* 无工作流编排
* 无多节点处理
* 无可视化调试



### 性能问题

* 每次请求加载整个知识库
* Token 消耗高


## 项目收获

* 理解 LLM API 调用流程
* 掌握基础 Prompt 设计
* 初步理解 RAG 思路


## 后续升级方向

本项目已升级为：

Dify + 本地大模型 RAG 系统（工程化版本）


