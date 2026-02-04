import streamlit as st
import json

st.set_page_config(page_title="Warm Random Popups", layout="wide")

st.title("随机位置暖心弹窗（Web 版）")
st.caption("打开页面自动开始：每 0.01 秒一个弹窗；最多保留 50 个，超过就删最早的。")

MESSAGES = [
    "看到你开心，我就觉得今天很值得。",
    "别硬撑啦，累了就靠我一下。",
    "你认真起来的样子真的很闪闪发光。",
    "不管你今天过得怎样，我都站在你这边。",
    "你已经做得很好了，真的。",
    "我喜欢你不是因为你完美，而是因为你是你。",
    "如果今天很难，那就把今天交给我抱抱。",
    "我想把所有温柔都留给你。",
    "你不用逞强，你可以依赖我。",
    "你一笑，我就想把全世界都给你。",
    "今天也要记得喝水、别熬太晚，好吗？",
    "你值得被认真对待，也值得被好好爱着。",
    "我会一直在，慢慢来就好。",
    "你不是麻烦，你是我最想照顾的人。",
    "你做不到也没关系，你已经很努力了。",
    "我想参与你的每一个明天。",
    "我不是来评判你的，我是来爱你的。",
    "如果你有一点点难过，分我一半。",
    "你已经很棒了，别对自己太苛刻。",
    "有我在，你可以放心做你自己。",
]

DEFAULT_INTERVAL_MS = 10
DEFAULT_MAX_TOASTS = 50

with st.expander("可选设置（卡就调大间隔）", expanded=False):
    interval_ms = st.number_input("弹窗间隔（毫秒）", 1, 2000, DEFAULT_INTERVAL_MS, 1)
    max_toasts = st.number_input("最大保留弹窗数", 1, 200, DEFAULT_MAX_TOASTS, 1)

msgs_json = json.dumps(MESSAGES, ensure_ascii=False)

# 注意：这里用 f-string，所以 JS 里的 ${...} 必须写成 ${{...}} 来转义给 Python
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue",
                 Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
  }}
  #layer {{
    position: fixed;
    inset: 0;
    z-index: 999999;
    pointer-events: none;
    overflow: hidden;
  }}
  .toast {{
    position: absolute;
    width: 320px;
    max-width: 70vw;
    border-radius: 14px;
    padding: 12px 14px;
    color: rgba(0,0,0,0.85);
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.06);
    backdrop-filter: blur(6px);
    line-height: 1.25;
    word-break: break-word;
    animation: popIn 140ms ease-out;
  }}
  .meta {{
    margin-top: 6px;
    font-size: 11px;
    opacity: 0.55;
  }}
  @keyframes popIn {{
    from {{ transform: scale(0.96); opacity: 0; }}
    to   {{ transform: scale(1.00); opacity: 1; }}
  }}
</style>
</head>
<body>
<div id="layer"></div>

<script>
  const MESSAGES = {msgs_json};
  const intervalMs = {int(interval_ms)};
  const maxToasts = {int(max_toasts)};

  function randInt(n) {{
    return Math.floor(Math.random() * n);
  }}

  function randomPastelBg() {{
    const h = randInt(360);
    const s = 70 + randInt(11);
    const l = 88 + randInt(6);
    // 关键：${{h}} 这种写法是为了让 Python f-string 输出 ${h} 给 JS
    return `hsl(${{h}}, ${{s}}%, ${{l}}%)`;
  }}

  function clamp(v, lo, hi) {{
    return Math.max(lo, Math.min(hi, v));
  }}

  function createToast(text) {{
    const layer = document.getElementById("layer");
    const toast = document.createElement("div");
    toast.className = "toast";
    toast.style.background = randomPastelBg();

    const now = new Date();
    const hh = String(now.getHours()).padStart(2, "0");
    const mm = String(now.getMinutes()).padStart(2, "0");
    const ss = String(now.getSeconds()).padStart(2, "0");

    toast.innerHTML = `
      <div>${{text}}</div>
      <div class="meta">${{hh}}:${{mm}}:${{ss}}</div>
    `;

    layer.appendChild(toast);

    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const rect = toast.getBoundingClientRect();

    const margin = 12;
    const maxX = vw - rect.width - margin;
    const maxY = vh - rect.height - margin;

    const x = clamp(margin + Math.random() * maxX, margin, Math.max(margin, maxX));
    const y = clamp(margin + Math.random() * maxY, margin, Math.max(margin, maxY));

    toast.style.left = `${{x}}px`;
    toast.style.top  = `${{y}}px`;

    while (layer.children.length > maxToasts) {{
      layer.removeChild(layer.firstElementChild);
    }}
  }}

  setInterval(() => {{
    const msg = MESSAGES[randInt(MESSAGES.length)];
    createToast(msg);
  }}, intervalMs);
</script>
</body>
</html>
"""

st.components.v1.html(html, height=120, scrolling=False)
