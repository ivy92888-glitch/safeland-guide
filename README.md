# 🌍 Safeland Guide · 海外生存指南

**为什么做这个项目？** 第一次去海外生活的人会遇到 101 个问题——租房怎么避押金坑？GP 和 ER 怎么区分？驾照怎么转？机场打车会不会被溢价？市面上要么是零散的游记，要么是只覆盖一个国家的单点攻略——**没有一个助手能把"海外生存"拆成 15 个独立主题，让你精准查、快速找**。

本项目把海外生存知识按**15 个场景入口彻底隔离**打包：侧栏选「居住常识」就只加载租房/水电网/室友相关的 17 个知识块，选「医疗与健康」就只加载看病/医保/急救的 10 个知识块，互不污染。知识库没命中的问题自动调用 DuckDuckGo 上网搜索权威结果兜底。

## ✨ 功能总览

| 功能 | 人话总结 | 数字例子 |
|---|---|---|
| **15 入口隔离** | 侧栏二选一（实际是十五选一），切换时只加载对应知识库 + 清空对话历史 | 医疗入口问"押金退还"→ 零结果；切居住常识 → 直接命中 |
| 知识库问答 | 给一段海外生活问题，自动从所选入口的知识库里定位最相关的段落，喂给 LLM 组织成答案 | "租房签合同注意什么" → 命中 housing_seed_03.md 合同陷阱 5 连环 |
| 上网兜底 | 如果知识库没命中或相关度低（top score < 0.15），自动调 DuckDuckGo 搜权威结果补充 | "2026 年日本入境政策" → 知识库没有 → 自动搜日本领馆官网 |
| 来源可追溯 | 每个回答下面都列参考来源（哪个知识文件 / 哪个网页） | 回答里能看到 `📚 知识库 housing_seed_03.md (相关度 0.122)` |
| 系统提示词隔离 | 每个入口有专属系统提示词（医疗专家 / 租房专家 / 求职专家），回答风格和深度不跑偏 | "医疗"入口的回答默认带症状描述模板；"社交"入口默认带各国小费规矩 |

## 🎯 15 入口速查表

| 入口 | 典型问题 | 知识块数 |
|---|---|---|
| 语言 | "办电话卡用什么词？" "点餐几分熟怎么说？" | 10 |
| 气候适应 | "冬天纽约穿什么？" "皮肤过敏当地买什么药膏？" | 14 |
| 居住常识 | "租房押金怎么退？" "水电网开户哪家便宜？" | 17 |
| 饮食与采购 | "买不到豆瓣酱用什么替？" "留学生快手菜 10 道" | 21 |
| 交通与出行 | "驾照怎么转？" "Uber 怎么防绕路？" | 11 |
| 医疗与健康 | "GP 和 ER 什么区别？" "救护车叫不起怎么办？" | 10 |
| 办事与政务 | "税号怎么申请？" "护照丢了怎么补？" | 6 |
| 社交与文化 | "小费给多少？" "哪些话题别跟外国人聊？" | 7 |
| 应急与安全 | "杀猪盘怎么识别？" "地震来了躲哪？" | 9 |
| 求职与生存 | "一页纸简历怎么写？" "面试 STAR 法则？" | 9 |
| 财务管理 | "Checking 和 Savings 区别？" "学生折扣都有哪些？" | 10 |
| 旅游 | "廉价航空行李额怎么算？" "Airbnb 假房源识别？" | 7 |
| 留学 | "选课 GPA 怎么算？" "OPT 工签怎么申？" | 4 |
| 兴趣 | "健身房月卡划算吗？" "哪里找语言交换？" | 8 |
| 人际关系 | "室友边界感怎么立？" "华人互助群怎么进？" | 6 |

## 🚀 快速开始

### 方式 A：一键启动（推荐 Windows 用户）

双击 `run.bat`，浏览器自动打开 http://localhost:8503。关掉那个黑色命令行窗口就是停止。

### 方式 B：命令行（Mac / Linux / 喜欢折腾）

```bash
pip install -r chatbot/requirements.txt

export LLM_BASE_URL="https://api.siliconflow.cn/v1"
export LLM_API_KEY="sk-your-key"
export LLM_MODEL="deepseek-ai/DeepSeek-V3"

python -m streamlit run chatbot/app.py --server.headless true --server.port 8503
```

侧边栏可以随时改 API Base URL、Key、Model、Top-K 检索参数。

## 📁 文件清单

| 文件 | 说明 |
|---|---|
| `chatbot/app.py` | Streamlit 前端（15 入口侧栏 + 聊天界面 + 侧边栏 API 配置） |
| `chatbot/rag.py` | RAG 引擎（TF-IDF char n-gram 检索 + DuckDuckGo 上网兜底 + LLM 流式调用 + `_StreamResult` 自定义迭代器） |
| `chatbot/requirements.txt` | 依赖清单（4 个包，`pip install` 秒装） |
| `knowledge/<15 入口>/` | 15 个入口的知识库，每个目录若干 .md 文件，总计 151 个 |
| `run.bat` | Windows 一键启动脚本（浏览器自动弹） |
| `.gitignore` | 忽略 `__pycache__`、`.venv`、临时脚本 |

## 🛠 技术栈

`Streamlit` · `scikit-learn TF-IDF (char n-gram 2~6)` · `DuckDuckGo Web Search (免费无 Key)` · `OpenAI-compatible LLM API`

## ⚠️ 说明

