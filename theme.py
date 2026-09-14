"""Design tokens, CSS and Plotly defaults for the Pakistan–Japan travel dashboard.

The palette is inherited from the printed source catalogue and was validated for
colour-vision deficiency with the dataviz palette validator:
  #2F57A6, #C4492A, #00806A, #B08312, #7050CE
  -> lightness band PASS · chroma floor PASS · CVD separation PASS (worst adjacent
     dE 9.9) · normal-vision floor PASS (worst adjacent dE 19.3) · contrast PASS.
"""

# ---------------------------------------------------------------- ink & surface
PAPER = "#F5F6F9"
SURFACE = "#FFFFFF"
SURFACE_2 = "#EDEFF4"
INK = "#171C2B"
INK_2 = "#3D4558"
INK_3 = "#697288"
RULE = "#D9DDE6"
RULE_SOFT = "#E7EAF1"

# ------------------------------------------------------------- categorical slots
S1 = "#2F57A6"   # indigo   — Pakistan / primary series
S2 = "#C4492A"   # vermilion — the contrasting series / emphasis
S3 = "#00806A"   # teal
S4 = "#B08312"   # ochre
S5 = "#7050CE"   # violet
SERIES = [S1, S2, S3, S4, S5]

MUTED = "#858DA3"        # de-emphasis grey, 3.3:1 on white
MUTED_SOFT = "#C7CCD8"
GRID = "#E7EAF1"
AXIS = "#C6CCD8"

# soft tints for callout panels
TINT_S1 = "#EAEFF9"
TINT_S2 = "#FAEDE9"
TINT_S3 = "#E3F0ED"
TINT_S4 = "#F7F0DE"

FONT = "'Source Sans 3','Noto Sans JP',-apple-system,'Hiragino Sans','Yu Gothic',sans-serif"

PLOTLY_CONFIG = {"displayModeBar": False, "displaylogo": False, "responsive": True}


def fmt(n, dp=0):
    """1234567 -> '1,234,567'"""
    if n is None:
        return "—"
    return f"{n:,.{dp}f}"


def pct(x, dp=1):
    """0.6208 -> '62.1%'"""
    if x is None:
        return "—"
    return f"{x * 100:,.{dp}f}%"


def signed_pct(x, dp=1):
    if x is None:
        return "—"
    return f"{'+' if x >= 0 else '−'}{abs(x) * 100:,.{dp}f}%"


CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+JP:wght@400;500;700&display=swap');

:root {{
  --paper:{PAPER}; --surface:{SURFACE}; --surface-2:{SURFACE_2};
  --ink:{INK}; --ink-2:{INK_2}; --ink-3:{INK_3};
  --rule:{RULE}; --rule-soft:{RULE_SOFT};
  --indigo:{S1}; --shu:{S2}; --teal:{S3}; --ochre:{S4}; --violet:{S5};
  --display:"Zilla Slab",Georgia,"Times New Roman",serif;
  --body:"Source Sans 3","Noto Sans JP",-apple-system,BlinkMacSystemFont,"Hiragino Sans","Yu Gothic",sans-serif;
  --mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  --ja:"Noto Sans JP","Hiragino Sans","Hiragino Kaku Gothic ProN","Yu Gothic","Meiryo",sans-serif;
  --shadow:0 1px 2px rgba(23,28,43,.05), 0 10px 28px -20px rgba(23,28,43,.28);
}}

/* ------------------------------------------------------------ app furniture */
html, body, [class*="css"] {{ font-family: var(--body); }}
.stApp {{ background: var(--paper); color: var(--ink); }}
.block-container {{ padding-top: 2.2rem; padding-bottom: 4.5rem; max-width: 1340px;
  padding-left: 3.4rem; padding-right: 3.4rem; }}
#MainMenu, footer, header[data-testid="stHeader"] {{ visibility: hidden; height: 0; }}
[data-testid="stDecoration"] {{ display: none; }}
[data-testid="stToolbar"] {{ display: none; }}

/* -------------------------------------------------------------------- sidebar */
[data-testid="stSidebar"] {{ background: var(--surface); border-right: 1px solid var(--rule); }}
[data-testid="stSidebar"] > div:first-child {{ padding-top: 1.4rem; }}
.side-brand {{ padding: 0 4px 14px; border-bottom: 1px solid var(--rule-soft); margin-bottom: 14px; }}
.side-brand .kicker {{ font-family: var(--mono); font-size: 10px; letter-spacing: .16em;
  text-transform: uppercase; color: var(--shu); margin: 0 0 7px; }}
