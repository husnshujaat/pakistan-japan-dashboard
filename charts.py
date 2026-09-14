"""Figure builders. One chart per function, no dual axes anywhere."""

import plotly.graph_objects as go

from data import DATA
from theme import (
    AXIS, FONT, GRID, INK, INK_2, INK_3, MUTED, MUTED_SOFT, RULE,
    S1, S2, S3, S4, S5, SURFACE, fmt, pct,
)

CORNER = 3  # rounded data-ends


def base(height=360, margin=None, legend=True):
    fig = go.Figure()
    fig.update_layout(
        height=height,
        margin=margin or dict(l=6, r=18, t=34 if legend else 10, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=13, color=INK_2),
        hoverlabel=dict(
            bgcolor=SURFACE, bordercolor=RULE,
            font=dict(family=FONT, size=13, color=INK),
        ),
        showlegend=legend,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.03, xanchor="left", x=0,
            font=dict(size=12.5, color=INK_2), bgcolor="rgba(0,0,0,0)",
            itemsizing="constant", itemwidth=30, tracegroupgap=6,
        ),
        xaxis=dict(
            showgrid=False, zeroline=False, showline=True, linecolor=AXIS, linewidth=1,
            ticks="outside", tickcolor=AXIS, ticklen=5,
            tickfont=dict(size=12, color=INK_3),
        ),
        yaxis=dict(
            gridcolor=GRID, gridwidth=1, zeroline=False, showline=False,
            tickfont=dict(size=12, color=INK_3),
        ),
        bargap=0.34,
        bargroupgap=0.12,
        dragmode=False,
    )
    return fig


def _bar(**kw):
    kw.setdefault("marker_line", dict(color=SURFACE, width=1.5))
    kw.setdefault("marker_cornerradius", CORNER)
    return go.Bar(**kw)


# ------------------------------------------------------------------ 1 · purpose
PURPOSE = [
    ("tourism", "Tourism", "観光", S1),
    ("business", "Business", "商用", S2),
    ("vfr", "Visiting relatives", "親族訪問", S3),
    ("other", "Other / cultural", "その他・文化", MUTED),
]


def purpose_stack():
    rows = DATA["arrivals"]
    years = [str(r["year"]) for r in rows]
    peak = max(r["total"] for r in rows)
    fig = base(height=380)
    for key, en, ja, colour in PURPOSE:
        vals = [r[key] + (r["cultural"] if key == "other" else 0) for r in rows]
        text = [fmt(v) if v / peak > 0.055 else "" for v in vals]
        fig.add_trace(_bar(
            x=years, y=vals, name=f"{en} · {ja}", marker_color=colour,
            text=text, textposition="inside", insidetextanchor="middle", textangle=0,
            textfont=dict(color="#FFFFFF", size=12.5, family=FONT),
            hovertemplate=f"<b>{en} · {ja}</b><br>%{{x}}: %{{y:,}} entries<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack",
        yaxis=dict(title=None, tickformat=",", gridcolor=GRID, zeroline=False,
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showgrid=False, showline=True, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(size=12.5, color=INK_3)),
    )
    return fig


def mix_comparison():
    rows = DATA["mix"]
    labels_ja = {"Tourism": "観光", "Business": "商用", "Visiting relatives": "親族訪問"}
    cats = [f"{r['purpose']}<br><span style='font-size:11px;color:#697288'>"
            f"{labels_ja[r['purpose']]}</span>" for r in rows][::-1]
    pk = [r["pk"] * 100 for r in rows][::-1]
    jp = [r["jp"] * 100 for r in rows][::-1]
    ratio = [r["ratio"] for r in rows][::-1]

    fig = base(height=320, margin=dict(l=6, r=120, t=34, b=8))
    fig.add_trace(_bar(
        y=cats, x=jp, orientation="h", name="Japan, all nationalities · 日本全体", legendrank=2,
        marker_color=MUTED_SOFT, marker_line=dict(color=SURFACE, width=1.5),
        text=[f"{v:.1f}%" for v in jp], textposition="outside",
        textfont=dict(color=INK_3, size=12),
        hovertemplate="Japan worldwide<br>%{x:.1f}% of short-stay entries<extra></extra>",
    ))
    fig.add_trace(_bar(
        y=cats, x=pk, orientation="h", name="Pakistan · パキスタン", legendrank=1,
        marker_color=S1, text=[f"<b>{v:.1f}%</b>" for v in pk], textposition="outside",
        textfont=dict(color=S1, size=13),
        hovertemplate="Pakistan<br>%{x:.1f}% of short-stay entries<extra></extra>",
    ))
    for i, r in enumerate(ratio):
        fig.add_annotation(
            x=1.0, xref="paper", y=i, yref="y", xanchor="left", xshift=8,
            text=(f"<b>×{r:.1f}</b>" if r > 1 else f"×{r:.2f}"),
            showarrow=False, align="left",
            font=dict(size=15, color=S2 if r > 1 else INK_3, family=FONT),
        )
    fig.add_annotation(
        x=1.0, xref="paper", y=2.55, yref="y", xanchor="left", xshift=8,
        text="Pakistan ÷ Japan<br><span style='font-size:10px'>対日本全体比</span>",
        showarrow=False, align="left", font=dict(size=10.5, color=INK_3, family=FONT),
    )
    fig.update_layout(
        barmode="group", xaxis=dict(ticksuffix="%", range=[0, 108], showgrid=False,
                                    showline=True, linecolor=AXIS, ticks="outside",
                                    tickcolor=AXIS, tickfont=dict(size=12, color=INK_3)),
        yaxis=dict(showgrid=False, tickfont=dict(size=13, color=INK_2)),
        bargap=0.42, bargroupgap=0.08, legend_traceorder="normal",
    )
    return fig


# ---------------------------------------------------------------- 2 · community
def residents_line():
    rows = DATA["residents_ts"]
    x = [r["asat"] for r in rows]
    y = [r["pk"] for r in rows]
    fig = base(height=330, legend=False, margin=dict(l=6, r=58, t=16, b=8))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", line=dict(color=S1, width=2.2, shape="linear"),
        marker=dict(size=9, color=S1, line=dict(color=SURFACE, width=2)),
        fill="tozeroy", fillcolor="rgba(47,87,166,0.07)",
        hovertemplate="%{x}<br><b>%{y:,}</b> residents<extra></extra>",
    ))
    fig.add_annotation(
        x=x[-1], y=y[-1], text=f"<b>{fmt(y[-1])}</b>", showarrow=False,
        xanchor="left", xshift=10, font=dict(size=15, color=S1, family=FONT),
    )
    fig.add_annotation(
        x=x[0], y=y[0], text=fmt(y[0]), showarrow=False, yanchor="top", yshift=-10,
        font=dict(size=12.5, color=INK_3, family=FONT),
    )
    fig.update_layout(
        yaxis=dict(range=[0, 40000], tickformat=",", gridcolor=GRID,
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, tickfont=dict(size=12, color=INK_3)),
    )
    return fig


