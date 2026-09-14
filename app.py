"""
Pakistan–Japan Travel Data — an evidence dashboard for an Embassy briefing, Tokyo.
パキスタン・日本 渡航データ — 東京・大使館ブリーフィング用ダッシュボード

Run:  streamlit run app.py
All data is embedded in data.py; no external file is required at runtime.
"""

import pandas as pd
import streamlit as st

import charts as C
from data import DATA
from jnto_data import JNTO
from theme import CSS, fmt, pct, signed_pct
from ui import H, chart_card, facts, kpis, masthead, panel, rule, section, stretch

st.set_page_config(
    page_title="Pakistan–Japan Travel Data",
    layout="wide",
    initial_sidebar_state="expanded",
)
H(CSS)

A = {r["year"]: r for r in DATA["arrivals"]}
W = {r["year"]: r for r in DATA["japan_ww"]}
RES = {r["asat"]: r for r in DATA["residents_ts"]}
CATS = {c["cat"]: c for c in DATA["res_cats"]}
VIS = {r["year"]: r for r in DATA["visas"]}
SASIA = {r["country"]: r for r in DATA["sasia"]}
LEARN = {r["measure"]: r for r in DATA["learners_pk"]}
CATALOGUE = DATA["catalogue"]
N_SOURCES = len(CATALOGUE)
N_IDENTIFIABLE = sum(
    1 for r in CATALOGUE if r["Pakistan in the data"] in ("NAMED", "BILATERAL")
)
TOP3_PORTS = sum(r["n"] for r in DATA["ports"][:3])
PORTS_TOTAL = sum(r["n"] for r in DATA["ports"])

SRC_IMMIG = (
    "SOURCE · Ministry of Justice / Immigration Services Agency, Immigration Control "
    "Statistics 出入国管理統計, tables 19-00-11 and 2X-00-07. Counts entries, not persons."
)
PK_ANN = {r["year"]: r["arrivals"] for r in JNTO["pk_annual"]}
JP_ANN = {r["year"]: r["inbound"] for r in JNTO["jp_annual"]}
PK_PUR = {r["year"]: r for r in JNTO["pk_purpose"]}
LOS = {r["year"]: r["nights"] for r in JNTO["los"]}
SEX = {r["year"]: r for r in JNTO["entries_by_sex"]}
JNTO_FULL = [r["year"] for r in JNTO["pk_annual"] if r["term"] == "Jan. - Dec."]
PART_2026 = next(r for r in JNTO["pk_annual"] if r["term"] != "Jan. - Dec.")
SAME_2025 = sum(r["arrivals"] for r in JNTO["pk_monthly"]
                if r["year"] == 2025 and r["month"] in
                ("Jan.", "Feb.", "Mar.", "Apr.", "May"))

SRC_JNTO = (
    "SOURCE · JNTO (Japan National Tourism Organization) statistics database, "
    "statistics.jnto.go.jp — 3-1 Visitor arrivals 訪日外客数. Compiled BY NATIONALITY from "
    "Ministry of Justice immigration statistics. Excludes permanent residents whose primary "
    "place of residence is Japan, and crew; INCLUDES foreigners entering or re-entering Japan "
    "such as expatriates, their families and international students, and travellers entering "
    "for transit. Each entry is counted as one."
)

SRC_RESIDENTS = (
    "SOURCE · Immigration Services Agency, Statistics on Foreign Residents 在留外国人統計, "
    "December 2025 edition (e-Stat lid=000001486479). Mid- and long-term residents only."
)


# ══════════════════════════════════════════════════════════════════ 01 OVERVIEW
def page_overview():
    masthead(
        "Embassy briefing · Tokyo · 東京 大使館ブリーフィング",
        "Pakistan–Japan travel, in the data that exists",
        "パキスタン・日本間の渡航 ― 存在するデータで見る",
        f"Every figure here was taken from the publisher's own file. {N_SOURCES} sources were "
        f"assessed and Pakistan can be identified in {N_IDENTIFIABLE} of them — plus JNTO's own "
        "statistics database, which carries an unbroken Pakistan series back to 1992. The "
        "<b>composition</b> of Pakistani travel to Japan — not its volume — is the finding; "
        "and the places where Pakistan is still missing from the data are themselves the case "
        "for action.",
        f"本資料の数値はすべて発行機関の原典ファイルから直接取得しています。{N_SOURCES}件の情報源を検証し、"
        f"パキスタンを個別に識別できたのは{N_IDENTIFIABLE}件、加えてJNTOの統計データベースには1992年"
        "以降の連続系列が存在します。所見は渡航の「量」ではなく「構成」にあり、統計上パキスタンが"
        "なお不在である領域自体が、行動を求める論拠となります。",
    )

    a25, w25 = A[2025], W[2025]
    kpis([
        dict(value=fmt(PK_ANN[2025]), accent=True,
             en="JNTO visitor arrivals from Pakistan, 2025",
             ja="訪日外客数（パキスタン、2025年）",
             foot=f"{signed_pct(PK_ANN[2025] / PK_ANN[2024] - 1)} on 2024 · record　"
                  "過去最高"),
        dict(value=fmt(a25["total"]),
             en="…of which short-stay entries",
             ja="うち短期滞在入国件数",
             foot=f"{signed_pct(a25['total'] / A[2019]['total'] - 1)} vs 2019　2019年比"),
        dict(value="62.1", unit="%",
             en="Tourism share of short-stay entries",
             ja="短期滞在に占める観光目的の割合",
             foot="Japan, all nationalities: 94.2%　日本全体 94.2%"),
        dict(value=fmt(RES["Dec 2025"]["pk"]),
             en="Pakistani residents of Japan, Dec 2025",
             ja="在日パキスタン人（中長期在留者、2025年12月）",
             foot=f"{signed_pct(RES['Dec 2025']['pk'] / RES['Dec 2019']['pk'] - 1)} since 2019　2019年比"),
        dict(value=f"{PK_ANN[2025] / JP_ANN[2025] * 100:.3f}", unit="%",
             en="Pakistan's share of Japan's visitor arrivals",
             ja="日本の訪日外客数に占める割合",
             foot="0.187% in 1992　1992年は0.187%"),
        dict(value="0", accent=True,
             en="Japan–Pakistan sister-city links",
             ja="日本・パキスタン間の姉妹都市提携",
             foot="of Japan's 1,878 partnerships　日本の全提携1,878件中"),
    ])

    section("01", "The finding, in one chart", "所見を一枚の図で",
            "Pakistani travel to Japan is business- and family-driven, not leisure-driven. "
            "Against Japan's worldwide inbound mix, Pakistan runs roughly ten times the "
            "business share and ten times the visiting-relatives share.",
            "対日渡航は観光主導ではなく、商用と家族訪問が牽引しています。日本全体の入国構成と比べ、"
            "商用・親族訪問の比率はいずれも約10倍です。")
    mix = pd.DataFrame([
        {"Purpose 目的": r["purpose"], "Pakistan パキスタン": pct(r["pk"]),
         "Japan worldwide 日本全体": pct(r["jp"]), "Ratio 倍率": f"×{r['ratio']:.2f}"}
        for r in DATA["mix"]
    ])
    chart_card(
        "Share of short-stay entries by stated purpose, 2025",
        "入国目的別に見た短期滞在入国の構成比（2025年）",
        C.mix_comparison(), table=mix,
        take_en="Tourism is 62.1% of Pakistani short-stay entries against 94.2% worldwide; "
                "business is 26.7% against 2.8% and visiting relatives 10.9% against 1.1%.",
        take_ja="観光は62.1%（日本全体94.2%）、商用は26.7%（同2.8%）、親族訪問は10.9%（同1.1%）。",
        src=SRC_IMMIG,
    )

    section("02", "Three definitions to get right before anything is quoted",
            "引用前に確認すべき三つの定義", None, None)
    H(
        '<div class="defs">'
        '<div class="def"><h4>Entries, not people</h4>'
        '<p class="ja">「人数」ではなく「入国件数」</p>'
        "<p>Japan's immigration data counts border crossings. A traveller who visits twice is "
        "counted twice. These figures are never to be described as “visitors”.</p></div>"
        '<div class="def"><h4>Nationality, not residence</h4>'
        '<p class="ja">居住地ではなく国籍による集計</p>'
        "<p>Nationality is taken from the passport, so a Pakistani national living in Dubai or "
        "London counts as Pakistan. JNTO compiles its visitor arrivals on the same basis — by "
        "nationality — so the two are comparable on that axis.</p></div>"
        '<div class="def"><h4>Four different populations</h4>'
        '<p class="ja">四つの母集団を混同しない</p>'
        "<p>All entrants including re-entry (37,275 in 2025), JNTO visitor arrivals (30,171), "
        "new entrants only (17,863) and short-stay status (11,360) are different things. "
        "Mixing them inflates the figure two- to threefold. Page 03 reconciles all four.</p></div>"
        "</div>"
    )

    section("03", "How the argument is built", "論旨の構成", None, None)
    H(
        '<div class="cards two">'
        '<div class="gcard"><p class="n">02 · 03 · 04</p><h4>The demand is already there, and it '
        'is the unusual kind</h4><p class="ja">需要はすでに存在し、しかも特異な構成である</p>'
        '<p class="d">JNTO\'s own series shows 34 unbroken years and a 2025 record of 30,171. '
        'Short-stay entries are 27.6% above 2019 and the mix is business and family. Behind it '
        'sits a resident community of 34,911 that is 55.9% family and settlement status.</p></div>'
        '<div class="gcard"><p class="n">05 · 06</p><h4>The leading indicators are moving faster '
        'than the travel</h4><p class="ja">先行指標は渡航実績を上回る速度で伸びている</p>'
        '<p class="d">Japanese-language learners up 272.8% in three years, tertiary students '
        'doubled through the pandemic while Japan\'s total fell, travel payments to Japan up '
        'roughly 26-fold since FY23.</p></div>'
        '<div class="gcard"><p class="n">07 · 08</p><h4>The infrastructure and the market listing '
        'are both missing</h4><p class="ja">インフラと市場区分の双方が欠落している</p>'
        '<p class="d">No non-stop air service, no e-visa through Islamabad or Karachi, no '
        'sister-city link and no bilateral tourism instrument — and Pakistan sits inside '
        '“Others” in every published JNTO market breakdown despite being in the database.</p></div>'
        '<div class="gcard"><p class="n">09 · 10</p><h4>Six proposals, each with its evidence '
        'line</h4><p class="ja">六つの提言 ― 各々に根拠を付して</p>'
        '<p class="d">Every proposal names the figure it rests on and the file that figure came '
        f'from. All {N_SOURCES} assessed sources, plus the JNTO datasets added since, remain '
        'browsable on the final page.</p></div>'
        "</div>"
    )


