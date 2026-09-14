"""Verification pass — recomputes every headline figure in the dashboard
from the embedded data. Run `python verify.py` after any data refresh.
数値検証スクリプト：ダッシュボード本文の主要数値を埋め込みデータから再計算します。
"""

from data import DATA
from jnto_data import JNTO

A = {r["year"]: r for r in DATA["arrivals"]}
W = {r["year"]: r for r in DATA["japan_ww"]}
R = {r["asat"]: r for r in DATA["residents_ts"]}
C = {c["cat"]: c for c in DATA["res_cats"]}
V = {r["year"]: r for r in DATA["visas"]}
S = {r["country"]: r for r in DATA["sasia"]}
ts, ports, cat = DATA["travel_services"], DATA["ports"], DATA["catalogue"]

PK = {r["year"]: r["arrivals"] for r in JNTO["pk_annual"]}
JP = {r["year"]: r["inbound"] for r in JNTO["jp_annual"]}
PUR = {r["year"]: r for r in JNTO["pk_purpose"]}
SEX = {r["year"]: r for r in JNTO["entries_by_sex"]}
LOS = {r["year"]: r["nights"] for r in JNTO["los"]}
JPORTS = {r["year"]: r["ports"] for r in JNTO["jnto_ports"]}


def chk(label, got, want, tol=5e-4):
    ok = abs(got - want) <= tol * max(1, abs(want))
    print(("PASS  " if ok else "FAIL  ") + f"{label:<42} got={got:,.4f}  want={want:,.4f}")
    return ok


