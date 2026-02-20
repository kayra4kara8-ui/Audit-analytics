"""
╔══════════════════════════════════════════════════════════════════════╗
║        İÇ DENETİM VERİ ANALİTİĞİ PLATFORMU v2.0                    ║
║        - Evrensel kolon tanıma (herhangi bir şirket verisi)         ║
║        - Yönetici özeti: temiz Streamlit bileşenleri                ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════
# SAYFA AYARLARI
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="İç Denetim Analitik Platformu",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# TEMA / CSS
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp { background: #0a0e1a; color: #f1f5f9; }

section[data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid #1e2a42 !important;
}

.au-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 60%, #0f172a 100%);
    border: 1px solid #3730a3; border-radius: 12px;
    padding: 26px 34px; margin-bottom: 22px;
}
.au-badge {
    display: inline-block;
    background: rgba(99,102,241,.18); border: 1px solid #6366f1; color: #a5b4fc;
    padding: 3px 10px; border-radius: 20px; font-size: .72rem;
    font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; margin-bottom: 6px;
}
.au-header h1 { font-size: 1.7rem; font-weight: 700; margin: 0; color: #f1f5f9; }
.au-header p  { color: #94a3b8; font-size: .87rem; margin: 5px 0 0 0; }

.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 14px; margin-bottom: 22px;
}
.kpi-card {
    background: #1a2235; border: 1px solid #1e2a42;
    border-radius: 10px; padding: 18px 22px;
    position: relative; overflow: hidden;
}
.kpi-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; border-radius: 10px 10px 0 0;
}
.kpi-card.blue::after   { background: #3b82f6; }
.kpi-card.red::after    { background: #ef4444; }
.kpi-card.amber::after  { background: #f59e0b; }
.kpi-card.green::after  { background: #10b981; }
.kpi-label { font-size:.72rem; font-weight:600; letter-spacing:1px;
             text-transform:uppercase; color:#94a3b8; margin-bottom:6px; }
.kpi-value { font-size:1.9rem; font-weight:700;
             font-family:'IBM Plex Mono',monospace; line-height:1; }
.kpi-card.blue .kpi-value  { color:#3b82f6; }
.kpi-card.red .kpi-value   { color:#ef4444; }
.kpi-card.amber .kpi-value { color:#f59e0b; }
.kpi-card.green .kpi-value { color:#10b981; }
.kpi-sub { font-size:.78rem; color:#475569; margin-top:4px; }

.info-box {
    background:rgba(59,130,246,.08); border:1px solid rgba(59,130,246,.25);
    border-radius:8px; padding:14px 18px; color:#93c5fd;
    font-size:.86rem; margin-bottom:16px;
}
.warn-box {
    background:rgba(245,158,11,.08); border:1px solid rgba(245,158,11,.25);
    border-radius:8px; padding:14px 18px; color:#fcd34d;
    font-size:.86rem; margin-bottom:16px;
}

.feat-grid {
    display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:10px;
}
.feat-card { background:#1a2235; border:1px solid #1e2a42; border-radius:10px; padding:18px; }
.feat-icon  { font-size:1.4rem; margin-bottom:8px; }
.feat-title { font-weight:600; color:#f1f5f9; font-size:.9rem; margin-bottom:5px; }
.feat-desc  { color:#64748b; font-size:.8rem; line-height:1.5; }

.colmap-row  { display:flex; align-items:center; gap:8px; font-size:.75rem; color:#64748b; padding:3px 0; }
.colmap-role { color:#818cf8; font-weight:600; min-width:85px; }
.colmap-col  { color:#94a3b8; font-family:'IBM Plex Mono',monospace; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background:#111827; border-radius:10px; padding:4px; gap:4px; border:1px solid #1e2a42;
}
.stTabs [data-baseweb="tab"]   { border-radius:7px; font-weight:500; font-size:.84rem; color:#94a3b8; }
.stTabs [aria-selected="true"] { background:#1a2235 !important; color:#f1f5f9 !important; }

/* exec summary header card */
.exec-hero {
    background: linear-gradient(135deg,#0f172a 0%,#1a1145 100%);
    border:1px solid #4338ca; border-radius:12px; padding:24px 30px; margin-bottom:20px;
}
.exec-hero h2  { font-size:1.35rem; font-weight:700; color:#e0e7ff; margin:0 0 4px 0; }
.exec-hero .meta { font-family:'IBM Plex Mono',monospace; font-size:.78rem; color:#818cf8; }

::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#0a0e1a; }
::-webkit-scrollbar-thumb { background:#1e2a42; border-radius:3px; }
</style>
""", unsafe_allow_html=True)

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(26,34,53,0.5)",
    font=dict(family="IBM Plex Sans", color="#94a3b8", size=12),
    xaxis=dict(gridcolor="#1e2a42", zerolinecolor="#1e2a42"),
    yaxis=dict(gridcolor="#1e2a42", zerolinecolor="#1e2a42"),
    colorway=["#3b82f6","#06b6d4","#8b5cf6","#f59e0b","#10b981","#ef4444"],
    margin=dict(l=24, r=24, t=44, b=24),
)

# ══════════════════════════════════════════════════════════
# EVRENSEl KOLON TANIMA  –  3 KATMANLI STRATEJİ
# ══════════════════════════════════════════════════════════
# Geniş anahtar-kelime havuzu:
# Türkçe + İngilizce + SAP alan kodları + Oracle alan kodları
COLUMN_KEYWORDS: dict[str, list[str]] = {
    "amount": [
        "tutar","amount","fiyat","price","total","net","gross","deger","değer",
        "bedel","sum","toplam","debit","credit","borc","borç","alacak",
        "wrbtr","dmbtr","netwr","brwrd","value","cost","maliyet","odeme",
        "ödeme","payment","invoice_amount","miktar","para","tl","usd","eur",
    ],
    "date": [
        "tarih","date","timestamp","time","zaman","gun","gün","bldat","budat",
        "cpudt","erdat","created","modified","updated","dt","period","donem",
        "dönem","ay","month","year","yil","yıl","tarihi","datetime","hareket",
    ],
    "vendor": [
        "tedarikci","tedarikçi","vendor","supplier","satici","satıcı","musteri",
        "müşteri","customer","client","lifnr","kunnr","partner","firma","company",
        "karsi","karşı","counterparty","account_name","isim","name","ad","title",
        "sirket","şirket","kurum","institution","payee","alici","alıcı",
    ],
    "user": [
        "kullanici","kullanıcı","user","personel","employee","ernam","aenam",
        "usnam","uname","operator","girenkisi","giren","olusturan","oluşturan",
        "created_by","entered_by","author","agent","staff","preparer","düzenleyen",
    ],
    "approver": [
        "onaylayan","approver","approved_by","onay_yapan","manager","mudur",
        "müdür","supervisor","reviewer","checker","controller","yetkili",
    ],
    "doc_id": [
        "belge","document","docnum","belnr","vbeln","ebeln","invoice","fatura",
        "siparis","siparış","order","id","no","num","number","ref","kod","code",
        "ticket","serial","seri","fis","fiş","evrak","makbuz","receipt",
    ],
    "category": [
        "kategori","category","tip","type","tur","tür","sinif","sınıf","hesap",
        "account","gl","cost_type","maliyet","hkont","matyp","class","grup",
        "group","bolum","bölüm","section","segment","kalem","item_type",
    ],
    "status": [
        "onay","approval","status","durum","state","approved","accepted","rejected",
        "pending","bekle","tamamla","complete","aktif","active","statü","statu",
    ],
    "department": [
        "departman","department","birim","unit","bolum","bölüm","division","branch",
        "sube","şube","merkez","center","profit_center","kostl","cost_center",
    ],
    "description": [
        "aciklama","açıklama","description","desc","detail","note","not","comment",
        "yorum","explanation","text","metin","narration","konu","subject",
    ],
}