CAT_COLOUR = {"Family": S1, "Work": S3, "Settlement": S2, "Study": S4, "Other": MUTED}
CAT_JA = {"Family": "家族", "Work": "就労", "Settlement": "定住・永住",
          "Study": "留学", "Other": "その他"}
CAT_ORDER = ["Family", "Settlement", "Work", "Study", "Other"]


def status_category_bar():
    cats = {c["cat"]: c for c in DATA["res_cats"] if c["cat"] in CAT_ORDER}
    fig = base(height=178, margin=dict(l=6, r=6, t=34, b=6))
    for name in CAT_ORDER:
        c = cats[name]
        share = c["share"] * 100
        fig.add_trace(_bar(
            x=[share], y=[""], orientation="h",
            name=f"{name} · {CAT_JA[name]}", marker_color=CAT_COLOUR[name],
            text=[f"<b>{share:.1f}%</b><br>{fmt(c['n'])}" if share > 6 else ""],
            textposition="inside", insidetextanchor="middle", textangle=0,
            textfont=dict(color="#FFFFFF", size=13, family=FONT),
            hovertemplate=f"<b>{name} · {CAT_JA[name]}</b><br>"
                          f"{fmt(c['n'])} residents · {share:.1f}%<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False),
        bargap=0.05,
    )
    return fig


SHORT_EN = {
    "Engineer / Specialist in Humanities / International Services":
        "Engineer · Humanities · Int'l Services",
    "Spouse or Child of Permanent Resident": "Spouse / child of permanent resident",
    "Spouse or Child of Japanese National": "Spouse / child of Japanese national",
    "Technical Intern Training (all)": "Technical Intern Training",
}


def status_detail_bar(top=11):
    rows = sorted(DATA["res_status"], key=lambda r: r["n"], reverse=True)[:top][::-1]
    labels = [f"{SHORT_EN.get(r['en'], r['en'])}"
              f"<br><span style='font-size:10.5px;color:#697288'>{r['ja']}</span>"
              for r in rows]
    fig = base(height=32 * len(rows) + 92, margin=dict(l=6, r=96, t=34, b=8))
    for cat in CAT_ORDER:                     # legend in a fixed, meaningful order
        fig.add_trace(_bar(
            y=[labels[0]], x=[None], orientation="h", marker_color=CAT_COLOUR[cat],
            name=f"{cat} · {CAT_JA[cat]}", hoverinfo="skip",
        ))
    for r, lab in zip(rows, labels):
        fig.add_trace(_bar(
            y=[lab], x=[r["n"]], orientation="h", marker_color=CAT_COLOUR[r["cat"]],
            showlegend=False,
            text=[f"{fmt(r['n'])}  <span style='color:#697288'>{r['share']*100:.1f}%</span>"],
            textposition="outside", textfont=dict(size=12, color=INK_2),
            cliponaxis=False,
            hovertemplate=f"<b>{r['en']}</b> ({r['ja']})<br>"
                          f"{fmt(r['n'])} residents · {r['share']*100:.1f}%<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, max(r["n"] for r in rows) * 1.2]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)),
        bargap=0.42,
    )
    return fig


def prefecture_bar():
    rows = DATA["prefectures"][::-1]
    labels = [r["pref"] for r in rows]
    groups = [("Kantō ring · 北関東・埼玉圏", S1, lambda r: r["kanto"]),
              ("Tokyo · 東京都", S2, lambda r: r["pref"] == "Tokyo"),
              ("Other prefectures · その他", MUTED,
               lambda r: not r["kanto"] and r["pref"] != "Tokyo")]
    fig = base(height=32 * len(rows) + 92, margin=dict(l=6, r=96, t=34, b=8))
    for name, colour, test in groups:
        vals = [r["n"] if test(r) else None for r in rows]
        text = [(f"{fmt(r['n'])}   <span style='color:{S2}'>6th · 6位</span>"
                 if r["pref"] == "Tokyo" else fmt(r["n"])) if v else None
                for r, v in zip(rows, vals)]
        fig.add_trace(_bar(
            y=labels, x=vals, orientation="h", name=name, marker_color=colour,
            text=text, textposition="outside",
            textfont=dict(size=12, color=INK_2), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x:,} residents<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, 5600]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)),
        bargap=0.4,
    )
    return fig


