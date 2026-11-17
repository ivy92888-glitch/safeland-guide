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


# ====== 15 入口定义 ======
MODES = {
    "language":         ("语言",          "knowledge/language",         "海外生活语言指南"),
    "climate":          ("气候适应",      "knowledge/climate",          "海外气候适应指南"),
    "housing":          ("居住常识",      "knowledge/housing",          "海外租房居住指南"),
    "food_shopping":    ("饮食与采购",    "knowledge/food_shopping",    "海外饮食采购指南"),
    "transport":        ("交通与出行",    "knowledge/transport",        "海外交通出行指南"),
    "medical":          ("医疗与健康",    "knowledge/medical",          "海外医疗健康指南"),
    "admin_gov":        ("办事与政务",    "knowledge/admin_gov",       "海外证件税务指南"),
    "social_culture":   ("社交与文化",    "knowledge/social_culture",   "海外社交文化指南"),
    "emergency_safety": ("应急与安全",    "knowledge/emergency_safety", "海外安全应急指南"),
    "job_survival":     ("求职与生存",    "knowledge/job_survival",     "海外求职生存指南"),
    "finance":          ("财务管理",      "knowledge/finance",          "海外财务管理指南"),
    "travel":           ("旅游",          "knowledge/travel",           "海外旅游指南"),
    "study_abroad":     ("留学",          "knowledge/study_abroad",     "海外留学指南"),
    "hobbies":          ("兴趣",          "knowledge/hobbies",          "海外兴趣爱好指南"),
    "relationships":    ("人际关系",      "knowledge/relationships",   "海外人际关系指南"),
}

# 各入口的系统提示词（告诉 LLM 自己是什么专家）
SYSTEM_PROMPTS = {
    "language": "你是海外语言交际专家。回答围绕：日常交际用语、办事词汇、职场术语、俚语禁忌、翻译工具推荐。全部用中文回答，场景化举例。",
    "climate":  "你是海外气候适应专家。回答围绕：不同气候带的穿衣策略、皮肤水土不服应对、极端天气防范、居家维护。分国家/气候带说。",
    "housing":  "你是海外租房居住专家。回答围绕：找房渠道、看房验房、租约陷阱、水电网开户、室友合租。给 step-by-step 模板。",
    "food_shopping": "你是海外饮食采购专家。回答围绕：当地超市菜市场区别、中国食材平替、留学生快手菜谱、外卖文化（小费）。",
    "transport": "你是海外交通出行专家。回答围绕：公共交通卡办理、打车安全、驾照转换、自驾车险、长途廉价航空避坑。",
    "medical":  "你是海外医疗健康专家。回答围绕：GP/ER 区分、医保报销、处方药流程、急救常识、心理健康资源。",
    "admin_gov": "你是海外政务办事专家。回答围绕：证件/签证/税号办理、银行开户信用记录、报税退税、小额法庭。",
    "social_culture": "你是海外社交文化专家。回答围绕：见面礼/排队/小费、节庆禁忌、人际边界（什么不能聊）、职场社交。",
    "emergency_safety": "你是海外安全应急专家。回答围绕：危险街区识别、自然灾害逃生、诈骗防范（杀猪盘/换汇诈骗）、突发意外处理。",
    "job_survival": "你是海外求职生存专家。回答围绕：一页纸简历模板、STAR 面试法、LinkedIn/Indeed 找工作、最低工资/解雇赔偿。",
    "finance":  "你是海外个人财务专家。回答围绕：预算模板、学生折扣/Coupon/返现卡、Checking vs Savings、退税。",
    "travel":   "你是海外旅行规划专家。回答围绕：签证速查、廉价航空行李额、Airbnb/酒店避坑、学生证景点优惠。",
    "study_abroad": "你是海外留学专家。回答围绕：选课 GPA、学术诚信（Turnitin）、校园资源（写作中心）、OPT/工签。",
    "hobbies":  "你是海外生活方式专家。回答围绕：健身房/户外运动、社团/兴趣班、志愿者活动、语言交换。",
    "relationships": "你是海外人际关系专家。回答围绕：老乡圈/互助群、室友边界、跨国约会 App、人际断舍离。",
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
