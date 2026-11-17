# 应急与安全 · 第8册_逻辑统计数学工具箱技术编程实战

# ========== 5. Adam Optimizer ==========
class Adam:
    def __init__(self, params, lr=0.01, beta1=0.9, beta2=0.999, eps=1e-8):
        self.params = params
        self.lr = lr
        self.beta1, self.beta2, self.eps = beta1, beta2, eps
        self.m = [0.0] * len(params)
        self.v = [0.0] * len(params)
        self.t = 0
    def step(self):
        self.t += 1
        for i, p in enumerate(self.params):
            self.m[i] = self.beta1 * self.m[i] + (1 - self.beta1) * p.grad
            self.v[i] = self.beta2 * self.v[i] + (1 - self.beta2) * p.grad ** 2
            mhat = self.m[i] / (1 - self.beta1 ** self.t)
            vhat = self.v[i] / (1 - self.beta2 ** self.t)
            p.data -= self.lr * mhat / (vhat ** 0.5 + self.eps)
# ========== 6. Training Loop ==========
def train_gpt(text, max_steps=100):
    tokenizer = Tokenizer(text)
    data = tokenizer.encode(text)
    block_size = 8
    model = GPT(tokenizer.vocab_size, block_size)
    params = []
    for row in model.token_emb:
        for v in row:
            params.append(v)
    for row in model.pos_emb:
        for v in row:
            params.append(v)
    # collect Layer params too (weights of head neurons)
    for neuron in model.head.neurons:
        for w in neuron.w:
            params.append(w)
        params.append(neuron.b)
    opt = Adam(params, lr=0.001)
    for step in range(max_steps):
        # sample a chunk
        i = random.randint(0, len(data) - block_size - 1)
        x = [data[i:i+block_size]]
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