# ------------------------------------------------------------------- 3 · ports
def ports_bar():
    rows = DATA["ports"]
    head = rows[:7]
    tail = rows[7:]
    items = [(r["port"], r["n"], r["share"]) for r in head]
    items.append((f"Other ports ({len(tail)})", sum(r["n"] for r in tail),
                  sum(r["share"] for r in tail)))
    items = items[::-1]
    ja = {"Narita": "成田", "Kansai": "関西", "Haneda": "羽田", "Chubu / Centrair": "中部",
          "Fukuoka": "福岡", "New Chitose": "新千歳", "Naha": "那覇"}
    labels = [f"{p}<br><span style='font-size:10.5px;color:#697288'>{ja.get(p,'その他')}</span>"
              for p, _, _ in items]
    colours = [S1 if n > 5000 else MUTED for _, n, _ in items]
    fig = base(height=350, legend=False, margin=dict(l=6, r=96, t=14, b=8))
    fig.add_trace(_bar(
        y=labels, x=[n for _, n, _ in items], orientation="h",
        marker_color=colours,
        text=[f"{fmt(n)}  <span style='color:#697288'>{s*100:.1f}%</span>"
              for _, n, s in items],
        textposition="outside", textfont=dict(size=12, color=INK_2), cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x:,} entrants<extra></extra>",
    ))
    fig.update_layout(
        xaxis=dict(visible=False, range=[0, 23500]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)),
        bargap=0.4,
    )
    return fig


# ------------------------------------------------------- 4 · leading indicators
def sasia_growth():
    rows = sorted(DATA["sasia"][:5], key=lambda r: r["growth"])
    ja = {"India": "インド", "Sri Lanka": "スリランカ", "Nepal": "ネパール",
          "Bangladesh": "バングラデシュ", "Pakistan": "パキスタン"}
    labels = [f"{r['country']}<br><span style='font-size:10.5px;color:#697288'>"
              f"{ja[r['country']]}</span>" for r in rows]
    fig = base(height=300, margin=dict(l=6, r=74, t=34, b=8))
    for name, colour, test in [("Pakistan · パキスタン", S2, lambda r: r["country"] == "Pakistan"),
                               ("Regional comparators · 域内比較国", MUTED,
                                lambda r: r["country"] != "Pakistan")]:
        vals = [r["growth"] * 100 if test(r) else None for r in rows]
        fig.add_trace(_bar(
            y=labels, x=vals, orientation="h", name=name, marker_color=colour,
            text=[f"+{v:.0f}%" if v else None for v in vals], textposition="outside",
            textfont=dict(size=12.5, color=INK_2), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>+%{x:.1f}% learners 2021→2024<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, 336]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)), bargap=0.4,
    )
    return fig