# ═══════════════════════════════════════════════════════════ 02 WHO TRAVELS
def page_who():
    masthead(
        "01 · Demand · 需要",
        "Who travels, and why",
        "誰が、なぜ渡航するのか",
        "Pakistani short-stay entries recovered past their pre-pandemic level in 2025 and "
        "then exceeded it. The composition of that travel is what separates Pakistan from "
        "every other origin market.",
        "パキスタン国籍者の短期滞在入国は2025年にコロナ禍前の水準を上回りました。他の市場と"
        "決定的に異なるのは、その渡航の「構成」です。",
    )

    a = DATA["arrivals"]
    tbl = pd.DataFrame([
        {"Year 年": r["year"], "Short-stay total 短期滞在計": r["total"],
         "Tourism 観光": r["tourism"], "Business 商用": r["business"],
         "Visiting relatives 親族訪問": r["vfr"],
         "Cultural / academic 文化・学術": r["cultural"], "Other その他": r["other"],
         "Tourism share 観光比率": f"{r['tourism'] / r['total'] * 100:.1f}%"}
        for r in a
    ])
    chart_card(
        "Pakistani short-stay entries to Japan, by stated purpose",
        "入国目的別 パキスタン国籍者の短期滞在入国件数",
        C.purpose_stack(), table=tbl,
        take_en=f"Short-stay entries reached {fmt(A[2025]['total'])} in 2025, "
                f"{signed_pct(A[2025]['total'] / A[2019]['total'] - 1)} on 2019. Business travel "
                f"grew faster than tourism: {fmt(A[2019]['business'])} → {fmt(A[2025]['business'])} "
                f"({signed_pct(A[2025]['business'] / A[2019]['business'] - 1)}).",
        take_ja=f"2025年の短期滞在入国は{fmt(A[2025]['total'])}件、2019年比"
                f"{signed_pct(A[2025]['total'] / A[2019]['total'] - 1)}。商用は観光を上回る伸びを示しました"
                f"（{fmt(A[2019]['business'])}→{fmt(A[2025]['business'])}件）。",
        src=SRC_IMMIG + " 2020 and 2021 are not shown: border closure left no meaningful mix. "
                        "2020・2021年は国境閉鎖のため表示していません。",
    )

    section("01", "Four populations, four different numbers",
            "四つの母集団、四つの異なる数字",
            "The most common error in this corridor is quoting the largest of these as "
            "“visitors”. For tourists, the correct chain is new entrants × short-stay × tourism. "
            "JNTO's own count sits inside this range — page 03 reconciles all four.",
            "この分野で最も多い誤りは、最大の数字を「訪問者数」として引用することです。観光客数は"
            "「新規入国 × 短期滞在 × 観光目的」の系列で捉える必要があります。JNTOの計数もこの範囲に"
            "収まります（03ページで四者を対照）。")
    agg = DATA["aggregates"]
    facts([(fmt(PK_ANN[2025]), "JNTO visitor arrivals", "訪日外客数（JNTO）",
            f"{signed_pct(PK_ANN[2025] / PK_ANN[2019] - 1)} vs 2019　2019年比")] + [
        (fmt(r["y2025"]), r["measure"].split(" (")[0],
         {"New entrants, all statuses": "新規入国外国人（全在留資格）",
          "All entrants incl. re-entry": "入国外国人（再入国を含む）",
          "Short-stay entries": "短期滞在入国",
          "of which tourism": "うち観光目的"}.get(r["measure"].split(" (")[0], ""),
         f"{signed_pct(r['chg'])} vs 2019　2019年比")
        for r in agg
    ])
    with st.expander("Data table  ·  データ表"):
        st.dataframe(pd.DataFrame([
            {"Measure 指標": r["measure"], "2019": r["y2019"], "2023": r["y2023"],
             "2024": r["y2024"], "2025": r["y2025"],
             "Change 2019→2025 増減": signed_pct(r["chg"])} for r in agg
        ]), hide_index=True, **stretch())
    panel(
        "caveat", "Caveat · 留意点",
        "“All entrants including re-entry” counts every border crossing by a Pakistani "
        "passport holder, including residents of Japan returning from abroad. Using it as a "
        "visitor number inflates the figure roughly three-fold against the short-stay series.",
        "「再入国を含む入国者数」には、海外から戻る在日パキスタン人の入国も含まれます。これを"
        "訪問者数として用いると、短期滞在系列の約3倍に膨らみます。",
    )

    section("02", "Against Japan's worldwide mix", "日本全体の入国構成との比較",
            "Pakistan is 0.019% of Japan's tourist entries — the headroom, not the volume, is "
            "the story. But it is roughly ten times the world average on both business and "
            "family travel.",
            "日本の観光目的入国に占めるパキスタンの割合は0.019%であり、論点は「量」ではなく"
            "「伸びしろ」です。一方で商用・親族訪問の比率はいずれも世界平均の約10倍です。")
    chart_card(
        "Purpose mix, Pakistan against Japan's worldwide inbound, 2025",
        "入国目的構成の比較：パキスタンと日本全体（2025年）",
        C.mix_comparison(),
        take_en="Business runs at 9.5 times the worldwide share and visiting relatives at "
                "9.6 times; tourism at 0.66 times.",
        take_ja="商用は世界平均の9.5倍、親族訪問は9.6倍、観光は0.66倍です。",
        src=SRC_IMMIG + " · Japan worldwide figures from the same tables.",
    )

    panel(
        "ask", "The ask · 提言",
        "That Pakistan be named in Japan's <b>published</b> market breakdowns. The arrivals "
        "series exists in JNTO's database (page 03) but Pakistan is folded into “Others” in the "
        "23-market breakdown, is absent from the Data Handbook's 33 markets and from all 24 "
        "market-intelligence pages — so the composition shown above cannot be tracked, targeted "
        "or budgeted for by either government from JNTO's published products.",
        "日本側の<b>公表</b>市場区分においてパキスタンを明示すること。入国者系列はJNTOのデータベースに"
        "存在します（03ページ）が、23市場の内訳では「その他」に包含され、データハンドブックの33市場にも"
        "24の市場分析ページにも登場しません。そのため上図の構成は、両国政府ともJNTOの公表資料からは"
        "追跡も、対象設定も、予算化もできません。",
    )