def detect_columns(df: pd.DataFrame) -> dict[str, str]:
    """
    Üç katmanlı evrensel kolon tanıma.
    1) Ağırlıklı anahtar-kelime skoru (normalize + substring)
    2) Veri tipi bazlı fallback
    3) İstatistik bazlı ince ayar (varyans, kardinalite)
    """
    # Normalize: küçük harf, boşluk→_, nokta→_
    norm = {c.lower().replace(" ","_").replace(".","_").replace("-","_"): c
            for c in df.columns}
    mapping: dict[str, str] = {}
    used: set[str] = set()

    def score(col_key: str, kws: list[str]) -> float:
        s = 0.0
        for kw in kws:
            if kw == col_key:             s += 10   # tam eşleşme
            elif col_key.startswith(kw):  s += 6    # önek
            elif col_key.endswith(kw):    s += 5    # sonek
            elif kw in col_key:           s += 3    # içeriyor
        return s

    for role, kws in COLUMN_KEYWORDS.items():
        best_col, best_sc = None, 0.0
        for lk, ok in norm.items():
            if ok in used:
                continue
            sc = score(lk, kws)
            if sc > best_sc:
                best_sc, best_col = sc, ok
        if best_col and best_sc > 0:
            mapping[role] = best_col
            used.add(best_col)

    # ── Fallback 1: veri tipi ──
    num_cols = [c for c in df.columns
                if pd.api.types.is_numeric_dtype(df[c]) and c not in used]
    dt_cols  = [c for c in df.columns
                if pd.api.types.is_datetime64_any_dtype(df[c]) and c not in used]
    str_cols = [c for c in df.columns
                if df[c].dtype == object and c not in used]

    if "amount" not in mapping and num_cols:
        # En yüksek varyansli sayisal sutun → tutar
        best = max(num_cols, key=lambda c: df[c].std() if df[c].std() > 0 else 0)
        mapping["amount"] = best; used.add(best)

    if "date" not in mapping:
        if dt_cols:
            mapping["date"] = dt_cols[0]; used.add(dt_cols[0])
        else:
            # String sütunlardan datetime parse dene
            for c in str_cols:
                try:
                    parsed = pd.to_datetime(
                        df[c].dropna().head(10), infer_datetime_format=True, errors="raise"
                    )
                    if parsed.notna().sum() >= 5:
                        mapping["date"] = c; used.add(c); break
                except Exception:
                    pass

    # Kalan string sütunları role_fallback sırasıyla ata
    remaining = [c for c in str_cols if c not in used]
    role_fallback = ["vendor","user","approver","category","doc_id",
                     "department","description","status"]
    for role in role_fallback:
        if role not in mapping and remaining:
            mapping[role] = remaining.pop(0)

    # ── Fallback 2: doc_id → en yüksek kardinaliteli string ──
    if "doc_id" not in mapping:
        all_str = [c for c in df.columns if df[c].dtype == object and c not in used]
        if all_str:
            best = max(all_str, key=lambda c: df[c].nunique())
            mapping["doc_id"] = best

    return mapping


def parse_dates(df: pd.DataFrame, col: str) -> pd.DataFrame:
    df = df.copy()
    try:
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
    except Exception:
        pass
    return df


def to_numeric(df: pd.DataFrame, col: str) -> pd.Series:
    """Para birimi sembolleri, binlik ayraçlar dahil temizleyerek sayıya çevir."""
    return pd.to_numeric(
        df[col].astype(str)
        .str.replace(r"[₺$€£¥,\s]", "", regex=True)
        .str.replace(",", ".")
        .str.strip(),
        errors="coerce",
    )


# ══════════════════════════════════════════════════════════
# MODÜL 1 – VERİ KALİTESİ
# ══════════════════════════════════════════════════════════

def run_data_quality(df: pd.DataFrame, col_map: dict) -> list[dict]:
    total = len(df)
    results = []

    # 1 – Eksik veri
    miss = df.isnull().sum()
    miss_pct = (miss / total * 100).round(1)
    crit_miss = miss[miss_pct > 10]
    results.append({
        "kontrol": "Eksik Veri Analizi",
        "bulgu": (f"{len(crit_miss)} sütunda >%10 eksik veri; "
                  f"toplam {df.isnull().any(axis=1).sum():,} kayıt etkileniyor."),
        "etki": int(df.isnull().any(axis=1).sum()),
        "risk": "Yüksek" if len(crit_miss) >= 3 else ("Orta" if len(crit_miss) > 0 else "Düşük"),
        "detay": miss_pct[miss_pct > 0].to_dict(),
    })

    # 2 – Belge mükerreri
    if "doc_id" in col_map:
        dup = int(df.duplicated(subset=[col_map["doc_id"]], keep=False).sum())
        results.append({
            "kontrol": "Mükerrer Belge Numarası",
            "bulgu": f"{dup:,} kayıt mükerrer belge numarası taşıyor ({col_map['doc_id']}).",
            "etki": dup,
            "risk": "Kritik" if dup > 0 else "Düşük",
            "detay": {},
        })

    # 3 – Tam satır mükerreri
    fd = int(df.duplicated().sum())
    results.append({
        "kontrol": "Tam Satır Mükerrerlik",
        "bulgu": f"{fd:,} birebir aynı satır tespit edildi.",
        "etki": fd,
        "risk": "Yüksek" if fd > 0 else "Düşük",
        "detay": {},
    })

    # 4 – Negatif / sıfır tutar
    if "amount" in col_map:
        amt = to_numeric(df, col_map["amount"])
        neg  = int((amt < 0).sum())
        zero = int((amt == 0).sum())
        results.append({
            "kontrol": "Negatif & Sıfır Tutar",
            "bulgu": f"{neg:,} negatif, {zero:,} sıfır değerli tutar.",
            "etki": neg + zero,
            "risk": "Yüksek" if neg > 5 else ("Orta" if neg > 0 else "Düşük"),
            "detay": {"negatif": neg, "sıfır": zero},
        })

    # 5 – Aykırı değer (IQR + Z-score)
    if "amount" in col_map:
        amt = to_numeric(df, col_map["amount"]).dropna()
        if len(amt) > 4:
            Q1, Q3 = amt.quantile(.25), amt.quantile(.75)
            IQR = Q3 - Q1
            iqr_out = int(((amt < Q1 - 1.5*IQR) | (amt > Q3 + 1.5*IQR)).sum())
            z = np.abs((amt - amt.mean()) / (amt.std() + 1e-9))
            z_out = int((z > 3).sum())
            results.append({
                "kontrol": "Aykırı Değer Analizi (IQR / Z-score)",
                "bulgu": f"IQR yöntemi → {iqr_out:,}, Z-score yöntemi → {z_out:,} aykırı tutar.",
                "etki": max(iqr_out, z_out),
                "risk": "Yüksek" if max(iqr_out, z_out) > 10 else "Orta",
                "detay": {"IQR": iqr_out, "Z-score": z_out},
            })

    # 6 – Yuvarlama deseni
    if "amount" in col_map:
        amt = to_numeric(df, col_map["amount"]).dropna()
        nonzero = amt[amt != 0]
        if len(nonzero):
            r100  = int((nonzero % 100 == 0).sum())
            r1000 = int((nonzero % 1000 == 0).sum())
            pct   = r100 / len(nonzero) * 100
            results.append({
                "kontrol": "Şüpheli Yuvarlama Deseni",
                "bulgu": f"Tutarların %{pct:.1f}'i 100'ün katı; {r1000:,} kayıt 1.000'in katı.",
                "etki": r100,
                "risk": "Yüksek" if pct > 30 else ("Orta" if pct > 15 else "Düşük"),
                "detay": {"%100_katı": round(pct, 1), "1000_katı": r1000},
            })

    # 7 – Tarih tutarsızlıkları
    if "date" in col_map:
        df2 = parse_dates(df, col_map["date"])
        nat  = int(df2[col_map["date"]].isna().sum())
        fut  = int((df2[col_map["date"]] > pd.Timestamp.now()).sum())
        results.append({
            "kontrol": "Tarih Tutarsızlıkları",
            "bulgu": f"{nat:,} geçersiz tarih, {fut:,} gelecek tarihli kayıt.",
            "etki": nat + fut,
            "risk": "Orta" if (nat + fut) > 0 else "Düşük",
            "detay": {"geçersiz": nat, "gelecek": fut},
        })

    return results