.side-brand h2 {{ font-family: var(--display); font-weight: 600; font-size: 19px; line-height: 1.15;
  margin: 0; color: var(--ink); letter-spacing: -.01em; }}
.side-brand .ja {{ font-family: var(--ja); font-size: 12px; color: var(--ink-3); margin: 5px 0 0; line-height:1.5; }}
[data-testid="stSidebar"] [role="radiogroup"] {{ gap: 1px; }}
[data-testid="stSidebar"] [role="radiogroup"] > label {{
  padding: 8px 10px; border-radius: 5px; margin: 0; transition: background .12s ease;
  border-left: 2px solid transparent; }}
[data-testid="stSidebar"] [role="radiogroup"] > label:hover {{ background: var(--surface-2); }}
[data-testid="stSidebar"] [role="radiogroup"] > label > div:first-child {{ display: none; }}
[data-testid="stSidebar"] [role="radiogroup"] > label p {{ font-size: 14px; color: var(--ink-2); line-height: 1.35; }}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {{
  background: {TINT_S1}; border-left: 2px solid var(--indigo); }}
[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) p {{ color: var(--indigo); font-weight: 600; }}
.side-note {{ font-family: var(--mono); font-size: 10.5px; line-height: 1.6; color: var(--ink-3);
  border-top: 1px solid var(--rule-soft); margin-top: 16px; padding-top: 12px; }}
.side-note b {{ color: var(--ink-2); font-weight: 500; }}

/* ------------------------------------------------------------------ masthead */
.mast {{ border-bottom: 1px solid var(--rule); padding-bottom: 20px; margin-bottom: 26px; }}
.mast .eyebrow {{ font-family: var(--mono); font-size: 11px; letter-spacing: .15em;
  text-transform: uppercase; color: var(--shu); margin: 0 0 10px; }}
.mast h1 {{ font-family: var(--display); font-weight: 600; font-size: clamp(28px,3.4vw,40px);
  line-height: 1.06; letter-spacing: -.018em; margin: 0; color: var(--ink); max-width: 26ch; }}
.mast .h1ja {{ font-family: var(--ja); font-weight: 500; font-size: 17px; color: var(--ink-2);
  margin: 9px 0 0; letter-spacing: .01em; }}
.mast .standfirst {{ margin: 14px 0 0; color: var(--ink-2); font-size: 16.5px; max-width: 74ch; line-height: 1.55; }}
.mast .standfirst-ja {{ font-family: var(--ja); margin: 6px 0 0; color: var(--ink-3); font-size: 13.5px;
  max-width: 70ch; line-height: 1.75; }}

/* ------------------------------------------------------------------- section */
.sect {{ margin: 34px 0 14px; }}
.sect .num {{ font-family: var(--mono); font-size: 11px; color: var(--shu); letter-spacing: .12em; }}
.sect h2 {{ font-family: var(--display); font-weight: 600; font-size: 23px; margin: 4px 0 0;
  letter-spacing: -.01em; color: var(--ink); }}
.sect .ja {{ font-family: var(--ja); font-size: 13.5px; color: var(--ink-3); margin: 4px 0 0; }}
.sect .lead {{ margin: 10px 0 0; color: var(--ink-2); font-size: 15.5px; max-width: 82ch; line-height: 1.55; }}
.sect .lead-ja {{ font-family: var(--ja); margin: 5px 0 0; color: var(--ink-3); font-size: 13px;
  max-width: 76ch; line-height: 1.7; }}

/* ------------------------------------------------------------------ KPI grid */
.kpis {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(152px, 1fr)); margin: 6px 0 4px; }}
.kpi {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 8px;
  padding: 15px 16px 14px; box-shadow: var(--shadow); }}
.kpi .v {{ font-family: var(--body); font-weight: 700; font-size: 31px; line-height: 1;
  letter-spacing: -.02em; color: var(--ink); }}
.kpi .v small {{ font-size: 17px; font-weight: 600; color: var(--ink-2); margin-left: 2px; letter-spacing: 0; }}
.kpi .l {{ font-size: 13px; color: var(--ink-2); margin: 9px 0 0; line-height: 1.35; font-weight: 600; }}
.kpi .lja {{ font-family: var(--ja); font-size: 11.5px; color: var(--ink-3); margin: 3px 0 0; line-height: 1.45; }}
.kpi .d {{ font-family: var(--mono); font-size: 11px; margin: 9px 0 0; padding-top: 8px;
  border-top: 1px solid var(--rule-soft); color: var(--ink-3); line-height: 1.5; }}