def main():
    tot_ports = sum(r["n"] for r in ports)
    b25 = next(r for r in DATA["beoe"] if r["year"] == "2025")
    kanto = sum(r["n"] for r in DATA["prefectures"] if r["kanto"])
    results = [
        chk("short-stay entries 2025", A[2025]["total"], 11360),
        chk("short-stay change 2019→2025", A[2025]["total"] / A[2019]["total"] - 1, 0.2755, 1e-3),
        chk("tourism share 2025", A[2025]["tourism"] / A[2025]["total"], 0.6209, 1e-3),
        chk("Japan worldwide tourism share", W[2025]["tourism"] / W[2025]["total"], 0.9425, 1e-3),
        chk("business over-index ratio",
            (A[2025]["business"] / A[2025]["total"]) / (W[2025]["business"] / W[2025]["total"]),
            9.54, 1e-2),
        chk("VFR over-index ratio",
            (A[2025]["vfr"] / A[2025]["total"]) / (W[2025]["vfr"] / W[2025]["total"]), 9.617, 1e-2),
        chk("share of Japan's tourist entries %", A[2025]["tourism"] / W[2025]["tourism"] * 100,
            0.019, 5e-2),
        chk("business growth 2019→2025", A[2025]["business"] / A[2019]["business"] - 1, 0.331, 1e-2),
        chk("Pakistani residents Dec 2025", R["Dec 2025"]["pk"], 34911),
        chk("residents growth 2019→2025", R["Dec 2025"]["pk"] / R["Dec 2019"]["pk"] - 1, 0.965, 1e-3),
        chk("Japan foreign-resident growth",
            R["Dec 2025"]["jp_total"] / R["Dec 2019"]["jp_total"] - 1, 0.406, 2e-3),
        chk("family + settlement share", C["Family + Settlement combined"]["share"], 0.559, 1e-2),
        chk("Kantō ring residents", kanto, 15687),
        chk("Kantō ring share", kanto / 34911, 0.449, 1e-2),
        chk("Tokyo prefecture rank",
            next(r["rank"] for r in DATA["prefectures"] if r["pref"] == "Tokyo"), 6),
        chk("entrants 2025 (all ports)", tot_ports, 37275),
        chk("top-3 airports share", sum(r["n"] for r in ports[:3]) / tot_ports, 0.911, 1e-2),
        chk("language-learner growth 2021→2024", S["Pakistan"]["growth"], 2.728, 1e-2),
        chk("Pakistan share of S Asia learners",
            S["Pakistan"]["y2024"] / S["South Asia total"]["y2024"], 0.00703, 1e-2),
        chk("visas issued 2025", V[2025]["total"], 20058),
        chk("visas issued outside Pakistan", V[2025]["total"] - 9587 - 2244, 8227),
        chk("…as a share of all visas", (V[2025]["total"] - 9587 - 2244) / V[2025]["total"],
            0.41, 1e-2),
        chk("BEOE registrations for Japan 2025", b25["total"], 2244),
        chk("…share of all destinations", b25["total"] / b25["all_dest"], 0.002939, 1e-3),
        chk("travel-services imports FY26 US$m", ts[-1]["imports"] / 1000, 11.0, 1e-2),
        chk("…growth on FY25", ts[-1]["imports"] / ts[-2]["imports"] - 1, 0.769, 1e-2),
        chk("…multiple since FY23", ts[-1]["imports"] / ts[-4]["imports"], 26.4, 1e-2),
        chk("remittances from Japan FY26 US$m", DATA["remit"][-1]["japan"], 67.62),
        chk("sources in catalogue", len(cat), 63),
        chk("sources naming Pakistan",
            sum(1 for r in cat if r["Pakistan in the data"] in ("NAMED", "BILATERAL")), 25),
        chk("Pakistani students in Japan 2023",
            next(r["pk"] for r in DATA["students"] if r["year"] == 2023), 455),
        chk("Japan inbound-student peak (2020)",
            max(r["jp_total"] for r in DATA["students"] if r["jp_total"]), 222661),

        # ── JNTO, added 13 September 2026 ────────────────────────────────────
        chk("JNTO visitor arrivals 2025", PK[2025], 30171),
        chk("…growth on 2024", PK[2025] / PK[2024] - 1, 0.2725, 1e-3),
        chk("…rise since 1992", PK[2025] / PK[1992], 4.50, 1e-2),
        chk("share of Japan's arrivals 2025 %", PK[2025] / JP[2025] * 100, 0.0707, 1e-2),
        chk("share of Japan's arrivals 1992 %", PK[1992] / JP[1992] * 100, 0.1874, 1e-2),
        chk("arrivals needed to hold 1992 share",
            JP[2025] * PK[1992] / JP[1992], 79988, 1e-3),
        chk("'other purposes' share 2025", PUR[2025]["others"] / PUR[2025]["total"], 0.511, 1e-2),
        chk("'other purposes' share 2019", PUR[2019]["others"] / PUR[2019]["total"], 0.380, 1e-2),
        chk("JNTO purpose rows sum to the total",
            PUR[2025]["tourism"] + PUR[2025]["business"] + PUR[2025]["others"], PK[2025]),
        chk("monthly rows sum to the annual total",
            sum(r["arrivals"] for r in JNTO["pk_monthly"] if r["year"] == 2025), PK[2025]),
        chk("average length of stay 2024", LOS[2024], 12.44, 1e-3),

        # the two export corrections, checked against independent sources
        chk("age/sex 2024 total = port total", SEX[2024]["total"], JPORTS[2024]["Total"]),
        chk("age bands 2024 sum to the sex total",
            sum(b["total"] for b in JNTO["age_bands_2024"]), SEX[2024]["total"]),
        chk("age/sex 2019 total = ISA all-entrants 2019", SEX[2019]["total"], 23709),
        chk("male share 2024", SEX[2024]["male"] / SEX[2024]["total"], 0.789, 1e-2),
        chk("25–44 share of 2024 entrants",
            sum(b["total"] for b in JNTO["age_bands_2024"]
                if b["band"] in ("25 - 29", "30 - 34", "35 - 39", "40 - 44"))
            / SEX[2024]["total"], 0.513, 1e-2),
        chk("under-15 share of 2024 entrants",
            sum(b["total"] for b in JNTO["age_bands_2024"]
                if b["band"] in ("0 - 4", "5 - 9", "10 - 14")) / SEX[2024]["total"], 0.110, 1e-2),
        chk("under-15 boys share",
            sum(b["male"] for b in JNTO["age_bands_2024"]
                if b["band"] in ("0 - 4", "5 - 9", "10 - 14"))
            / sum(b["total"] for b in JNTO["age_bands_2024"]
                  if b["band"] in ("0 - 4", "5 - 9", "10 - 14")), 0.541, 1e-2),
        chk("Haneda 2024", JPORTS[2024]["Haneda"], 6391),
        chk("Narita share 2024", JPORTS[2024]["Narita"] / JPORTS[2024]["Total"], 0.540, 1e-2),
    ]
    print(f"\n{sum(results)} / {len(results)} checks passed")
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