def sasia_size():
    rows = sorted(DATA["sasia"][:5], key=lambda r: r["y2024"])
    ja = {"India": "インド", "Sri Lanka": "スリランカ", "Nepal": "ネパール",
          "Bangladesh": "バングラデシュ", "Pakistan": "パキスタン"}
    labels = [f"{r['country']}<br><span style='font-size:10.5px;color:#697288'>"
              f"{ja[r['country']]}</span>" for r in rows]
    fig = base(height=300, margin=dict(l=6, r=84, t=34, b=8))
    for name, colour, test in [("Pakistan · パキスタン", S2, lambda r: r["country"] == "Pakistan"),
                               ("Regional comparators · 域内比較国", MUTED,
                                lambda r: r["country"] != "Pakistan")]:
        vals = [r["y2024"] if test(r) else None for r in rows]
        fig.add_trace(_bar(
            y=labels, x=vals, orientation="h", name=name, marker_color=colour,
            text=[fmt(v) if v else None for v in vals], textposition="outside",
            textfont=dict(size=12.5, color=INK_2), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x:,} learners, 2024<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, 63000]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)), bargap=0.4,
    )
    return fig


def students_indexed():
    rows = [r for r in DATA["students"] if r["jp_total"]]
    base_pk, base_jp = rows[0]["pk"], rows[0]["jp_total"]
    x = [r["year"] for r in rows]
    pk = [r["pk"] / base_pk * 100 for r in rows]
    jp = [r["jp_total"] / base_jp * 100 for r in rows]
    fig = base(height=340, margin=dict(l=6, r=96, t=34, b=8))
    fig.add_trace(go.Scatter(
        x=x, y=jp, mode="lines", name="Japan, all inbound students · 日本の受入留学生総数",
        line=dict(color=MUTED, width=2),
        hovertemplate="%{x}: index %{y:.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=pk, mode="lines+markers", name="Pakistani students · パキスタン人留学生",
        line=dict(color=S1, width=2.4),
        marker=dict(size=7, color=S1, line=dict(color=SURFACE, width=1.6)),
        hovertemplate="%{x}: index %{y:.0f}<extra></extra>",
    ))
    fig.add_hline(y=100, line=dict(color=AXIS, width=1))
    for y_end, colour, label in [(pk[-1], S1, f"<b>{pk[-1]:.0f}</b>"),
                                 (jp[-1], MUTED, f"{jp[-1]:.0f}")]:
        fig.add_annotation(x=x[-1], y=y_end, text=label, showarrow=False, xanchor="left",
                           xshift=10, font=dict(size=14, color=colour, family=FONT))
    fig.update_layout(
        yaxis=dict(title=dict(text="Index, 2013 = 100", font=dict(size=11.5, color=INK_3)),
                   gridcolor=GRID, tickfont=dict(size=12, color=INK_3), range=[60, 320]),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, dtick=1, tickfont=dict(size=11.5, color=INK_3)),
    )
    return fig


def visas_bar():
    rows = DATA["visas"]
    years = [str(r["year"]) for r in rows]
    fig = base(height=330)
    series = [("total", "All visas issued · 査証発給総数", S1),
              ("short", "of which short-stay · うち短期滞在", S3),
              ("online", "of which issued online · うちオンライン発給", S4)]
    for key, name, colour in series:
        vals = [r[key] for r in rows]
        fig.add_trace(_bar(
            x=years, y=vals, name=name, marker_color=colour,
            text=[fmt(v) for v in vals], textposition="outside",
            textfont=dict(size=11.5, color=INK_2), cliponaxis=False,
            hovertemplate=f"<b>{name}</b><br>%{{x}}: %{{y:,}}<extra></extra>",
        ))
    fig.update_layout(
        barmode="group",
        yaxis=dict(tickformat=",", gridcolor=GRID, range=[0, 23500],
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showgrid=False, showline=True, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(size=12.5, color=INK_3)),
        bargap=0.45, bargroupgap=0.08,
    )
    return fig


# --------------------------------------------------------- 5 · money and labour
def beoe_bar():
    rows = [r for r in DATA["beoe"] if r["year"] != "1971–2013 cum."]
    labels = [r["year"].replace(" (Jan–Aug)", "*") for r in rows]
    vals = [r["total"] for r in rows]
    colours = [MUTED if "*" in l else S1 for l in labels]
    fig = base(height=350, legend=False, margin=dict(l=6, r=10, t=30, b=8))
    fig.add_trace(_bar(
        x=labels, y=vals, marker_color=colours,
        text=[fmt(v) for v in vals], textposition="outside",
        textfont=dict(size=11.5, color=INK_2), cliponaxis=False,
        hovertemplate="<b>%{x}</b><br>%{y:,} workers registered<extra></extra>",
    ))
    fig.update_layout(
        yaxis=dict(tickformat=",", gridcolor=GRID, range=[0, 2720],
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, tickfont=dict(size=11.5, color=INK_3)),
    )
    fig.add_annotation(                      # category axes take the index, not the label
        x=labels.index("2021"), y=17, text="17 — border closure　国境閉鎖", showarrow=True,
        arrowhead=0, arrowcolor=AXIS, arrowwidth=1, ax=-26, ay=-96, xanchor="right",
        font=dict(size=11, color=INK_3, family=FONT),
    )
    return fig