# ══════════════════════════════════════════════════════════
# MODÜL 2 – SENARYO MOTORU
# ══════════════════════════════════════════════════════════

def run_scenarios(df: pd.DataFrame, col_map: dict) -> list[dict]:
    scenarios = []
    amt = to_numeric(df, col_map["amount"]) if "amount" in col_map else None

    # S1 – Olağandışı yoğunluk
    if "date" in col_map:
        df2 = parse_dates(df.copy(), col_map["date"])
        dc  = df2.groupby(df2[col_map["date"]].dt.date).size()
        if len(dc) > 3:
            mean, std = dc.mean(), dc.std()
            spikes = dc[dc > mean + 2*std]
            scenarios.append({
                "senaryo": "Olağandışı İşlem Yoğunluğu",
                "aciklama": (f"{len(spikes)} günde işlem sayısı istatistiksel ortalamanın "
                             f"2 standart sapma üstüne çıktı."),
                "risk": "Yüksek" if len(spikes) > 2 else "Orta",
                "etki": int(spikes.sum()),
                "ornek": dc.nlargest(5).reset_index().rename(
                    columns={0: "İşlem Sayısı", "index": "Tarih"}),
            })

    # S2 – Yoğunlaşma
    if "vendor" in col_map and amt is not None:
        va = df.assign(_a=amt).groupby(col_map["vendor"])["_a"].agg(["sum", "count"])
        va.columns = ["Toplam Tutar", "İşlem Sayısı"]
        va = va.sort_values("Toplam Tutar", ascending=False)
        share = va["Toplam Tutar"].iloc[0] / (va["Toplam Tutar"].sum() + 1e-9) * 100
        scenarios.append({
            "senaryo": "Karşı Taraf Yoğunlaşması",
            "aciklama": f"En büyük karşı taraf toplam tutarın %{share:.1f}'ini oluşturuyor.",
            "risk": "Kritik" if share > 50 else ("Yüksek" if share > 30 else "Orta"),
            "etki": len(va[va["Toplam Tutar"] > va["Toplam Tutar"].mean() * 3]),
            "ornek": va.head(8).reset_index(),
        })

    # S3 – Mesai dışı
    if "date" in col_map:
        df2 = parse_dates(df.copy(), col_map["date"])
        try:
            h = df2[col_map["date"]].dt.hour
            off = ((h < 8) | (h > 18)) & h.notna()
            off_n = int(off.sum())
            if off_n > 0:
                scenarios.append({
                    "senaryo": "Mesai Dışı Saat İşlemleri",
                    "aciklama": f"{off_n:,} işlem 08:00–18:00 dışında gerçekleştirilmiş.",
                    "risk": "Yüksek" if off_n > 10 else "Orta",
                    "etki": off_n,
                    "ornek": df2[off].head(10),
                })
        except Exception:
            pass

    # S4 – Eşik altı yapılandırma
    if amt is not None:
        for thresh in [5_000, 10_000, 25_000, 50_000, 100_000]:
            below = int(((amt > thresh * .9) & (amt < thresh)).sum())
            if below >= 3:
                scenarios.append({
                    "senaryo": f"Eşik Altı Yapılandırma ({thresh:,} TL)",
                    "aciklama": f"{below:,} işlem {thresh:,} TL eşiğinin %90–100 bandında.",
                    "risk": "Kritik" if below > 10 else "Yüksek",
                    "etki": below,
                    "ornek": df.assign(_a=amt)[(amt > thresh*.9) & (amt < thresh)].head(10),
                })
                break

    # S5 – SoD (oluşturan = onaylayan)
    if "user" in col_map and "approver" in col_map:
        mask = df[col_map["user"]] == df[col_map["approver"]]
        sod  = int(mask.sum())
        if sod > 0:
            scenarios.append({
                "senaryo": "Görevler Ayrılığı (SoD) İhlali",
                "aciklama": f"{sod:,} kayıtta aynı kişi hem oluşturucu hem onaylayıcı rolünde.",
                "risk": "Kritik",
                "etki": sod,
                "ornek": df[mask].head(10),
            })

    # S6 – Tekrarlayan tutar
    if amt is not None:
        vc  = amt.round(2).value_counts()
        rep = vc[vc > 5]
        if len(rep):
            scenarios.append({
                "senaryo": "Tekrarlayan Sabit Tutar Deseni",
                "aciklama": f"{len(rep)} farklı tutar değeri 5'ten fazla tekrarlandı.",
                "risk": "Yüksek" if len(rep) > 5 else "Orta",
                "etki": int(rep.sum()),
                "ornek": rep.head(8).reset_index().rename(
                    columns={"index": "Tutar", col_map["amount"]: "Tekrar"}),
            })

    return scenarios


# ══════════════════════════════════════════════════════════
# MODÜL 3 – RİSK SKORLAMA
# ══════════════════════════════════════════════════════════

def compute_risk_scores(df: pd.DataFrame, col_map: dict) -> pd.DataFrame:
    df = df.copy()
    score = pd.Series(0.0, index=df.index)

    if "amount" in col_map:
        amt = to_numeric(df, col_map["amount"]).fillna(0).abs()
        cap = amt.quantile(.99) + 1e-9
        score += (amt / cap).clip(0, 1) * 40
        z = np.abs((amt - amt.mean()) / (amt.std() + 1e-9))
        score += (z / (z.quantile(.99) + 1e-9)).clip(0, 1) * 35

    if "vendor" in col_map:
        freq = df[col_map["vendor"]].map(df[col_map["vendor"]].value_counts())
        score += (freq / (freq.max() + 1e-9)) * 15

    if "user" in col_map:
        freq = df[col_map["user"]].map(df[col_map["user"]].value_counts())
        score += (freq / (freq.max() + 1e-9)) * 10

    df["risk_skoru"]    = score.clip(0, 100).round(1)
    df["risk_seviyesi"] = df["risk_skoru"].apply(
        lambda s: "Kritik" if s >= 75 else ("Yüksek" if s >= 50 else ("Orta" if s >= 25 else "Düşük"))
    )
    return df


