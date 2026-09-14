"""Small bilingual render helpers. Every component takes English and Japanese."""

import inspect

import streamlit as st

from theme import PLOTLY_CONFIG

# Streamlit renamed use_container_width -> width="stretch" (deprecated after 2025-12-31).
# Detect once so the app runs on either side of that change.
_WIDTH_KW = ({"width": "stretch"}
             if "width" in inspect.signature(st.dataframe).parameters
             else {"use_container_width": True})


def stretch(**extra):
    return {**_WIDTH_KW, **extra}


def H(html: str):
    """Render a compact HTML block. Keep the string on one line: blank lines
    inside make Streamlit's markdown parser treat it as a code block."""
    st.markdown(html, unsafe_allow_html=True)


def masthead(eyebrow, title_en, title_ja, stand_en=None, stand_ja=None):
    parts = [
        '<div class="mast">',
        f'<p class="eyebrow">{eyebrow}</p>',
        f"<h1>{title_en}</h1>",
        f'<p class="h1ja">{title_ja}</p>',
    ]
    if stand_en:
        parts.append(f'<p class="standfirst">{stand_en}</p>')
    if stand_ja:
        parts.append(f'<p class="standfirst-ja">{stand_ja}</p>')
    parts.append("</div>")
    H("".join(parts))


def section(num, en, ja, lead_en=None, lead_ja=None):
    parts = [
        '<div class="sect">',
        f'<p class="num">{num}</p>',
        f"<h2>{en}</h2>",
        f'<p class="ja">{ja}</p>',
    ]
    if lead_en:
        parts.append(f'<p class="lead">{lead_en}</p>')
    if lead_ja:
        parts.append(f'<p class="lead-ja">{lead_ja}</p>')
    parts.append("</div>")
    H("".join(parts))


def kpis(items):
    """items: list of dicts with value, unit(optional), en, ja, foot(optional),
    accent(optional bool)."""
    cells = []
    for k in items:
        unit = f"<small>{k['unit']}</small>" if k.get("unit") else ""
        foot = f'<p class="d">{k["foot"]}</p>' if k.get("foot") else ""
        cls = "kpi accent" if k.get("accent") else "kpi"
        cells.append(
            f'<div class="{cls}"><div class="v">{k["value"]}{unit}</div>'
            f'<p class="l">{k["en"]}</p><p class="lja">{k["ja"]}</p>{foot}</div>'
        )
    H(f'<div class="kpis">{"".join(cells)}</div>')


def panel(kind, tag, en, ja):
    """kind: ask | caveat | finding | flag"""
    H(
        f'<div class="panel {kind}"><p class="tag">{tag}</p>'
        f"<p>{en}</p><p class=\"ja\">{ja}</p></div>"
    )


def facts(items):
    """items: list of (value, en, ja, foot)"""
    cells = [
        f'<div class="fact"><b>{v}</b><span>{en}</span><i>{ja}</i><em>{foot}</em></div>'
        for v, en, ja, foot in items
    ]
    H(f'<div class="strip">{"".join(cells)}</div>')


def chart_card(title_en, title_ja, fig, table=None, take_en=None, take_ja=None, src=None):
    with st.container(border=True):
        H(f'<div class="card-head"><h3>{title_en}</h3><p class="ja">{title_ja}</p></div>')
        st.plotly_chart(fig, config=PLOTLY_CONFIG, **stretch())
        if take_en:
            H(f'<p class="takeaway">{take_en}<span class="ja">{take_ja or ""}</span></p>')
        if src:
            H(f'<p class="src">{src}</p>')
        if table is not None:
            with st.expander("Data table  ·  データ表"):
                st.dataframe(table, hide_index=True, **stretch())


def rule():
    H('<hr class="rule">')