def remit_line():
    rows = DATA["remit"]
    x = [r["fy"] for r in rows]
    y = [r["japan"] for r in rows]
    brk = x.index("FY20")
    fig = base(height=340, legend=False, margin=dict(l=6, r=56, t=22, b=8))
    fig.add_vrect(x0=-0.5, x1=brk - 0.5, fillcolor="#F1F2F6", opacity=1, layer="below",
                  line_width=0)
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", line=dict(color=S1, width=2.2),
        marker=dict(size=7, color=S1, line=dict(color=SURFACE, width=1.6)),
        hovertemplate="%{x}: <b>US$%{y:.2f}m</b><extra></extra>",
    ))
    fig.add_vline(x=brk - 0.5, line=dict(color=S4, width=1.5))
    fig.add_annotation(
        x=brk - 0.5, y=1.0, yref="paper", yanchor="bottom", xanchor="center",
        text="<b>Definitional break, July 2019</b>　<span style='color:#697288'>統計定義の変更</span>",
        showarrow=False, font=dict(size=11.5, color=S4, family=FONT),
    )
    fig.add_annotation(x="FY21", y=85.24, text="<b>85.2</b> peak<br>ピーク", showarrow=False,
                      yanchor="bottom", yshift=8, font=dict(size=11.5, color=INK_2, family=FONT))
    fig.add_annotation(x=x[-1], y=y[-1], text=f"<b>{y[-1]:.1f}</b>", showarrow=False,
                      xanchor="left", xshift=9, font=dict(size=14, color=S1, family=FONT))
    fig.update_layout(
        yaxis=dict(title=dict(text="US$ million　百万米ドル", font=dict(size=11.5, color=INK_3)),
                   gridcolor=GRID, range=[0, 100], tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, tickfont=dict(size=11.5, color=INK_3)),
    )
    return fig


def travel_services():
    rows = DATA["travel_services"]
    x = [r["fy"] for r in rows]
    imp = [r["imports"] / 1000 for r in rows]
    exp = [r["exports"] / 1000 for r in rows]
    fig = base(height=340, margin=dict(l=6, r=64, t=34, b=8))
    fig.add_trace(go.Scatter(
        x=x, y=exp, mode="lines+markers",
        name="Exports to Japan · 対日輸出（受取）", legendrank=2,
        line=dict(color=S2, width=2.1),
        marker=dict(size=6.5, color=S2, line=dict(color=SURFACE, width=1.6)),
        hovertemplate="%{x}: US$%{y:.2f}m<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=x, y=imp, mode="lines+markers",
        name="Imports from Japan · 対日輸入（支払）", legendrank=1,
        line=dict(color=S1, width=2.4),
        marker=dict(size=7, color=S1, line=dict(color=SURFACE, width=1.6)),
        hovertemplate="%{x}: US$%{y:.2f}m<extra></extra>",
    ))
    fig.add_annotation(x=x[-1], y=imp[-1], text=f"<b>{imp[-1]:.1f}</b>", showarrow=False,
                      xanchor="left", xshift=9, font=dict(size=14, color=S1, family=FONT))
    fig.add_annotation(x=x[-1], y=exp[-1], text=f"{exp[-1]:.1f}", showarrow=False,
                      xanchor="left", xshift=9, font=dict(size=13, color=S2, family=FONT))
    fig.update_layout(
        legend_traceorder="normal",
        yaxis=dict(title=dict(text="US$ million　百万米ドル", font=dict(size=11.5, color=INK_3)),
                   gridcolor=GRID, range=[0, 12.6], tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, tickfont=dict(size=11.5, color=INK_3)),
    )
    return fig


# --------------------------------------------------------------- 6 · catalogue
STATUS_COLOUR = {"NAMED": S3, "BILATERAL": S1, "IN 'OTHER'": S4,
                 "ABSENT": S2, "UNRESOLVED": MUTED}
STATUS_JA = {"NAMED": "個別掲載", "BILATERAL": "二国間対応",
             "IN 'OTHER'": "「その他」に包含", "ABSENT": "データ不在", "UNRESOLVED": "未確認"}
STATUS_ORDER = ["NAMED", "BILATERAL", "IN 'OTHER'", "ABSENT", "UNRESOLVED"]


