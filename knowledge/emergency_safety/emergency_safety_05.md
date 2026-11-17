# 应急与安全 · 第8册_逻辑统计数学工具箱技术编程实战

科学方法论找 bug
靠 print 和猜，改 bug 效率低 10 倍
Profiling 性能分析
找到程序慢在哪
盲目优化，越改越慢
安全与加密
理解 HTTPS、SSH、GPG
密码泄露、被中间人攻击
自动化
shell 脚本 + Makefile / Cron
重复劳动、容易忘
💡  上这课最快的办法：missing.csail.mit.edu 有免费课程笔记和习题。B站「常青藤中英字幕课程」搬运了 602 分钟中英字幕版。建议先学 Git 和 Shell，这俩是回报率最高的。
📌  RAG = Retrieval Augmented Generation，让 AI 引用你的知识库回答问题。核心三步：文本分块 → 向量化 → 存向量数据库。
步骤
做什么
常用工具
1. 采集
把 PDF / Doc / 网页转成纯文本
Unstructured、PyMuPDF、BeautifulSoup
2. 分块
把长文本切成 500–1000 字的块
LangChain RecursiveCharacterTextSplitter
3. 向量化
把每个块变成向量
OpenAI ada-002、bge-large-zh、text2vec-base
4. 存库
向量存进向量数据库
Chroma（轻量）/ Faiss（本地）/ Milvus（企业级）/ Pinecone（云）
5. 检索
用户提问 → 搜最相似的块
cosine 相似度 / hybrid search
6. 生成
把检索结果喂给 LLM
GPT / Claude / Qwen / Llama
📌  普通人 1 年超别人 10 年：自学最核心部分 + 借力 + 边做边改快速试错。
原则
做什么
为什么比传统学习快
例子
自学核心
先学骨架，再填血肉
传统学习先填几十年血肉还没骨架
学编程先写「Hello World」，再学数据结构
借力
用别人已经总结好的
别自己从 0 造轮子
学 AI 先用 LangChain 框架，别自己手写神经网络
快速试错
做出来 → 发布 → 改 → 再发布
别完美主义，先发再优化
做自媒体先发 10 条烂内容，观察数据后调整
来源文件
主要覆盖内容
手册八（第8册_逻辑统计数学工具箱）
行为经济学工具箱（参照点/损失厌恶/禀赋效应/处置效应/当下享乐偏误/助推/心理账户）/ 统计学八步法 / 凯利公式 / 赌徒输光 / 圣彼得堡悖论 / 线性代数 / AI 数学基础
01 手册（01_技术与编程实战手册）
HTTP 奶茶店类比 / VSCode / 整洁架构 / AI 蒸馏 4 条规矩 / GitHub 红利 / Karpathy 200 行 microGPT / MIT Missing Semester 8 门补课 / RAG 搭建 / Steve Brunton 数学基础 / 独立游戏 10 工具
对比维度
手册八
01 手册
主题
行为经济学 + 统计学 + 概率投资
HTTP / API / Git / Karpathy microGPT
篇幅
37KB / 62 paras / 0 tables
51KB / 105 paras / 15 tables
重叠度
零
零
合并方式
编一～编三
编四～编九