# ══════════════════════════════════════════════════════════
# MODÜL 4 – BULGULAR
# ══════════════════════════════════════════════════════════

_ROOT_CAUSE = {
    "Eksik":      "Zorunlu alan kuralları veya sistem entegrasyon kontrolü eksikliği.",
    "Mükerrer":   "Benzersiz kısıtlama (unique constraint) eksikliği veya onay sürecindeki boşluk.",
    "Negatif":    "Ters kayıt prosedürlerinde kontrol mekanizması yetersizliği.",
    "Aykırı":     "Tutar onay limitleri veya istatistiksel izleme kontrol boşluğu.",
    "Yuvarlama":  "Tahmini ya da sahte veri girişine işaret eden sistematik kalıp.",
    "Tarih":      "Sistem tarih/saat kontrolü yetersizliği veya geriye dönük değişiklik.",
    "Yoğunlaşma": "Alternatif teklif politikası veya harcama limit uygulamasının eksikliği.",
    "Mesai":      "Zaman bazlı sistem erişim kısıtlaması bulunmaması.",
    "Eşik":       "Birikimli limit kontrol sürecinin tasarlanmamış olması.",
    "SoD":        "Rol bazlı erişim kontrolü (RBAC) politikası yetersizliği.",
    "Tekrarlayan":"Veri doğrulama ve çift kayıt kontrol mekanizması eksikliği.",
    "Olağandışı": "İşlem izleme ve anomali tespiti kontrol eksikliği.",
}

def _root(text: str) -> str:
    for k, v in _ROOT_CAUSE.items():
        if k.lower() in text.lower():
            return v
    return "İlgili süreçte yeterli iç kontrol mekanizması bulunmaması."

def generate_findings(quality: list, scenarios: list, df: pd.DataFrame) -> list:
    prio = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3}
    findings = []

    for q in quality:
        if q["etki"] > 0 and q["risk"] in ("Kritik", "Yüksek", "Orta"):
            findings.append({
                "baslik":    f"VERİ KALİTESİ · {q['kontrol']}",
                "bulgu":     q["bulgu"],
                "kok_neden": _root(q["kontrol"]),
                "is_etkisi": (f"{q['etki']:,} etkilenen kayıt; finansal raporlama "
                              "güvenilirliğine olumsuz etki riski."),
                "risk":      q["risk"],
                "etki":      q["etki"],
                "kaynak":    "Veri Kalite Modülü",
            })

    for s in scenarios:
        if s["etki"] > 0:
            findings.append({
                "baslik":    f"DENETİM SENARYOSU · {s['senaryo']}",
                "bulgu":     s["aciklama"],
                "kok_neden": _root(s["senaryo"]),
                "is_etkisi": f"{s['etki']:,} etkilenen kayıt; usulsüzlük veya uyumsuzluk riski.",
                "risk":      s["risk"],
                "etki":      s["etki"],
                "kaynak":    "Senaryo Motoru",
            })

    if "risk_seviyesi" in df.columns:
        crit_pct = (df["risk_seviyesi"] == "Kritik").mean() * 100
        if crit_pct > 5:
            findings.append({
                "baslik":    "RİSK SKORU · Kritik Kayıt Yoğunluğu",
                "bulgu":     f"Kayıtların %{crit_pct:.1f}'i kritik risk seviyesinde.",
                "kok_neden": "Kontrol ortamında sistemik zafiyetler.",
                "is_etkisi": "Finansal kayıp, uyumsuzluk cezası ve itibar riski.",
                "risk":      "Kritik",
                "etki":      int((df["risk_seviyesi"] == "Kritik").sum()),
                "kaynak":    "Risk Skorlama",
            })

    findings.sort(key=lambda x: prio.get(x["risk"], 4))
    return findings


# ══════════════════════════════════════════════════════════
# MODÜL 5 – AKSİYON PLANLARI
# ══════════════════════════════════════════════════════════

_ACTIONS = {
    "Mükerrer":    ("ERP'de benzersiz kısıtlama aktivasyonu; mükerrer kontrol kuralı eklenmesi.", "BT / Finans", "Düşük"),
    "Negatif":     ("Negatif değer politikası revizyonu; kural motoru kurulumu.", "Finans / İç Kontrol", "Düşük"),
    "Aykırı":      ("Tutar onay matrisinin yeniden yapılandırılması; anomali izleme aracı.", "Finans / İç Denetim", "Yüksek"),
    "Yuvarlama":   ("Yuvarlak tutarlara ek onay süreci; zorunlu alan denetimi.", "Finans / Operasyon", "Düşük"),
    "Yoğunlaşma":  ("En az 3 alternatif teklif politikası; yoğunlaşma üst limiti.", "Satınalma / Yönetim", "Orta"),
    "Mesai":       ("Zaman bazlı erişim profili; mesai dışı girişlerde MFA zorunluluğu.", "BT / Güvenlik", "Orta"),
    "Eşik":        ("Birikimli limit kontrol süreci; toplu değerlendirme mekanizması.", "Finans / Satınalma", "Yüksek"),
    "SoD":         ("RBAC politikası güncellemesi; oluşturma ve onay rolü ayrıştırması.", "BT / İK / İç Kontrol", "Yüksek"),
    "Eksik":       ("Zorunlu alan (mandatory field) aktivasyonu; veri tamamlama prosedürü.", "BT / Finans", "Düşük"),
    "Tarih":       ("Sistem tarih kontrolü güçlendirme; geriye dönük kayıt üst yönetim onayı.", "BT / Finans", "Orta"),
    "Tekrarlayan": ("Çift kayıt kontrol motoru; tutar karşılaştırma kuralı.", "BT / Operasyon", "Orta"),
    "Olağandışı":  ("Günlük işlem limiti; gerçek zamanlı anomali uyarı sistemi.", "Finans / İç Denetim", "Orta"),
}

PRIO = {"Kritik": "P1 – Acil", "Yüksek": "P2 – Yüksek", "Orta": "P3 – Orta", "Düşük": "P4 – Düşük"}

def generate_action_plans(findings: list) -> list:
    plans = []
    for f in findings:
        if f["risk"] not in ("Kritik", "Yüksek", "Orta"):
            continue
        aksiyon = "Sürecin kapsamlı incelenmesi ve kontrol açığını kapatan prosedür oluşturulması."
        birim   = "İç Kontrol / Yönetim"
        zorluk  = "Orta"
        for kw, val in _ACTIONS.items():
            if kw.lower() in f["baslik"].lower() or kw.lower() in f["bulgu"].lower():
                aksiyon, birim, zorluk = val
                break
        plans.append({
            "bulgu":   f["baslik"],
            "aksiyon": aksiyon,
            "birim":   birim,
            "oncelik": PRIO.get(f["risk"], "P3"),
            "zorluk":  zorluk,
            "risk":    f["risk"],
        })
    return plans


# ══════════════════════════════════════════════════════════
# MODÜL 6 – GRAFİKLER
# ══════════════════════════════════════════════════════════