def catalogue_status_bar():
    rows = DATA["catalogue"]
    total = len(rows)
    counts = {s: sum(1 for r in rows if r["Pakistan in the data"] == s) for s in STATUS_ORDER}
    fig = base(height=175, margin=dict(l=6, r=6, t=34, b=6))
    for s in STATUS_ORDER:
        share = counts[s] / total * 100
        fig.add_trace(_bar(
            x=[share], y=[""], orientation="h", name=f"{s} · {STATUS_JA[s]}",
            marker_color=STATUS_COLOUR[s],
            text=[f"<b>{counts[s]}</b>" if share > 3 else ""],
            textposition="inside", insidetextanchor="middle", textangle=0,
            textfont=dict(color="#FFFFFF", size=14, family=FONT),
            hovertemplate=f"<b>{s} · {STATUS_JA[s]}</b><br>{counts[s]} of {total} sources"
                          f" · {share:.0f}%<extra></extra>",
        ))
    fig.update_layout(barmode="stack", legend_traceorder="normal",
                      xaxis=dict(visible=False, range=[0, 100]),
                      yaxis=dict(visible=False), bargap=0.05)
    return fig


# ═══════════════════════════════════════════════════════════ 7 · JNTO series
from jnto_data import JNTO  # noqa: E402

PK_ANN = {r["year"]: r["arrivals"] for r in JNTO["pk_annual"]}
JP_ANN = {r["year"]: r["inbound"] for r in JNTO["jp_annual"]}
PK_PUR = {r["year"]: r for r in JNTO["pk_purpose"]}
FULL_YEARS = [r["year"] for r in JNTO["pk_annual"] if r["term"] == "Jan. - Dec."]
MONTHS = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
          "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]


def jnto_series():
    """Pakistan visitor arrivals to Japan, 1992–2025. One series — emphasis form."""
    x = FULL_YEARS
    y = [PK_ANN[v] for v in x]
    fig = base(height=370, legend=False, margin=dict(l=6, r=66, t=26, b=8))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", line=dict(color=S1, width=2.4),
        fill="tozeroy", fillcolor="rgba(47,87,166,0.08)",
        hovertemplate="%{x}<br><b>%{y:,}</b> visitor arrivals<extra></extra>",
    ))
    for yr, colour, weight in [(2019, INK_3, ""), (2021, INK_3, ""), (2025, S1, "<b>")]:
        fig.add_trace(go.Scatter(
            x=[yr], y=[PK_ANN[yr]], mode="markers", showlegend=False, hoverinfo="skip",
            marker=dict(size=9, color=colour if yr != 2025 else S1,
                        line=dict(color=SURFACE, width=2)),
        ))
    fig.add_annotation(x=2025, y=PK_ANN[2025], text=f"<b>{fmt(PK_ANN[2025])}</b>",
                       showarrow=False, xanchor="left", xshift=10,
                       font=dict(size=15, color=S1, family=FONT))
    fig.add_annotation(x=2019, y=PK_ANN[2019], text=f"2019 peak {fmt(PK_ANN[2019])}",
                       showarrow=False, yanchor="bottom", yshift=12, xanchor="right",
                       font=dict(size=11.5, color=INK_3, family=FONT))
    fig.add_annotation(x=2021, y=PK_ANN[2021], text=f"{fmt(PK_ANN[2021])}", showarrow=False,
                       yanchor="top", yshift=-10, font=dict(size=11.5, color=INK_3, family=FONT))
    fig.update_layout(
        yaxis=dict(tickformat=",", gridcolor=GRID, range=[0, 34000],
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, dtick=4, tickfont=dict(size=12, color=INK_3)),
    )
    return fig


def jnto_share_of_japan():
    """The same arrivals as a share of Japan's total inbound — the relative story.

    2020-22 are omitted: Japan's border closure collapsed the denominator (Pakistan
    was 1.7% of a 245,862 total in 2021), so the ratio measures the closure, not the
    market. The line is broken rather than bridged.
    """
    x = FULL_YEARS
    closed = {2020, 2021, 2022}
    y = [None if v in closed else PK_ANN[v] / JP_ANN[v] * 100 for v in x]
    fig = base(height=330, legend=False, margin=dict(l=6, r=62, t=26, b=8))
    fig.add_vrect(x0=2019.5, x1=2022.5, fillcolor="#F1F2F6", opacity=1, layer="below",
                  line_width=0)
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", line=dict(color=S2, width=2.4), connectgaps=False,
        hovertemplate="%{x}<br><b>%{y:.3f}%</b> of Japan's visitor arrivals<extra></extra>",
    ))
    first, last = y[0], y[-1]
    fig.add_annotation(x=1992, y=first, text=f"<b>{first:.3f}%</b>", showarrow=False,
                       xanchor="left", xshift=8, yanchor="bottom", yshift=6,
                       font=dict(size=13.5, color=S2, family=FONT))
    fig.add_annotation(x=2025, y=last, text=f"<b>{last:.3f}%</b>", showarrow=False,
                       xanchor="left", xshift=10, font=dict(size=13.5, color=S2, family=FONT))
    fig.add_annotation(x=2021, y=0.205, text="2020–22 omitted<br>国境閉鎖のため除外",
                       showarrow=False, xanchor="center", yanchor="top",
                       font=dict(size=10.5, color=INK_3, family=FONT))
    fig.update_layout(
        yaxis=dict(ticksuffix="%", gridcolor=GRID, range=[0, 0.215],
                   tickfont=dict(size=12, color=INK_3), tickformat=".2f"),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, dtick=4, tickfont=dict(size=12, color=INK_3)),
    )
    return fig