# ══════════════════════════════════════════════════════════════════ 03 JNTO
def page_jnto():
    masthead(
        "02 · JNTO · 訪日外客数",
        "JNTO does hold a Pakistan series — and it runs back to 1992",
        "JNTOにはパキスタンの系列が存在する ― 1992年まで遡る",
        "Japan's national tourism organisation carries a named Pakistan row in its statistics "
        "database: 34 unbroken years of arrivals, split by purpose and by month, with port of "
        "entry, age and sex, and an average length of stay. Pakistan is still absent from the "
        "published 23-market breakdown, where it is folded into “Others” — but the series "
        "exists, and it is Japan's own.",
        "日本政府観光局（JNTO）の統計データベースには、パキスタンが独立した項目として収録されています。"
        "1992年以降34年間の連続系列に加え、目的別・月別、入国港、年齢・性別、平均泊数まで取得できます。"
        "公表されている23市場の内訳では依然として「その他」に包含されていますが、系列そのものは存在し、"
        "しかも日本側の統計です。",
    )

    panel(
        "flag", "Correction · 訂正",
        "This supersedes <b>Gap 03</b> in the source workbook, which recorded that JNTO publishes "
        "no Pakistan arrivals figure. The precise position is narrower and still useful: Pakistan "
        "<b>is</b> in JNTO's statistics database, and is <b>not</b> in the 23-market published "
        "breakdown, the Data Handbook's 33 markets, or the 24 market-intelligence pages. "
        "Proposal 02 has been narrowed accordingly, from “begin measuring Pakistan” to "
        "“promote Pakistan out of the residual”. Part of Gap 04 is also superseded: an average "
        "length of stay for Pakistan is published, though per-head spending and itinerary "
        "remain unavailable.",
        "本ページは元資料の<b>欠落03</b>（JNTOはパキスタンの入国者数を公表していない）を訂正するものです。"
        "正確には、パキスタンはJNTOの統計データベースには<b>収録されており</b>、公表される23市場の内訳、"
        "データハンドブックの33市場、24の市場分析ページには<b>含まれていません</b>。これに伴い提言02を"
        "「計上を開始すること」から「『その他』から独立させること」へと限定しました。欠落04も一部訂正され、"
        "平均泊数は公表されています（一人当たり消費額・周遊行動は依然として取得できません）。",
    )

    kpis([
        dict(value=fmt(PK_ANN[2025]), accent=True,
             en="JNTO visitor arrivals from Pakistan, 2025",
             ja="訪日外客数（パキスタン、2025年）",
             foot=f"{signed_pct(PK_ANN[2025] / PK_ANN[2024] - 1)} on 2024　2024年比"),
        dict(value=f"{PK_ANN[2025] / JP_ANN[2025] * 100:.3f}", unit="%",
             en="Pakistan's share of Japan's 42.7m arrivals",
             ja="日本の訪日外客数4,268万人に占める割合",
             foot=f"was {PK_ANN[1992] / JP_ANN[1992] * 100:.3f}% in 1992　"
                  "1992年は0.187%"),
        dict(value=f"{PK_PUR[2025]['others'] / PK_PUR[2025]['total'] * 100:.1f}", unit="%",
             en="Neither tourism nor business",
             ja="観光でも商用でもない区分",
             foot=f"{PK_PUR[2019]['others'] / PK_PUR[2019]['total'] * 100:.1f}% in 2019　"
                  "2019年は38.0%"),
        dict(value=f"{LOS[2024]:.1f}", unit=" nights",
             en="Average length of stay, 2024",
             ja="平均泊数（2024年）",
             foot=f"{LOS[2012]:.1f} in 2012　2012年は26.0泊"),
        dict(value=f"{SEX[2024]['male'] / SEX[2024]['total'] * 100:.0f}", unit="%",
             en="Male, of all Pakistani entrants 2024",
             ja="入国者に占める男性の割合（2024年）",
             foot="79% in 2019 too　2019年も79%"),
    ])

    section("01", "Thirty-four unbroken years", "34年間の連続系列",
            "This is the longest Pakistan–Japan travel series in existence, from any publisher "
            "on either side. 2025 is a record at every point in it.",
            "これは、両国いずれの発行機関を通じても存在する最長のパキスタン・日本間渡航系列です。"
            "2025年は全期間を通じた過去最高です。")
    ann_tbl = pd.DataFrame([
        {"Year 年": r["year"], "Visitor arrivals 訪日外客数": r["arrivals"],
         "Growth 前年比": f"{r['growth']:+.1f}%" if r["growth"] is not None else "—",
         "Term 対象期": r["term"]}
        for r in JNTO["pk_annual"]
    ])
    chart_card(
        "Pakistani visitor arrivals to Japan, 1992–2025",
        "訪日外客数（パキスタン）1992〜2025年",
        C.jnto_series(), table=ann_tbl,
        take_en=f"{fmt(PK_ANN[1992])} in 1992 → {fmt(PK_ANN[2025])} in 2025, a 4.5-fold rise. "
                f"The 2019 peak of {fmt(PK_ANN[2019])} was passed in 2023 and has been exceeded "
                f"every year since.",
        take_ja=f"1992年の{fmt(PK_ANN[1992])}人から2025年の{fmt(PK_ANN[2025])}人へ、約4.5倍。"
                f"2019年のピーク{fmt(PK_ANN[2019])}人は2023年に超え、以後毎年更新しています。",
        src=SRC_JNTO,
    )
    panel(
        "caveat", "The part year · 部分年に注意",
        f"January–May 2026 stands at {fmt(PART_2026['arrivals'])} against {fmt(SAME_2025)} in the "
        f"same five months of 2025 — <b>{signed_pct(PART_2026['arrivals'] / SAME_2025 - 1)}</b>, "
        "the first decline in the recovery. One part year is not a trend and the cause is not "
        "established here. It is excluded from the chart above, which shows full years only.",
        f"2026年1〜5月は{fmt(PART_2026['arrivals'])}人で、2025年の同5か月"
        f"（{fmt(SAME_2025)}人）に対し<b>{signed_pct(PART_2026['arrivals'] / SAME_2025 - 1)}</b>と、"
        "回復局面で初めての減少です。部分年をもって趨勢とは言えず、要因も本資料では未確認です。"
        "上図は暦年完全年のみを表示しています。",
    )

    section("02", "The absolute number rose. The share fell.", "実数は増え、シェアは下がった",
            "Japan's inbound total grew twelvefold over the same period while Pakistan grew "
            "4.5-fold. Measured against the market Japan actually built, Pakistan went backwards.",
            "同期間に日本の訪日外客総数は約12倍となった一方、パキスタンは約4.5倍にとどまりました。"
            "日本が実際に築いた市場規模に照らせば、パキスタンの位置づけは後退しています。")
    share_tbl = pd.DataFrame([
        {"Year 年": y, "Pakistan パキスタン": PK_ANN[y], "Japan total 日本計": JP_ANN[y],
         "Pakistan share 構成比": f"{PK_ANN[y] / JP_ANN[y] * 100:.4f}%"}
        for y in JNTO_FULL
    ])
    chart_card(
        "Pakistan as a share of Japan's total visitor arrivals",
        "日本の訪日外客数に占めるパキスタンの割合",
        C.jnto_share_of_japan(), table=share_tbl,
        take_en=f"0.187% in 1992 → {PK_ANN[2025] / JP_ANN[2025] * 100:.3f}% in 2025; the low "
                "point was 0.053% in 2015. This is the headroom argument stated in Japan's own "
                "numbers: to hold its 1992 share, Pakistan would need about "
                f"{fmt(JP_ANN[2025] * PK_ANN[1992] / JP_ANN[1992])} arrivals today. 2023 reads "
                "high because Japan's own recovery was incomplete that year.",
        take_ja=f"1992年の0.187%から2025年の{PK_ANN[2025] / JP_ANN[2025] * 100:.3f}%へ"
                "（最低は2015年の0.053%）。日本側の数字で「伸びしろ」を示す指標であり、1992年当時の"
                f"シェアを維持していれば現在は約{fmt(JP_ANN[2025] * PK_ANN[1992] / JP_ANN[1992])}人に"
                "相当します。2023年が高いのは、日本全体の回復が途上だったためです。",
        src=SRC_JNTO + " 2020–22 are omitted from the chart: Japan's border closure collapsed the "
                       "denominator — Pakistan was 1.7% of a 245,862 total in 2021 — so the ratio "
                       "in those years measures the closure, not the market.",
    )

    section("03", "Over half of it is neither tourism nor business",
            "半数超は観光でも商用でもない",
            "JNTO's definition includes expatriates, their families and international students. "
            "That is why “Other purposes” is the largest and fastest-growing block — and it is "
            "the resident community of page 04 arriving and re-arriving.",
            "JNTOの定義には駐在員とその家族、留学生が含まれます。「その他の目的」が最大かつ最も急増している"
            "区分である理由はここにあり、これは04ページの在留コミュニティの入国・再入国そのものです。")
    pur_tbl = pd.DataFrame([
        {"Year 年": r["year"], "Tourism 観光": r["tourism"], "Business 商用": r["business"],
         "Other purposes その他": r["others"], "Transit 通過": r["transit"] or "—",
         "Total 計": r["total"]}
        for r in JNTO["pk_purpose"]
    ])
    chart_card(
        "Pakistani visitor arrivals by purpose, 2012–2025",
        "目的別 訪日外客数（パキスタン）2012〜2025年",
        C.jnto_purpose_stack(), table=pur_tbl,
        take_en=f"“Other purposes” went from {PK_PUR[2019]['others'] / PK_PUR[2019]['total']:.1%} "
                f"of arrivals in 2019 to {PK_PUR[2025]['others'] / PK_PUR[2025]['total']:.1%} in "
                f"2025. Tourism grew too — {fmt(PK_PUR[2019]['tourism'])} to "
                f"{fmt(PK_PUR[2025]['tourism'])} — but it is no longer the largest block.",
        take_ja=f"「その他の目的」は2019年の{PK_PUR[2019]['others'] / PK_PUR[2019]['total']:.1%}から"
                f"2025年には{PK_PUR[2025]['others'] / PK_PUR[2025]['total']:.1%}へ拡大しました。"
                f"観光も{fmt(PK_PUR[2019]['tourism'])}人から{fmt(PK_PUR[2025]['tourism'])}人へ増えて"
                "いますが、もはや最大区分ではありません。",
        src=SRC_JNTO + " Transit was reported separately only to 2006.",
    )

    section("04", "Four counts of the same year, and why they differ",
            "同じ年の四つの数字 ― その違いの理由",
            "None of these is wrong; they count different populations.",
            "いずれも誤りではなく、それぞれ異なる母集団を数えています。")
    rec_tbl = pd.DataFrame([
        {"Measure 指標": "All entrants, incl. re-entry 入国外国人（再入国を含む）",
         "2025": 37275, "Publisher 発行": "ISA 出入国在留管理庁",
         "What it counts 内容": "every border crossing by a Pakistani passport holder, "
                               "residents of Japan included"},
        {"Measure 指標": "JNTO visitor arrivals 訪日外客数", "2025": PK_ANN[2025],
         "Publisher 発行": "JNTO 日本政府観光局",
         "What it counts 内容": "the above minus permanent residents of Japan and crew, "
                               "plus transit"},
        {"Measure 指標": "New entrants, all statuses 新規入国外国人", "2025": 17863,
         "Publisher 発行": "ISA 出入国在留管理庁",
         "What it counts 内容": "first entries only, any residence status"},
        {"Measure 指標": "Short-stay entries 短期滞在入国", "2025": 11360,
         "Publisher 発行": "ISA 出入国在留管理庁",
         "What it counts 内容": "new entries on short-stay status only"},
        {"Measure 指標": "…of which tourism うち観光目的", "2025": 7053,
         "Publisher 発行": "ISA 出入国在留管理庁",
         "What it counts 内容": "short-stay entries whose stated purpose is tourism"},
    ])
    chart_card(
        "Pakistani arrivals in 2025, on five definitions",
        "2025年のパキスタンからの入国 ― 五つの定義",
        C.population_reconcile(), table=rec_tbl,
        take_en=f"JNTO's {fmt(PK_ANN[2025])} sits between all entrants ({fmt(37275)}) and new "
                f"entrants ({fmt(17863)}); the gap to all entrants — {fmt(37275 - PK_ANN[2025])} "
                "— is broadly the permanent residents of Japan that JNTO removes. The tourism "
                f"figure is {fmt(7053)}. Quoting the largest as “tourists” overstates it "
                f"{37275 / 7053:.1f}-fold.",
        take_ja=f"JNTOの{fmt(PK_ANN[2025])}人は、入国外国人（{fmt(37275)}人）と新規入国"
                f"（{fmt(17863)}人）の間に位置します。入国外国人との差{fmt(37275 - PK_ANN[2025])}人は、"
                f"概ねJNTOが除外する在日永住者にあたります。観光目的は{fmt(7053)}人であり、"
                f"最大の数字を「観光客」として引用すると約{37275 / 7053:.1f}倍の過大評価となります。",
        src=SRC_JNTO + " · " + SRC_IMMIG,
    )

    section("05", "Seasonality", "月別の分布", None, None)
    seas_tbl = pd.DataFrame([
        {"Month 月": m,
         "2019": next((r["arrivals"] for r in JNTO["pk_monthly"]
                       if r["year"] == 2019 and r["month"] == m), None),
         "2025": next((r["arrivals"] for r in JNTO["pk_monthly"]
                       if r["year"] == 2025 and r["month"] == m), None)}
        for m in ["Jan.", "Feb.", "Mar.", "Apr.", "May", "Jun.",
                  "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."]
    ])
    chart_card(
        "Monthly arrivals, 2025 against 2019",
        "月別入国者数：2025年と2019年の比較",
        C.jnto_seasonality(), table=seas_tbl,
        take_en="The profile is flatter than a leisure market's, with no concentration in the "
                "cherry-blossom or autumn-colour months — consistent with business and family "
                "travel.",
        take_ja="レジャー市場に比べて月別の起伏が小さく、桜や紅葉の時期への集中が見られません。"
                "商用・家族訪問型の需要と整合的です。",
        src=SRC_JNTO,
    )

    section("06", "Length of stay", "平均泊数", None, None)
    los_tbl = pd.DataFrame([{"Year 年": r["year"], "Average nights 平均泊数": r["nights"]}
                            for r in JNTO["los"]])
    chart_card(
        "Average length of stay, Pakistani visitors",
        "パキスタンからの訪日客の平均泊数",
        C.jnto_los(), table=los_tbl,
        take_en=f"{LOS[2024]:.1f} nights in 2024, down from {LOS[2012]:.1f} in 2012 — a long "
                "stay converging slowly toward a conventional visitor profile.",
        take_ja=f"2024年は{LOS[2024]:.1f}泊で、2012年の{LOS[2012]:.1f}泊から短縮し、"
                "一般的な訪日客の滞在パターンへ緩やかに近づいています。",
        src="SOURCE · JNTO statistics database, 3-2 Facts on trips to Japan 訪日旅行の実態. "
            "CAVEAT · the derivation of this figure is not stated in the export and JNTO's FAQ "
            "does not cover it. Confirm the basis with JNTO before quoting it as a tourism "
            "statistic. 算出根拠はエクスポートに明示されておらず、引用前にJNTOへの確認が必要です。",
    )

    section("07", "Age and sex of entrants", "入国者の年齢と性別",
            "Age and sex are published for Pakistan too. The profile is working-age and heavily "
            "male — but the children's bands are almost evenly split, which is the family "
            "travel showing up in the data.",
            "年齢・性別もパキスタンについて公表されています。就労年齢層と男性に大きく偏る一方、"
            "子どもの年齢層はほぼ男女均等であり、家族での渡航がデータに現れています。")
    pyr_tbl = pd.DataFrame([
        {"Age band 年齢階層": r["band"], "Male 男性": r["male"], "Female 女性": r["female"],
         "Total 計": r["total"],
         "Share 構成比": f"{r['total'] / SEX[2024]['total'] * 100:.1f}%"}
        for r in JNTO["age_bands_2024"]
    ])
    chart_card(
        "Pakistani entrants to Japan by age and sex, 2024",
        "年齢・性別 パキスタン国籍入国者（2024年）",
        C.jnto_pyramid(), table=pyr_tbl,
        take_en=f"{fmt(SEX[2024]['total'])} entrants in 2024, "
                f"{SEX[2024]['male'] / SEX[2024]['total']:.0%} male. The 25–44 bands alone are "
                "51% of the total. Under-15s are 11% of arrivals and close to an even split — "
                "54% boys against 79% male overall — so the family segment is real and "
                "measurable, not an inference.",
        take_ja=f"2024年の入国者は{fmt(SEX[2024]['total'])}人、うち男性が"
                f"{SEX[2024]['male'] / SEX[2024]['total']:.0%}。25〜44歳だけで全体の51%を占めます。"
                "15歳未満は全体の11%で、男子54%と男女差が小さく（全体では男性79%）、家族層が"
                "推論ではなく実測として確認できます。",
        src="SOURCE · JNTO statistics database, 3-5 Foreigners entries 外国人入国者数 "
            "(JNTO's republication of Immigration Services Agency data). NOTE · in the raw "
            "export the “Total” and “70 -” rows belong to two age groupings and are emitted at "
            "twice their value; they are halved here. After halving, the bands sum to 30,333 — "
            "equal to the port-of-entry total in the companion file — and the 2019 total of "
            "23,709 equals the ISA all-entrants figure in the source workbook exactly.",
    )

    panel(
        "ask", "The ask · 提言",
        "That Pakistan be promoted out of “Others” in JNTO's published market breakdown. The "
        "series already exists, is already compiled monthly, and already carries purpose, port, "
        "age and sex. Nothing has to be built — a market that is in the database but not in the "
        "market list cannot be tracked, targeted or budgeted for by either government.",
        "JNTOの公表市場区分において、パキスタンを「その他」から独立させること。系列はすでに存在し、"
        "月次で作成され、目的別・入国港別・年齢別・性別まで備えています。新たに構築すべきものは"
        "ありません。データベースにありながら市場一覧にない市場は、両国政府とも追跡も、対象設定も、"
        "予算化もできません。",
    )


