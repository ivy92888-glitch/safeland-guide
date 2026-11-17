# 应急与安全 · 第8册_逻辑统计数学工具箱技术编程实战

8.1 AI 蒸馏：给 AI 编程立规矩（6 万星项目）
第 9 章  Python 常用库（pandas / numpy / matplotlib）
Steve Brunton（华盛顿大学教授）610 分钟数学基础课专为工程师讲机器学习核心数学：SVD、特征值、线性代数。不用严格证明，讲直觉、讲应用、讲代码。
第 10 章  2026 AI 时代自学编程的路径
10.1 RAG 从 0 到实战
10.2 自学三原则
附录 A  来源对照表
附录 B  去重说明
✅ 两本手册**完全零重叠**，直接合并为一本「硬技能工具箱」。
📌  标准经济学假设人理性，但真实的人被参照点、损失厌恶、当下享乐左右。
📌  统计学八步法骨架（记住这条链）：描述数据 → 建立概率模型 → 抽样分布 → 区间估计 → 假设检验
📌  AI 数学四块内容与顺序：线性代数（漂浮）→ 微积分（划水）→ 概率（换气）→ 统计（看方向）
AI 数学支柱
对应概念
这门课讲什么
在 AI 里用来干嘛
线性代数
向量 / 矩阵 / SVD / 特征值
矩阵就是数据表、特征分解就是拆数据、SVD 就是数学滤镜
LLM 注意力机制、CNN 卷积、推荐系统矩阵分解
微积分
导数 / 梯度 / 链式法则
导数就是变化率、梯度下降就是下山找最低点
训练所有神经网络的核心算法
概率统计
分布 / 期望 / 贝叶斯
数据长什么样、怎么看模型靠不靠谱
朴素贝叶斯分类器、HMM、评估指标
优化理论
梯度下降 / SGD / Adam
从爬山到梯度下降的进化史
所有大模型的训练优化器
📌  以下内容完全来自「01_技术与编程实战手册」，与前三编零重叠。
📌  本章速览
• HTTP = 奶茶店点餐流程：客户端（你）→ 服务员（HTTP）→ 后厨（服务器）
• localhost 是你自己电脑的别名，别人访问你得用 IP + 端口
• 域名 → DNS → IP → 端口 → 服务，五步找到网页
• HTTPS 加了 TLS 加密，像密封信封送外卖
• CORS 跨域 = 奶茶店只接待指定外卖平台
奶茶店角色
Web 概念
一句话解释
菜单 / 扫码点单
前端（Frontend）
你直接看得到、能交互的界面
后厨
后端（Backend）
处理逻辑、存数据、调 API 的看不见的部分
传餐服务员
HTTP 协议
规定了「请求 → 响应」的交流格式
奶茶店地址
URL / 域名
用户能记的名字，比如 milktea.com
店的 GPS 坐标
IP 地址
电脑能读的数字地址，比如 112.66.78.9
DNS 指路牌
域名系统（DNS）
把域名翻译成 IP 地址
奶茶制作间门牌号
端口（Port）
一台服务器跑多个服务，端口区分
安全组门禁
防火墙
限制哪些 IP 能访问哪些端口
保温套 + 密封条
HTTPS / TLS
加密传输，防窃听防篡改
💡  打个比方：你扫码点单（HTTP GET 请求）→ 菜单转到后厨（服务器收到请求）→ 后厨做奶茶（后端处理）→ 奶茶包好给服务员（HTTP 响应）→ 服务员端给你（浏览器渲染页面）。
HTTP 方法
奶茶店对应
前端含义
后端操作
GET
看菜单
获取数据 / 查页面
读数据库
POST
下单
提交表单 / 发请求
创建资源 / 写数据库
PUT
换一整杯
全量更新数据
覆盖整个对象
PATCH
改配料（少糖多冰）
局部更新
只改几个字段
DELETE
撤单
删除数据
删数据库记录
⚠️  踩坑提示：90% 的新人分不清 PUT 和 PATCH——PUT 是「整杯换掉」（你给完整对象），PATCH 是「只改配料」（你只给要改的字段）。用错不报错，但以后重构会炸。
🚨  常见坑：改了 CSS 文件刷新没变化？大概率是缓存没清。Ctrl + F5 强制刷新，或加版本号参数 main.css?v=2 绕过缓存。
📌  小白学编程第一步：不要装 IDE 全家桶（PyCharm / WebStorm / IntelliJ），一个 VSCode 搞定所有语言。必装 5 个插件。
插件名
干什么的
装了以后有什么感觉
Python (Microsoft)
Python 语法高亮、运行按钮、调试
写完按 F5 直接跑
Prettier
一键格式化代码
乱糟糟代码瞬间整齐
Remote SSH
远程连服务器写代码
本地电脑变服务器终端
Markdown PDF
把 .md 转 .pdf
写文档一键导出
Error Lens
把错误红线直接显示在行尾
不用 hover 看小窗口了
💡  打个比方：按数据模型分包 = 把奶茶店按「杯子 / 吸管 / 珍珠」分类放，加个「外带」功能你要去杯子区找杯子、吸管区找吸管、珍珠区找珍珠，来回跑。按业务用例分包 = 按「堂食 / 外带 / 外卖」分柜台，外带柜台自己有杯子有吸管有珍珠，一站搞定。
层级
放什么
替换成本
奶茶店类比
内层：业务逻辑
核心规则、用例编排
几乎不变
奶茶怎么调、配方是什么
中层：数据接口
DAO、Repository、DTO
半年可能变
收银机 / 订单管理系统
外层：基础设施
Web 框架、数据库、第三方 API
随时可以换
外卖平台、支付渠道
⚠️  踩坑：新人容易犯的错——在业务逻辑层直接写 SQL。正确做法是业务逻辑只调用接口，SQL 写在数据层。换 MySQL 成 MongoDB 时只改数据层，业务逻辑不动。
📌  Karpathy = OpenAI 联合创始人、前 Tesla AI 总监、AI 教育布道者。2026 年 2 月发布 microGPT：200 行纯 Python、零依赖、完整 GPT 实现。
模块
做什么
行数（约）
对应 GPT 组件
Tokenizer
把文本分成 token 序列
~20
BPE 分词
Autograd 引擎
手动实现反向传播
~50
PyTorch / TF 的核心
Transformer
GELU 激活 + 注意力 + 前馈层
~70
GPT-2 同款架构
Adam 优化器
自适应学习率训练
~20
GPT 训练标配
训练循环
数据 → 前向 → 反向 → 更新
~20
标准训练流程
推理循环
给定前缀逐个生成
~20
GPT 最核心的「续写」能力
阶段
做什么
输入 → 输出
奶茶店类比
1. Tokenizer
把自然语言切成 token
「你好啊」→ [231, 456, 789]
把整杯奶茶分装成小份珍珠
2. Pretrain
海量文本预训练
整个互联网 → 会续写的模型
奶茶店开 1 年学所有配方
3. SFT
监督微调
高质量对话 → 能按指令执行
专门学「加冰少糖」这种定制
4. RLHF
人类反馈强化学习
人类偏好 → 更符合人类价值观
学哪些是好评哪些是差评
5. Inference
上线推理
用户提问 → 模型回答
营业接单
6. Web UI
用户界面
浏览器 → 模型 → 浏览器
扫码点单界面
"""
microGPT: 200-line pure Python GPT implementation
Andrej Karpathy, Feb 2026. Zero dependencies.
Run: python microgpt.py
"""
import math, random
# ========== 1. Tokenizer (BPE-lite) ==========
class Tokenizer:
    def __init__(self, text):
        self.chars = sorted(list(set(text)))
        self.vocab_size = len(self.chars)
        self.stoi = {c: i for i, c in enumerate(self.chars)}
        self.itos = {i: c for i, c in enumerate(self.chars)}
    def encode(self, s):
        return [self.stoi[c] for c in s]
    def decode(self, l):
        return ''.join(self.itos[i] for i in l)
# ========== 2. Tiny Autograd Engine ==========
class Value:
    def __init__(self, data, _prev=(), _op=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None