JNTO_PURPOSE = [("tourism", "Tourism", "観光", S1),
                ("business", "Business", "商用", S2),
                ("others", "Other purposes", "その他の目的", S3)]


def jnto_purpose_stack(start=2012):
    rows = [PK_PUR[y] for y in FULL_YEARS if y >= start]
    years = [str(r["year"]) for r in rows]
    peak = max(r["total"] for r in rows)
    fig = base(height=380)
    for key, en, ja, colour in JNTO_PURPOSE:
        vals = [r[key] or 0 for r in rows]
        fig.add_trace(_bar(
            x=years, y=vals, name=f"{en} · {ja}", marker_color=colour,
            text=[fmt(v) if v / peak > 0.055 else "" for v in vals],
            textposition="inside", insidetextanchor="middle", textangle=0,
            textfont=dict(color="#FFFFFF", size=12, family=FONT),
            hovertemplate=f"<b>{en} · {ja}</b><br>%{{x}}: %{{y:,}}<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack",
        yaxis=dict(tickformat=",", gridcolor=GRID, tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showgrid=False, showline=True, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(size=11.5, color=INK_3)),
    )
    return fig


def population_reconcile():
    """The four different 2025 counts, side by side, coloured by publisher."""
    items = [
        ("All entrants, incl. re-entry<br><span style='font-size:11px;color:#697288'>"
         "入国外国人（再入国を含む）</span>", 37275, "isa"),
        ("JNTO visitor arrivals<br><span style='font-size:11px;color:#697288'>"
         "訪日外客数</span>", 30171, "jnto"),
        ("New entrants, all statuses<br><span style='font-size:11px;color:#697288'>"
         "新規入国外国人</span>", 17863, "isa"),
        ("Short-stay entries<br><span style='font-size:11px;color:#697288'>"
         "短期滞在入国</span>", 11360, "isa"),
        ("…of which tourism<br><span style='font-size:11px;color:#697288'>"
         "うち観光目的</span>", 7053, "isa"),
    ][::-1]
    labels = [i[0] for i in items]
    fig = base(height=340, margin=dict(l=6, r=96, t=34, b=8))
    for name, tag, colour in [("JNTO 訪日外客数", "jnto", S2),
                              ("Immigration Services Agency 出入国管理統計", "isa", S1)]:
        vals = [v if t == tag else None for _, v, t in items]
        fig.add_trace(_bar(
            y=labels, x=vals, orientation="h", name=name, marker_color=colour,
            text=[fmt(v) if v else None for v in vals], textposition="outside",
            textfont=dict(size=12.5, color=INK_2), cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x:,} in 2025<extra></extra>",
        ))
    fig.update_layout(
        barmode="stack", legend_traceorder="normal",
        xaxis=dict(visible=False, range=[0, 44000]),
        yaxis=dict(showgrid=False, tickfont=dict(size=12.5, color=INK_2)),
        bargap=0.42,
    )
    return fig


def jnto_seasonality():
    m = {(r["year"], r["month"]): r["arrivals"] for r in JNTO["pk_monthly"]}
    fig = base(height=330, margin=dict(l=6, r=54, t=34, b=8))
    for yr, colour, width, rank in [(2019, MUTED, 2.0, 2), (2025, S1, 2.4, 1)]:
        vals = [m.get((yr, mm)) for mm in MONTHS]
        fig.add_trace(go.Scatter(
            x=MONTHS, y=vals, mode="lines+markers", name=f"{yr}", legendrank=rank,
            line=dict(color=colour, width=width),
            marker=dict(size=7, color=colour, line=dict(color=SURFACE, width=1.6)),
            hovertemplate=f"{yr} %{{x}}<br><b>%{{y:,}}</b><extra></extra>",
        ))
    peak_m = max(MONTHS, key=lambda mm: m.get((2025, mm), 0))
    fig.add_annotation(x=peak_m, y=m[(2025, peak_m)],
                       text=f"<b>{fmt(m[(2025, peak_m)])}</b>", showarrow=False,
                       yanchor="bottom", yshift=10, font=dict(size=12.5, color=S1, family=FONT))
    fig.update_layout(
        legend_traceorder="normal",
        yaxis=dict(tickformat=",", gridcolor=GRID, rangemode="tozero",
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showgrid=False, showline=True, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(size=12, color=INK_3)),
    )
    return fig


