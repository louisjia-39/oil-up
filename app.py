import time
import random
import streamlit as st

# ========= 可调参数（对应你 Tkinter 里那堆常量） =========
TIP_MAX_WIDTH = 420          # Web里是卡片宽度（像素）
TIP_INTERVAL_SEC = 6         # 每隔几秒生成一个tip
TIP_COUNT = 6                # 页面同时最多显示多少条

TIP_TEXT_LIST = [
    "坚持一下，你已经比昨天更强了。",
    "今天的你，值得一个小小的奖励。",
    "别焦虑，先做完这一小步。",
    "专注 10 分钟就好，先开始。",
    "喝口水，放松肩膀，再继续。",
    "你不需要完美，你只需要推进。",
]

TIP_BG_COLORS = ["#FCE4EC", "#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA"]


# ========= Streamlit 页面基础 =========
st.set_page_config(page_title="Tip Popups (Web)", layout="centered")

st.title("Web 版随机提示（Streamlit）")

# ========= Session State 初始化 =========
if "running" not in st.session_state:
    st.session_state.running = False

if "tips" not in st.session_state:
    # 每条 tip: {"text":..., "bg":..., "ts":...}
    st.session_state.tips = []

if "last_emit" not in st.session_state:
    st.session_state.last_emit = 0.0


# ========= 控制区 =========
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("▶️ 开始", use_container_width=True):
        st.session_state.running = True
        st.session_state.last_emit = 0.0
        st.rerun()

with col2:
    if st.button("⏸ 停止", use_container_width=True):
        st.session_state.running = False
        st.rerun()

with col3:
    TIP_INTERVAL_SEC = st.slider("提示间隔（秒）", 1, 30, TIP_INTERVAL_SEC, 1)

st.caption("说明：Web 端无法像 Tkinter 那样在屏幕任意位置弹窗；这里用页面右侧/中间的提示卡片模拟。")


# ========= 生成 tip 的逻辑（替代 Tkinter thread + sleep） =========
now = time.time()
if st.session_state.running:
    if st.session_state.last_emit == 0.0:
        st.session_state.last_emit = now

    if now - st.session_state.last_emit >= TIP_INTERVAL_SEC:
        new_tip = {
            "text": random.choice(TIP_TEXT_LIST),
            "bg": random.choice(TIP_BG_COLORS),
            "ts": now,
        }
        st.session_state.tips.insert(0, new_tip)
        st.session_state.tips = st.session_state.tips[:TIP_COUNT]
        st.session_state.last_emit = now


# ========= 展示 tip（替代 Toplevel 窗口） =========
st.subheader("提示区")

# 用 CSS 做成更像“弹窗卡片”的效果
st.markdown(
    """
    <style>
    .tip-card {
        border-radius: 14px;
        padding: 14px 16px;
        margin: 10px 0;
        box-shadow: 0 6px 18px rgba(0,0,0,0.10);
        border: 1px solid rgba(0,0,0,0.06);
        max-width: 420px;
    }
    .tip-text {
        font-size: 16px;
        line-height: 1.35;
    }
    .tip-meta {
        margin-top: 8px;
        font-size: 12px;
        opacity: 0.65;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.tips:
    st.info("还没有提示。点击“开始”。")

for t in st.session_state.tips:
    age = int(now - t["ts"])
    st.markdown(
        f"""
        <div class="tip-card" style="background:{t['bg']}">
            <div class="tip-text">{t['text']}</div>
            <div class="tip-meta">出现于 {age}s 前</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ========= 自动刷新（关键：让它“定时出现”） =========
# Streamlit 没有 Tkinter 的主循环，这里用 autorefresh 来让脚本周期性 rerun。
# 只在 running 时刷新，避免浪费资源。
if st.session_state.running:
    st.experimental_set_query_params(_=str(int(now)))  # 防止某些缓存行为
    st.rerun()
