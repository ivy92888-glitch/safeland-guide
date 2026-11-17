# 应急与安全 知识库 · 第8册_逻辑统计数学工具箱技术编程实战

        y = [data[i+1:i+block_size+1]]
        # forward
        logits = model.forward(x)
        # simple cross-entropy (one-hot)
        loss = Value(0.0)
        for t in range(block_size):
            target = y[0][t]
            pred = logits[0][t]
            loss = loss + pred[target] * -1 + math.log(sum(math.exp(p.data) for p in pred))
        # backward
        for p in params: p.grad = 0.0
        loss.backward()
        opt.step()
        if step % 20 == 0:
            print(f"Step {step}, loss: {loss.data:.4f}")
    return model, tokenizer
# ========== 7. Run ==========
if __name__ == '__main__':
    text = "hello world this is a tiny gpt demo " * 50
    model, tok = train_gpt(text, max_steps=200)
    out = model.generate([[0]], max_new_tokens=40)
    print(tok.decode(out[0]))
📌  Git 是版本控制，不是备份工具；commit 是快照，push 是上传，pull 是拉取。
📌  GitHub 6 万星项目，程序员「蒸馏自己」给 AI 注入软件工程之魂。源自 Karpathy 对 LLM 编程陷阱的观察，4 条规矩管住 AI。把规矩丢进项目根目录（CLAUDE.md / .cursorrules），AI 自动遵守。
规矩
原话
通俗解释
规则 1
不确定的先问，别瞎猜
AI 遇到模糊需求会瞎编——让它问清楚再动手
规则 2
代码能简短就别写长
AI 喜欢把简单逻辑写复杂——让它用最少代码解决问题
规则 3
没让你改的地方别碰
AI 爱自动「优化」你没让它动的代码——划定边界
规则 4
给目标，别给步骤
告诉 AI「要什么」比告诉 AI「怎么做」效果好 10 倍
💡  AI 时代红利：GitHub = 全球最大开源社区 + AI 时代万能宝库。6 个宝藏区域：免费 AI 工具、自动化工作流、软件平替、学习资料、简历模板、电子书。AI 能帮你写代码，但 AI 不知道该写什么——你需要用 GitHub 学别人怎么写好代码 → 把学到的喂给 AI → AI 帮你写 → 你负责审查和方向。
宝藏类型
怎么找
典型案例
免费 AI 工具
搜 awesome-llm-apps、free-gpt-clone
Ollama 本地跑模型、Chatbot UI 套壳
自动化工作流
搜 github-actions-workflow、automation
定时发周报、自动发推文、CI/CD
软件平替
搜 xxx-alternative
免费替代 Photoshop 的 GIMP、替代 Notion 的 AppFlowy
学习资料
搜 free-programming-books、public-apis
MIT 课程笔记、1000+ 免费 API
简历模板
搜 resume-template、developer-resume
JSON Resume 一键生成 ATS 友好简历
电子书 / PPT
搜 free-ebook、ppt-template
各类行业免费学习资源
💡  怎么学：B站视频 + 讲义 + 作业，按顺序学。视频是英文的，有字幕配合中文字幕看。这门课最大的好处是——每讲完一个数学概念，立刻演示在 Python 里怎么用。
📌  MIT 计算机补课：Missing Semester = MIT 给新生开的「计算机教育中缺失的一门课」。8 个核心技能——Shell / Git / Vim / 调试 / 数据处理 / 安全 / 命令行 / 自动化。
课程主题
为什么重要
你缺这个会怎样
Shell Tools & Scripting
命令行是程序员的瑞士军刀
不会快速处理批量文件、不会写自动化脚本
Git 版本控制
不只是 commit / push
合并冲突炸锅、代码丢了找不回来
Vim 编辑器
高效编辑利器
每次改代码都在鼠标键盘之间切换
数据处理
sed / awk / xargs / pandas 一行搞定
CSV 大文件只能手动处理
调试方法
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