# -*- coding: utf-8 -*-
"""
Safeland Guide Chatbot — RAG 引擎
15 入口隔离 + TF-IDF 检索 + DuckDuckGo 上网兜底 + LLM 流式调用
"""

import os, re, json, time
from glob import glob
from collections import defaultdict

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests


# ====== 17 入口定义 ======
# 定位: 毕业独自到陌生城市独立生活指南（不是海外！）
MODES = {
    "language":         ("语言沟通",    "knowledge/language",         "陌生城市语言沟通指南"),
    "climate":          ("气候适应",    "knowledge/climate",          "陌生城市气候适应指南"),
    "housing":          ("居住常识",    "knowledge/housing",          "陌生城市租房居住指南"),
    "food_shopping":    ("饮食与采购",  "knowledge/food_shopping",     "陌生城市饮食采购指南"),
    "transport":        ("交通与出行",  "knowledge/transport",        "陌生城市交通出行指南"),
    "medical":          ("医疗与健康",  "knowledge/medical",          "陌生城市医疗健康指南"),
    "admin_gov":        ("办事与政务",  "knowledge/admin_gov",       "陌生城市社保报税指南"),
    "social_culture":   ("社交与文化",  "knowledge/social_culture",   "陌生城市社交文化指南"),
    "emergency_safety": ("应急与安全",  "knowledge/emergency_safety", "陌生城市安全应急指南"),
    "job_survival":     ("求职与生存",  "knowledge/job_survival",     "陌生城市求职生存指南"),
    "finance":          ("财务管理",    "knowledge/finance",          "陌生城市财务管理指南"),
    "travel":           ("旅游",        "knowledge/travel",           "城市周边与国内外旅游"),
    "study_abroad":     ("学习提升",    "knowledge/study_abroad",     "在职学习考证指南"),
    "hobbies":          ("兴趣爱好",    "knowledge/hobbies",          "陌生城市兴趣爱好指南"),
    "relationships":    ("人际关系",    "knowledge/relationships",   "陌生城市人际关系指南"),
    "parenting":        ("育儿与家庭",  "knowledge/parenting",        "备孕到育儿全指南"),
    "pets":             ("宠物养护",    "knowledge/pets",             "养猫养狗入门指南"),
}

# 各入口的系统提示词
# 定位: 一个刚毕业的年轻人/刚结婚的新手爸妈，遇到了问题需要实用、可操作的建议
SYSTEM_PROMPTS = {
    "language": "你是独立生活语言沟通专家。回答围绕：陌生城市的方言/口音适应、打电话办业务的礼貌用语、跟房东/物业/快递员的沟通模板、求职面试表达。用中文，场景化举例。",
    "climate":  "你是陌生城市气候适应专家。回答围绕：不同城市的穿衣策略（南方/北方/高原）、皮肤过敏/干燥/保湿应对、极端天气（台风/暴雪/沙尘）防范、租房居家维护（发霉/漏水/虫害）。",
    "housing":  "你是陌生城市租房居住专家。回答围绕：找房渠道（贝壳/自如/豆瓣）、看房验房清单、租约陷阱（中介/二房东）、水电网开户、收纳整理、室友合租规则。给 step-by-step 模板。",
    "food_shopping": "你是陌生城市饮食采购专家。回答围绕：当地超市/菜市场/农贸市场对比、不会做饭的人怎么开始、美团/饿了么外卖避坑、省钱买菜技巧。",
    "transport": "你是陌生城市交通出行专家。回答围绕：地铁/公交卡怎么办公、网约车安全（滴滴/高德）、驾照迁回/摇号限行、长途汽车/高铁票怎么买不踩坑。",
    "medical":  "你是陌生城市医疗健康专家。回答围绕：社区医院 vs 三甲医院怎么选、医保怎么用、挂号流程、处方药怎么买、心理健康渠道。",
    "admin_gov": "你是陌生城市办事与报税专家。回答围绕：居住证/暂住证办理、社保/公积金开户与转移、身份证异地补办、银行开户、个税年度汇算、专项附加扣除、工商年报、自由职业者报税。",
    "social_culture": "你是陌生城市社交文化专家。回答围绕：本地人生活习惯差异（南/北/一线 vs 三四线）、饭局文化、职场新人注意事项、什么样的社交要远离。",
    "emergency_safety": "你是陌生城市安全应急专家。回答围绕：租房/出行/兼职的诈骗防范（二房东/刷单/传销）、自然灾害逃生、丢手机/钱包/身份证怎么处理、夜间出行安全。",
    "job_survival": "你是陌生城市求职生存专家。回答围绕：应届生简历模板、STAR 面试法、Boss 直聘/智联怎么选、试用期注意什么、劳动仲裁/欠薪怎么办。",
    "finance":  "你是独立生活财务管理专家。回答围绕：每月预算模板、学生优惠/折扣/Coupon、信用卡/花呗/借呗的坑、存钱和理财入门、记账 App 推荐。",
    "travel":   "你是旅行规划专家。回答围绕：城市周边游/跨省游/出国游、廉价航空行李额、民宿/酒店避坑、学生证景点优惠、行程预算、出国签证速查。",
    "study_abroad": "你是在职学习提升专家。回答围绕：考公/考研/考证怎么规划、在职和全职怎么选、网课 vs 面授、学习方法推荐（费曼/番茄工作法）。",
    "hobbies":  "你是独立生活兴趣引导专家。回答围绕：陌生城市怎么找到同好、健身房/球场/社团怎么加入、一个人也能做的爱好推荐、怎么开始第一个爱好。",
    "relationships": "你是陌生城市人际关系专家。回答围绕：怎么认识新朋友（同事/邻居/兴趣群）、室友边界感、相亲/交友 App 使用、人际断舍离（远离消耗你的人）。",
    "parenting": "你是新手爸妈育儿专家。回答围绕：备孕/怀孕/产检时间线、新生儿护理（喂奶/换尿布/抚触/小儿推拿）、辅食添加、疫苗接种、0-3 岁育儿、母婴开销预算。",
    "pets":     "你是新手铲屎官专家。回答围绕：第一次养猫/养狗准备什么、猫粮狗粮怎么选、每月预算、驱虫/疫苗/体检、常见疾病（猫耳螨/狗皮肤病）、能不能喂人类食物。",
}