def jnto_los():
    rows = JNTO["los"]
    x = [r["year"] for r in rows]
    y = [r["nights"] for r in rows]
    fig = base(height=320, legend=False, margin=dict(l=6, r=58, t=26, b=8))
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers", line=dict(color=S3, width=2.4),
        marker=dict(size=7, color=S3, line=dict(color=SURFACE, width=1.6)),
        hovertemplate="%{x}<br><b>%{y:.1f}</b> nights<extra></extra>",
    ))
    fig.add_annotation(x=2021, y=43.18, text="43.2 — pandemic year,<br>not a travel pattern",
                       showarrow=False, xanchor="left", xshift=10, yanchor="top",
                       font=dict(size=11, color=INK_3, family=FONT))
    fig.add_annotation(x=x[-1], y=y[-1], text=f"<b>{y[-1]:.1f}</b>", showarrow=False,
                       xanchor="left", xshift=10, font=dict(size=14, color=S3, family=FONT))
    fig.update_layout(
        yaxis=dict(title=dict(text="Nights　泊数", font=dict(size=11.5, color=INK_3)),
                   gridcolor=GRID, range=[0, 48], tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(showgrid=False, showline=True, linecolor=AXIS, ticks="outside",
                   tickcolor=AXIS, dtick=2, tickfont=dict(size=12, color=INK_3)),
    )
    return fig


def jnto_pyramid():
    rows = JNTO["age_bands_2024"]
    bands = [r["band"].replace(" - ", "–").replace("70–", "70+") for r in rows]
    male = [-r["male"] for r in rows]
    female = [r["female"] for r in rows]
    fig = base(height=430, margin=dict(l=6, r=10, t=34, b=8))
    fig.add_trace(_bar(
        y=bands, x=male, orientation="h", name="Male · 男性", legendrank=1, marker_color=S1,
        hovertemplate="<b>%{y}</b><br>Male %{customdata:,}<extra></extra>",
        customdata=[r["male"] for r in rows],
    ))
    fig.add_trace(_bar(
        y=bands, x=female, orientation="h", name="Female · 女性", legendrank=2, marker_color=S2,
        hovertemplate="<b>%{y}</b><br>Female %{x:,}<extra></extra>",
    ))
    fig.update_layout(
        barmode="relative", legend_traceorder="normal",
        xaxis=dict(showgrid=True, gridcolor=GRID, zeroline=True, zerolinecolor=AXIS,
                   zerolinewidth=1, showline=False, ticks="",
                   tickvals=[-3500, -2500, -1500, -500, 500, 1000],
                   ticktext=["3,500", "2,500", "1,500", "500", "500", "1,000"],
                   tickfont=dict(size=11.5, color=INK_3), range=[-3850, 1180]),
        yaxis=dict(showgrid=False, tickfont=dict(size=11.5, color=INK_2)),
        bargap=0.22,
    )
    return fig


JNTO_PORT_JA = {"Narita": "成田", "Haneda": "羽田", "Kansai": "関西", "Chubu": "中部"}


def jnto_ports_trend():
    series = {p: [] for p in JNTO_PORT_JA}
    years = [r["year"] for r in JNTO["jnto_ports"]]
    for r in JNTO["jnto_ports"]:
        for p in JNTO_PORT_JA:
            series[p].append(r["ports"].get(p, 0))
    colours = {"Narita": S1, "Haneda": S2, "Kansai": S3, "Chubu": S4}
    nudge = {"Narita": 0, "Haneda": 9, "Kansai": -10, "Chubu": 0}  # 2024 endpoints nearly touch
    fig = base(height=340, margin=dict(l=6, r=76, t=34, b=8))
    for i, (p, vals) in enumerate(series.items()):
        fig.add_trace(go.Scatter(
            x=[str(y) for y in years], y=vals, mode="lines+markers",
            name=f"{p} · {JNTO_PORT_JA[p]}", legendrank=i + 1,
            line=dict(color=colours[p], width=2.3),
            marker=dict(size=7, color=colours[p], line=dict(color=SURFACE, width=1.6)),
            hovertemplate=f"<b>{p}</b> %{{x}}<br>%{{y:,}} entrants<extra></extra>",
        ))
        # category axes resolve annotation x by index, not by label
        fig.add_annotation(x=len(years) - 1, y=vals[-1], text=fmt(vals[-1]), showarrow=False,
                           xanchor="left", xshift=9, yshift=nudge[p],
                           font=dict(size=12, color=colours[p], family=FONT))
    fig.update_layout(
        legend_traceorder="normal",
        yaxis=dict(tickformat=",", gridcolor=GRID, rangemode="tozero",
                   tickfont=dict(size=12, color=INK_3)),
        xaxis=dict(type="category", showgrid=False, showline=True, linecolor=AXIS,
                   ticks="outside", tickcolor=AXIS, tickfont=dict(size=12, color=INK_3)),
    )
    return fig