def fig_risk_dist(df):
    counts = df["risk_seviyesi"].value_counts().reindex(
        ["Kritik", "Yüksek", "Orta", "Düşük"], fill_value=0)
    colors = {"Kritik": "#ef4444", "Yüksek": "#f59e0b", "Orta": "#3b82f6", "Düşük": "#10b981"}
    fig = go.Figure(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=[colors[r] for r in counts.index],
        text=counts.values, textposition="outside",
        textfont=dict(color="#f1f5f9", size=13, family="IBM Plex Mono"),
    ))
    fig.update_layout(title="Risk Dağılımı", title_font_size=14, height=300, **PLOTLY_BASE)
    return fig

def fig_score_hist(df):
    fig = go.Figure(go.Histogram(
        x=df["risk_skoru"], nbinsx=20,
        marker=dict(color=df["risk_skoru"],
                    colorscale=[[0,"#10b981"],[.5,"#f59e0b"],[1,"#ef4444"]]),
    ))
    fig.update_layout(title="Risk Skoru Histogramı", height=300,
                      xaxis_title="Skor (0–100)", yaxis_title="Kayıt Sayısı",
                      title_font_size=14, **PLOTLY_BASE)
    return fig

def fig_time_trend(df, col_map):
    df2 = parse_dates(df.copy(), col_map["date"])
    df2["_m"] = df2[col_map["date"]].dt.to_period("M").astype(str)
    m = df2.groupby("_m").agg(
        Sayı=("risk_skoru", "count"), OrtRisk=("risk_skoru", "mean")
    ).reset_index()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=m["_m"], y=m["Sayı"], name="İşlem Sayısı",
                         marker_color="rgba(59,130,246,.5)"), secondary_y=False)
    fig.add_trace(go.Scatter(x=m["_m"], y=m["OrtRisk"], name="Ort. Risk",
                             mode="lines+markers",
                             line=dict(color="#ef4444", width=2),
                             marker=dict(size=6)), secondary_y=True)
    fig.update_layout(title="Aylık Trend", height=320, title_font_size=14, **PLOTLY_BASE,
                      legend=dict(orientation="h", y=1.1))
    fig.update_yaxes(title_text="İşlem Sayısı", secondary_y=False)
    fig.update_yaxes(title_text="Risk Skoru", secondary_y=True)
    return fig

def fig_vendor_conc(df, col_map):
    amt = to_numeric(df, col_map["amount"])
    vc  = df.assign(_a=amt).groupby(col_map["vendor"])["_a"].sum().nlargest(10)
    fig = go.Figure(go.Bar(
        y=vc.index.astype(str), x=vc.values, orientation="h",
        marker=dict(color=vc.values,
                    colorscale=[[0,"#1a2235"],[.5,"#3b82f6"],[1,"#ef4444"]]),
        text=[f"{v:,.0f}" for v in vc.values], textposition="outside",
        textfont=dict(color="#94a3b8", size=10),
    ))
    fig.update_layout(
        title="Karşı Taraf Yoğunlaşması (Top 10)", height=360, title_font_size=14,
        **PLOTLY_BASE,
        yaxis=dict(autorange="reversed", gridcolor="#1e2a42", zerolinecolor="#1e2a42"),
    )
    return fig

def fig_heatmap(df, col_map):
    cat_col = col_map.get("category") or col_map.get("vendor")
    if not cat_col:
        return None
    top  = df[cat_col].value_counts().nlargest(8).index
    sub  = df[df[cat_col].isin(top)]
    heat = sub.groupby([cat_col, "risk_seviyesi"]).size().unstack(fill_value=0)
    heat = heat.reindex(columns=["Kritik","Yüksek","Orta","Düşük"], fill_value=0)
    fig  = go.Figure(go.Heatmap(
        z=heat.values, x=heat.columns, y=heat.index.astype(str),
        colorscale=[[0,"#1a2235"],[.3,"#1d4ed8"],[.7,"#f59e0b"],[1,"#ef4444"]],
        text=heat.values, texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
    ))
    fig.update_layout(title="Risk Isı Haritası", height=360,
                      title_font_size=14, **PLOTLY_BASE)
    return fig


# ══════════════════════════════════════════════════════════
# MODÜL 7 – YÖNETİCİ ÖZETİ  (100 % Streamlit native)
# ══════════════════════════════════════════════════════════

