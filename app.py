import streamlit as st
import json

st.set_page_config(layout="wide")

# 120 条不重复暖心文案（可继续加）
MESSAGES = [
    "今天辛苦啦，我抱抱你。",
    "你已经很努力了，真的。",
    "别逞强，累了就靠我一下。",
    "我一直都在你这边。",
    "你不用完美，你只要做你自己。",
    "你一出现，我就安心了。",
    "你值得被温柔对待。",
    "不开心也没关系，有我呢。",
    "你已经做得很好了，别苛责自己。",
    "你可以慢慢来，我陪你。",
    "我喜欢你认真生活的样子。",
    "你笑一下，我整天都甜。",
    "今天的你也很棒。",
    "我想把所有好东西都给你。",
    "你不是麻烦，你是我最在意的人。",
    "难过就告诉我，别一个人扛。",
    "你已经很强了，别再逼自己了。",
    "我会站在你身后，给你力量。",
    "你值得被坚定选择。",
    "你走慢一点也没关系，我等你。",
    "你累了就休息，我守着你。",
    "你一皱眉，我就想哄你。",
    "我愿意做你的避风港。",
    "你不需要证明什么，你本来就很好。",
    "今天也要记得喝水哦。",
    "别熬太晚，我会心疼。",
    "你值得拥有轻松的夜晚。",
    "你今天做的每一步都算数。",
    "你已经很棒了，别否定自己。",
    "你是我最想认真对待的人。",
    "你发的消息我都会认真看。",
    "你的小情绪我也想照顾。",
    "你可以脆弱，我会接住你。",
    "你不说我也懂一点点。",
    "你一出现，我就想笑。",
    "你的存在本身就很可爱。",
    "你别怕，有我在。",
    "我想替你分担一点点。",
    "今天也请对自己温柔一点。",
    "你已经做得比你想的更好。",
    "你是我心里最重要的那个人。",
    "如果你累了，我们就停一停。",
    "你不需要强撑，真的。",
    "你今天的努力我都看见了。",
    "你值得被拥抱，被理解，被偏爱。",
    "不管发生什么，我都会在。",
    "你可以依赖我，没关系的。",
    "你是我的小骄傲。",
    "你认真起来真的会发光。",
    "你别自责，你已经尽力了。",
    "我相信你，也心疼你。",
    "你一定要睡个好觉。",
    "别担心，事情会慢慢变好的。",
    "你今天一定也很辛苦吧。",
    "我想给你一个大大的拥抱。",
    "你是我最想保护的人。",
    "你不开心的时候，我更想靠近你。",
    "你不用说对不起，你没有错。",
    "你在我这里永远有台阶下。",
    "你可以哭，我不会嫌你脆弱。",
    "我喜欢你的全部，包括小缺点。",
    "你别急，我们慢慢来。",
    "你已经很勇敢了。",
    "你值得被认真爱。",
    "你的小小努力我都记得。",
    "你不是一个人。",
    "你今天也辛苦啦，抱一下。",
    "你是我生活里的甜。",
    "你别担心，我会陪你走。",
    "你可以把烦恼说给我听。",
    "你不用硬撑着笑。",
    "你今天的样子也很好看。",
    "你一认真，我就更喜欢你了。",
    "你是我最想见的人。",
    "你不用迎合任何人，做你自己就好。",
    "你已经很棒了，别对自己太狠。",
    "你值得拥有很多很多幸福。",
    "你是我最放心不下的人。",
    "你别怕麻烦我，我很愿意。",
    "你的情绪也很重要。",
    "你可以慢一点，但不要停。",
    "我会一直站在你身旁。",
    "你今天一定做得很不错。",
    "你别怕失败，我陪你一起。",
    "你值得被偏爱、被宠。",
    "你一累，我就想抱你。",
    "你是我心里的小星星。",
    "你今天也要好好吃饭。",
    "你别把难过都藏起来。",
    "你不说话我也会在。",
    "我愿意听你说很多很多。",
    "你比你想象中更厉害。",
    "你已经做得很好了，别急。",
    "你是我最重要的牵挂。",
    "你别委屈自己。",
    "你可以软弱，我会保护你。",
    "你别一个人胡思乱想。",
    "你今天的努力特别可爱。",
    "你值得被温柔接住。",
    "你可以把我当成安全感。",
    "你是我最想安慰的人。",
    "你别担心，我会一直在。",
    "你已经很优秀了。",
    "你别太累，我会心疼。",
    "你今天也要开心一点点。",
    "你是我最喜欢的例外。",
    "你一出现，我就觉得世界温柔了。",
    "你别急，我陪你慢慢走。",
    "你值得所有好事发生。",
    "你不需要独自坚强。",
    "你永远是我偏爱的人。",
    "你别怕，我在。",
    "你今天也很棒，我很骄傲。",
    "你值得被好好爱着。",
    "你已经足够好了。",
    "你是我最想拥抱的人。",
    "你别把自己逼太紧。",
    "你累的时候，我会更爱你。",
    "你是我最心软的牵挂。",
    "你今天也发光了。",
    "你别怕麻烦，我真的很愿意。",
    "你在我心里一直很重要。",
    "你不开心就找我。",
    "你已经很了不起了。",
    "你今天也要被我夸夸。",
    "你是我想认真走下去的人。",
    "你别怕慢，我陪你到最后。",
    "你值得被世界温柔以待。",
    "你不用讨好谁，你已经很好了。",
    "你是我最最最在意的人。",
    "你今天也辛苦了，晚安抱抱。",
]

