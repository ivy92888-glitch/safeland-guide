# -*- coding: utf-8 -*-
"""批量提取桌面知识库 docx 内容，按 15 个入口分类"""
import os, glob, re
from docx import Document

KBP = r"C:\Users\Ivy\Desktop\safeland-guide-异地生存指南知识库"
OUT = os.path.join(os.path.dirname(__file__), "knowledge")

# 15 个入口 + 中文名 + 目标关键词（用于自动分类）
MODES = {
    "language":        ("语言",       ["语言", "口语", "翻译", "英语", "词汇", "俚语"]),
    "climate":         ("气候适应",   ["气候", "适应", "皮肤", "过敏", "水土不服", "湿度", "干燥", "寒冷", "炎热"]),
    "housing":         ("居住常识",   ["房子", "租房", "租到", "WiFi", "wifi", "网络", "收纳", "家具", "居住"]),
    "food_shopping":   ("饮食与采购", ["饮食", "做饭", "菜谱", "菜", "粉类", "营养学", "低成本饮食"]),
    "transport":       ("交通与出行", ["交通", "地铁", "出行", "自驾"]),
    "medical":         ("医疗与健康", ["医疗", "健康", "推拿"]),
    "admin_gov":       ("办事与政务", ["税务", "退税"]),
    "social_culture":  ("社交与文化", ["社交", "文化"]),
    "emergency_safety":("应急与安全", ["安全", "隐私", "网络安全"]),
    "job_survival":    ("求职与生存", ["职业", "求职", "简历", "面试", "职场", "搞钱", "副业"]),
    "finance":         ("财务管理",   ["财务", "理财", "资产", "赚钱", "收入", "记账"]),
    "travel":          ("旅游",       ["签证", "旅游", "旅行"]),
    "study_abroad":    ("留学",       ["留学", "大学", "选课", "GPA", "论文"]),
    "hobbies":         ("兴趣",       ["兴趣", "手工", "陶艺", "运动", "健身", "爱好", "猫", "养狗"]),
    "relationships":   ("人际关系",   ["关系", "婚恋", "家庭", "人际"]),
}

# 直接排除的文件名关键词（完全不相关的）
HARD_SKIP = [
    "九寨", "北疆", "甘南", "昆大丽", "纯玩", "跟团", "旅游团", "邮轮",
    "报税", "税务年报", "年报", "企业所得", "所得税清算",
    "创业示例", "创业",
    "宝宝百问", "妈妈百问", "宝宝", "母婴", "早教", "小儿推拿", "护理师", "新生儿",
    "古代", "古人", "汉朝", "清朝", "古代骗术",
    "深圳46年",
    "Korea之行", "Pi.docx",
    "手工.docx",  # 注意单独手工可能和陶艺混，但手工内容太大先排除
    "陶艺.docx",
    "2026+九寨",
    "暑假安排计划表",
    "海景度假",
    "星漾南洋",
    "爱达邮轮",
    "高耗能工作",
    "宅家电影",
    "理财·经济",  # 这个太大了，用更小粒度的
    "收纳职业生涯规划",
    "07_深圳46年",
    "锦绣湖南",
    "（天水进出）",
    "【江南小资味】",
    "【烟花三月",
    "全国【伊起Happy",
    "2026+九寨慢时光",
    "【28人全季】",
    "【2+1纯玩】",
]


def extract_text(path):
    """从 docx 提取纯文本"""
    try:
        doc = Document(path)
        paras = [p.text.strip() for p in doc.paragraphs]
        tables = []
        for t in doc.tables:
            for row in t.rows:
                for cell in row.cells:
                    tables.append(cell.text.strip())
        all_text = "\n".join(p for p in paras + tables if p)
        return all_text
    except Exception as e:
        return ""


