# 🏠 Safeland Guide · 独立生活指南

**为什么做这个项目？** 毕业到陌生城市独立生活的年轻人会遇到 101 个没人教的问题——租房怎么避押金坑？社医保怎么转？新手爸妈怎么带娃？第一次养猫要准备什么？报税退税怎么填？市面上要么是零散的小红书笔记，要么是只覆盖一个城市的单点攻略——**没有一个助手能把"独立生活"拆成 17 个独立主题，让你精准查、快速找**。

本项目把独立生活知识按**17 个场景入口彻底隔离**打包：侧栏选「育儿与家庭」就只加载备孕/产检/新生儿/辅食/疫苗相关的知识块，选「宠物养护」就只加载养猫养狗入门。每个入口有专属系统提示词，保证回答风格和深度不跑偏。知识库没命中的问题自动调用 DuckDuckGo 上网搜索权威结果兜底。

## ✨ 功能总览

| 功能 | 人话总结 | 数字例子 |
|---|---|---|
| **17 入口隔离** | 侧栏选一，切换时只加载对应知识库 + 清空对话历史 | 宠物入口问"租房押金怎么退"→ 零结果；切居住常识 → 直接命中 |
| 知识库问答 | 给一段生活问题，自动从所选入口的知识库里定位最相关的段落，喂给 LLM 组织成答案 | "个税年度汇算怎么操作" → 命中 admin_gov 报税种子 |
| 上网兜底 | 如果知识库没命中或相关度低（top score < 0.15），自动调 DuckDuckGo 搜权威结果补充 | "2026 年社保新政" → 知识库没有 → 自动搜人社部官网 |
| 来源可追溯 | 每个回答下面都列参考来源（哪个知识文件 / 哪个网页） | 回答里能看到 `📚 知识库 admin_gov_seed_02.md (相关度 0.182)` |
| 系统提示词隔离 | 每个入口有专属提示词（新手爸妈专家 / 铲屎官专家 / 报税专家），回答风格不跑偏 | "宠物"入口的回答默认带你算每月预算；"育儿"入口默认带你看产检时间线 |

## 🎯 17 入口速查表

| # | 入口 | 典型问题 | 知识块 |
|---|---|---|---|
| 1 | 语言沟通 | "打电话办业务怎么礼貌开场？" "面试自我介绍怎么说？" | 12 |
| 2 | 气候适应 | "北方冬天穿什么？" "墙发霉怎么处理？" | 1 |
| 3 | 居住常识 | "租房押金怎么退？" "收纳整理有什么好方法？" | 3 |
| 4 | 饮食与采购 | "不会做饭从哪开始？" "买菜怎么省钱？" | 27 |
| 5 | 交通与出行 | "驾照怎么迁回异地？" "网约车怎么防绕路？" | 6 |
| 6 | 医疗与健康 | "社区医院 vs 三甲医院怎么选？" "医保异地能用吗？" | 3 |
| 7 | 办事与政务 | "社保怎么转异地？" "个税年度汇算怎么填？" | 3 |
| 8 | 社交与文化 | "南北方买菜差异？" "同事聚餐怎么不踩雷？" | 3 |
| 9 | 应急与安全 | "刷单诈骗怎么识别？" "丢身份证异地怎么补？" | 6 |
| 10 | 求职与生存 | "简历怎么写一页纸？" "试用期被辞退怎么维权？" | 11 |
| 11 | 财务管理 | "每月房租占收入多少合适？" "信用卡最低还款的坑？" | 36 |
| 12 | 旅游 | "廉价航空行李额怎么算？" "周边游怎么规划？" | 9 |
| 13 | 学习提升 | "考公 vs 考研怎么选？" "怎么科学备考？" | 0 |
| 14 | 兴趣爱好 | "健身房怎么选？" "不会社交怎么认识朋友？" | 12 |
| 15 | 人际关系 | "室友边界感怎么立？" "借钱怎么说不？" | 4 |
| 16 | 育儿与家庭 | "产检时间线？" "新生儿喂奶频率？" "辅食怎么加？" | 32 |
| 17 | 宠物养护 | "第一次养猫准备什么？" "猫耳螨怎么治？" | 0 |

（注：学习提升 / 宠物养护 桌面知识库暂无对口文件，完全靠 AI 知识图谱种子填充。）

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
| `chatbot/app.py` | Streamlit 前端（17 入口侧栏 + 聊天界面 + 侧边栏 API 配置） |
| `chatbot/rag.py` | RAG 引擎（TF-IDF char n-gram 检索 + DuckDuckGo 上网兜底 + LLM 流式调用 + `_StreamResult` 自定义迭代器） |
| `chatbot/requirements.txt` | 依赖清单（4 个包，`pip install` 秒装） |
| `knowledge/<17 入口>/` | 17 个入口的知识库，总计 207 个 .md 文件 |
| `run.bat` | Windows 一键启动脚本（浏览器自动弹） |
| `.gitignore` | 忽略 `__pycache__`、`.venv`、临时构建脚本 |

## 🛠 技术栈

`Streamlit` · `scikit-learn TF-IDF (char n-gram 2~6, sublinear_tf)` · `DuckDuckGo Web Search (免费无 Key)` · `OpenAI-compatible LLM API`

## ⚠️ 说明