INTERVAL_MS = 70
MAX_TOASTS = 100

# 页面上不显示任何东西：把 Streamlit 的默认 padding 也干掉
st.markdown(
    """
    <style>
      .block-container { padding-top: 0rem; padding-bottom: 0rem; }
      header { visibility: hidden; height: 0px; }
    </style>
    """,
    unsafe_allow_html=True,
)

msgs_json = json.dumps(MESSAGES, ensure_ascii=False)

# 关键：把 layer 挂到 parent document（Streamlit 主页面）里，这样就能覆盖全屏
html = f"""
<script>
(function() {{
  const MESSAGES = {msgs_json};
  const intervalMs = {INTERVAL_MS};
  const maxToasts = {MAX_TOASTS};

  function randInt(n) {{ return Math.floor(Math.random() * n); }}

  function randomPastelBg() {{
    const h = randInt(360);
    const s = 70 + randInt(11);
    const l = 88 + randInt(6);
    return `hsl(${{h}}, ${{s}}%, ${{l}}%)`;
  }}

  // 拿到父页面 document（最关键）
  const doc = window.parent.document;

  // 避免重复注入（Streamlit 会 rerun）
  if (doc.getElementById("warm-toast-layer")) return;

  // 注入样式
  const style = doc.createElement("style");
  style.innerHTML = `
    #warm-toast-layer {{
      position: fixed;
      inset: 0;
      z-index: 999999;
      pointer-events: none;
      overflow: hidden;
    }}
    .warm-toast {{
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
      animation: warmPopIn 140ms ease-out;
      transform-origin: center;
    }}
    .warm-meta {{
      margin-top: 6px;
      font-size: 11px;
      opacity: 0.55;
    }}
    @keyframes warmPopIn {{
      from {{ transform: scale(0.96); opacity: 0; }}
      to   {{ transform: scale(1.00); opacity: 1; }}
    }}
  `;
  doc.head.appendChild(style);

  // 注入全屏 layer
  const layer = doc.createElement("div");
  layer.id = "warm-toast-layer";
  doc.body.appendChild(layer);

  function clamp(v, lo, hi) {{ return Math.max(lo, Math.min(hi, v)); }}

  function createToast(text) {{
    const toast = doc.createElement("div");
    toast.className = "warm-toast";
    toast.style.background = randomPastelBg();

    const now = new Date();
    const hh = String(now.getHours()).padStart(2, "0");
    const mm = String(now.getMinutes()).padStart(2, "0");
    const ss = String(now.getSeconds()).padStart(2, "0");

    toast.innerHTML = `
      <div>${{text}}</div>
      <div class="warm-meta">${{hh}}:${{mm}}:${{ss}}</div>
    `;

    layer.appendChild(toast);

    // 随机全屏位置
    const vw = doc.documentElement.clientWidth;
    const vh = doc.documentElement.clientHeight;
    const rect = toast.getBoundingClientRect();
    const margin = 12;

    const maxX = vw - rect.width - margin;
    const maxY = vh - rect.height - margin;

    const x = clamp(margin + Math.random() * maxX, margin, Math.max(margin, maxX));
    const y = clamp(margin + Math.random() * maxY, margin, Math.max(margin, maxY));

    toast.style.left = `${{x}}px`;
    toast.style.top  = `${{y}}px`;

    // 超过 50 删除最早
    while (layer.children.length > maxToasts) {{
      layer.removeChild(layer.firstElementChild);
    }}
  }}

  // 开始狂弹
  setInterval(() => {{
    const msg = MESSAGES[randInt(MESSAGES.length)];
    createToast(msg);
  }}, intervalMs);

}})();
</script>
"""

# height=0 会不稳定，给一点高度，但页面上不会看到东西
st.components.v1.html(html, height=0)
"""

"""