def classify(name, text):
    """根据文件名 + 内容关键词判定归属，返回入口 key 或 None"""
    combined = name + text[:2000]
    scores = {}
    for mode, (label, kws) in MODES.items():
        s = 0
        for kw in kws:
            if kw in combined:
                s += len(kw)  # 长关键词权重高
        if s > 0:
            scores[mode] = s
    if not scores:
        return None
    best = max(scores, key=scores.get)
    # 最低门槛
    if scores[best] < 2:
        return None
    return best


def chunk_text(text, max_chars=4000):
    """按段落切分，每块 ≤ max_chars"""
    lines = [l for l in text.split("\n") if l.strip()]
    chunks, cur = [], []
    cur_len = 0
    for line in lines:
        if cur_len + len(line) > max_chars and cur:
            chunks.append("\n".join(cur))
            cur = [line]
            cur_len = len(line)
        else:
            cur.append(line)
            cur_len += len(line)
    if cur:
        chunks.append("\n".join(cur))
    return chunks


def sanitize(text):
    """脱敏：去掉疑似个人信息"""
    text = re.sub(r"1[3-9]\d{9}", "[手机号]", text)
    text = re.sub(r"\d{17}[\dXx]", "[身份证号]", text)
    text = re.sub(r"[\w.-]+@[\w.-]+", "[邮箱]", text)
    text = re.sub(r"(?:微信|wechat|wx)[:\s]*[\w-]{6,}", "[微信号]", text, flags=re.I)
    # 具体人名/公司名过于困难，保守处理：常见的前公司标志
    bad = ["前XX", "XX公司", "XX科技", "XX集团"]
    for b in bad:
        text = text.replace(b, "[示例公司]")
    return text.strip()


# === 主流程 ===
files = sorted(glob.glob(os.path.join(KBP, "*.docx")) + glob.glob(os.path.join(KBP, "*.doc")))
print(f"桌面 docx 总数: {len(files)}")

# 输出目录
for mode in MODES:
    os.makedirs(os.path.join(OUT, mode), exist_ok=True)

stats = {m: 0 for m in MODES}
skipped = []

for f in files:
    name = os.path.basename(f)

    # 硬排除
    if any(kw in name for kw in HARD_SKIP):
        skipped.append((name, "HARD_SKIP"))
        continue

    text = extract_text(f)
    if not text or len(text) < 200:
        skipped.append((name, "EMPTY_OR_TOO_SHORT"))
        continue

    # 分类
    mode = classify(name, text)
    if mode is None:
        skipped.append((name, f"NO_MATCH({len(text)} chars)"))
        continue

    # 切分
    clean = sanitize(text)
    chunks = chunk_text(clean)
    label = MODES[mode][0]

    for i, chunk in enumerate(chunks):
        out_name = f"{mode}_{stats[mode]+1:02d}.md"
        out_path = os.path.join(OUT, mode, out_name)
        header = f"# {label} 知识库 · {os.path.splitext(name)[0]}\n\n"
        with open(out_path, "w", encoding="utf-8") as fw:
            fw.write(header + chunk)
        stats[mode] += 1

# === 同时用用户给的 15 大纲写一份总索引 ===
INDEX = os.path.join(OUT, "_INDEX.md")
with open(INDEX, "w", encoding="utf-8") as fw:
    fw.write("# Safeland Guide 异地生存指南知识库\n\n")
    fw.write("## 15 个入口\n\n")
    for mode, (label, _) in MODES.items():
        cnt = stats[mode]
        fw.write(f"- **{label}** (`{mode}`) — {cnt} chunks\n")
    fw.write(f"\n## 桌面文档匹配结果\n\n")
    fw.write(f"- 总 docx 数: {len(files)}\n")
    fw.write(f"- 已分类入库: {sum(stats.values())} chunks\n")
    fw.write(f"- 跳过（不相关/过短/无匹配）: {len(skipped)}\n")

print("\n=== 15 入口入库统计 ===")
for mode, (label, _) in MODES.items():
    print(f"  {stats[mode]:>4} chunks  {label}  ({mode})")
print(f"\n=== 跳过的文档（{len(skipped)} 个）===")
for name, reason in skipped[:30]:
    print(f"  [{reason}] {name}")
