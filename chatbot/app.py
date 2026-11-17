# -*- coding: utf-8 -*-
"""Safeland Guide Streamlit 前端 — 15 入口侧栏切换"""

import os, sys
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rag import SafelandChatbot, MODES

# ====== 页面配置 ======
st.set_page_config(
    page_title="Safeland Guide · 海外生存指南",
    page_icon="🌍",
    layout="wide",
)

# 模式显示标签
MODE_LABELS = {
    k: f"🌍 {label}" for k, (label, _, _) in MODES.items()
}

# ====== 侧边栏 ======
with st.sidebar:
    st.title("🌍 Safeland Guide")
    st.caption("海外生存指南智能客服 · 15 入口隔离")

    st.subheader("选择入口")
    mode = st.radio(
        "你想解决哪方面的问题？",
        options=list(MODES.keys()),
        format_func=lambda k: f"{MODES[k][0]}",
        label_visibility="collapsed",
    )

    st.divider()
    st.subheader("⚙️ LLM 参数")
    llm_base = st.text_input(
        "Base URL",
        value=os.environ.get("LLM_BASE_URL", "https://api.siliconflow.cn/v1"),
    )
    llm_key = st.text_input(
        "API Key",
        value=os.environ.get("LLM_API_KEY", ""),
        type="password",
    )
    llm_model = st.text_input(
        "Model",
        value=os.environ.get("LLM_MODEL", "deepseek-ai/DeepSeek-V3"),
    )
    top_k = st.slider("Top-K 检索数量", min_value=3, max_value=10, value=5)
    web_on = st.toggle("上网兜底", value=True)

    os.environ["LLM_BASE_URL"] = llm_base
    os.environ["LLM_API_KEY"] = llm_key
    os.environ["LLM_MODEL"] = llm_model

    st.divider()
    st.caption(
        f"📚 {MODES[mode][0]} · "
        f"知识块数 {len(SafelandChatbot(mode=mode).chunks)}"
    )

# ====== Session State: 入口切换时重建 chatbot ======
if "_chatbot" not in st.session_state or st.session_state.get("_prev_mode") != mode:
    st.session_state._chatbot = SafelandChatbot(
        mode=mode, top_k=top_k, web_fallback=web_on
    )
    st.session_state.messages = []
    st.session_state._prev_mode = mode

# Top-K 或 Web 兜底设置变了也重建
cb = st.session_state._chatbot
if cb.top_k != top_k or cb.web_fallback != web_on:
    cb.top_k = top_k
    cb.web_fallback = web_on

# ====== 主区域 ======
label = MODES[mode][0]
st.title(f"🌍 Safeland Guide · {label}")
st.info(
    f"👋 你好！我是「{label}」海外生存专家。"
    f"当前只加载「{label}」知识库（{len(cb.chunks)} 个知识块），"
    f"没命中的问题会自动上网搜权威结果。"
)

# ====== 聊天历史 ======
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📎 参考来源"):
                for s in msg["sources"]:
                    if s.get("type") == "knowledge":
                        st.markdown(
                            f"- 📚 知识库 `{s['name']}` "
                            f"（相关度 {s.get('score', 0):.3f}）"
                        )
                    else:
                        url = s.get("url", "")
                        name = s.get("name", "")
                        st.markdown(f"- 🌐 [{name}]({url})" if url else f"- 🌐 {name}")

# ====== 输入 ======
if prompt := st.chat_input(f"问我任何关于「{label}」的问题..."):
    # 用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 检索知识库
    retrieved = cb.retrieve(prompt)
    top_score = retrieved[0][2] if retrieved else 0.0

    # 检索结果提示
    hints = []
    if top_score >= 0.25:
        hints.append(f"📚 知识库直接命中（相关度 {top_score:.3f}）")
    elif top_score >= 0.15:
        hints.append(f"🧩 知识库弱命中（相关度 {top_score:.3f}）— 补充上网搜索")
    else:
        hints.append(f"🌐 知识库未命中（top {top_score:.3f}）— 全面上网搜索")
    st.caption(" · ".join(hints))

    # 流式生成
    with st.chat_message("assistant"):
        stream = cb.stream_llm(prompt, retrieved, [])
        full_response = st.write_stream(iter(stream))

        # 收集 sources
        all_sources = []
        for _, src, score in retrieved:
            all_sources.append({"type": "knowledge", "name": src, "score": score})
        for s in stream.sources:
            if s not in all_sources:
                all_sources.append(s)

        if all_sources:
            with st.expander("📎 参考来源"):
                for s in all_sources:
                    if s.get("type") == "knowledge":
                        st.markdown(
                            f"- 📚 知识库 `{s['name']}` "
                            f"（相关度 {s.get('score', 0):.3f}）"
                        )
                    else:
                        url = s.get("url", "")
                        name = s.get("name", "")
                        st.markdown(
                            f"- 🌐 [{name}]({url})" if url else f"- 🌐 {name}"
                        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response,
        "sources": all_sources,
    })

# ====== 底部重置按钮 ======
st.caption("— 点击侧栏的入口即可切换主题（历史对话自动清空）—")