def render_executive_summary(df, col_map, findings, scenarios):
    total  = len(df)
    crit_n = int((df["risk_seviyesi"] == "Kritik").sum())
    high_n = int((df["risk_seviyesi"] == "Yüksek").sum())
    avg_s  = float(df["risk_skoru"].mean())

    # Genel risk seviyesi hesapla
    if avg_s >= 60 or crit_n / (total or 1) > .15:
        genel_risk, risk_color = "KRİTİK", "#ef4444"
        yorum = ("Analiz sonuçları, incelenen veri setinde iç kontrol ortamının "
                 "kritik düzeyde zayıfladığını ortaya koymaktadır. "
                 "Acil müdahale gerektiren bulgular mevcuttur.")
    elif avg_s >= 40 or (crit_n + high_n) / (total or 1) > .25:
        genel_risk, risk_color = "YÜKSEK", "#f59e0b"
        yorum = ("Birden fazla kritik kontrol zafiyetine işaret eden bulgular "
                 "tespit edilmiştir. Öncelikli aksiyon planlaması gerekmektedir.")
    elif avg_s >= 25:
        genel_risk, risk_color = "ORTA", "#3b82f6"
        yorum = ("Belirli süreç alanlarında kontrol iyileştirme ihtiyacı bulunmaktadır. "
                 "Takip döneminde düzenli izleme önerilmektedir.")
    else:
        genel_risk, risk_color = "DÜŞÜK", "#10b981"
        yorum = ("Analiz edilen veri seti makul düzeyde kontrol bütünlüğü sergilemektedir. "
                 "Tespit edilen düşük riskli bulgular izleme kapsamına alınmalıdır.")

    kritik_b = [f for f in findings if f["risk"] == "Kritik"][:3]
    yuksek_b = [f for f in findings if f["risk"] == "Yüksek"][:3]

    # Öncelikli aksiyon alanları
    sc_text = " ".join(s["senaryo"].lower() for s in scenarios)
    oncelik = []
    if "eşik" in sc_text:
        oncelik.append("Tutar onay limitleri ve satınalma kontrollerinin kapsamlı gözden geçirilmesi")
    if "yoğunlaşma" in sc_text:
        oncelik.append("Tedarikçi yoğunlaşması ve bağımlılık yönetim sürecinin değerlendirilmesi")
    if "sod" in sc_text or "görevler" in sc_text:
        oncelik.append("Görevler ayrılığı matrisinin tam revizyonu")
    if "mesai" in sc_text:
        oncelik.append("Sistem erişim kontrolü ve kullanıcı yetkilendirme politikasının güçlendirilmesi")
    if not oncelik:
        oncelik = ["Veri kalite süreçlerinin iyileştirilmesi",
                   "Anomali tespiti kapasitesinin artırılması"]

    sonraki = [
        "Kritik bulgular için 30 gün içinde kapatma aksiyonu başlatılması",
        "Yönetim Kurulu Denetim Komitesi'ne özet sunum hazırlanması",
        "Sürekli denetim (continuous auditing) mekanizmasının devreye alınması",
        "Belirlenen yüksek riskli alanlar için özel denetim planı oluşturulması",
    ]

    # ── RENDER ──────────────────────────────────────────

    # Başlık
    st.markdown(f"""
    <div class="exec-hero">
        <div class="au-badge">İÇ DENETİM YÖNETİCİ ÖZETİ</div>
        <h2>Analitik Değerlendirme Raporu</h2>
        <div class="meta">
            Tarih: {datetime.now().strftime('%d %B %Y')}
            &nbsp;·&nbsp; Kayıt: {total:,}
            &nbsp;·&nbsp; Ort. Risk: {avg_s:.1f}/100
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Risk göstergesi + metrikler
    col_r, col_m = st.columns([1, 3])
    with col_r:
        st.markdown(f"""
        <div style="background:rgba(99,102,241,.08);border:1px solid #4338ca;
                    border-radius:12px;padding:18px 22px;text-align:center;">
            <div style="font-size:.68rem;letter-spacing:2px;text-transform:uppercase;
                        color:#818cf8;margin-bottom:5px;">GENEL RİSK</div>
            <div style="font-size:2rem;font-weight:800;color:{risk_color};
                        font-family:'IBM Plex Mono',monospace;">{genel_risk}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_m:
        c1, c2, c3 = st.columns(3)
        c1.metric("Kritik Kayıt",    f"{crit_n:,}")
        c2.metric("Yüksek Riskli",   f"{high_n:,}")
        c3.metric("Ort. Risk Skoru", f"{avg_s:.1f}")

    st.divider()

    # ── 1. Genel Risk Değerlendirmesi ──
    st.markdown("### 1 · Genel Risk Değerlendirmesi")
    st.info(
        f"{yorum}\n\n"
        f"İncelenen **{total:,}** kayıt içerisinde **{crit_n:,} kritik** ve "
        f"**{high_n:,} yüksek** riskli kayıt tespit edilmiştir. "
        f"Ortalama risk skoru **{avg_s:.1f}/100** olarak hesaplanmıştır."
    )

    # ── 2. Kritik Kontrol Zafiyetleri ──
    st.markdown("### 2 · Kritik Kontrol Zafiyetleri")
    if kritik_b:
        for b in kritik_b:
            st.error(
                f"**{b['baslik']}**\n\n"
                f"📌 {b['bulgu']}\n\n"
                f"🔍 *Kök Neden:* {b['kok_neden']}"
            )
    else:
        st.success("✅ Kritik seviyede kontrol zafiyeti tespit edilmemiştir.")

    # ── 3. Öncelikli Denetim Bulguları ──
    st.markdown("### 3 · Öncelikli Denetim Bulguları")
    if yuksek_b:
        for b in yuksek_b:
            st.warning(
                f"**{b['baslik']}**\n\n"
                f"📌 {b['bulgu']}\n\n"
                f"💼 *İş Etkisi:* {b['is_etkisi']}"
            )
    else:
        st.success("✅ Yüksek riskli bulgu sayısı yönetilebilir düzeydedir.")

    # ── 4. Öncelikli Aksiyon Alanları ──
    st.markdown("### 4 · Öncelikli Aksiyon Alanları")
    for i, item in enumerate(oncelik, 1):
        st.markdown(f"**{i}.** {item}")

    # ── 5. Sonraki Dönem Odak Alanları ──
    st.markdown("### 5 · Sonraki Dönem Denetim Odak Alanları")
    for i, item in enumerate(sonraki, 1):
        st.markdown(f"**{i}.** {item}")

    st.divider()
    st.caption(
        "Bu rapor IIA Uluslararası İç Denetim Standartları (IPPF) çerçevesinde "
        "otomatik veri analitiği yöntemleriyle üretilmiştir. "
        "Son karar yetkisi sorumlu iç denetçiye aittir."
    )

    # İndirme butonu
    txt = f"""İÇ DENETİM ANALİTİK DEĞERLENDİRME RAPORU
{'='*52}
Tarih            : {datetime.now().strftime('%d %B %Y')}
Toplam Kayıt     : {total:,}
Genel Risk       : {genel_risk}
Ort. Risk Skoru  : {avg_s:.1f} / 100
Kritik Kayıt     : {crit_n:,}
Yüksek Riskli    : {high_n:,}

1. GENEL RİSK DEĞERLENDİRMESİ
{yorum}

2. KRİTİK KONTROL ZAFİYETLERİ
{''.join(chr(10)+'• '+b['baslik']+': '+b['bulgu'] for b in kritik_b) or 'Kritik bulgu tespit edilmemiştir.'}

3. ÖNCELİKLİ DENETİM BULGULARI
{''.join(chr(10)+'• '+b['baslik']+': '+b['bulgu'] for b in yuksek_b) or 'Yüksek riskli bulgu yönetilebilir düzeyde.'}

4. ÖNCELİKLİ AKSİYON ALANLARI
{''.join(chr(10)+'• '+a for a in oncelik)}

5. SONRAKI DÖNEM ODAK ALANLARI
{''.join(chr(10)+'• '+a for a in sonraki)}

{'─'*52}
IIA IPPF Standartlarına uygun otomatik analitik raporu.
"""
    st.download_button(
        "📥 Yönetici Özetini İndir (.txt)",
        data=txt,
        file_name=f"yonetici_ozeti_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain",
    )


# ══════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════

ROLE_TR = {
    "amount": "Tutar", "date": "Tarih", "vendor": "Karşı Taraf",
    "user": "Kullanıcı", "approver": "Onaylayan", "doc_id": "Belge No",
    "category": "Kategori", "status": "Durum", "department": "Departman",
    "description": "Açıklama",
}

def render_sidebar(df, col_map):
    with st.sidebar:
        st.markdown("""
        <div style="padding:12px 0 10px;">
            <div style="font-size:.67rem;letter-spacing:2px;text-transform:uppercase;
                        color:#6366f1;font-weight:700;">İÇ DENETİM</div>
            <div style="font-size:1.05rem;font-weight:700;color:#f1f5f9;margin-top:3px;">
                Analitik Platform</div>
        </div>
        <hr style="border-color:#1e2a42;margin:0 0 12px 0;">
        """, unsafe_allow_html=True)

        filters = {}

        st.markdown("**Risk Seviyesi**")
        filters["risk"] = st.multiselect(
            "_rf", ["Kritik","Yüksek","Orta","Düşük"],
            default=["Kritik","Yüksek","Orta","Düşük"],
            label_visibility="collapsed",
        )

        if "date" in col_map:
            df2 = parse_dates(df, col_map["date"])
            mn, mx = df2[col_map["date"]].min(), df2[col_map["date"]].max()
            if pd.notna(mn) and pd.notna(mx):
                st.markdown("**Tarih Aralığı**")
                rng = st.date_input("_df", (mn.date(), mx.date()),
                                    min_value=mn.date(), max_value=mx.date(),
                                    label_visibility="collapsed")
                filters["date_range"] = rng

        st.markdown("**Min. Risk Skoru**")
        filters["min_score"] = st.slider("_sf", 0, 100, 0, label_visibility="collapsed")

        if "amount" in col_map:
            st.markdown("**Min. Tutar**")
            filters["min_amount"] = st.number_input("_af", value=0.0,
                                                    label_visibility="collapsed")

        st.markdown("---")
        st.markdown("""<div style="font-size:.68rem;color:#6366f1;font-weight:700;
                    letter-spacing:1px;margin-bottom:6px;">ALGILANAN SÜTUNLAR</div>""",
                    unsafe_allow_html=True)

        for role, col in col_map.items():
            st.markdown(
                f"<div class='colmap-row'>"
                f"<span class='colmap-role'>{ROLE_TR.get(role, role)}</span>"
                f"<span class='colmap-col'>→ {col}</span></div>",
                unsafe_allow_html=True,
            )

    return filters


def apply_filters(df, col_map, filters):
    out = df.copy()
    if "risk" in filters and "risk_seviyesi" in out.columns:
        out = out[out["risk_seviyesi"].isin(filters["risk"])]
    if "min_score" in filters:
        out = out[out["risk_skoru"] >= filters["min_score"]]
    if "date_range" in filters and "date" in col_map:
        out = parse_dates(out, col_map["date"])
        try:
            r = filters["date_range"]
            if len(r) == 2:
                out = out[(out[col_map["date"]].dt.date >= r[0]) &
                          (out[col_map["date"]].dt.date <= r[1])]
        except Exception:
            pass
    if "min_amount" in filters and "amount" in col_map:
        amt = to_numeric(out, col_map["amount"])
        out = out[amt >= filters["min_amount"]]
    return out


def css_class(level):
    return {"Kritik":"critical","Yüksek":"high","Orta":"medium","Düşük":"low"}.get(level,"medium")

def risk_icon(level):
    return {"Kritik":"🔴","Yüksek":"🟠","Orta":"🔵","Düşük":"🟢"}.get(level,"⚪")


# ══════════════════════════════════════════════════════════
# DEMO VERİ
# ══════════════════════════════════════════════════════════

def demo_data() -> pd.DataFrame:
    np.random.seed(42)
    n = 500
    vendors = ["Teknoloji A AŞ","Lojistik B Ltd","Danışmanlık C GmbH",
               "İnşaat D Ort","Temizlik E Firm","Malzeme F Koop",
               "Servis G SRL","Yazılım H Inc"]
    users  = ["ahmet.kaya","fatma.demir","mehmet.yilmaz",
               "zeynep.arslan","ali.celik","ayse.sahin"]
    cats   = ["BT Harcaması","Danışmanlık","Kira","Seyahat",
               "Bakım","Hizmet Alımı","Malzeme","Eğitim"]
    depts  = ["Finans","Satınalma","İK","BT","Operasyon"]

    amounts = np.abs(np.random.lognormal(8.5, 1.8, n)).round(2)
    amounts[5:12]    = np.random.uniform(9500, 9999, 7).round(2)
    amounts[20:25]   = np.random.uniform(24500, 24999, 5).round(2)
    amounts[50:60]   = np.random.choice([5000, 10000, 25000, 50000], 10)
    amounts[80:85]   = np.random.uniform(-15000, -500, 5).round(2)
    amounts[100]     = 985000; amounts[150] = 742000
    amounts[120:123] = 0
    amounts[300:315] = 3750.00

    dates = [datetime(2024, 1, 1) + pd.Timedelta(hours=int(h))
             for h in np.random.randint(0, 8760, n)]
    for i in [30, 31, 32, 33, 34]:
        dates[i] = dates[i].replace(hour=int(np.random.choice([1, 2, 22, 23])))

    user_c = np.random.choice(users, n)
    appr_c = np.random.choice(users, n)
    for i in [10, 11, 12, 13, 14]:
        appr_c[i] = user_c[i]

    df = pd.DataFrame({
        "Belge_No":    [f"FTR-2024-{i+1:05d}" for i in range(n)],
        "Tarih":       dates,
        "Tedarikci":   np.random.choice(vendors, n, p=[.38,.2,.08,.08,.07,.07,.06,.06]),
        "Birim":       np.random.choice(depts, n),
        "Kategori":    np.random.choice(cats, n),
        "Kullanici":   user_c,
        "Onaylayan":   appr_c,
        "Tutar_TL":    amounts,
        "Onay_Durumu": np.random.choice(
            ["Onaylandı","Beklemede","Reddedildi"], n, p=[.75,.15,.10]),
    })
    df = pd.concat([df, df.iloc[40:44].copy()], ignore_index=True)
    df.loc[498, "Belge_No"] = "FTR-2024-00025"
    df.loc[499, "Belge_No"] = "FTR-2024-00025"
    df.loc[60:65, "Tedarikci"] = np.nan
    return df.sort_values("Tarih").reset_index(drop=True)


# ══════════════════════════════════════════════════════════
# ANA FONKSİYON
# ══════════════════════════════════════════════════════════

def main():
    # Header
    st.markdown("""
    <div class="au-header">
        <div class="au-badge">İç Denetim Veri Analitiği · v2.0</div>
        <h1>🔍 Denetim Analitik Platformu</h1>
        <p>ERP Uyumlu &nbsp;·&nbsp; Evrensel Kolon Tanıma &nbsp;·&nbsp;
           Otomatik Bulgu Üretimi &nbsp;·&nbsp; IIA IPPF Standartları</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Excel (.xlsx) veya CSV (.csv) yükleyin",
        type=["xlsx", "csv"],
        help="SAP, Oracle, Netsis, Logo, Mikro ve diğer ERP çıktıları desteklenir. "
             "Sütun adları otomatik tanınır.",
    )

    if uploaded is None and not st.session_state.get("use_demo"):
        st.markdown("""
        <div class="info-box">
        📂 <b>Veri dosyanızı yükleyin</b> — sütun adları ve sayıları otomatik tanınır, ön tanımlama gerekmez.<br>
        Desteklenen: <b>Excel (.xlsx) &nbsp;/&nbsp; CSV (.csv)</b> &nbsp;·&nbsp;
        SAP · Oracle · Netsis · Logo · Mikro · genel muhasebe çıktıları
        </div>
        """, unsafe_allow_html=True)
        if st.button("🎲 Demo Veri ile Dene", type="primary"):
            st.session_state["use_demo"] = True
            st.rerun()
        st.markdown("""
        <div class="feat-grid">
            <div class="feat-card"><div class="feat-icon">🧪</div>
                <div class="feat-title">7 Kalite Kontrolü</div>
                <div class="feat-desc">Eksik veri · Mükerrer kayıt · Negatif tutar · Aykırı değer · Yuvarlama deseni · Tarih tutarsızlığı</div></div>
            <div class="feat-card"><div class="feat-icon">🎯</div>
                <div class="feat-title">Senaryo Motoru</div>
                <div class="feat-desc">Eşik ihlali · Yoğunlaşma · Mesai dışı işlem · SoD ihlali · Tekrarlayan tutar</div></div>
            <div class="feat-card"><div class="feat-icon">📊</div>
                <div class="feat-title">Risk Skorlama</div>
                <div class="feat-desc">Her kayıt için 0–100 birleşik skor: Tutar etkisi · Anomali · İşlem frekansı</div></div>
            <div class="feat-card"><div class="feat-icon">🔎</div>
                <div class="feat-title">Otomatik Bulgular</div>
                <div class="feat-desc">Kök neden analizi · İş etkisi · IIA uyumlu yapılandırılmış bulgu formatı</div></div>
            <div class="feat-card"><div class="feat-icon">✅</div>
                <div class="feat-title">Aksiyon Planları</div>
                <div class="feat-desc">Sorumlu birim · P1–P4 öncelik · Uygulama zorluğu değerlendirmesi</div></div>
            <div class="feat-card"><div class="feat-icon">📌</div>
                <div class="feat-title">Yönetici Özeti</div>
                <div class="feat-desc">Kurumsal dil · Sektör bağımsız · İndirilebilir rapor</div></div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Veri yükle
    try:
        if uploaded is not None:
            st.session_state["use_demo"] = False
            df_raw = (pd.read_csv(uploaded, encoding="utf-8-sig")
                      if uploaded.name.endswith(".csv")
                      else pd.read_excel(uploaded))
        else:
            df_raw = demo_data()
            st.markdown("""<div class="warn-box">⚠️ Demo modunda çalışıyorsunuz.
            Gerçek analiz için veri dosyanızı yükleyin.</div>""", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Dosya okunamadı: {e}")
        return

    if df_raw.empty:
        st.error("Dosya boş veya desteklenmeyen formatta.")
        return

    # Kolon tanıma + analiz
    col_map = detect_columns(df_raw)

    with st.spinner("Denetim analizleri çalıştırılıyor…"):
        df_s      = compute_risk_scores(df_raw, col_map)
        quality   = run_data_quality(df_s, col_map)
        scenarios = run_scenarios(df_s, col_map)
        findings  = generate_findings(quality, scenarios, df_s)
        plans     = generate_action_plans(findings)

    filters  = render_sidebar(df_s, col_map)
    df_f     = apply_filters(df_s, col_map, filters)
    total    = len(df_f)
    crit_n   = int((df_f["risk_seviyesi"] == "Kritik").sum())
    high_n   = int((df_f["risk_seviyesi"] == "Yüksek").sum())
    avg_risk = float(df_f["risk_skoru"].mean()) if total else 0
    high_pct = (crit_n + high_n) / total * 100 if total else 0

    # KPI
    color4 = "red" if high_pct > 20 else ("amber" if high_pct > 10 else "green")
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Toplam Kayıt</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">Filtrelenmiş veri seti</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Kritik Kayıt</div>
            <div class="kpi-value">{crit_n:,}</div>
            <div class="kpi-sub">Acil aksiyon gerektirir</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Ort. Risk Skoru</div>
            <div class="kpi-value">{avg_risk:.0f}</div>
            <div class="kpi-sub">0–100 skala</div>
        </div>
        <div class="kpi-card {color4}">
            <div class="kpi-label">Yüksek Risk %</div>
            <div class="kpi-value">{high_pct:.1f}%</div>
            <div class="kpi-sub">Kritik + Yüksek oranı</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # SEKMELER
    t1, t2, t3, t4, t5 = st.tabs([
        "📋 Veri Genel Görünüm",
        "📊 Risk Analizi",
        "🔎 Denetim Bulguları",
        "✅ Aksiyon Planları",
        "📌 Yönetici Özeti",
    ])

    # TAB 1
    with t1:
        st.markdown("#### Ham Veri Önizleme")
        st.dataframe(df_f.head(200), use_container_width=True, height=340)
        st.markdown("#### Veri Kalitesi Kontrol Sonuçları")
        for q in quality:
            icon = risk_icon(q["risk"])
            with st.expander(
                f"{icon} {q['kontrol']}  —  **{q['risk']}**  ·  {q['etki']:,} etkilenen kayıt"
            ):
                st.write(q["bulgu"])
                if q["detay"]:
                    st.json(q["detay"])
        st.markdown("#### Sayısal İstatistikler")
        st.dataframe(df_raw.describe().round(2), use_container_width=True)

    # TAB 2
    with t2:
        c1, c2 = st.columns(2)
        with c1: st.plotly_chart(fig_risk_dist(df_f), use_container_width=True)
        with c2: st.plotly_chart(fig_score_hist(df_f), use_container_width=True)
        if "date" in col_map:
            try: st.plotly_chart(fig_time_trend(df_f, col_map), use_container_width=True)
            except Exception: pass
        c3, c4 = st.columns(2)
        with c3:
            if "vendor" in col_map and "amount" in col_map:
                try: st.plotly_chart(fig_vendor_conc(df_f, col_map), use_container_width=True)
                except Exception: pass
        with c4:
            try:
                hm = fig_heatmap(df_f, col_map)
                if hm: st.plotly_chart(hm, use_container_width=True)
            except Exception: pass

        st.markdown("#### Denetim Senaryo Sonuçları")
        for sc in scenarios:
            icon = risk_icon(sc["risk"])
            with st.expander(
                f"{icon} {sc['senaryo']}  —  **{sc['risk']}**  ·  {sc['etki']:,} kayıt"
            ):
                st.write(sc["aciklama"])
                if isinstance(sc.get("ornek"), pd.DataFrame) and not sc["ornek"].empty:
                    st.dataframe(sc["ornek"].head(10), use_container_width=True)

        st.markdown("#### En Riskli İşlemler (Top 25)")
        st.dataframe(df_f.nlargest(25, "risk_skoru"), use_container_width=True, height=400)

    # TAB 3
    with t3:
        if not findings:
            st.info("Seçili filtreler dahilinde önemli bulgu tespit edilmedi.")
        else:
            st.dataframe(pd.DataFrame([{
                "Bulgu": f["baslik"], "Risk": f["risk"],
                "Etkilenen": f["etki"], "Kaynak": f["kaynak"],
            } for f in findings]), use_container_width=True)
            st.markdown("---")
            for i, f in enumerate(findings, 1):
                icon = risk_icon(f["risk"])
                with st.expander(
                    f"{icon} Bulgu #{i} · {f['baslik']}  [{f['risk']}]",
                    expanded=(i <= 3)
                ):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**📌 Bulgu**\n\n{f['bulgu']}")
                        st.markdown(f"**🔍 Kök Neden**\n\n{f['kok_neden']}")
                    with col_b:
                        st.markdown(f"**💼 İş Etkisi**\n\n{f['is_etkisi']}")
                        st.markdown(f"**📁 Kaynak:** {f['kaynak']}")
                        st.markdown(f"**⚠️ Etkilenen Kayıt:** {f['etki']:,}")

    # TAB 4
    with t4:
        if not plans:
            st.info("Aksiyon planı gerektiren bulgu yok.")
        else:
            st.dataframe(pd.DataFrame(plans), use_container_width=True)
            st.markdown("---")
            prio_color = {
                "P1 – Acil": "#ef4444", "P2 – Yüksek": "#f59e0b",
                "P3 – Orta": "#3b82f6", "P4 – Düşük": "#10b981",
            }
            for p in plans:
                pc   = prio_color.get(p["oncelik"], "#6366f1")
                icon = risk_icon(p["risk"])
                with st.expander(f"{icon} {p['bulgu']}  [{p['oncelik']}]"):
                    st.markdown(f"**🔧 Önerilen Aksiyon**\n\n{p['aksiyon']}")
                    x, y, z = st.columns(3)
                    x.markdown(f"**🏢 Sorumlu Birim**\n\n{p['birim']}")
                    y.markdown(f"**⚙️ Uygulama Zorluğu**\n\n{p['zorluk']}")
                    z.markdown(f"**🚦 Öncelik**\n\n{p['oncelik']}")

    # TAB 5
    with t5:
        render_executive_summary(df_f, col_map, findings, scenarios)


if __name__ == "__main__":
    main()