.kpi.accent {{ border-color: {S2}; }}
.kpi.accent .v {{ color: var(--shu); }}

/* --------------------------------------------------------------- chart cards */
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > div > .card-head) {{
  background: var(--surface); border: 1px solid var(--rule) !important; border-radius: 8px;
  box-shadow: var(--shadow); padding: 4px 6px 2px; }}
.card-head {{ padding: 10px 10px 2px; }}
.card-head h3 {{ font-family: var(--display); font-weight: 600; font-size: 17.5px; margin: 0;
  color: var(--ink); letter-spacing: -.005em; }}
.card-head .ja {{ font-family: var(--ja); font-size: 12px; color: var(--ink-3); margin: 3px 0 0; }}
.takeaway {{ font-size: 14px; color: var(--ink-2); margin: 2px 10px 0; line-height: 1.55; }}
.takeaway .ja {{ font-family: var(--ja); font-size: 12.5px; color: var(--ink-3); display: block; margin-top: 4px; line-height:1.7; }}
.src {{ font-family: var(--mono); font-size: 10px; color: var(--ink-3); margin: 10px 10px 6px;
  padding-top: 8px; border-top: 1px solid var(--rule-soft); line-height: 1.7; }}
.cards.two {{ grid-template-columns: repeat(auto-fit, minmax(398px, 1fr)); }}

/* ------------------------------------------------------------------- panels */
.panel {{ border-radius: 8px; padding: 15px 17px; margin: 14px 0; border: 1px solid var(--rule);
  background: var(--surface); }}
.panel .tag {{ font-family: var(--mono); font-size: 10px; letter-spacing: .14em; text-transform: uppercase;
  margin: 0 0 7px; font-weight: 500; }}