# ═══════════════════════════════════════════════════════════ 04 THE COMMUNITY
def page_community():
    masthead(
        "03 · The base · 基盤",
        "The resident community behind the travel",
        "渡航を生み出す在留コミュニティ",
        "34,911 Pakistani nationals hold mid- or long-term residence in Japan, nearly double "
        "the 2019 figure. What makes this a travel-generating population rather than a "
        "transient workforce is its composition: 55.9% hold family or settlement status.",
        "在日パキスタン人の中長期在留者は34,911人で、2019年のほぼ2倍です。これを一時的な労働力ではなく"
        "「渡航を生む人口」たらしめているのは構成であり、55.9%が家族・定住系の在留資格を有しています。",
    )

    kpis([
        dict(value=fmt(RES["Dec 2025"]["pk"]),
             en="Pakistani residents, Dec 2025", ja="在日パキスタン人（2025年12月）",
             foot=f"{pct(RES['Dec 2025']['pk'] / RES['Dec 2025']['jp_total'], 3)} of all "
                  f"foreign residents　在留外国人全体比"),
        dict(value="55.9", unit="%", accent=True,
             en="Family or settlement status", ja="家族・定住系の在留資格",
             foot=f"{fmt(CATS['Family + Settlement combined']['n'])} residents　人"),
        dict(value=fmt(15687),
             en="Live in the Kantō ring, not Tokyo", ja="東京都以外の関東周縁部に居住",
             foot="44.9% of all Pakistani residents　全体の44.9%"),
        dict(value="6th",
             en="Tokyo's rank among prefectures", ja="都道府県別で東京都は6位",
             foot=f"{fmt(1962)} residents　人"),
    ])

    section("01", "A population that nearly doubled in six years",
            "6年間でほぼ倍増した在留人口",
            None, None)
    res_tbl = pd.DataFrame([
        {"As at 時点": r["asat"], "Pakistani residents 在留者数": r["pk"],
         "Japan, all foreign residents 在留外国人総数": r["jp_total"] or "—"}
        for r in DATA["residents_ts"]
    ])
    chart_card(
        "Pakistani mid- and long-term residents of Japan",
        "在日パキスタン人（中長期在留者）の推移",
        C.residents_line(), table=res_tbl,
        take_en=f"{fmt(RES['Dec 2019']['pk'])} (Dec 2019) → {fmt(RES['Dec 2025']['pk'])} "
                f"(Dec 2025), {signed_pct(RES['Dec 2025']['pk'] / RES['Dec 2019']['pk'] - 1)}. "
                "Japan's total foreign resident population grew 40.6% over the same period.",
        take_ja=f"2019年12月の{fmt(RES['Dec 2019']['pk'])}人から2025年12月の"
                f"{fmt(RES['Dec 2025']['pk'])}人へ、"
                f"{signed_pct(RES['Dec 2025']['pk'] / RES['Dec 2019']['pk'] - 1)}。同期間の"
                "在留外国人全体の伸びは40.6%でした。",
        src=SRC_RESIDENTS + " NOTE · MOFA's English basic-data page still shows 25,334 (2023); "
                            "cite the Japanese page or the ISA source directly.",
    )

    section("02", "The composition is the argument", "構成こそが論拠",
            "A workforce goes home. A settled community with dependants generates repeat, "
            "multi-generational, visiting-friends-and-relatives travel in both directions.",
            "労働力はいずれ帰国します。扶養家族を伴う定住コミュニティは、双方向かつ世代をまたぐ"
            "反復的な親族訪問需要を生み出します。")
    cat_tbl = pd.DataFrame([
        {"Category 区分": c["cat"], "Residents 在留者数": c["n"],
         "Share 構成比": pct(c["share"])} for c in DATA["res_cats"]
    ])
    chart_card(
        "Pakistani residents by status category, December 2025",
        "在留資格区分別の構成（2025年12月）",
        C.status_category_bar(), table=cat_tbl,
        take_en="Family 33.7% and settlement 22.2% together are 55.9% of the community; work "
                "status is 33.5% and study 7.6%.",
        take_ja="家族33.7%と定住・永住22.2%で全体の55.9%を占めます。就労は33.5%、留学は7.6%です。",
        src=DATA["res_status_src"],
    )

    st_tbl = pd.DataFrame([
        {"Residence status 在留資格": r["en"], "Japanese 日本語": r["ja"],
         "Residents 在留者数": r["n"], "Share 構成比": pct(r["share"]),
         "Category 区分": r["cat"]}
        for r in sorted(DATA["res_status"], key=lambda x: x["n"], reverse=True)
    ])
    chart_card(
        "The eleven largest residence statuses",
        "在留者数上位11の在留資格",
        C.status_detail_bar(), table=st_tbl,
        take_en="Dependant status (家族滞在) is the single largest category at 9,211 — larger "
                "than the main skilled-work status. Permanent residents number 5,616.",
        take_ja="最大区分は「家族滞在」の9,211人で、主要な就労資格を上回ります。永住者は5,616人です。",
        src=DATA["res_status_src"],
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        panel(
            "finding", "Note · 補足",
            "Specified Skilled Worker (i) stands at <b>11</b> against a Japan-wide programme of "
            "382,341 — six years after the bilateral Memorandum of Cooperation was signed. "
            "Working Holiday is zero: Japan has no working-holiday agreement with Pakistan.",
            "特定技能1号は<b>11人</b>にとどまります（制度全体は382,341人）。二国間協力覚書の署名から"
            "6年が経過しています。ワーキングホリデーは0人で、日本とパキスタンの間に同協定はありません。",
        )
    with c2:
        panel(
            "caveat", "Caveat · 留意点",
            "Of the 978 on Designated Activities status, 842 are asylum applications pending — "
            "a distinct population from the travel and settlement figures.",
            "「特定活動」978人のうち842人は難民認定申請中であり、渡航・定住の数値とは性質の異なる"
            "集団です。",
        )

    section("03", "Distribution by prefecture", "都道府県別の分布",
            "Tokyo is sixth. This is a regional footprint, not a metropolitan one.",
            "東京都は6位にすぎません。分布は首都圏一極ではなく地方に広がっています。")
    pref_tbl = pd.DataFrame([
        {"Rank 順位": r["rank"], "Prefecture 都道府県": r["pref"],
         "Residents 在留者数": r["n"], "Share 構成比": pct(r["share"]),
         "Kantō ring 関東周縁": "Yes" if r["kanto"] else ""}
        for r in DATA["prefectures"]
    ])
    chart_card(
        "Pakistani residents by prefecture, December 2025 — top 18",
        "都道府県別 在日パキスタン人（2025年12月、上位18）",
        C.prefecture_bar(), table=pref_tbl,
        take_en="Saitama, Ibaraki, Chiba, Tochigi and Gunma together hold 15,687 residents — "
                "44.9% of the national total, against Tokyo's 5.6%. The Kantō ring plus Toyama "
                "tracks the used-car export trade, which is how this community was largely built.",
        take_ja="埼玉・茨城・千葉・栃木・群馬の5県で15,687人、全国の44.9%を占めます（東京都は5.6%）。"
                "関東周縁部と富山県への集中は中古車輸出業の分布と重なり、それが当コミュニティ形成の"
                "主要な経路でした。",
        src=DATA["pref_src"] + " · Municipality-level detail (Yashio, Misato) is locked in a "
                               "Power Pivot data model in table 25-12-t2.",
    )

    panel(
        "ask", "The ask · 提言",
        "That twinning and regional-tourism proposals be directed at Saitama, Ibaraki, Tochigi, "
        "Gunma and Toyama, where the constituency already exists — not at Tokyo. Japan operates "
        "1,878 local-government partnerships and not one is with Pakistan.",
        "姉妹都市提携および地方観光の提案先を、実際に基盤のある埼玉・茨城・栃木・群馬・富山に向けること"
        "（東京ではなく）。日本の自治体国際提携は1,878件ありますが、パキスタンとの提携は皆無です。",
    )


# ═══════════════════════════════════════════════════════ 04 LEADING INDICATORS
def page_indicators():
    masthead(
        "04 · Intent · 先行指標",
        "Leading indicators of Japan-bound intent",
        "対日渡航意向の先行指標",
        "Language learning and study precede travel; visas and residence measure the flow and "
        "the stock. On every one of these measures Pakistan is growing faster than the "
        "corridor it sits in — from the smallest base in the region.",
        "語学学習と留学は渡航に先行し、査証と在留はフローとストックを示します。これらすべての指標で、"
        "パキスタンは域内最小の基盤から、周辺国を上回る速度で伸びています。",
    )

    kpis([
        dict(value=fmt(LEARN["Learners"]["y2024"]), accent=True,
             en="Japanese-language learners in Pakistan, 2024",
             ja="パキスタンの日本語学習者数（2024年）",
             foot=f"{signed_pct(LEARN['Learners']['chg'])} on 2021 (243)　2021年比"),
        dict(value=fmt(LEARN["Teachers"]["y2024"]),
             en="Japanese-language teachers", ja="日本語教師数",
             foot=f"{signed_pct(LEARN['Teachers']['chg'])} on 2021　2021年比"),
        dict(value=fmt(LEARN["Institutions"]["y2024"]),
             en="Teaching institutions", ja="教育機関数",
             foot=f"{signed_pct(LEARN['Institutions']['chg'])} on 2021　2021年比"),
        dict(value=fmt(455),
             en="Pakistani tertiary students in Japan, 2023",
             ja="在日パキスタン人高等教育留学生（2023年）",
             foot="doubled from 227 in 2019　2019年の227人から倍増"),
        dict(value=fmt(VIS[2025]["total"]),
             en="Visas issued to Pakistani nationals, 2025",
             ja="パキスタン国籍者への査証発給数（2025年）",
             foot=f"{pct(VIS[2025]['share'], 3)} of all Japanese visas　日本の発給総数比"),
    ])

    section("01", "Fastest growth in South Asia, from the smallest base",
            "南アジアで最速の伸び、しかし最小の基盤",
            "The Japan Foundation attributes the regional surge to the Specified Skilled Worker "
            "and Technical Intern Training systems — the causal mechanism supplied by a "
            "Japanese government-affiliated institution rather than inferred here.",
            "国際交流基金は、この域内急増の要因を特定技能制度および技能実習制度に帰しています。"
            "因果の説明は本資料の推論ではなく、日本の政府関係機関自身によるものです。")
    sa_tbl = pd.DataFrame([
        {"Country 国": r["country"], "Learners 2021 学習者数": r["y2021"],
         "Learners 2024 学習者数": r["y2024"], "Growth 増加率": signed_pct(r["growth"]),
         "Teachers 教師数": r["teachers"], "Institutions 機関数": r["inst"]}
        for r in DATA["sasia"]
    ])
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        chart_card(
            "Growth in Japanese-language learners, 2021 → 2024",
            "日本語学習者数の増加率（2021→2024年）",
            C.sasia_growth(), take_en="Pakistan +272.8% — the fastest in South Asia.",
            take_ja="パキスタンは+272.8%で南アジア最速。",
        )
    with c2:
        chart_card(
            "Japanese-language learners, 2024",
            "日本語学習者数（2024年）",
            C.sasia_size(), table=sa_tbl,
            take_en="Pakistan is 0.70% of South Asia's 128,890 learners. Nepal has roughly 28 "
                    "times Pakistan's learners on about an eighth of its population.",
            take_ja="南アジア128,890人のうちパキスタンは0.70%。ネパールは人口が約8分の1ながら、"
                    "学習者数はパキスタンの約28倍です。",
        )
    H('<p class="src" style="margin-top:-2px">SOURCE · The Japan Foundation, Survey Report on '
      'Japanese-Language Education Abroad, South Asia chapter (2024 round, corrected March 2026). '
      'Triennial: the next round is 2027 fieldwork, reporting 2028.　国際交流基金「海外日本語教育機関調査」'
      '南アジア編（2024年度調査、2026年3月修正）。3年ごと実施、次回は2027年調査・2028年公表。</p>')
    panel(
        "finding", "Finding · 所見",
        "Over 1,000 Pakistanis sat the JLPT (Embassy of Japan figure) — more test-takers than "
        "the Japan Foundation counts as enrolled learners. Self-taught demand appears to exceed "
        "measured institutional capacity. The next survey round is 2027 fieldwork, reporting "
        "2028: a 2027 initiative would shape the next data point rather than react to the last.",
        "日本語能力試験（JLPT）の受験者は1,000人超（在パキスタン日本国大使館発表）で、国際交流基金が"
        "把握する在籍学習者数を上回ります。独学による需要が、測定された教育供給を超えている可能性があります。"
        "次回調査は2027年実施・2028年公表であり、2027年の施策は「過去の数値への対応」ではなく"
        "「次の数値の形成」となります。",
    )

    section("02", "Students: Pakistan doubled while Japan's total fell",
            "留学生：日本全体が減少する中でパキスタンは倍増",
            "Both series are indexed to 2013 = 100 so they share one axis. This is the only "
            "reproducible Pakistan–Japan bilateral education series that exists.",
            "両系列は2013年=100として指数化し、単一の軸で比較しています。これは再現可能な唯一の"
            "パキスタン・日本間の教育統計です。")
    stu_tbl = pd.DataFrame([
        {"Year 年": r["year"], "Pakistani students パキスタン人留学生": r["pk"],
         "Japan total inbound 日本の受入留学生総数": r["jp_total"] or "—"}
        for r in DATA["students"]
    ])
    chart_card(
        "Pakistani tertiary students in Japan, indexed against Japan's total inbound",
        "在日パキスタン人高等教育留学生と日本の受入留学生総数（指数比較）",
        C.students_indexed(), table=stu_tbl,
        take_en="227 (2019) → 455 (2023), straight through the pandemic, while Japan's total "
                "inbound student population fell from its 2020 peak of 222,661 to 181,821.",
        take_ja="パキスタン人留学生は227人（2019年）から455人（2023年）へ、コロナ禍を通じて増加。"
                "同期間、日本の受入留学生総数は2020年の222,661人をピークに181,821人へ減少しました。",
        src="SOURCE · UNESCO Institute for Statistics, indicator 26554, geoUnit=JPN. "
            "Tertiary degree-mobile students (ISCED 5–8) only — far smaller than JASSO's "
            "headline and never to be charted alongside it. 2000–2012 is a genuine data gap.",
    )

    section("03", "Visas: the policy finding", "査証：政策上の所見", None, None)
    vis_tbl = pd.DataFrame([
        {"Year 年": r["year"], "Total visas 発給総数": r["total"],
         "of which short-stay うち短期滞在": r["short"],
         "of which online うちオンライン": r["online"],
         "Japan total 日本の発給総数": r["jp_total"] or "—",
         "Pakistan share 構成比": pct(r["share"], 3) if r["share"] else "—"}
        for r in DATA["visas"]
    ])
    chart_card(
        "Visas issued to Pakistani nationals",
        "パキスタン国籍者への査証発給数",
        C.visas_bar(), table=vis_tbl,
        take_en="20,058 visas in 2025, of which 13,611 short-stay. By mission: Islamabad 9,587 "
                "and Karachi 2,244 — so about 8,227 (41%) were issued at posts outside Pakistan, "
                "largely to Gulf residents.",
        take_ja="2025年の発給は20,058件、うち短期滞在13,611件。公館別ではイスラマバード9,587件、"
                "カラチ2,244件であり、約8,227件（41%）はパキスタン国外の公館で発給されています"
                "（主に湾岸諸国在住者）。",
        src="SOURCE · MOFA Japan, Visa Issuance Statistics 査証発給統計, e-Stat 00300500. "
            "Pakistan is named in the Excel file but not in the press release, which shows only "
            "the top ten countries.",
    )
    panel(
        "ask", "The ask · 提言",
        "That Japan's e-visa be made available through Islamabad and Karachi. Both posts "
        "recorded <b>zero</b> online visas in 2025 while 4,402 Pakistani nationals obtained one "
        "elsewhere — a pattern consistent with the e-visa not being offered at the Pakistan "
        "posts. <b>Confirm against MOFA's published eligibility list before asserting this.</b>",
        "日本の電子査証（e-visa）をイスラマバードおよびカラチの公館で利用可能とすること。2025年、両公館の"
        "オンライン発給は<b>ゼロ</b>である一方、他国の公館では4,402件が発給されました。両公館で制度が"
        "提供されていない可能性を示す分布です。<b>断定の前に外務省公表の対象国リストで確認が必要です。</b>",
    )


# ════════════════════════════════════════════════════════════ 05 MONEY, LABOUR
def page_money():
    masthead(
        "05 · Value · 資金と労働",
        "What Pakistan's own institutions publish",
        "パキスタン側の公式統計が示すもの",
        "Pakistan publishes no traveller count to Japan from any source — only value and labour "
        "registrations. These three series are the whole of the Pakistan-side evidence, and "
        "each carries a caveat that has to travel with it.",
        "パキスタン側には対日渡航者数の統計が一切存在せず、公表されるのは金額と労働者登録のみです。"
        "以下の三系列がパキスタン側エビデンスのすべてであり、それぞれ必ず併記すべき留意点があります。",
    )

    beoe25 = next(r for r in DATA["beoe"] if r["year"] == "2025")
    ts = DATA["travel_services"]
    kpis([
        dict(value=fmt(beoe25["total"]),
             en="Workers registered for employment in Japan, 2025",
             ja="対日就労登録者数（2025年）",
             foot=f"{pct(beoe25['total'] / beoe25['all_dest'], 3)} of all destinations　"
                  "全渡航先中"),
        dict(value="14th",
             en="Japan's rank among 54 destinations, 2025",
             ja="全54渡航先中における日本の順位（2025年）",
             foot="between Cyprus (2,393) and China (2,230)"),
        dict(value=f"{DATA['remit'][-1]['japan']:.1f}", unit=" US$m",
             en="Workers' remittances from Japan, FY26",
             ja="日本からの労働者送金（FY26）",
             foot=f"peak was US$85.2m in FY21　FY21の85.2百万ドルがピーク"),
        dict(value=f"{ts[-1]['imports'] / 1000:.1f}", unit=" US$m", accent=True,
             en="Travel-services payments to Japan, FY26",
             ja="対日旅行サービス支払額（FY26）",
             foot=f"{signed_pct(ts[-1]['imports'] / ts[-2]['imports'] - 1)} on FY25 · "
                  f"×{ts[-1]['imports'] / ts[-4]['imports']:.0f} since FY23"),
    ])

    section("01", "Registered labour emigration to Japan", "対日労働者登録の推移",
            None, None)
    beoe_tbl = pd.DataFrame([
        {"Year 年": r["year"], "BE&OE channel": r["beoe"] or "—",
         "OEC channel": r["oec"] or "—", "Total 計": r["total"],
         "All destinations 全渡航先": r["all_dest"] or "—"}
        for r in DATA["beoe"]
    ])
    chart_card(
        "Pakistani workers registered for employment in Japan",
        "対日就労のために登録されたパキスタン人労働者数",
        C.beoe_bar(), table=beoe_tbl,
        take_en="69 in 2014 → 2,244 in 2025. Cumulative 1971–2026: 8,979. The 2021 collapse to "
                "17 is border closure, not a change in demand.",
        take_ja="2014年の69人から2025年の2,244人へ。1971〜2026年の累計は8,979人。2021年の17人への"
                "落ち込みは需要の変化ではなく国境閉鎖によるものです。",
        src="SOURCE · Bureau of Emigration & Overseas Employment, Country Wise Emigrations. "
            "CAVEAT · counts registered labour emigrants through official channels only — no "
            "tourists, students or business travellers — and is a flow of departures, not a "
            "stock of Pakistanis in Japan.",
    )

    section("02", "Remittances — and the break that is not growth",
            "送金 ― 「成長」ではない統計上の断絶",
            None, None)
    rem_tbl = pd.DataFrame([
        {"Fiscal year 会計年度": r["fy"], "From Japan US$m 日本から": r["japan"],
         "Pakistan total US$m 総額": r["total"] or "—",
         "Japan share 構成比": pct(r["share"], 3) if r["share"] else "—",
         "Year-on-year 前年比": signed_pct(r["yoy"]) if r["yoy"] is not None else "—"}
        for r in DATA["remit"]
    ])
    chart_card(
        "Workers' remittances from Japan to Pakistan",
        "日本からパキスタンへの労働者送金額",
        C.remit_line(), table=rem_tbl,
        take_en="The FY19 → FY20 jump is a definitional break, not growth: from July 2019 the "
                "State Bank attributes remittances by the remitter's original country. The "
                "series also peaked in FY21 at US$85.2m and has not returned.",
        take_ja="FY19からFY20への急増は成長ではなく定義変更によるものです（2019年7月以降、国家銀行は"
                "送金元の原国籍ベースで計上）。また同系列はFY21の85.2百万ドルをピークに、その水準へは"
                "戻っていません。",
        src="SOURCE · State Bank of Pakistan, Country-wise Workers' Remittances. "
            "The shaded years to the left of the marked break are not comparable with those "
            "to its right.",
    )

    section("03", "Travel services — the steepest curve in the dataset",
            "旅行サービス収支 ― 本データ中で最も急な曲線",
            None, None)
    ts_tbl = pd.DataFrame([
        {"Fiscal year 会計年度": r["fy"], "Imports from Japan US$'000 対日支払": r["imports"],
         "Exports to Japan US$'000 対日受取": r["exports"], "Net 収支": r["net"],
         "Japan share of travel imports 構成比": pct(r["share"], 3) if r["share"] else "—"}
        for r in DATA["travel_services"]
    ])
    chart_card(
        "Bilateral travel services with Japan",
        "対日 旅行サービス収支",
        C.travel_services(), table=ts_tbl,
        take_en=f"Payments to Japan-resident travel providers grew from US$0.42m in FY23 to "
                f"US${ts[-1]['imports'] / 1000:.1f}m in FY26 — roughly 26-fold, and "
                f"{signed_pct(ts[-1]['imports'] / ts[-2]['imports'] - 1)} in the last year alone.",
        take_ja=f"日本側事業者への支払額はFY23の0.42百万ドルからFY26の"
                f"{ts[-1]['imports'] / 1000:.1f}百万ドルへ、約26倍に拡大しました"
                f"（直近1年だけで{signed_pct(ts[-1]['imports'] / ts[-2]['imports'] - 1)}）。",
        src="SOURCE · State Bank of Pakistan, Import_Count-Arc.xlsx (sheet 'Categ by Count _IMP', "
            "Travel block) and EXP_Count_ARc.xlsx.",
    )
    panel(
        "caveat", "Caveat · 留意点",
        "The State Bank attributes a services import to the counterparty or <b>settlement</b> "
        "country, not the traveller's destination. This measures payments to Japan-resident "
        "providers — airlines, hotels, agencies, card settlements. It is a strong directional "
        "proxy for Pakistani travel spending in Japan, not a measured destination statistic — "
        "and it is value, never headcount. A single large month (March 2026, US$3.99m) moves "
        "the annual figure noticeably; the cause was not investigated.",
        "国家銀行はサービス輸入を渡航先ではなく取引相手国・<b>決済国</b>に計上します。したがって本系列は"
        "日本側事業者（航空会社・ホテル・代理店・カード決済）への支払額を示すものであり、渡航先として測定された"
        "統計ではありません。方向性の代理指標としては有力ですが、金額であって人数ではありません。なお単月"
        "（2026年3月、3.99百万ドル）の影響が年計に無視できない形で現れており、その要因は未調査です。",
    )


# ════════════════════════════════════════════════════════════════ 06 ROUTES
def page_routes():
    masthead(
        "06 · Access · 経路とアクセス",
        "How Pakistani travellers actually reach Japan",
        "パキスタンからの実際の入国経路",
        "There is no non-stop air service between Pakistan and Japan, confirmed from five "
        "airports at both ends. Every one of the 37,275 entries in 2025 was a connection.",
        "パキスタン・日本間に直行便は存在しません（両国5空港で確認）。2025年の37,275件の入国は"
        "すべて乗り継ぎによるものです。",
    )

    kpis([
        dict(value=fmt(PORTS_TOTAL),
             en="Pakistani entrants, 2025 (incl. re-entry)",
             ja="パキスタン国籍者の入国者数（2025年、再入国含む）",
             foot="across 18 ports of entry　18の入国港"),
        dict(value=f"{TOP3_PORTS / PORTS_TOTAL * 100:.1f}", unit="%",
             en="Arrive via Narita, Kansai or Haneda",
             ja="成田・関西・羽田の3空港経由",
             foot=f"{fmt(TOP3_PORTS)} of {fmt(PORTS_TOTAL)} entrants"),
        dict(value="0", accent=True,
             en="Non-stop Pakistan–Japan air services",
             ja="パキスタン・日本間の直行便",
             foot="checked at KHI, ISB, LHE, NRT, HND"),
        dict(value="11",
             en="Carriers offering a single-airline one-stop KHI→NRT",
             ja="カラチ→成田を1社1回乗継で結べる航空会社数",
             foot="narrowing to 5 for Haneda　羽田便では5社"),
    ])

    section("01", "Ports of entry", "入国港別の内訳", None, None)
    port_tbl = pd.DataFrame([
        {"Port of entry 入国港": r["port"], "Entrants 入国者数": r["n"],
         "Share 構成比": pct(r["share"], 2)} for r in DATA["ports"]
    ])
    chart_card(
        "Pakistani entrants to Japan by port of entry, 2025",
        "入国港別 パキスタン国籍者の入国者数（2025年）",
        C.ports_bar(), table=port_tbl,
        take_en="Kansai's 21.0% share is higher than its share of Japan's overall inbound "
                "traffic — consistent with the Osaka-area community and with Expo 2025 traffic "
                "in that year. Narita alone takes 50.5%.",
        take_ja="関西空港の21.0%は、日本全体の入国者に占める同空港の割合を上回ります。大阪圏の"
                "コミュニティおよび2025年の万博需要と整合的です。成田単独で50.5%を占めます。",
        src=DATA["ports_src"] + " All entrants including re-entry, not new entrants only.",
    )

    section("02", "Haneda is taking share from Kansai", "羽田が関西からシェアを奪っている",
            "JNTO republishes the same immigration data as a four-year run, which the single-year "
            "snapshot above cannot show. Haneda has roughly quadrupled since 2022 and overtook "
            "Kansai in 2024.",
            "JNTOは同じ出入国統計を4年間の系列として再公表しており、上記の単年スナップショットでは"
            "見えない変化が読み取れます。羽田は2022年以降およそ4倍となり、2024年に関西を上回りました。")
    jp_tbl = pd.DataFrame([
        {"Year 年": r["year"], **{k: v for k, v in list(r["ports"].items())[:6]}}
        for r in JNTO["jnto_ports"]
    ])
    chart_card(
        "Pakistani entrants by main airport, 2021–2024",
        "主要空港別 パキスタン国籍入国者（2021〜2024年）",
        C.jnto_ports_trend(), table=jp_tbl,
        take_en="Narita's share fell from 75% in 2022 to 54% in 2024 while Haneda rose from 615 "
                "to 6,391, overtaking Kansai.",
        take_ja="成田のシェアは2022年の75%から2024年には54%へ低下する一方、羽田は615人から6,391人へ"
                "増加し、関西を上回りました。",
        src="SOURCE · JNTO statistics database, 3-5 Foreigners entries 外国人入国者数 — JNTO's "
            "republication of Immigration Services Agency data. All entrants including re-entry, "
            "consistent with the 2025 snapshot above.",
    )

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        panel(
            "finding", "Air connectivity · 航空接続",
            "Eleven carriers can offer a single-airline one-stop Karachi–Narita itinerary "
            "(Air China, Batik Air, Biman, Emirates, Ethiopian, Etihad, Qatar, Saudia, "
            "SriLankan, Thai, Turkish), narrowing to five for Haneda. Practical hubs are the "
            "Gulf, Istanbul, Bangkok and two mainland China one-stops. Schedule-derived: "
            "carries no passenger volumes.",
            "カラチ〜成田を1社1回乗継で結べる航空会社は11社（エア・チャイナ、バティック、ビーマン、"
            "エミレーツ、エチオピア、エティハド、カタール、サウディア、スリランカン、タイ、ターキッシュ）、"
            "羽田便では5社に絞られます。実質的なハブは湾岸、イスタンブール、バンコク、中国本土2都市。"
            "スケジュール由来のデータであり、旅客数は含みません。",
        )
    with c2:
        panel(
            "caveat", "Unresolved · 未確認事項",
            "PIA began Tokyo service in 1969 and a 2019 resumption was announced, but whether "
            "it operated and when passenger service ended is unestablished in any source. The "
            "existence of a Japan–Pakistan air services agreement is likewise unresolved.",
            "PIAは1969年に東京線を開設し、2019年に再開が発表されましたが、実際に運航されたか、"
            "旅客運航がいつ終了したかは、いずれの資料でも未確定です。日本・パキスタン航空協定の有無も"
            "同様に未確認です。",
        )

    panel(
        "ask", "The ask · 提言",
        "That air connectivity be placed on the bilateral agenda alongside the visa question. "
        "The connectivity gap and the e-visa gap compound: a traveller from Islamabad currently "
        "needs both a connection and an in-person visa application, where a traveller from a "
        "comparator market needs neither.",
        "航空接続を査証問題と併せて二国間協議の議題とすること。接続の欠如と電子査証の不在は相乗的に作用します。"
        "現状、イスラマバードからの渡航者は乗り継ぎと対面での査証申請の双方を要しますが、比較対象市場の"
        "渡航者はそのいずれも必要としません。",
    )


# ══════════════════════════════════════════════════════════════════ 07 GAPS
def page_gaps():
    masthead(
        "07 · The gaps · 存在しないデータ",
        "What does not exist — stated plainly",
        "存在しないデータ ― 率直な明示",
        "Several of these gaps are not weaknesses in the evidence at all: they are the "
        "argument for action.",
        "以下のうちいくつかはエビデンスの弱点ではなく、行動を求める論拠そのものです。",
    )

    cat_tbl = pd.DataFrame([
        {"Pakistan in the data": s,
         "Sources 件数": sum(1 for r in CATALOGUE if r["Pakistan in the data"] == s),
         "Meaning 意味": m}
        for s, m in [
            ("NAMED", "Pakistan is its own row · 個別に掲載"),
            ("BILATERAL", "a genuine origin-to-destination pair · 二国間の対応あり"),
            ("IN 'OTHER'", "pooled into a residual; no figure extractable at any price · 残差に包含"),
            ("ABSENT", "the data does not exist · データ自体が存在しない"),
            ("UNRESOLVED", "could not be established · 確認できず"),
        ]
    ])
    chart_card(
        f"Where Pakistan stands across all {N_SOURCES} assessed sources",
        f"検証した{N_SOURCES}件の情報源におけるパキスタンの扱い",
        C.catalogue_status_bar(), table=cat_tbl,
        take_en=f"Pakistan can be identified in {N_IDENTIFIABLE} of {N_SOURCES} sources. In 9 "
                "more the data exists but Pakistan is pooled into a residual — no Pakistan "
                "figure can be extracted at any price. In 22 the data does not exist at all.",
        take_ja=f"{N_SOURCES}件中{N_IDENTIFIABLE}件でパキスタンを識別できます。9件はデータは存在するものの"
                "「その他」に包含され、いかなる手段でも数値を取り出せません。22件はデータ自体が存在しません。",
        src="Full source-by-source detail is on the Sources and method page.",
    )

    panel(
        "flag", "Two gaps corrected since compilation · 編集後に訂正された2件",
        "The JNTO exports added on 13 September 2026 supersede <b>Gap 03</b> and part of "
        "<b>Gap 04</b>. Pakistan <b>is</b> a named row in JNTO's statistics database — 34 "
        "unbroken years, by purpose, month, port, age and sex, with an average length of stay. "
        "What remains true, and is what the ask now rests on, is that Pakistan is absent from "
        "every <b>published</b> JNTO market breakdown. Both cards below carry the corrected "
        "text; page 03 sets out the evidence.",
        "2026年9月13日に追加したJNTOのエクスポートにより、<b>欠落03</b>および<b>欠落04</b>の一部を"
        "訂正します。パキスタンはJNTOの統計データベースに独立項目として<b>収録されており</b>、"
        "34年間の連続系列、目的別・月別・入国港別・年齢別・性別、平均泊数まで取得できます。なお有効なのは、"
        "<b>公表される</b>JNTOの市場区分にはパキスタンが一切登場しないという点であり、提言はこれに基づきます。"
        "下記2枚は訂正後の記述です。根拠は03ページに示しています。",
    )

    section("01", "The fourteen confirmed gaps", "確認された14の欠落",
            "Each card states what is missing and how that was established.",
            "各カードは、何が欠落しているか、そしてそれをどう確認したかを示します。")
    gap_ja = {
        1: "パキスタン側に出国観光統計が一切存在しない",
        2: "対日渡航者数を公表するパキスタン側の情報源が存在しない",
        3: "JNTOはパキスタンの入国者数を公表していない",
        4: "パキスタン人の消費額・滞在日数・周遊行動のデータが存在しない",
        5: "国連世界観光機関では当該二国間の組み合わせを取得できない",
        6: "世界銀行はパキスタンの出国者数を一度も保有していない",
        7: "直行便が存在せず、最後の運航終了時期も未確認",
        8: "日本・パキスタン間の姉妹都市提携はゼロ",
        9: "二国間の観光協定・作業部会・覚書が存在しない",
        10: "当該回廊に関する学術研究が存在しない",
        11: "日本の労働・宿泊統計でもパキスタンは残差に包含されている",
        12: "パキスタン観光担当省庁のサイトが開かない",
        13: "JASSOのパキスタン人留学生数を取得できなかった",
        14: "日本・パキスタン航空協定の有無が未確認",
    }
    corrected = {
        3: dict(
            gap="JNTO names Pakistan in its database but in no published market breakdown",
            ja="JNTOはデータベースではパキスタンを個別掲載しているが、公表される市場区分には含めていない",
            detail="JNTO's statistics database carries a named Pakistan row — 34 unbroken years "
                   "of arrivals from 1992, by purpose and by month, with port of entry, age and "
                   "sex, and an average length of stay. In the published 23-market breakdown "
                   "Pakistan's monthly figures appear under “Others”, identical to the person. "
                   "Pakistan is also absent from the Data Handbook's 33 markets and from all 24 "
                   "market-intelligence pages; all 24 annual sheets were searched.",
            ),
        4: dict(
            gap="Length of stay exists; per-head spending and itinerary do not",
            ja="平均泊数は存在するが、一人当たり消費額と周遊行動は存在しない",
            detail="JNTO's Facts on trips to Japan publishes an average length of stay for "
                   "Pakistan, 2012–2024 (12.4 nights in 2024). Per-head spending, prefectures "
                   "visited and repeat rate remain unavailable: the Inbound Consumption Trend "
                   "Survey uses a fixed 24-category split ending in “Other”, and Pakistan is in "
                   "it. All 23 sheets searched. The derivation of the length-of-stay figure is "
                   "not stated in the export — confirm with JNTO before quoting it.",
            ),
    }
    cards = []
    for g in DATA["gaps"]:
        c = corrected.get(g["n"])
        title = c["gap"] if c else g["gap"]
        ja = c["ja"] if c else gap_ja.get(g["n"], "")
        detail = c["detail"] if c else g["detail"]
        badge = '<span class="rev">corrected 13 Sep 2026</span>' if c else ""
        cards.append(
            f'<div class="gcard{" corrected" if c else ""}"><p class="n">GAP {g["n"]:02d}'
            f"{badge}</p>"
            f'<h4>{title}</h4><p class="ja">{ja}</p>'
            f'<p class="d">{detail}</p></div>'
        )
    H(f'<div class="cards">{"".join(cards)}</div>')

    section("02", "Two unresolved items in the source record",
            "出典上の未確定事項2件", None, None)
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        panel(
            "flag", "Confirm first · 要確認",
            "MOFA's English-language Japan–Pakistan basic-data page appears to have its trade "
            "direction labels transposed against its own commodity lists. The Japanese page "
            "reads correctly and is about eighteen months fresher.",
            "外務省の日本・パキスタン基礎データ英語版は、自らの品目一覧と照合すると貿易の方向表示が"
            "入れ替わっている可能性があります。日本語版は正しく、かつ約1年半新しいものです。",
        )
    with c2:
        panel(
            "flag", "Confirm first · 要確認",
            "The PIA Tokyo route: service began in 1969 and a 2019 resumption was announced, "
            "but whether it operated and when passenger service ended is unestablished. No "
            "non-stop service exists today, and no end date is established in any source.",
            "PIA東京線について：1969年に開設され、2019年に再開が発表されましたが、実際の運航の有無と"
            "旅客運航の終了時期は未確定です。現在直行便は存在せず、終了時期を示す資料も確認できて"
            "いません。",
        )


# ═════════════════════════════════════════════════════════════ 08 PROPOSALS
PROPOSALS = [
    dict(
        en="A bilateral tourism instrument — a memorandum or a standing working group",
        ja="二国間の観光枠組み ― 覚書または常設作業部会の設置",
        body_en="There is nothing on MOFA's Pakistan record, nothing in the Economic Policy "
                "Dialogue and nothing on the Tourism Agency's pages. The 2019 Specified Skilled "
                "Worker Memorandum of Cooperation is the only signed mobility instrument between "
                "the two countries and it has no tourism limb. Japan has concluded tourism "
                "instruments with comparable partners; the Philippines model is the closest fit.",
        body_ja="外務省のパキスタン関連記録、経済政策対話、観光庁の各ページのいずれにも該当する枠組みは"
                "ありません。2019年の特定技能に関する協力覚書が両国唯一の署名済み人の移動に関する文書で"
                "あり、観光に関する条項を含みません。日本は同等の相手国と観光分野の文書を締結しており、"
                "フィリピンとの枠組みが最も近いモデルです。",
        ev="Gap 09 · MOFA Japan–Pakistan record; Economic Policy Dialogue; Japan Tourism Agency",
        pill="Headline proposal", hot=True),
    dict(
        en="That JNTO promote Pakistan out of “Others” in its published market breakdowns",
        ja="JNTOの公表市場区分において、パキスタンを「その他」から独立させること",
        body_en="This costs nothing to compile, because it is already compiled. JNTO's statistics "
                "database carries a named Pakistan row back to 1992 — monthly, by purpose, by "
                "port, by age and sex, with an average length of stay. What it does not carry is "
                "Pakistan in the published 23-market breakdown, where the same monthly figures "
                "appear under “Others”; nor in the Data Handbook's 33 markets; nor in any of the "
                "24 market-intelligence pages. A market that is in the database but not in the "
                "market list cannot be tracked, targeted or budgeted for by either government.",
        body_ja="集計の追加費用は生じません。すでに集計されているからです。JNTOの統計データベースには"
                "1992年以降のパキスタンの系列が独立項目として存在し、月次・目的別・入国港別・年齢別・"
                "性別、平均泊数まで備えています。欠けているのは公表側で、23市場の内訳では同じ月次数値が"
                "「その他」として現れ、データハンドブックの33市場にも、24の市場分析ページにも登場しません。"
                "データベースにありながら市場一覧にない市場は、両国政府とも追跡・対象設定・予算化が"
                "できません。",
        ev="Gap 03, corrected · JNTO statistics database 3-1 Visitor arrivals; 23-market "
           "breakdown; Data Handbook; market intelligence pages",
        pill="Nothing to build", hot=True),
    dict(
        en="A first Japan–Pakistan sister-city link, through CLAIR",
        ja="CLAIRを通じた日本・パキスタン間初の姉妹都市提携",
        body_en="None of Japan's 1,878 local-government partnerships is with Pakistan, while "
                "India has 7, Nepal 5, Sri Lanka 3, Bangladesh 1 and Bhutan 1. This was "
                "re-checked with a targeted enumeration to confirm the absence. CLAIR runs a "
                "standing partner-seeking page, and the natural Japanese counterparties are the "
                "prefectures where the community already lives: Saitama, Ibaraki, Tochigi, "
                "Gunma and Toyama.",
        body_ja="日本の自治体国際提携1,878件のうちパキスタンとの提携は皆無です（インド7件、ネパール5件、"
                "スリランカ3件、バングラデシュ1件、ブータン1件）。不在であることは個別列挙により再確認しました。"
                "CLAIRは提携先募集の常設ページを運営しており、日本側の自然な相手方はコミュニティが集中する"
                "埼玉・茨城・栃木・群馬・富山の各県です。",
        ev="Gap 08 · CLAIR sister-city register, by country · Residents by prefecture, ISA Dec 2025",
        pill="Cheapest to fix", hot=True),
    dict(
        en="E-visa availability through the Islamabad and Karachi posts",
        ja="イスラマバード・カラチ両公館における電子査証の提供",
        body_en="Both Pakistan posts recorded zero online visas in 2025 while 4,402 Pakistani "
                "nationals obtained one elsewhere — largely Gulf residents applying at other "
                "posts. Online issuance is the single highest-leverage friction point, because "
                "it is the one that applies to every traveller regardless of purpose. This is a "
                "strong inference from the issuance data and must be confirmed against MOFA's "
                "published eligibility list before it is asserted.",
        body_ja="2025年、パキスタン国内2公館のオンライン発給はゼロである一方、他国の公館では4,402件が"
                "発給されました（主に湾岸在住者）。オンライン発給は渡航目的を問わずすべての渡航者に及ぶため、"
                "最も効果の大きい摩擦要因です。これは発給統計からの強い推論であり、断定の前に外務省公表の"
                "対象国リストによる確認を要します。",
        ev="Leading indicators C · MOFA Visa Issuance Statistics, e-Stat 00300500",
        pill="Confirm first", hot=False),
    dict(
        en="Use the existing anniversary-campaign vehicle rather than building a new one",
        ja="新規の枠組みではなく既存の周年キャンペーン制度を活用すること",
        body_en="The Japan Tourism Agency maintains a standing, budgeted, contractor-delivered "
                "model for anniversary-linked bilateral tourism promotion — the SJ60 exhibition "
                "programme, whose applications ran 19 August to 2 September 2026, actively "
                "solicits Japanese regional participation. It is a funded vehicle that could "
                "carry a Pakistan campaign without new machinery. Note it runs one-directionally, "
                "promoting Japanese regions to the partner market.",
        body_ja="観光庁は周年事業と連動した二国間観光プロモーションについて、予算措置と受託事業者を伴う常設の"
                "枠組みを維持しています。SJ60展示事業（応募期間2026年8月19日〜9月2日）は日本の地方自治体の"
                "参加を積極的に募っており、新たな制度を設けずにパキスタン向け施策を載せられる既存の"
                "受け皿です。ただし当該事業は日本の地方を相手国市場に売り込む一方向の設計です。",
        ev="Catalogue 02 · Japan Tourism Agency (MLIT), SJ60 anniversary exhibition programme",
        pill="No new machinery", hot=False),
    dict(
        en="Support the first research on this corridor, and close two open questions",
        ja="当該回廊に関する最初の研究支援と、未解決2点の確定",
        body_en="Japan's own national journal platform holds no study of Pakistani nationals as "
                "international tourists or of their travel to Japan. Two outstanding retrievals "
                "would also strengthen the base materially: JASSO's Pakistani student count, "
                "and MOFA's treaty database on the air services agreement.",
        body_ja="日本の学術論文プラットフォームには、パキスタン国籍者の国際観光行動や対日渡航に関する研究が"
                "存在しません。また未取得の2件 ― JASSOのパキスタン人留学生数と、外務省条約検索による"
                "航空協定の有無 ― を確定できれば、基礎資料は実質的に強化されます。",
        ev="Gaps 10, 13, 14 · J-STAGE / CiNii search; JASSO annual survey; MOFA treaty database",
        pill="Low cost", hot=False),
]


def page_proposals():
    masthead(
        "08 · The ask · 提言",
        "Six proposals, each with the figure it rests on",
        "六つの提言 ― それぞれの根拠となる数値とともに",
        "Nothing here asks for a new dataset to be invented or a new institution to be built. "
        "Each proposal either names something that already exists and is not being used, or "
        "closes a gap that was confirmed to be a gap.",
        "いずれも新たな統計の創設や新組織の設立を求めるものではありません。各提言は、すでに存在しながら"
        "活用されていない仕組みを指すか、確認済みの欠落を埋めるものです。",
    )
    for i, p in enumerate(PROPOSALS, 1):
        H(
            f'<div class="pcard"><div class="row1"><span class="idx">{i:02d}</span>'
            f'<h4>{p["en"]}</h4>'
            f'<span class="pill{" hot" if p["hot"] else ""}">{p["pill"]}</span></div>'
            f'<p class="ja">{p["ja"]}</p><div class="body"><p>{p["body_en"]}</p>'
            f'<p class="ja" style="font-family:var(--ja);font-size:12.5px;color:var(--ink-3);'
            f'line-height:1.8">{p["body_ja"]}</p>'
            f'<p class="ev"><b>EVIDENCE ·</b> {p["ev"]}</p></div></div>'
        )

    panel(
        "caveat", "What this evidence cannot support · 本資料が支えられない主張",
        "No claim about per-head spending, length of stay, itinerary or repeat rate: the "
        "Inbound Consumption Trend Survey pools Pakistan into “Other” and all 23 sheets were "
        "searched. No claim of a Pakistan-to-Japan tourism figure from a Pakistani official "
        "source: none exists. No dated claim about the PIA Tokyo route.",
        "一人当たり消費額・滞在日数・周遊行動・リピート率に関する主張は行えません（訪日外国人消費動向調査は"
        "パキスタンを「その他」に包含。23シートすべてを検索済み）。パキスタン公式統計に基づく対日観光客数も"
        "主張できません（存在しないため）。PIA東京線に関する年月を伴う主張も行えません。",
    )


# ═══════════════════════════════════════════════════════════ 09 SOURCES
def page_sources():
    masthead(
        "09 · Provenance · 出典",
        "Sources and method",
        "出典と方法",
        f"All {N_SOURCES} assessed sources, one row each, filterable. VERIFIED means the figure "
        "was extracted from the publisher's own file during compilation, not from a secondary "
        "citation. NOT REACHED means the source could not be opened.",
        f"検証した{N_SOURCES}件の情報源を1行ずつ収録し、絞り込み可能です。VERIFIEDは、当該数値を編集時に"
        "発行機関の原典ファイルから直接取得したことを意味します（二次引用ではありません）。NOT REACHEDは"
        "情報源を開けなかったことを意味します。",
    )

    df = pd.DataFrame(CATALOGUE)
    c1, c2, c3 = st.columns([1.1, 1.1, 2], gap="medium")
    with c1:
        fam = st.multiselect("Family · 分類", sorted(df["Family"].dropna().unique()), [])
    with c2:
        status = st.multiselect(
            "Pakistan in the data · パキスタンの扱い",
            ["NAMED", "BILATERAL", "IN 'OTHER'", "ABSENT", "UNRESOLVED"], [])
    with c3:
        q = st.text_input("Search source, publisher or caveat · 検索", "")

    view = df.copy()
    if fam:
        view = view[view["Family"].isin(fam)]
    if status:
        view = view[view["Pakistan in the data"].isin(status)]
    if q:
        mask = view.apply(
            lambda r: q.lower() in " ".join(str(v) for v in r.values).lower(), axis=1)
        view = view[mask]

    H(f'<p class="src" style="margin:4px 0 8px">Showing <b>{len(view)}</b> of {N_SOURCES} '
      f'sources　{N_SOURCES}件中{len(view)}件を表示</p>')
    st.dataframe(
        view[["#", "Family", "Source", "Publisher", "Pakistan in the data",
              "Verification", "Key caveat", "URL"]],
        hide_index=True, **stretch(height=458),
        column_config={
            "#": st.column_config.NumberColumn("#", width=40),
            "Family": st.column_config.TextColumn("Family 分類", width=104),
            "Source": st.column_config.TextColumn("Source 情報源", width=190),
            "Publisher": st.column_config.TextColumn("Publisher 発行機関", width=162),
            "Pakistan in the data": st.column_config.TextColumn("Pakistan 扱い", width=96),
            "Verification": st.column_config.TextColumn("Verified 検証", width=86),
            "Key caveat": st.column_config.TextColumn("Key caveat 主な留意点", width=298),
            "URL": st.column_config.LinkColumn("URL", display_text="open", width=56),
        },
    )
    H('<p class="src" style="margin:6px 0 0">Coverage, granularity, update frequency, format, '
      'language and the Japanese source name are carried for every row in the workbook; the '
      'columns above are the ones most often needed. Click any caveat cell to read it in '
      'full.　対象範囲・粒度・更新頻度・形式・言語・原語名称は元データに収録済みです。'
      '留意点はセルをクリックすると全文が表示されます。</p>')

    section("01", "Added since compilation · JNTO", "編集後に追加した情報源 ― JNTO",
            "Eight JNTO statistics-database exports were added on 13 September 2026. They "
            "supersede Gap 03 and part of Gap 04, and they are the basis of page 03.",
            "2026年9月13日にJNTO統計データベースのエクスポート8件を追加しました。これにより欠落03および"
            "欠落04の一部を訂正し、03ページの根拠としています。")
    st.dataframe(
        pd.DataFrame([
            {"Dataset データセット": "3-1 Visitor arrivals 訪日外客数 — Pakistan, annual",
             "Coverage 対象範囲": "1992–2025 full years, 2026 Jan–May",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-1 Visitor arrivals — Pakistan, monthly",
             "Coverage 対象範囲": "1992–2026, 420 observations",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-1 Visitor arrivals — Pakistan, by purpose",
             "Coverage 対象範囲": "1992–2025; transit reported to 2006",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-1 Visitor arrivals — 23-market breakdown",
             "Coverage 対象範囲": "1992–2026 monthly",
             "Pakistan パキスタン": "IN 'OTHER'", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-1 Visitor arrivals — Japan total & Japanese outbound",
             "Coverage 対象範囲": "1973–2026",
             "Pakistan パキスタン": "n/a", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-2 Facts on trips to Japan — average length of stay",
             "Coverage 対象範囲": "2012–2024",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "BASIS UNCONFIRMED"},
            {"Dataset データセット": "3-5 Foreigners entries — by port of entry",
             "Coverage 対象範囲": "2021–2024, 131 ports",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "VERIFIED"},
            {"Dataset データセット": "3-5 Foreigners entries — by age and sex",
             "Coverage 対象範囲": "2013–2024",
             "Pakistan パキスタン": "NAMED", "Verified 検証": "VERIFIED, EXPORT CORRECTED"},
        ]), hide_index=True, **stretch(height=35 * 9 + 3))
    H('<p class="src">RETRIEVE · statistics.jnto.go.jp — Japan Tourism Statistics, free, no '
      'registration. Definition of Visitor Arrivals from the same site\'s FAQ, retrieved '
      '13 September 2026: compiled by nationality; excludes permanent residents whose primary '
      'place of residence is Japan, and crew; includes expatriates, their families, '
      'international students and transit; each entry counted as one.<br>'
      'EXPORT CORRECTION · in the age-and-sex file the “Total” and “70 -” rows belong to two age '
      'groupings and are emitted at twice their value. They are halved. After halving, the bands '
      'sum to 30,333 for 2024 — equal to the port-of-entry total in the companion file — and the '
      '2019 total of 23,709 equals the ISA all-entrants figure in the source workbook exactly.　'
      '年齢・性別ファイルの「Total」「70 -」行は2つの年齢区分に属するため2倍で出力されており、'
      '本ダッシュボードでは半分に補正しています。</p>')

    section("02", "Reproduce every number yourself", "すべての数値の再現手順",
            "Japan's e-Stat serves statistical tables through a stable download endpoint. "
            "Everything below is free and needs no registration. Tables are Japanese-only; "
            "Pakistan is the row パキスタン.",
            "日本のe-Statは安定したダウンロード用エンドポイントを提供しています。以下はすべて無料で、"
            "登録も不要です。表は日本語のみで、パキスタンは「パキスタン」の行にあります。")
    H('<p class="src" style="margin:0 0 10px">PATTERN · '
      'https://www.e-stat.go.jp/stat-search/file-download?statInfId=&lt;ID&gt;&amp;fileKind=&lt;KIND&gt;'
      '　Annual releases land in late July for the prior calendar year; monthly data runs about '
      'two months behind.</p>')
    st.dataframe(
        pd.DataFrame([
            {"statInfId": r["id"], "Table 表番号": r["table"], "Content 内容": r["content"],
             "Period 対象期": r["period"], "fileKind": r["kind"]}
            for r in DATA["estat"]
        ]), hide_index=True, **stretch(height=35 * (len(DATA["estat"]) + 1) + 3))

    section("03", "Direct files", "直接取得先", None, None)
    st.dataframe(
        pd.DataFrame(DATA["urls"]).rename(columns={"source": "Source 情報源", "url": "URL"}),
        hide_index=True, **stretch(height=35 * (len(DATA["urls"]) + 1) + 3),
        column_config={"URL": st.column_config.LinkColumn("URL", display_text="open")})

    rule()
    H('<p class="src">COMPILED · 10 September 2026 from the workbook '
      '<b>Pakistan-Japan-Travel-Data.xlsx</b>. Figures in this dashboard are embedded at build '
      'time and do not update automatically. Chart palette validated for colour-vision '
      'deficiency (adjacent-pair ΔE 9.9 minimum, OKLab ×100).　'
      '本ダッシュボードの数値は作成時点で埋め込まれており、自動更新はされません。</p>')


# ═════════════════════════════════════════════════════════════════ NAVIGATION
PAGES = {
    "01　Overview · 概観": page_overview,
    "02　Who travels, and why · 誰が、なぜ": page_who,
    "03　JNTO's Pakistan series · JNTOの統計": page_jnto,
    "04　The resident community · 在留コミュニティ": page_community,
    "05　Leading indicators · 先行指標": page_indicators,
    "06　Money and labour · 送金・労働": page_money,
    "07　Routes and access · 経路とアクセス": page_routes,
    "08　What does not exist · 存在しないデータ": page_gaps,
    "09　The proposals · 提言": page_proposals,
    "10　Sources and method · 出典と方法": page_sources,
}

with st.sidebar:
    H(
        '<div class="side-brand"><p class="kicker">Embassy briefing · Tokyo</p>'
        "<h2>Pakistan–Japan<br>Travel Data</h2>"
        '<p class="ja">パキスタン・日本 渡航データ<br>東京 大使館ブリーフィング</p></div>'
    )
    choice = st.radio("Navigation", list(PAGES), label_visibility="collapsed")
    H(
        '<div class="side-note"><b>COMPILED</b> 10 Sep 2026<br>'
        "<b>JNTO DATA ADDED</b> 13 Sep 2026<br>"
        f"<b>SOURCES ASSESSED</b> {N_SOURCES} + 8<br>"
        f"<b>PAKISTAN IDENTIFIABLE IN</b> {N_IDENTIFIABLE} + JNTO<br><br>"
        "<b>ENTRIES, NOT PEOPLE</b><br>Japan's immigration data counts border crossings.<br><br>"
        "<b>NATIONALITY, NOT RESIDENCE</b><br>Taken from the passport, so Gulf-resident "
        "Pakistanis count as Pakistan. JNTO compiles on the same basis.</div>"
    )

PAGES[choice]()