class SafelandChatbot:
    """15 入口隔离智能客服"""

    def __init__(self, base_dir=".", mode="housing", top_k=5, web_fallback=True):
        assert mode in MODES, f"未知入口: {mode}"
        self.base_dir = base_dir
        self.mode = mode
        self.label, self.knowledge_dir, self.system_label = MODES[mode]
        self.top_k = top_k
        self.web_fallback = web_fallback
        self._load_knowledge()

    # ============ 知识库加载 ============
    def _load_knowledge(self):
        full_dir = os.path.join(self.base_dir, self.knowledge_dir)
        md_files = sorted(glob(os.path.join(full_dir, "*.md")))
        chunks, sources = [], []
        for path in md_files:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if not text:
                continue
            # 按 ## 或 \n\n 切分
            parts = re.split(r"\n##+\s|\n\n{2,}", text)
            for part in parts:
                part = part.strip()
                if len(part) > 80:
                    chunks.append(part)
                    sources.append(os.path.basename(path))
        self.chunks = chunks
        self.sources = sources
        self.vectorizer = TfidfVectorizer(
            analyzer="char", ngram_range=(2, 6), min_df=1, sublinear_tf=True
        )
        if chunks:
            self.matrix = self.vectorizer.fit_transform(chunks)
        else:
            self.matrix = None
        print(f"[{self.label}] 加载 {len(chunks)} 知识块 from {len(md_files)} 文件")

    # ============ 检索 ============
    def retrieve(self, query, k=None):
        k = k or self.top_k
        if self.matrix is None or not self.chunks:
            return []
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.matrix).flatten()
        top_idx = np.argsort(-sims)[:k]
        results = []
        for i in top_idx:
            if sims[i] > 0.01:
                results.append((self.chunks[i], self.sources[i], float(sims[i])))
        return results

    # ============ 上网兜底 ============
    def web_search(self, query, max_results=5):
        """DuckDuckGo 免费搜索（Instant Answer API + HTML 回退）"""
        results = []
        try:
            # 方式 1: Instant Answer API
            url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
            r = requests.get(url, params=params, timeout=8)
            if r.status_code == 200:
                data = r.json()
                if data.get("AbstractText"):
                    results.append({
                        "title": data.get("Heading", query),
                        "body": data["AbstractText"],
                        "url": data.get("AbstractURL", ""),
                    })
                for topic in data.get("RelatedTopics", [])[:max_results - 1]:
                    if "Text" in topic:
                        results.append({
                            "title": topic.get("FirstURL", ""),
                            "body": topic["Text"],
                            "url": topic.get("FirstURL", ""),
                        })
        except Exception:
            pass

        if not results:
            # 方式 2: DuckDuckGo HTML 页抓取
            try:
                url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                r = requests.get(url, headers=headers, timeout=8)
                if r.status_code == 200:
                    blocks = re.findall(
                        r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>.*?'
                        r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>',
                        r.text, re.DOTALL,
                    )
                    for href, title, snippet in blocks[:max_results]:
                        snippet = re.sub(r"<[^>]+>", "", snippet)
                        snippet = re.sub(r"\s+", " ", snippet).strip()
                        if snippet:
                            results.append({
                                "title": title.strip(),
                                "body": snippet,
                                "url": href,
                            })
            except Exception:
                pass
        return results

    # ============ LLM 流式调用 ============
    def stream_llm(self, query, knowledge_results, web_results, stream=True):
        """
        返回 _StreamResult 实例（可迭代 + 带属性）
        规则:
          - top score >= 0.25 → 只用知识库
          - 0.15 ~ 0.25       → 知识 + Web
          - < 0.15            → 只用 Web
        """
        top_score = knowledge_results[0][2] if knowledge_results else 0.0
        used_knowledge, used_web = True, False

        kb_text = ""
        if knowledge_results and top_score >= 0.15:
            kb_text = "\n\n".join(
                f"[来源: {src} (相关度 {score:.3f})]\n{chunk}"
                for chunk, src, score in knowledge_results
            )
        else:
            used_knowledge = False

        web_text = ""
        if self.web_fallback and (top_score < 0.25 or not knowledge_results):
            if not web_results:
                web_results = self.web_search(query)
            if web_results:
                used_web = True
                web_text = "\n\n".join(
                    f"[网页来源: {r.get('title', r.get('url', ''))}]\n{r.get('body', '')[:400]}"
                    for r in web_results[:3]
                )

        system_prompt = SYSTEM_PROMPTS.get(
            self.mode,
            f"你是海外生存指南专家（{self.system_label}）。用中文回答，场景化举例。"
        )

        user_parts = [f"【用户问题】{query}"]
        if kb_text:
            user_parts.append(f"【我的知识库】\n{kb_text}")
        if web_text:
            user_parts.append(f"【网络搜索结果】\n{web_text}")
        user_parts.append(
            "\n请综合以上内容，用中文给出实用、可操作的回答。"
            "如果提到具体数字/费用/时效，标注仅供参考以当地实际为准。"
        )
        user_prompt = "\n\n".join(user_parts)

        api_url = os.environ.get("LLM_BASE_URL", "https://api.siliconflow.cn/v1")
        api_key = os.environ.get("LLM_API_KEY", "")
        model = os.environ.get("LLM_MODEL", "deepseek-ai/DeepSeek-V3")

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": stream,
            "temperature": 0.7,
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(
                f"{api_url.rstrip('/')}/chat/completions",
                json=payload, headers=headers, stream=True, timeout=120,
            )
            resp.encoding = "utf-8"
        except Exception as e:
            # 本地 fallback
            return _StreamResult(None, [], top_score, used_knowledge, used_web,
                                 fallback_text=f"⚠️ LLM 调用失败: {e}\n"
                                               "请检查 API Key / 网络 / LLM_BASE_URL 设置")

        sources = []
        if knowledge_results:
            sources.extend([
                {"type": "knowledge", "name": f"{src}", "score": score}
                for _, src, score in knowledge_results[:5]
            ])
        if web_results:
            sources.extend([
                {"type": "web", "name": r.get("title", ""), "url": r.get("url", "")}
                for r in web_results[:3]
            ])

        return _StreamResult(resp, sources, top_score, used_knowledge, used_web)


class _StreamResult:
    """可迭代 + 带属性的流式结果容器"""
    def __init__(self, response, sources, top_score, used_knowledge, used_web,
                 fallback_text=None):
        self._resp = response
        self.sources = sources
        self.top_score = top_score
        self.used_knowledge = used_knowledge
        self.used_web = used_web
        self._fallback = fallback_text

    def __iter__(self):
        if self._fallback:
            yield self._fallback
            return
        try:
            for line in self._resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if line.startswith("data: "):
                    raw = line[6:]
                    if raw.strip() == "[DONE]":
                        break
                    try:
                        chunk = json.loads(raw)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except Exception:
                        continue
        except Exception as e:
            yield f"\n\n⚠️ 流式中断: {e}"


# ============ CLI 测试 ============
if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "housing"
    q = sys.argv[2] if len(sys.argv) > 2 else "租房怎么避免押金被坑？"
    cb = SafelandChatbot(mode=mode)
    results = cb.retrieve(q)
    print(f"\n[{cb.label}] 查询: {q}")
    print(f"知识库命中 {len(results)} 条 (top score={results[0][2] if results else 0:.3f})")
    for chunk, src, score in results[:3]:
        print(f"  → {src} (score={score:.3f}): {chunk[:80]}...")