- 知识库内容混合了：桌面上传的生活相关 docx + AI 生成的 17 入口知识图谱种子。AI 种子可能过时，请以实际当地规则/政策为准。
- 所有 docx 内容已脱敏：无前公司/前雇主/内部账号/具体报价/自媒体链接。
- 平台规则、费用、时效等数字内容标注"仅供参考，以实际后台为准"。

---

# Safeland Guide · Independent Living Assistant (English)

## Why this project?

Young people moving to a new city after graduation face 101 untaught questions — how to avoid a rental security-deposit scam? How to transfer social insurance? How to be a new parent? What to buy before adopting a cat? How to file a tax refund? Existing resources are scattered (小红书 posts, single-city guides, 5-minute Douyin videos) — **nothing that breaks "independent living" into 17 isolated themes so you can ask precisely and find fast**.

This project packages independent-living knowledge **with strict isolation across 17 entry points**: pick "Parenting" → loads only pregnancy/prenatal/newborn/solid-food/vaccination knowledge; pick "Pets" → loads only cat+dog-care basics. Each entry has its own system prompt so responses stay in-character. When the knowledge base comes up empty, it automatically falls back to authoritative web search via DuckDuckGo (free, no API key).

## What it does

| Feature | Plain English | Numbers |
|---|---|---|
| **17 isolated entry points** | Sidebar radio pick: one of 17 themes. Each loads only its own knowledge base — zero cross-contamination | Pets mode asks "how to get a rental deposit back" → zero hits; switch to Housing → instant hit |
| Knowledge-base Q&A | Ask any question — the assistant digs through the selected theme's knowledge chunks to find the most relevant passages, then feeds them to the LLM | "How to do my annual tax filing?" → hits admin_gov tax seeds |
| Web search fallback | When nothing relevant is found (top score < 0.15), automatically queries DuckDuckGo for authoritative sources | "2026 social insurance policy" → not in KB → auto-searches government site |
| Traceable sources | Every answer lists its references (which knowledge file / which webpage) | Shows `📚 admin_gov_seed_02.md (relevance 0.182)` |
| Per-mode system prompts | Each entry has its own persona (new-parent expert / cat-dog expert / tax expert) so answers don't drift | Pets mode defaults to calculating monthly pet budget; Parenting mode defaults to prenatal timeline |

## 17 Entry Points Quick Reference

| # | Entry | Typical question | Chunks |
|---|---|---|---|
| 1 | Language | "How to politely start a phone call for business?" "Tell me a self-intro template" | 12 |
| 2 | Climate | "What to wear in northern winter?" "How to treat mold on walls?" | 1 |
| 3 | Housing | "How to get security deposit back?" "Any good decluttering tips?" | 3 |
| 4 | Food & Shopping | "I can't cook — where to start?" "How to save money at the market?" | 27 |
| 5 | Transportation | "How to convert driver's license?" "How to avoid rideshare detours?" | 6 |
| 6 | Medical | "Community clinic vs 3A hospital — which to choose?" "Can medical insurance be used cross-city?" | 3 |
| 7 | Admin & Government | "How to transfer social insurance?" "How to do annual tax filing?" | 3 |
| 8 | Social & Culture | "North vs south buying habits — any difference?" "How not to step on toes at office dinners?" | 3 |
| 9 | Emergency & Safety | "How to spot a job-scam?" "How to replace lost ID in another city?" | 6 |
| 10 | Job & Survival | "How to write a one-page resume?" "How to fight unfair dismissal during probation?" | 11 |
| 11 | Finance | "How much rent should be ≤ of my income?" "What's the trap with credit-card minimum payments?" | 36 |
| 12 | Travel | "How to calculate budget-airline baggage allowance?" "How to plan a weekend trip?" | 9 |
| 13 | Study Up | "Civil service exam vs grad school — how to choose?" "How to study effectively?" | 0 |
| 14 | Hobbies | "How to pick a gym?" "How to make friends when you don't drink?" | 12 |
| 15 | Relationships | "How to set roommate boundaries?" "How to say no when someone asks to borrow money?" | 4 |
| 16 | Parenting | "Prenatal exam timeline?" "How often to feed a newborn?" "How to introduce solid food?" | 32 |
| 17 | Pets | "What to buy before adopting a cat?" "How to treat ear mites in cats?" | 0 |

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
| `chatbot/app.py` | Streamlit front-end (17-entry sidebar + chat UI + sidebar API config) |
| `chatbot/rag.py` | RAG engine (TF-IDF char n-gram retrieval + DuckDuckGo web fallback + LLM streaming + `_StreamResult` custom iterable class) |
| `chatbot/requirements.txt` | Dependencies (4 packages, `pip install` in seconds) |
| `knowledge/<17 modes>/` | Knowledge bases for each entry, 207 .md files total |
| `run.bat` | Windows one-click launch script |
| `.gitignore` | Ignores `__pycache__`, `.venv`, temp build scripts |

## Tech stack

`Streamlit` · `scikit-learn TF-IDF (char n-gram 2~6, sublinear_tf)` · `DuckDuckGo Web Search (free, no API key)` · `OpenAI-compatible LLM API`

## Notes

- Knowledge base is a mix of: user-uploaded lifestyle docx files + AI-generated 17-entry knowledge graph seeds. AI seeds may be outdated — verify with actual local rules/policies.
- All docx content desensitized: no prior company / employer / internal accounts / specific pricing / social media links.
- Platform rules, fees, timelines marked "for reference only — verify in your actual dashboard".