.panel p {{ margin: 0; font-size: 14.5px; color: var(--ink-2); line-height: 1.6; }}
.panel p + p {{ margin-top: 7px; }}
.panel .ja {{ font-family: var(--ja); font-size: 12.5px; color: var(--ink-3); line-height: 1.75; }}
.panel.ask {{ border-left: 3px solid var(--shu); background: {TINT_S2}; border-color: #EFD9D1; }}
.panel.ask .tag {{ color: var(--shu); }}
.panel.caveat {{ border-left: 3px solid var(--ochre); background: {TINT_S4}; border-color: #EADFC2; }}
.panel.caveat .tag {{ color: #8E6A17; }}
.panel.finding {{ border-left: 3px solid var(--indigo); background: {TINT_S1}; border-color: #D5DEF2; }}
.panel.finding .tag {{ color: var(--indigo); }}
.panel.flag {{ border-left: 3px solid var(--teal); background: {TINT_S3}; border-color: #CBE2DC; }}
.panel.flag .tag {{ color: var(--teal); }}

/* --------------------------------------------------------------- definitions */
.defs {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); margin: 8px 0 4px; }}
.def {{ background: var(--surface); border: 1px solid var(--rule); border-left: 3px solid var(--ochre);
  border-radius: 7px; padding: 13px 15px; }}
.def h4 {{ font-family: var(--display); font-size: 15px; font-weight: 600; margin: 0 0 3px; color: var(--ink); }}
.def .ja {{ font-family: var(--ja); font-size: 11.5px; color: var(--ink-3); margin: 0 0 7px; }}
.def p {{ font-size: 13px; color: var(--ink-2); margin: 0; line-height: 1.55; }}

/* -------------------------------------------------------------------- cards */
.cards {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); }}
.gcard {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 8px;
  padding: 15px 17px 14px; box-shadow: var(--shadow); }}
.gcard .n {{ font-family: var(--mono); font-size: 10.5px; color: var(--shu); letter-spacing: .1em; }}
.gcard h4 {{ font-family: var(--display); font-size: 16.5px; font-weight: 600; margin: 5px 0 0;
  color: var(--ink); line-height: 1.25; }}
.gcard .ja {{ font-family: var(--ja); font-size: 11.5px; color: var(--ink-3); margin: 4px 0 0; line-height: 1.6; }}
.gcard p.d {{ font-size: 13.5px; color: var(--ink-2); margin: 9px 0 0; line-height: 1.55; }}
.gcard .use {{ font-family: var(--mono); font-size: 10.5px; color: var(--ink-3); margin: 11px 0 0;
  padding-top: 9px; border-top: 1px solid var(--rule-soft); line-height: 1.6; }}
.gcard .use b {{ color: var(--shu); font-weight: 500; letter-spacing: .08em; }}
.gcard.corrected {{ border-color: #A9CFC5; background: linear-gradient(0deg,{TINT_S3},{TINT_S3}); }}
.gcard .rev {{ font-family: var(--mono); font-size: 9.5px; letter-spacing: .12em;
  text-transform: uppercase; color: var(--teal); background: var(--surface);
  border: 1px solid #A9CFC5; border-radius: 20px; padding: 2px 7px; display: inline-block;
  margin-left: 8px; vertical-align: 2px; }}

/* ------------------------------------------------------------ proposal cards */
.pcard {{ background: var(--surface); border: 1px solid var(--rule); border-radius: 8px;
  box-shadow: var(--shadow); padding: 18px 20px 16px; margin-bottom: 12px; }}
.pcard .row1 {{ display: flex; gap: 14px; align-items: baseline; flex-wrap: wrap; }}
.pcard .idx {{ font-family: var(--display); font-size: 26px; font-weight: 600; color: var(--shu); line-height: 1; }}
.pcard h4 {{ font-family: var(--display); font-size: 19px; font-weight: 600; margin: 0; color: var(--ink);
  line-height: 1.2; flex: 1 1 320px; }}
.pcard .ja {{ font-family: var(--ja); font-size: 12.5px; color: var(--ink-3); margin: 6px 0 0 40px; line-height: 1.6; }}
.pcard .body {{ margin-left: 40px; }}
.pcard .body p {{ font-size: 14.5px; color: var(--ink-2); margin: 10px 0 0; line-height: 1.6; }}
.pcard .ev {{ font-family: var(--mono); font-size: 11px; color: var(--ink-3); margin: 12px 0 0;
  padding-top: 10px; border-top: 1px solid var(--rule-soft); line-height: 1.7; }}
.pcard .ev b {{ color: var(--indigo); font-weight: 500; letter-spacing: .07em; }}
.pill {{ display: inline-block; font-family: var(--mono); font-size: 10px; letter-spacing: .1em;
  text-transform: uppercase; padding: 3px 8px; border-radius: 20px; background: var(--surface-2);
  color: var(--ink-3); border: 1px solid var(--rule); }}
.pill.hot {{ background: {TINT_S2}; color: var(--shu); border-color: #EFD9D1; }}

/* -------------------------------------------------------------------- misc */
.strip {{ display: grid; gap: 10px; grid-template-columns: repeat(auto-fit, minmax(188px, 1fr)); margin: 10px 0 0; }}
.fact {{ border: 1px solid var(--rule); border-radius: 7px; background: var(--surface); padding: 12px 14px; }}
.fact b {{ display: block; font-size: 21px; font-weight: 700; color: var(--ink); letter-spacing: -.01em; }}
.fact span {{ font-size: 12.5px; color: var(--ink-2); display: block; margin-top: 4px; line-height: 1.4; }}
.fact i {{ font-family: var(--ja); font-style: normal; font-size: 11px; color: var(--ink-3);
  display: block; margin-top: 2px; }}
.fact em {{ font-family: var(--mono); font-style: normal; font-size: 10.5px; color: var(--ink-3);
  display: block; margin-top: 7px; padding-top: 6px; border-top: 1px solid var(--rule-soft); }}
.rule {{ height: 1px; background: var(--rule-soft); margin: 26px 0 0; border: 0; }}

[data-testid="stExpander"] {{ border: 0 !important; box-shadow: none !important; background: transparent; }}
[data-testid="stExpander"] summary {{ font-family: var(--mono) !important; font-size: 11px !important;
  color: var(--ink-3) !important; letter-spacing: .06em; padding-left: 10px !important; }}
[data-testid="stExpander"] summary:hover {{ color: var(--indigo) !important; }}
[data-testid="stElementToolbar"] {{ display: none; }}
[data-testid="stWidgetLabel"] p {{ font-family: var(--mono) !important; font-size: 10.5px !important;
  letter-spacing: .08em; color: var(--ink-3) !important; text-transform: uppercase; }}
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {{ text-transform: none; }}
h1, h2, h3, h4, .mast .h1ja {{ word-break: keep-all; }}
.stDataFrame {{ border: 1px solid var(--rule-soft); border-radius: 6px; }}
</style>
"""
