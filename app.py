import streamlit as st
import json

st.set_page_config(page_title="Warm Popup Toaster", layout="wide")

st.title("自动暖心弹窗（Web Toast）")

st.caption("打开页面会自动开始：每 0.01 秒生成一个 toast；最多保留 50 条，超过就删最早的。")

# 你可以自己继续加更多“对女朋友”的暖心话
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

# 控制参数（按你要求：0.01 秒、最多 50 个）
INTERVAL_MS = 10          # 0.01s = 10ms
MAX_TOASTS = 50

# 可选：让你在网页上关掉（不影响默认自动弹）
with st.expander("可选设置（不改也能直接用）", expanded=False):
    st.write("如果你发现浏览器卡顿，可以把间隔调大一点，比如 50ms / 100ms。")
    interval_ms = st.number_input("弹窗间隔（毫秒）", min_value=1, max_value=2000, value=INTERVAL_MS, step=1)
    max_toasts = st.number_input("最大保留弹窗数", min_value=1, max_value=200, value=MAX_TOASTS, step=1)
else:
    interval_ms = INTERVAL_MS
    max_toasts = MAX_TOASTS

msgs_json = json.dumps(MESSAGES, ensure_ascii=False)

# 用组件注入前端：右下角 toast，随机内容，10ms 一个，超过 50 删除最早的
# 注意：部分浏览器/设备会对超高频 timer 做节流，这是正常现象（尤其 iOS/后台标签页）
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
  :root {{
    --toast-width: 360px;
  }}
  body {{
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue",
                 Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji";
  }}
  #toast-container {{
    position: fixed;
    right: 16px;
    bottom: 16px;
    width: var(--toast-width);
    display: flex;
    flex-direction: column-reverse; /* 新的在下面更像“冒出来” */
    gap: 10px;
    z-index: 999999;
    pointer-events: none;
  }}
  .toast {{
    pointer-events: none;
    border-radius: 14px;
    padding: 12px 14px;
    color: rgba(0,0,0,0.85);
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    border: 1px solid rgba(0,0,0,0.06);
    backdrop-filter: blur(6px);
    animation: popIn 160ms ease-out;
    line-height: 1.25;
    word-break: break-word;
  }}
  .meta {{
    margin-top: 6px;
    font-size: 11px;
    opacity: 0.55;
  }}
  @keyframes popIn {{
    from {{
      transform: translateY(10px);
      opacity: 0;
    }}
    to {{
      transform: translateY(0px);
      opacity: 1;
    }}
  }}
</style>
</head>
<body>
<div id="toast-container"></div>

<script>
  const MESSAGES = {msgs_json};

  const intervalMs = {int(interval_ms)};
  const maxToasts = {int(max_toasts)};

  function randInt(n) {{
    return Math.floor(Math.random() * n);
  }}

  function randomPastelBg() {{
    // 柔和背景：用 HSL 生成
    const h = randInt(360);
    const s = 70 + randInt(11);  // 70~80
    const l = 88 + randInt(6);   // 88~93
    return `hsl(${h}, ${{s}}%, ${{l}}%)`;
  }}

  function createToast(text) {{
    const container = document.getElementById("toast-container");
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

    container.appendChild(toast);

    // 超过 maxToasts 删除最早的
    while (container.children.length > maxToasts) {{
      container.removeChild(container.firstElementChild);
    }}
  }}

  // 自动开始：每 intervalMs 生成一个
  // 注意：在 iOS / 低性能设备上 10ms 会非常卡；浏览器也可能节流
  setInterval(() => {{
    const msg = MESSAGES[randInt(MESSAGES.length)];
    createToast(msg);
  }}, intervalMs);
</script>
</body>
</html>
"""

# 关键：高度设为 0 也能显示浮层（因为是 fixed），但有的环境会裁剪；给一点高度更稳
st.components.v1.html(html, height=120, scrolling=False)