- 知识库内容混合了：用户上传的海外生存 docx 文档 + AI 生成的 15 入口知识图谱种子。后者可能过时，请以实际当地规则为准。
- 所有 docx 内容已脱敏：无前公司/前雇主/内部账号/具体报价/自媒体链接。
- 平台规则、费用、时效等数字内容标注"仅供参考，以实际后台为准"。

---

# Safeland Guide · Overseas Survival Assistant (English)

## Why this project?

People moving abroad for the first time face 101 questions — how to avoid losing a security deposit? When to go to ER vs GP? How to convert a driver's license? Will the airport taxi rip you off? Existing resources are either scattered travel blogs or single-country guides — **nothing that breaks "surviving abroad" into 15 isolated themes so you can ask precisely and find fast**.

This project packages overseas survival knowledge **with strict isolation across 15 entry points**: pick "Housing" in the sidebar → loads only rental/utilities/roommate knowledge chunks; pick "Medical" → loads only doctor/insurance/emergency chunks. Zero cross-contamination. When the knowledge base comes up empty, it automatically falls back to authoritative web search via DuckDuckGo (free, no API key).

## What it does

| Feature | Plain English | Numbers |
|---|---|---|
| **15 isolated entry points** | Sidebar pick: one of 15 themes. Each loads only its own knowledge base — zero cross-contamination | Medical mode asks "security deposit refund" → zero hits; switch to Housing → instant hit |
| Knowledge-base Q&A | Ask any question — the assistant digs through the selected theme's knowledge chunks to find the most relevant passages, then feeds them to the LLM | "Rental contract red flags" → hits housing_seed_03.md with the 5 red-flag traps |
| Web search fallback | When nothing relevant is found (top score < 0.15), automatically queries DuckDuckGo for authoritative sources | "Japan 2026 entry policy" → not in knowledge base → auto-searches Japanese embassy |
| Traceable sources | Every answer lists its references (which knowledge file / which webpage) | Answers show `📚 housing_seed_03.md (relevance 0.122)` |
| Per-mode system prompts | Each entry has its own system prompt — Medical prompts the LLM to use symptom-description templates; Social prompts it to cover tipping norms | Different entry → different expert persona |

## 15 Entry Points Quick Reference

| Entry | Typical question | Chunks |
|---|---|---|
| Language | "What word for a phone card?" "How do I order medium-rare?" | 10 |
| Climate | "What to wear in NYC winter?" "What cream for allergic skin?" | 14 |
| Housing | "How to get security deposit back?" "Which broadband is cheapest?" | 17 |
| Food & Shopping | "Substitute for doubanjiang?" "10 lazy student meals" | 21 |
| Transportation | "How to convert driver's license?" "Uber route-fraud tips" | 11 |
| Medical & Health | "ER vs GP — when to go where?" "Ambulance too expensive?" | 10 |
| Admin & Government | "How to apply for a tax number?" "Lost passport — what now?" | 6 |
| Social & Culture | "How much to tip?" "What topics are off-limits with foreigners?" | 7 |
| Emergency & Safety | "How to spot a pig-butchering scam?" "Where to hide during an earthquake?" | 9 |
| Job & Survival | "One-page resume template?" "STAR interview method?" | 9 |
| Finance | "Checking vs Savings account?" "All student discounts available" | 10 |
| Travel | "Budget airline baggage allowance?" "Airbnb fake-listing detection" | 7 |
| Study Abroad | "How is GPA calculated?" "OPT work permit application" | 4 |
| Hobbies | "Gym monthly pass worth it?" "Where to find language exchange" | 8 |
| Relationships | "How to set boundaries with roommates?" "How to join Chinese expat groups" | 6 |

## Quick start

### Option A: One-click launch (Windows users)

Double-click `run.bat`. Browser opens automatically at http://localhost:8503. Close the black command-line window to stop.

### Option B: Command line (Mac / Linux / curious types)

```bash
pip install -r chatbot/requirements.txt

export LLM_BASE_URL="https://api.siliconflow.cn/v1"
export LLM_API_KEY="sk-your-key"
export LLM_MODEL="deepseek-ai/DeepSeek-V3"

python -m streamlit run chatbot/app.py --server.headless true --server.port 8503
```

Change the API base URL, key, model, and top-K retrieval from the sidebar at any time.

## File list

| File | What it does |
|---|---|
| `chatbot/app.py` | Streamlit front-end (15-entry sidebar + chat UI + sidebar API config) |
| `chatbot/rag.py` | RAG engine (TF-IDF char n-gram retrieval + DuckDuckGo web fallback + LLM streaming + custom `_StreamResult` iterable class) |
| `chatbot/requirements.txt` | Dependencies (4 packages, `pip install` in seconds) |
| `knowledge/<15 modes>/` | Knowledge bases for each entry, 151 .md files total |
| `run.bat` | Windows one-click launch script |
| `.gitignore` | Ignores `__pycache__`, `.venv`, temp scripts |

## Tech stack

`Streamlit` · `scikit-learn TF-IDF (char n-gram 2~6)` · `DuckDuckGo Web Search (free, no API key)` · `OpenAI-compatible LLM API`

## Notes

- Knowledge base is a mix of: user-uploaded overseas survival docx files + AI-generated 15-entry knowledge graph seeds. The latter may be outdated — verify with actual local rules.
- All docx content desensitized: no prior company / employer / internal accounts / specific pricing / social media links.
- Platform rules, fees, timelines marked "for reference only — verify in your actual dashboard".
