"""
╔══════════════════════════════════════════════════════════════════════╗
║        İÇ DENETİM VERİ ANALİTİĞİ PLATFORMU v1.0                    ║
║        Kıdemli İç Denetim Veri Analitiği Uzmanı tarafından          ║
║        geliştirilmiştir.                                             ║
╚══════════════════════════════════════════════════════════════════════╝

Özellikler:
- Otomatik sütun tanıma ve akıllı yorumlama
- 7 zorunlu denetim modülü
- Risk skorlama motoru
- Yönetici özeti otomatik üretimi
- ERP (SAP/Oracle) uyumlu veri yapısı desteği
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import io
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# SAYFA KONFIGÜRASYONU
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="İç Denetim Analitik Platformu",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS – Kurumsal & Profesyonel Tema
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: #1a2235;
    --bg-card-hover: #1e2a42;
    --accent-blue: #3b82f6;
    --accent-cyan: #06b6d4;
    --accent-red: #ef4444;
    --accent-amber: #f59e0b;
    --accent-green: #10b981;
    --accent-purple: #8b5cf6;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --border: #1e2a42;
    --border-accent: #3b82f6;
}

* { font-family: 'IBM Plex Sans', sans-serif; }
code, .mono { font-family: 'IBM Plex Mono', monospace; }

.stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
}

/* ── Header Banner ── */
.audit-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #3730a3;
    border-radius: 12px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.audit-header::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.audit-header h1 {
    font-size: 1.8rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
    letter-spacing: -0.5px;
}
.audit-header p {
    color: #94a3b8;
    margin: 6px 0 0 0;
    font-size: 0.9rem;
}
.audit-badge {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid #6366f1;
    color: #a5b4fc;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}
.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 10px 10px 0 0;
}
.kpi-card.blue::after { background: var(--accent-blue); }
.kpi-card.red::after { background: var(--accent-red); }
.kpi-card.amber::after { background: var(--accent-amber); }
.kpi-card.green::after { background: var(--accent-green); }

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--text-secondary);
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    font-family: 'IBM Plex Mono', monospace;
    line-height: 1;
}
.kpi-card.blue .kpi-value { color: var(--accent-blue); }
.kpi-card.red .kpi-value { color: var(--accent-red); }
.kpi-card.amber .kpi-value { color: var(--accent-amber); }
.kpi-card.green .kpi-value { color: var(--accent-green); }
.kpi-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 24px 0 16px 0;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
}
.section-header h2 {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0;
}
.section-icon {
    width: 32px; height: 32px;
    background: rgba(59,130,246,0.1);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
}

/* ── Finding Cards ── */
.finding-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 4px solid;
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.finding-card.critical { border-left-color: var(--accent-red); }
.finding-card.high { border-left-color: var(--accent-amber); }
.finding-card.medium { border-left-color: var(--accent-blue); }
.finding-card.low { border-left-color: var(--accent-green); }

.finding-title {
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 6px;
}
.finding-body {
    color: var(--text-secondary);
    font-size: 0.85rem;
    line-height: 1.5;
}
.risk-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-right: 8px;
}
.risk-badge.critical { background: rgba(239,68,68,0.15); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.risk-badge.high { background: rgba(245,158,11,0.15); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }
.risk-badge.medium { background: rgba(59,130,246,0.15); color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
.risk-badge.low { background: rgba(16,185,129,0.15); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }

/* ── Action Plan Cards ── */
.action-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 10px;
}
.action-card h4 {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-primary);
    margin: 0 0 8px 0;
}
.action-meta {
    display: flex;
    gap: 16px;
    font-size: 0.78rem;
    color: var(--text-secondary);
    flex-wrap: wrap;
}
.action-meta span { display: flex; align-items: center; gap: 4px; }

/* ── Executive Summary ── */
.exec-summary {
    background: linear-gradient(135deg, #0f172a 0%, #1a1145 100%);
    border: 1px solid #4338ca;
    border-radius: 12px;
    padding: 32px 36px;
}
.exec-summary h2 {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e0e7ff;
    margin-bottom: 6px;
}
.exec-summary .subtitle {
    color: #818cf8;
    font-size: 0.85rem;
    margin-bottom: 24px;
    font-family: 'IBM Plex Mono', monospace;
}
.exec-section {
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid rgba(99,102,241,0.2);
}
.exec-section:last-child { border-bottom: none; }
.exec-section h3 {
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #818cf8;
    margin-bottom: 10px;
}
.exec-section p {
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.7;
    margin: 0;
}

/* ── Data Table Styling ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0d1424 !important;
    border-right: 1px solid #1e2a42 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--text-secondary);
}
.stTabs [aria-selected="true"] {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

/* ── Upload Area ── */
.stFileUploader {
    background: var(--bg-card);
    border-radius: 10px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ── Metric override ── */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
}

.info-box {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 8px;
    padding: 14px 18px;
    color: #93c5fd;
    font-size: 0.85rem;
    margin-bottom: 16px;
}
.warning-box {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 8px;
    padding: 14px 18px;
    color: #fcd34d;
    font-size: 0.85rem;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# YARDIMCI FONKSİYONLAR
# ═══════════════════════════════════════════════════════════════

def detect_columns(df: pd.DataFrame) -> dict:
    """
    Sütun isimlerini otomatik tanı ve semantik kategorilere ayır.
    SAP/Oracle ERP terminolojisi dahil geniş kelime havuzu kullanılır.
    """
    cols = {c.lower().strip(): c for c in df.columns}
    mapping = {}

    # --- TUTAR sütunu ---
    amount_kws = ['tutar', 'amount', 'fiyat', 'price', 'miktar', 'total',
                  'net', 'gross', 'deger', 'değer', 'bedel', 'sum', 'toplam',
                  'debit', 'credit', 'borc', 'borç', 'alacak', 'wrbtr', 'dmbtr']
    for kw in amount_kws:
        for lk, ok in cols.items():
            if kw in lk and 'amount' not in mapping:
                mapping['amount'] = ok

    # --- TARİH sütunu ---
    date_kws = ['tarih', 'date', 'timestamp', 'time', 'zaman', 'gün', 'gun',
                'bldat', 'budat', 'cpudt', 'erdat']
    for kw in date_kws:
        for lk, ok in cols.items():
            if kw in lk and 'date' not in mapping:
                mapping['date'] = ok

    # --- TEDARİKÇİ/MÜŞTERI sütunu ---
    vendor_kws = ['tedarikci', 'tedarikçi', 'vendor', 'supplier', 'satici',
                  'satıcı', 'müşteri', 'musteri', 'customer', 'client',
                  'lifnr', 'kunnr', 'partner']
    for kw in vendor_kws:
        for lk, ok in cols.items():
            if kw in lk and 'vendor' not in mapping:
                mapping['vendor'] = ok

    # --- KULLANICI/PERSONEL sütunu ---
    user_kws = ['kullanici', 'kullanıcı', 'user', 'personel', 'employee',
                'ernam', 'aenam', 'usnam', 'uname', 'operator']
    for kw in user_kws:
        for lk, ok in cols.items():
            if kw in lk and 'user' not in mapping:
                mapping['user'] = ok

    # --- BELGE NO sütunu ---
    doc_kws = ['belge', 'document', 'docnum', 'belnr', 'vbeln', 'ebeln',
               'invoice', 'fatura', 'siparis', 'siparış', 'order', 'id',
               'no', 'num', 'number', 'ref']
    for kw in doc_kws:
        for lk, ok in cols.items():
            if kw in lk and 'doc_id' not in mapping:
                mapping['doc_id'] = ok

    # --- KATEGORİ / TİP sütunu ---
    cat_kws = ['kategori', 'category', 'tip', 'type', 'tur', 'tür', 'sinif',
               'sınıf', 'hesap', 'account', 'gl', 'cost', 'maliyet', 'hkont']
    for kw in cat_kws:
        for lk, ok in cols.items():
            if kw in lk and 'category' not in mapping:
                mapping['category'] = ok

    # --- ONAY/DURUM sütunu ---
    status_kws = ['onay', 'approval', 'status', 'durum', 'state', 'approved']
    for kw in status_kws:
        for lk, ok in cols.items():
            if kw in lk and 'status' not in mapping:
                mapping['status'] = ok

    # Hiç tespit edilemezse ilk sayısal sütunu amount, ilk datetime'ı date yap
    num_cols = df.select_dtypes(include='number').columns.tolist()
    dt_cols = df.select_dtypes(include='datetime').columns.tolist()
    if 'amount' not in mapping and num_cols:
        mapping['amount'] = num_cols[0]
    if 'date' not in mapping and dt_cols:
        mapping['date'] = dt_cols[0]
    if 'date' not in mapping:
        # String sütunlarda tarih ara
        for c in df.columns:
            try:
                pd.to_datetime(df[c].dropna().head(5))
                mapping['date'] = c
                break
            except Exception:
                pass

    # vendor bulunamazsa string sütunlardan birini ata
    str_cols = df.select_dtypes(include='object').columns.tolist()
    if 'vendor' not in mapping and str_cols:
        mapping['vendor'] = str_cols[0]
    if 'user' not in mapping and len(str_cols) > 1:
        mapping['user'] = str_cols[1]
    if 'category' not in mapping and len(str_cols) > 2:
        mapping['category'] = str_cols[2]

    return mapping


def parse_dates(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    """Tarih sütununu güvenli biçimde parse et."""
    try:
        df[date_col] = pd.to_datetime(df[date_col], infer_format=True, errors='coerce')
    except Exception:
        pass
    return df


def get_amount_series(df: pd.DataFrame, col: str) -> pd.Series:
    """Tutar sütununu sayısal seriye çevir."""
    s = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace(' ', ''),
                      errors='coerce')
    return s


# ═══════════════════════════════════════════════════════════════
# MODÜL 1 – VERİ KALİTESİ VE KONTROL TESTLERİ
# ═══════════════════════════════════════════════════════════════

def run_data_quality_tests(df: pd.DataFrame, col_map: dict) -> dict:
    """
    Denetim standartlarına uygun veri kalite kontrolleri.
    Her kontrol bir bulgu nesnesi döndürür.
    """
    results = []
    total = len(df)

    # 1. Eksik veri analizi
    missing = df.isnull().sum()
    missing_pct = (missing / total * 100).round(2)
    critical_missing = missing[missing_pct > 10]
    results.append({
        'kontrol': 'Eksik Veri Analizi',
        'bulgu': f"{len(critical_missing)} sütunda >%10 eksik veri tespit edildi.",
        'etkilenen_kayit': int(df.isnull().any(axis=1).sum()),
        'risk': 'Orta' if len(critical_missing) < 3 else 'Yüksek',
        'detay': missing_pct[missing_pct > 0].to_dict()
    })

    # 2. Mükerrer kayıt tespiti
    if 'doc_id' in col_map:
        dup_col = col_map['doc_id']
        dup_count = df.duplicated(subset=[dup_col], keep=False).sum()
        results.append({
            'kontrol': 'Mükerrer Kayıt Tespiti',
            'bulgu': f"{dup_count} kayıt mükerrer belge numarası içeriyor ({dup_col}).",
            'etkilenen_kayit': int(dup_count),
            'risk': 'Kritik' if dup_count > 0 else 'Düşük',
            'detay': {}
        })

    # 3. Tam mükerrer satır
    full_dup = df.duplicated().sum()
    results.append({
        'kontrol': 'Tam Satır Mükerrerlik',
        'bulgu': f"{full_dup} adet birebir aynı satır tespit edildi.",
        'etkilenen_kayit': int(full_dup),
        'risk': 'Yüksek' if full_dup > 0 else 'Düşük',
        'detay': {}
    })

    # 4. Negatif/sıfır tutar kontrolü
    if 'amount' in col_map:
        amt = get_amount_series(df, col_map['amount'])
        neg_count = int((amt < 0).sum())
        zero_count = int((amt == 0).sum())
        results.append({
            'kontrol': 'Negatif & Sıfır Tutar Kontrolü',
            'bulgu': f"{neg_count} negatif, {zero_count} sıfır değerli kayıt bulundu.",
            'etkilenen_kayit': neg_count + zero_count,
            'risk': 'Yüksek' if neg_count > 5 else ('Orta' if neg_count > 0 else 'Düşük'),
            'detay': {'negatif': neg_count, 'sifir': zero_count}
        })

    # 5. Aykırı değer analizi – IQR ve Z-score
    if 'amount' in col_map:
        amt = get_amount_series(df, col_map['amount']).dropna()
        Q1, Q3 = amt.quantile(0.25), amt.quantile(0.75)
        IQR = Q3 - Q1
        iqr_outliers = int(((amt < Q1 - 1.5 * IQR) | (amt > Q3 + 1.5 * IQR)).sum())
        z_scores = np.abs((amt - amt.mean()) / (amt.std() + 1e-9))
        z_outliers = int((z_scores > 3).sum())
        results.append({
            'kontrol': 'Aykırı Değer Analizi (IQR / Z-score)',
            'bulgu': f"IQR yöntemiyle {iqr_outliers}, Z-score yöntemiyle {z_outliers} aykırı tutar tespit edildi.",
            'etkilenen_kayit': max(iqr_outliers, z_outliers),
            'risk': 'Yüksek' if max(iqr_outliers, z_outliers) > 10 else 'Orta',
            'detay': {'iqr': iqr_outliers, 'z_score': z_outliers}
        })

    # 6. Şüpheli yuvarlama desenleri (ending in 00, 000)
    if 'amount' in col_map:
        amt = get_amount_series(df, col_map['amount']).dropna()
        round_100 = int(((amt % 100 == 0) & (amt != 0)).sum())
        round_1000 = int(((amt % 1000 == 0) & (amt != 0)).sum())
        total_nonzero = int((amt != 0).sum())
        pct_round = (round_100 / total_nonzero * 100) if total_nonzero > 0 else 0
        results.append({
            'kontrol': 'Şüpheli Yuvarlama Deseni',
            'bulgu': f"Tutarların %{pct_round:.1f}'i 100'ün katı. {round_1000} kayıt 1000'in katı.",
            'etkilenen_kayit': round_100,
            'risk': 'Yüksek' if pct_round > 30 else ('Orta' if pct_round > 15 else 'Düşük'),
            'detay': {'yuzde_100_kat': round(pct_round, 1), 'round_1000': round_1000}
        })

    # 7. Tarih tutarsızlıkları
    if 'date' in col_map:
        df2 = parse_dates(df.copy(), col_map['date'])
        nat_count = int(df2[col_map['date']].isna().sum())
        future_count = int((df2[col_map['date']] > pd.Timestamp.now()).sum())
        results.append({
            'kontrol': 'Tarih Tutarsızlıkları',
            'bulgu': f"{nat_count} geçersiz tarih, {future_count} gelecek tarihli kayıt.",
            'etkilenen_kayit': nat_count + future_count,
            'risk': 'Orta' if (nat_count + future_count) > 0 else 'Düşük',
            'detay': {'gecersiz': nat_count, 'gelecek': future_count}
        })

    return results


# ═══════════════════════════════════════════════════════════════
# MODÜL 2 – DENETİM SENARYOSU MOTORU
# ═══════════════════════════════════════════════════════════════

def run_audit_scenarios(df: pd.DataFrame, col_map: dict) -> list:
    """
    Denetim risk senaryolarını otomatik çalıştır.
    Her senaryo standart bir bulgu formatında döndürülür.
    """
    scenarios = []
    amt = get_amount_series(df, col_map['amount']) if 'amount' in col_map else None

    # ── SENARYO 1: Olağandışı işlem sıklığı ──
    if 'date' in col_map:
        df2 = parse_dates(df.copy(), col_map['date'])
        daily_counts = df2.groupby(df2[col_map['date']].dt.date).size()
        if len(daily_counts) > 0:
            mean_tx = daily_counts.mean()
            std_tx = daily_counts.std()
            spike_days = daily_counts[daily_counts > mean_tx + 2 * std_tx]
            scenarios.append({
                'senaryo': 'Olağandışı İşlem Yoğunluğu',
                'aciklama': 'Günlük işlem sayısının istatistiksel ortalamayı 2 standart sapma aşması.',
                'risk': 'Veride manipülasyon veya sistem hatası riski.',
                'etkilenen': int(spike_days.sum()),
                'risk_seviyesi': 'Yüksek' if len(spike_days) > 2 else 'Orta',
                'ornek': daily_counts.nlargest(5).reset_index().rename(
                    columns={col_map['date']: 'Tarih', 0: 'İşlem Sayısı'}
                ) if len(daily_counts) > 0 else pd.DataFrame()
            })

    # ── SENARYO 2: Tedarikçi yoğunlaşması ──
    if 'vendor' in col_map and amt is not None:
        vendor_amt = df.assign(_amt=amt).groupby(col_map['vendor'])['_amt'].agg(['sum', 'count'])
        vendor_amt.columns = ['Toplam Tutar', 'İşlem Sayısı']
        vendor_amt = vendor_amt.sort_values('Toplam Tutar', ascending=False)
        top1_share = vendor_amt['Toplam Tutar'].iloc[0] / (vendor_amt['Toplam Tutar'].sum() + 1e-9) * 100
        scenarios.append({
            'senaryo': 'Tedarikçi Yoğunlaşması (Concentration Risk)',
            'aciklama': f"En büyük tedarikçi toplam tutarın %{top1_share:.1f}'ini oluşturuyor.",
            'risk': 'Bağımlılık riski, gizli ilişki veya rekabetçi ihale süreçlerini atlatma.',
            'etkilenen': len(vendor_amt[vendor_amt['Toplam Tutar'] > vendor_amt['Toplam Tutar'].mean() * 3]),
            'risk_seviyesi': 'Kritik' if top1_share > 50 else ('Yüksek' if top1_share > 30 else 'Orta'),
            'ornek': vendor_amt.head(10).reset_index()
        })

    # ── SENARYO 3: Mesai dışı işlemler ──
    if 'date' in col_map:
        df2 = parse_dates(df.copy(), col_map['date'])
        try:
            hours = df2[col_map['date']].dt.hour
            off_hours = (hours < 8) | (hours > 18)
            off_count = int(off_hours.sum())
            if off_count > 0:
                scenarios.append({
                    'senaryo': 'Mesai Dışı Saat İşlemleri',
                    'aciklama': f"{off_count} işlem 08:00–18:00 dışında gerçekleştirilmiş.",
                    'risk': 'Yetkisiz erişim, veri manipülasyonu veya iç kontrol atlatma riski.',
                    'etkilenen': off_count,
                    'risk_seviyesi': 'Yüksek' if off_count > 10 else 'Orta',
                    'ornek': df2[off_hours].head(10)
                })
        except Exception:
            pass

    # ── SENARYO 4: Yetki eşiği altı işlemler (Just Below Threshold) ──
    if amt is not None:
        thresholds = [5000, 10000, 25000, 50000, 100000]
        for thresh in thresholds:
            below = ((amt > thresh * 0.9) & (amt < thresh)).sum()
            if below > 3:
                scenarios.append({
                    'senaryo': f'Eşik Altı İşlemler ({thresh:,} TL)',
                    'aciklama': f"{int(below)} işlem {thresh:,} TL eşiğinin hemen altında (%90-100 arasında).",
                    'risk': 'Onay eşiğini kasıtlı aşındırma (Structuring / Threshold Avoidance) riski.',
                    'etkilenen': int(below),
                    'risk_seviyesi': 'Kritik' if below > 10 else 'Yüksek',
                    'ornek': df.assign(_amt=amt)[(amt > thresh * 0.9) & (amt < thresh)].head(10)
                })
                break  # İlk bulunan eşik yeterli

    # ── SENARYO 5: Görevler Ayrılığı (SoD) – Aynı kullanıcı ──
    if 'user' in col_map and 'status' in col_map:
        user_status = df.groupby([col_map['user'], col_map['status']]).size().unstack(fill_value=0)
        # Kullanıcı hem oluşturma hem onay rolünde ise SoD ihlali
        cols_lower = [c.lower() for c in user_status.columns]
        create_cols = [c for c in user_status.columns if any(k in c.lower() for k in ['onay', 'approv', 'onayla'])]
        if create_cols:
            sod_users = user_status[user_status[create_cols[0]] > 0]
            scenarios.append({
                'senaryo': 'Görevler Ayrılığı (SoD) Riski',
                'aciklama': f"{len(sod_users)} kullanıcı hem işlem oluşturma hem onaylama yetkisine sahip görünüyor.",
                'risk': 'İç kontrol çerçevesinde kritik görevler ayrılığı ihlali.',
                'etkilenen': len(sod_users),
                'risk_seviyesi': 'Kritik' if len(sod_users) > 0 else 'Düşük',
                'ornek': sod_users.reset_index().head(10)
            })

    # ── SENARYO 6: Tekrarlayan aynı tutar ──
    if amt is not None:
        val_counts = amt.round(2).value_counts()
        repeated = val_counts[val_counts > 5]
        if len(repeated) > 0:
            scenarios.append({
                'senaryo': 'Tekrarlayan Aynı Tutar Deseni',
                'aciklama': f"{len(repeated)} farklı tutar değeri 5'ten fazla tekrar ediyor.",
                'risk': 'Sistematik veri girişi hatası veya sahte işlem dizisi riski.',
                'etkilenen': int(repeated.sum()),
                'risk_seviyesi': 'Yüksek' if len(repeated) > 5 else 'Orta',
                'ornek': repeated.head(10).reset_index().rename(
                    columns={'index': 'Tutar', col_map['amount']: 'Tekrar Sayısı'}
                )
            })

    return scenarios


# ═══════════════════════════════════════════════════════════════
# MODÜL 3 – RİSK SKORLAMA MODELİ
# ═══════════════════════════════════════════════════════════════

def compute_risk_scores(df: pd.DataFrame, col_map: dict) -> pd.DataFrame:
    """
    Her kayıt için 0-100 arası birleşik risk skoru hesapla.
    Ağırlıklar: Tutar etkisi 40%, Aykırılık 35%, Frekans 25%
    """
    df = df.copy()
    scores = pd.Series(0.0, index=df.index)

    # Tutar bileşeni (0-40)
    if 'amount' in col_map:
        amt = get_amount_series(df, col_map['amount']).fillna(0)
        amt_abs = amt.abs()
        max_amt = amt_abs.quantile(0.99) + 1e-9
        amount_score = (amt_abs / max_amt).clip(0, 1) * 40
        scores += amount_score

    # Aykırılık bileşeni (0-35) – Z-score tabanlı
    if 'amount' in col_map:
        amt = get_amount_series(df, col_map['amount']).fillna(0)
        z = np.abs((amt - amt.mean()) / (amt.std() + 1e-9))
        anomaly_score = (z / (z.quantile(0.99) + 1e-9)).clip(0, 1) * 35
        scores += anomaly_score

    # Frekans bileşeni (0-25) – Aynı vendor/user frekansı
    if 'vendor' in col_map:
        vendor_freq = df[col_map['vendor']].map(df[col_map['vendor']].value_counts())
        max_freq = vendor_freq.max() + 1e-9
        freq_score = (vendor_freq / max_freq) * 25
        scores += freq_score
    elif 'user' in col_map:
        user_freq = df[col_map['user']].map(df[col_map['user']].value_counts())
        max_freq = user_freq.max() + 1e-9
        freq_score = (user_freq / max_freq) * 25
        scores += freq_score

    df['risk_skoru'] = scores.clip(0, 100).round(1)

    def classify(s):
        if s >= 75: return 'Kritik'
        elif s >= 50: return 'Yüksek'
        elif s >= 25: return 'Orta'
        else: return 'Düşük'

    df['risk_seviyesi'] = df['risk_skoru'].apply(classify)
    return df


# ═══════════════════════════════════════════════════════════════
# MODÜL 4 – DENETİM BULGULARI
# ═══════════════════════════════════════════════════════════════

def generate_audit_findings(df: pd.DataFrame, col_map: dict,
                            quality_results: list, scenarios: list) -> list:
    """
    Denetim standartlarına uygun yapılandırılmış bulgular üret.
    Her bulgu: başlık, açıklama, kök neden, iş etkisi.
    """
    findings = []

    # Kalite testlerinden bulgular
    risk_priority = {'Kritik': 0, 'Yüksek': 1, 'Orta': 2, 'Düşük': 3}
    for qr in quality_results:
        if qr['etkilenen_kayit'] > 0 and qr['risk'] in ['Kritik', 'Yüksek', 'Orta']:
            findings.append({
                'baslik': f"VERİ KALİTESİ: {qr['kontrol']}",
                'aciklama': f"BULGU: {qr['bulgu']}",
                'kok_neden': _infer_root_cause(qr['kontrol']),
                'is_etkisi': _infer_business_impact(qr['kontrol'], qr['etkilened_kayit'] if 'etkilened_kayit' in qr else qr['etkilenen_kayit']),
                'risk_seviyesi': qr['risk'],
                'etkilenen': qr['etkilenen_kayit'],
                'kaynak': 'Veri Kalite Kontrolleri'
            })

    # Senaryo bulgularından
    for sc in scenarios:
        if sc['etkilenen'] > 0:
            findings.append({
                'baslik': f"DENETİM SENARYOSU: {sc['senaryo']}",
                'aciklama': f"BULGU: {sc['aciklama']} {sc['risk']}",
                'kok_neden': _infer_scenario_root_cause(sc['senaryo']),
                'is_etkisi': _infer_scenario_impact(sc['senaryo'], sc['etkilenen']),
                'risk_seviyesi': sc['risk_seviyesi'],
                'etkilenen': sc['etkilenen'],
                'kaynak': 'Denetim Senaryo Motoru'
            })

    # Risk skoru yüksek kayıt özeti
    if 'risk_skoru' in df.columns:
        critical_pct = (df['risk_seviyesi'] == 'Kritik').mean() * 100
        if critical_pct > 5:
            findings.append({
                'baslik': 'RİSK SKORU: Kritik Kayıt Yoğunluğu',
                'aciklama': f"BULGU: Kayıtların %{critical_pct:.1f}'i kritik risk seviyesinde. Bu oran kabul edilebilir eşiğin üzerindedir.",
                'kok_neden': 'Kontrol ortamında sistemik zafiyetler veya yüksek riskli işlem profilinin varlığı.',
                'is_etkisi': 'Finansal kayıp, uyumsuzluk cezası ve itibar riski.',
                'risk_seviyesi': 'Kritik',
                'etkilenen': int((df['risk_seviyesi'] == 'Kritik').sum()),
                'kaynak': 'Risk Skorlama Modeli'
            })

    # Öncelik sırasına göre sırala
    findings.sort(key=lambda x: risk_priority.get(x['risk_seviyesi'], 4))
    return findings


def _infer_root_cause(control_name: str) -> str:
    mapping = {
        'Eksik Veri': 'Veri giriş kontrollerinin yetersizliği veya sistem entegrasyon hatası.',
        'Mükerrer': 'Benzersiz kısıtlama (unique constraint) eksikliği veya onay sürecindeki boşluklar.',
        'Negatif': 'Ters kayıt prosedürlerinde kontrol mekanizması eksikliği.',
        'Aykırı': 'Tutar onay limitleri veya istatistiksel izleme kontrollerinin bulunmaması.',
        'Yuvarlama': 'Tahmini ya da sahte veri girişine işaret eden sistematik veri kalıbı.',
        'Tarih': 'Sistem tarih/saat kontrollerinin yetersizliği veya geriye dönük veri değişikliği.'
    }
    for k, v in mapping.items():
        if k.lower() in control_name.lower():
            return v
    return 'İlgili süreçte yeterli iç kontrol mekanizmasının bulunmaması.'


def _infer_business_impact(control_name: str, count: int) -> str:
    return (f"{count} etkilenen kayıt ile finansal raporlama güvenilirliğine ve "
            f"uyumluluk çerçevesine olumsuz etki riski bulunmaktadır.")


def _infer_scenario_root_cause(scenario_name: str) -> str:
    mapping = {
        'yoğunlaşma': 'Satınalma politikasında alternatif teklif zorunluluğu veya harcama onay limitlerinin uygulanmaması.',
        'mesai dışı': 'Sistem erişim politikasında zaman bazlı kısıtlamaların bulunmaması.',
        'eşik': 'Kontrol tasarımında tutar bazlı onay eşiklerini aşındırmaya yönelik sistemik açık.',
        'sod': 'Rol bazlı erişim kontrol (RBAC) politikasının yetersiz tanımlanmış olması.',
        'tekrarlayan': 'Veri doğrulama ve sistem kontrol mekanizmalarının yetersizliği.',
        'olağandışı': 'İşlem izleme ve anomali tespitine yönelik kontrol eksikliği.'
    }
    for k, v in mapping.items():
        if k.lower() in scenario_name.lower():
            return v
    return 'İlgili süreçte preventif kontrol mekanizmasının bulunmaması.'


def _infer_scenario_impact(scenario_name: str, count: int) -> str:
    return (f"{count} etkilenen kayıt; usulsüzlük, hata veya uyumsuzluk sonucu "
            f"finansal ve operasyonel risk oluşturmaktadır.")


# ═══════════════════════════════════════════════════════════════
# MODÜL 5 – AKSİYON PLANI ÜRETİCİSİ
# ═══════════════════════════════════════════════════════════════

def generate_action_plans(findings: list) -> list:
    """
    Her önemli bulgu için somut düzeltici aksiyon planı üret.
    """
    action_mapping = {
        'Mükerrer': {
            'aksiyon': 'Veritabanı düzeyinde benzersiz kısıtlama (unique constraint) tanımlanması ve ERP sisteminde mükerrer kayıt kontrolü aktivasyonu.',
            'birim': 'Bilgi Teknolojileri / Finans',
            'zorluk': 'Orta'
        },
        'Negatif': {
            'aksiyon': 'Negatif değer giriş politikasının gözden geçirilmesi; kural motoru ile otomatik uyarı sistemi kurulumu.',
            'birim': 'Finans / İç Kontrol',
            'zorluk': 'Düşük'
        },
        'Aykırı': {
            'aksiyon': 'Tutar onay matrisinin yeniden yapılandırılması; istatistiksel anomali tespiti için sürekli izleme aracı entegrasyonu.',
            'birim': 'Finans / İç Denetim',
            'zorluk': 'Yüksek'
        },
        'Yuvarlama': {
            'aksiyon': 'Yüksek risk profilli yuvarlak tutarlı işlemlerin ek onay sürecine tabi tutulması; veri girişi zorunlu alan denetimi.',
            'birim': 'Finans / Operasyon',
            'zorluk': 'Düşük'
        },
        'Yoğunlaşma': {
            'aksiyon': 'Alternatif teklif (en az 3 teklif) politikasının uygulamaya alınması; yoğunlaşma limitlerinin satınalma prosedürüne eklenmesi.',
            'birim': 'Satınalma / Üst Yönetim',
            'zorluk': 'Orta'
        },
        'Mesai Dışı': {
            'aksiyon': 'Sistem erişiminde zaman bazlı kısıtlama profilleri oluşturulması; mesai dışı giriş için çok faktörlü kimlik doğrulama zorunluluğu.',
            'birim': 'Bilgi Teknolojileri / Güvenlik',
            'zorluk': 'Orta'
        },
        'Eşik': {
            'aksiyon': 'Eşik altı işlemlerin toplu değerlendirme mekanizmasına dahil edilmesi; birikimli limit kontrol sürecinin tasarlanması.',
            'birim': 'Finans / Satınalma / İç Kontrol',
            'zorluk': 'Yüksek'
        },
        'SoD': {
            'aksiyon': 'Rol bazlı erişim kontrolü (RBAC) politikasının güncellenmesi; oluşturma ve onay rollerinin ayrıştırılması; SoD matrisi revizyonu.',
            'birim': 'Bilgi Teknolojileri / İnsan Kaynakları / İç Kontrol',
            'zorluk': 'Yüksek'
        },
        'Eksik': {
            'aksiyon': 'Zorunlu alan kurallarının (mandatory field) ERP sisteminde aktive edilmesi; veri tamamlama prosedürünün oluşturulması.',
            'birim': 'Bilgi Teknolojileri / Finans',
            'zorluk': 'Düşük'
        },
        'Tarih': {
            'aksiyon': 'Sistem tarih kontrollerinin güçlendirilmesi; geriye dönük kayıt girişi için üst yönetim onay sürecinin tasarlanması.',
            'birim': 'Bilgi Teknolojileri / Finans',
            'zorluk': 'Orta'
        }
    }

    priority_map = {'Kritik': 'P1 – Acil', 'Yüksek': 'P2 – Yüksek',
                    'Orta': 'P3 – Orta', 'Düşük': 'P4 – Düşük'}
    plans = []

    for f in findings:
        if f['risk_seviyesi'] in ['Kritik', 'Yüksek', 'Orta']:
            matched_action = None
            for kw, action_data in action_mapping.items():
                if kw.lower() in f['baslik'].lower() or kw.lower() in f['aciklama'].lower():
                    matched_action = action_data
                    break
            if not matched_action:
                matched_action = {
                    'aksiyon': 'İlgili sürecin kapsamlı incelenmesi ve kontrol açığını kapatan prosedür oluşturulması.',
                    'birim': 'İç Kontrol / Yönetim',
                    'zorluk': 'Orta'
                }
            plans.append({
                'bulgu': f['baslik'],
                'aksiyon': matched_action['aksiyon'],
                'birim': matched_action['birim'],
                'oncelik': priority_map.get(f['risk_seviyesi'], 'P3'),
                'zorluk': matched_action['zorluk'],
                'risk_seviyesi': f['risk_seviyesi']
            })

    return plans


# ═══════════════════════════════════════════════════════════════
# MODÜL 6 – GRAFİKLER
# ═══════════════════════════════════════════════════════════════

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(17,24,39,0)',
    plot_bgcolor='rgba(26,34,53,0.5)',
    font=dict(family='IBM Plex Sans', color='#94a3b8', size=12),
    xaxis=dict(gridcolor='#1e2a42', zerolinecolor='#1e2a42'),
    yaxis=dict(gridcolor='#1e2a42', zerolinecolor='#1e2a42'),
    colorway=['#3b82f6', '#06b6d4', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444']
)


def plot_risk_distribution(df: pd.DataFrame) -> go.Figure:
    counts = df['risk_seviyesi'].value_counts().reindex(
        ['Kritik', 'Yüksek', 'Orta', 'Düşük'], fill_value=0
    )
    colors = {'Kritik': '#ef4444', 'Yüksek': '#f59e0b',
               'Orta': '#3b82f6', 'Düşük': '#10b981'}
    fig = go.Figure(go.Bar(
        x=counts.index, y=counts.values,
        marker_color=[colors[r] for r in counts.index],
        text=counts.values, textposition='outside',
        textfont=dict(color='#f1f5f9', size=13, family='IBM Plex Mono')
    ))
    fig.update_layout(
        title='Risk Dağılımı', title_font_size=14,
        **PLOTLY_THEME, height=320,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def plot_time_trend(df: pd.DataFrame, col_map: dict) -> go.Figure:
    df2 = parse_dates(df.copy(), col_map['date'])
    df2['_month'] = df2[col_map['date']].dt.to_period('M').astype(str)
    monthly = df2.groupby('_month').agg(
        Sayı=('risk_skoru', 'count'),
        Ort_Risk=('risk_skoru', 'mean')
    ).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=monthly['_month'], y=monthly['Sayı'],
        name='İşlem Sayısı', marker_color='rgba(59,130,246,0.5)'
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly['_month'], y=monthly['Ort_Risk'],
        name='Ort. Risk Skoru', mode='lines+markers',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=6)
    ), secondary_y=True)
    fig.update_layout(
        title='Aylık İşlem & Risk Trendi', title_font_size=14,
        **PLOTLY_THEME, height=320,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation='h', yanchor='bottom', y=1.02)
    )
    fig.update_yaxes(title_text="İşlem Sayısı", secondary_y=False)
    fig.update_yaxes(title_text="Risk Skoru", secondary_y=True)
    return fig


def plot_vendor_concentration(df: pd.DataFrame, col_map: dict) -> go.Figure:
    amt = get_amount_series(df, col_map['amount'])
    vc = df.assign(_amt=amt).groupby(col_map['vendor'])['_amt'].sum().nlargest(10)
    fig = go.Figure(go.Bar(
        y=vc.index.astype(str), x=vc.values,
        orientation='h',
        marker=dict(
            color=vc.values,
            colorscale=[[0, '#1a2235'], [0.5, '#3b82f6'], [1, '#ef4444']],
            showscale=False
        ),
        text=[f"{v:,.0f}" for v in vc.values],
        textposition='outside',
        textfont=dict(color='#94a3b8', size=10)
    ))
    fig.update_layout(
        title='Tedarikçi / Karşı Taraf Yoğunlaşması (Top 10)',
        title_font_size=14,
        **PLOTLY_THEME, height=360,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis=dict(autorange='reversed', **PLOTLY_THEME.get('yaxis', {}))
    )
    return fig


def plot_risk_heatmap(df: pd.DataFrame, col_map: dict) -> go.Figure:
    """Kategori x Risk Seviyesi ısı haritası."""
    cat_col = col_map.get('category') or col_map.get('vendor')
    if not cat_col:
        return None
    top_cats = df[cat_col].value_counts().nlargest(8).index
    sub = df[df[cat_col].isin(top_cats)]
    heat = sub.groupby([cat_col, 'risk_seviyesi']).size().unstack(fill_value=0)
    heat = heat.reindex(columns=['Kritik', 'Yüksek', 'Orta', 'Düşük'], fill_value=0)

    fig = go.Figure(go.Heatmap(
        z=heat.values, x=heat.columns, y=heat.index.astype(str),
        colorscale=[[0, '#1a2235'], [0.3, '#1d4ed8'], [0.7, '#f59e0b'], [1, '#ef4444']],
        text=heat.values, texttemplate='%{text}',
        textfont=dict(size=11, color='white')
    ))
    fig.update_layout(
        title='Risk Isı Haritası (Kategori x Risk Seviyesi)', title_font_size=14,
        **PLOTLY_THEME, height=360,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


def plot_score_histogram(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=df['risk_skoru'],
        nbinsx=20,
        marker=dict(
            color=df['risk_skoru'],
            colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#ef4444']],
            showscale=True,
            colorbar=dict(title='Risk')
        )
    ))
    fig.update_layout(
        title='Risk Skoru Dağılımı', title_font_size=14,
        **PLOTLY_THEME, height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_title='Risk Skoru (0-100)',
        yaxis_title='Kayıt Sayısı'
    )
    return fig


# ═══════════════════════════════════════════════════════════════
# MODÜL 7 – YÖNETİCİ ÖZETİ
# ═══════════════════════════════════════════════════════════════

def generate_executive_summary(df: pd.DataFrame, col_map: dict,
                               findings: list, scenarios: list,
                               quality_results: list) -> dict:
    """
    Profesyonel İç Denetim Yönetici Özeti metni üret.
    """
    total = len(df)
    critical = (df['risk_seviyesi'] == 'Kritik').sum()
    high = (df['risk_seviyesi'] == 'Yüksek').sum()
    avg_score = df['risk_skoru'].mean()
    date_str = datetime.now().strftime('%d %B %Y')

    # Genel risk değerlendirmesi
    if avg_score >= 60 or critical / total > 0.15:
        genel_risk = 'KRİTİK'
        genel_yorum = ('Analiz sonuçları, incelenen veri setinde iç kontrol ortamının kritik düzeyde '
                      'zayıfladığını ortaya koymaktadır. Acil müdahale gerektiren bulgular mevcuttur.')
    elif avg_score >= 40 or (critical + high) / total > 0.25:
        genel_risk = 'YÜKSEK'
        genel_yorum = ('İnceleme kapsamındaki veriler, birden fazla kritik kontrol zafiyetine işaret '
                      'etmektedir. Bulgular, öncelikli aksiyon planlaması gerektirmektedir.')
    elif avg_score >= 25:
        genel_risk = 'ORTA'
        genel_yorum = ('Veri kalitesi ve denetim senaryoları, belirli süreç alanlarında kontrol '
                      'iyileştirme ihtiyacını ortaya koymaktadır. Takip döneminde izleme önerilmektedir.')
    else:
        genel_risk = 'DÜŞÜK'
        genel_yorum = ('Analiz edilen veri seti makul düzeyde kontrol bütünlüğü sergilemektedir. '
                      'Tespit edilen birkaç düşük riskli bulgu izleme kapsamına alınmalıdır.')

    # Kritik kontrol zafiyetleri
    kritik_bulgular = [f for f in findings if f['risk_seviyesi'] == 'Kritik']
    yuksek_bulgular = [f for f in findings if f['risk_seviyesi'] == 'Yüksek']

    # Öncelikli alanlar
    oncelikli_alanlar = []
    if any('eşik' in s['senaryo'].lower() for s in scenarios):
        oncelikli_alanlar.append('Tutar onay limitleri ve satınalma kontrollerinin kapsamlı gözden geçirilmesi')
    if any('yoğunlaşma' in s['senaryo'].lower() for s in scenarios):
        oncelikli_alanlar.append('Tedarikçi riski ve bağımlılık yönetim sürecinin değerlendirilmesi')
    if any('sod' in s['senaryo'].lower() for s in scenarios):
        oncelikli_alanlar.append('Görevler ayrılığı matrisinin tam revizyonu')
    if any('mesai dışı' in s['senaryo'].lower() for s in scenarios):
        oncelikli_alanlar.append('Sistem erişim kontrolü ve kullanıcı yetkilendirme politikasının güçlendirilmesi')
    if not oncelikli_alanlar:
        oncelikli_alanlar = ['Veri kalite süreçlerinin iyileştirilmesi',
                             'Anomali tespiti kapasitesinin artırılması']

    return {
        'tarih': date_str,
        'toplam_kayit': total,
        'kritik_sayi': int(critical),
        'yuksek_sayi': int(high),
        'ort_risk': round(float(avg_score), 1),
        'genel_risk': genel_risk,
        'genel_yorum': genel_yorum,
        'kritik_bulgular': kritik_bulgular[:3],
        'yuksek_bulgular': yuksek_bulgular[:3],
        'oncelikli_alanlar': oncelikli_alanlar,
        'sonraki_adimlar': [
            'Kritik bulgular için 30 gün içinde kapatma aksiyonu başlatılması',
            'Yönetim Kurulu Denetim Komitesi\'ne özet sunum hazırlanması',
            'Sürekli denetim (continuous auditing) mekanizmasının devreye alınması',
            'Belirlenen yüksek riskli alanlar için özel denetim planı hazırlanması'
        ]
    }


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

def render_sidebar(df: pd.DataFrame, col_map: dict) -> dict:
    with st.sidebar:
        st.markdown("""
        <div style="padding:16px 0 8px; border-bottom: 1px solid #1e2a42; margin-bottom:16px;">
            <div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#6366f1;font-weight:600;">İÇ DENETİM</div>
            <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;margin-top:4px;">Analitik Platform</div>
        </div>
        """, unsafe_allow_html=True)

        filters = {}

        # Risk Seviyesi Filtresi
        st.markdown("**Risk Seviyesi**")
        risk_filter = st.multiselect(
            label="risk_filter", options=['Kritik', 'Yüksek', 'Orta', 'Düşük'],
            default=['Kritik', 'Yüksek', 'Orta', 'Düşük'],
            label_visibility='collapsed'
        )
        filters['risk'] = risk_filter

        # Tarih Filtresi
        if 'date' in col_map:
            df2 = parse_dates(df.copy(), col_map['date'])
            min_d = df2[col_map['date']].min()
            max_d = df2[col_map['date']].max()
            if pd.notna(min_d) and pd.notna(max_d):
                st.markdown("**Tarih Aralığı**")
                d_range = st.date_input(
                    label="date_filter",
                    value=(min_d.date(), max_d.date()),
                    min_value=min_d.date(), max_value=max_d.date(),
                    label_visibility='collapsed'
                )
                filters['date_range'] = d_range

        # Minimum Risk Skoru
        st.markdown("**Minimum Risk Skoru**")
        min_score = st.slider("min_score", 0, 100, 0, label_visibility='collapsed')
        filters['min_score'] = min_score

        # Tutar Filtresi
        if 'amount' in col_map:
            amt = get_amount_series(df, col_map['amount']).dropna()
            if len(amt) > 0:
                st.markdown("**Minimum Tutar**")
                min_amt = st.number_input("min_amt", value=0.0, label_visibility='collapsed')
                filters['min_amount'] = min_amt

        st.markdown("---")
        st.markdown("""
        <div style="font-size:0.72rem;color:#475569;line-height:1.6;">
        <b style="color:#6366f1;">SÜTUN HARİTASI</b><br>
        Sistem aşağıdaki sütunları otomatik tespit etti:
        </div>
        """, unsafe_allow_html=True)
        for role, col in col_map.items():
            st.markdown(f"<div style='font-size:0.72rem;color:#64748b;padding:1px 0;'><span style='color:#818cf8;'>●</span> <b>{role}</b>: {col}</div>", unsafe_allow_html=True)

    return filters


def apply_filters(df: pd.DataFrame, col_map: dict, filters: dict) -> pd.DataFrame:
    result = df.copy()

    if 'risk' in filters and 'risk_seviyesi' in result.columns:
        result = result[result['risk_seviyesi'].isin(filters['risk'])]

    if 'min_score' in filters and 'risk_skoru' in result.columns:
        result = result[result['risk_skoru'] >= filters['min_score']]

    if 'date_range' in filters and 'date' in col_map:
        result = parse_dates(result, col_map['date'])
        try:
            d_range = filters['date_range']
            if len(d_range) == 2:
                result = result[
                    (result[col_map['date']].dt.date >= d_range[0]) &
                    (result[col_map['date']].dt.date <= d_range[1])
                ]
        except Exception:
            pass

    if 'min_amount' in filters and 'amount' in col_map:
        amt = get_amount_series(result, col_map['amount'])
        result = result[amt >= filters['min_amount']]

    return result


# ═══════════════════════════════════════════════════════════════
# RENK YARDIMCISI
# ═══════════════════════════════════════════════════════════════

def risk_color(level: str) -> str:
    return {'Kritik': 'red', 'Yüksek': 'amber', 'Orta': 'medium', 'Düşük': 'low'}.get(level, 'medium')


def risk_css_class(level: str) -> str:
    return {'Kritik': 'critical', 'Yüksek': 'high', 'Orta': 'medium', 'Düşük': 'low'}.get(level, 'medium')


# ═══════════════════════════════════════════════════════════════
# ANA UYGULAMA
# ═══════════════════════════════════════════════════════════════

def main():
    # ── Header ──
    st.markdown("""
    <div class="audit-header">
        <div class="audit-badge">İç Denetim Veri Analitiği</div>
        <h1>🔍 Denetim Analitik Platformu</h1>
        <p>ERP Uyumlu · Risk Bazlı · Otomatik Bulgu Üretimi · IIA Standartları</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Dosya Yükleme ──
    uploaded_file = st.file_uploader(
        "Excel (.xlsx) veya CSV (.csv) dosyası yükleyin",
        type=['xlsx', 'csv'],
        help="SAP, Oracle veya diğer ERP sistemlerinden alınan raporlar desteklenmektedir."
    )

    if uploaded_file is None:
        st.markdown("""
        <div class="info-box">
            📂 <b>Başlamak için bir veri dosyası yükleyin.</b><br>
            Sistem sütunları otomatik olarak tanıyacak ve tüm denetim analizlerini çalıştıracaktır.
            Desteklenen formatlar: Excel (.xlsx) ve CSV (.csv)
        </div>
        """, unsafe_allow_html=True)

        # Demo veri seçeneği
        if st.button("🎲 Demo Veri ile Başla", type="primary"):
            st.session_state['use_demo'] = True
        
        if not st.session_state.get('use_demo'):
            _render_feature_cards()
            return

    # ── Veri Yükleme ──
    try:
        if uploaded_file is not None:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file, encoding='utf-8-sig')
            else:
                df_raw = pd.read_excel(uploaded_file)
            st.session_state['use_demo'] = False
        else:
            # Demo veri
            df_raw = _generate_demo_data()
            st.markdown("""
            <div class="warning-box">⚠️ Demo modunda çalışıyorsunuz. Gerçek analiz için kendi verilerinizi yükleyin.</div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Dosya yükleme hatası: {e}")
        return

    if df_raw.empty:
        st.error("Yüklenen dosya boş veya okunamadı.")
        return

    # ── Sütun Tanıma ──
    col_map = detect_columns(df_raw)

    # ── Analizleri Çalıştır ──
    with st.spinner("🔄 Denetim analizleri çalıştırılıyor..."):
        df_scored = compute_risk_scores(df_raw, col_map)
        quality_results = run_data_quality_tests(df_scored, col_map)
        scenarios = run_audit_scenarios(df_scored, col_map)
        findings = generate_audit_findings(df_scored, col_map, quality_results, scenarios)
        action_plans = generate_action_plans(findings)
        exec_summary = generate_executive_summary(df_scored, col_map, findings, scenarios, quality_results)

    # ── Sidebar Filtreleri ──
    filters = render_sidebar(df_scored, col_map)
    df_filtered = apply_filters(df_scored, col_map, filters)

    # ── KPI Kartları ──
    total = len(df_filtered)
    critical_count = (df_filtered['risk_seviyesi'] == 'Kritik').sum()
    high_count = (df_filtered['risk_seviyesi'] == 'Yüksek').sum()
    avg_risk = df_filtered['risk_skoru'].mean() if total > 0 else 0
    high_pct = ((critical_count + high_count) / total * 100) if total > 0 else 0

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card blue">
            <div class="kpi-label">Toplam Kayıt</div>
            <div class="kpi-value">{total:,}</div>
            <div class="kpi-sub">Filtrelenmiş veri seti</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Kritik Risk</div>
            <div class="kpi-value">{critical_count:,}</div>
            <div class="kpi-sub">Acil aksiyon gerektirir</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Ort. Risk Skoru</div>
            <div class="kpi-value">{avg_risk:.0f}</div>
            <div class="kpi-sub">0–100 skala</div>
        </div>
        <div class="kpi-card {'red' if high_pct > 20 else 'amber' if high_pct > 10 else 'green'}">
            <div class="kpi-label">Yüksek Risk %</div>
            <div class="kpi-value">{high_pct:.1f}%</div>
            <div class="kpi-sub">Kritik + Yüksek oranı</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sekmeler ──
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Veri Genel Görünüm",
        "📊 Risk Analizi",
        "🔎 Denetim Bulguları",
        "✅ Aksiyon Planları",
        "📌 Yönetici Özeti"
    ])

    # ══════════════════════════════════════════
    # SEKME 1: VERİ GENEL GÖRÜNÜM
    # ══════════════════════════════════════════
    with tab1:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📋</div>
            <h2>Veri Genel Görünüm</h2>
        </div>
        """, unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Toplam Satır", f"{len(df_raw):,}")
        with col_b:
            st.metric("Toplam Sütun", f"{len(df_raw.columns)}")
        with col_c:
            st.metric("Eksik Hücre %", f"{df_raw.isnull().mean().mean()*100:.1f}%")

        st.markdown("**Ham Veri (İlk 100 Kayıt)**")
        st.dataframe(
            df_filtered.head(100),
            use_container_width=True,
            height=350
        )

        # Veri Kalitesi Kontrol Özeti
        st.markdown("""
        <div class="section-header" style="margin-top:24px;">
            <div class="section-icon">🧪</div>
            <h2>Veri Kalitesi Kontrol Sonuçları</h2>
        </div>
        """, unsafe_allow_html=True)

        for qr in quality_results:
            css = risk_css_class(qr['risk'])
            st.markdown(f"""
            <div class="finding-card {css}">
                <div class="finding-title">
                    <span class="risk-badge {css}">{qr['risk']}</span>
                    {qr['kontrol']}
                </div>
                <div class="finding-body">
                    {qr['bulgu']}<br>
                    <span style="color:#64748b;font-size:0.8rem;">Etkilenen kayıt: <b style="color:#94a3b8;">{qr['etkilenen_kayit']:,}</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Sütun istatistikleri
        st.markdown("**Sayısal Sütun İstatistikleri**")
        num_stats = df_raw.describe().round(2)
        st.dataframe(num_stats, use_container_width=True)

    # ══════════════════════════════════════════
    # SEKME 2: RİSK ANALİZİ
    # ══════════════════════════════════════════
    with tab2:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📊</div>
            <h2>Risk Analizi Dashboard</h2>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(plot_risk_distribution(df_filtered), use_container_width=True)
        with col2:
            st.plotly_chart(plot_score_histogram(df_filtered), use_container_width=True)

        if 'date' in col_map:
            try:
                st.plotly_chart(plot_time_trend(df_filtered, col_map), use_container_width=True)
            except Exception:
                pass

        col3, col4 = st.columns(2)
        with col3:
            if 'vendor' in col_map and 'amount' in col_map:
                try:
                    st.plotly_chart(plot_vendor_concentration(df_filtered, col_map), use_container_width=True)
                except Exception:
                    pass
        with col4:
            try:
                hm = plot_risk_heatmap(df_filtered, col_map)
                if hm:
                    st.plotly_chart(hm, use_container_width=True)
            except Exception:
                pass

        # Senaryo Sonuçları
        st.markdown("""
        <div class="section-header" style="margin-top:8px;">
            <div class="section-icon">🎯</div>
            <h2>Denetim Senaryo Motoru Sonuçları</h2>
        </div>
        """, unsafe_allow_html=True)

        for sc in scenarios:
            css = risk_css_class(sc['risk_seviyesi'])
            with st.expander(f"{'🔴' if sc['risk_seviyesi']=='Kritik' else '🟠' if sc['risk_seviyesi']=='Yüksek' else '🔵'} {sc['senaryo']} — {sc['etkilenen']:,} Etkilenen Kayıt"):
                st.markdown(f"""
                <div class="finding-card {css}">
                    <div class="finding-title">
                        <span class="risk-badge {css}">{sc['risk_seviyesi']}</span>
                        {sc['senaryo']}
                    </div>
                    <div class="finding-body">
                        <b>Açıklama:</b> {sc['aciklama']}<br><br>
                        <b>Denetim Riski:</b> {sc['risk']}<br>
                        <b>Etkilenen Kayıt Sayısı:</b> {sc['etkilenen']:,}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if isinstance(sc.get('ornek'), pd.DataFrame) and not sc['ornek'].empty:
                    st.markdown("**📎 Örnek Kanıt Tablosu:**")
                    st.dataframe(sc['ornek'], use_container_width=True)

        # En riskli kayıtlar
        st.markdown("""
        <div class="section-header" style="margin-top:8px;">
            <div class="section-icon">⚠️</div>
            <h2>En Riskli İşlemler (Top 20)</h2>
        </div>
        """, unsafe_allow_html=True)
        top_risky = df_filtered.nlargest(20, 'risk_skoru')
        st.dataframe(top_risky, use_container_width=True, height=400)

    # ══════════════════════════════════════════
    # SEKME 3: DENETİM BULGULARI
    # ══════════════════════════════════════════
    with tab3:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🔎</div>
            <h2>Denetim Bulguları</h2>
        </div>
        """, unsafe_allow_html=True)

        if not findings:
            st.info("Seçili filtreler dahilinde önemli bulgu tespit edilmedi.")
        else:
            # Özet tablo
            findings_df = pd.DataFrame([{
                'Bulgu': f['baslik'],
                'Risk Seviyesi': f['risk_seviyesi'],
                'Etkilenen Kayıt': f['etkilenen'],
                'Kaynak': f['kaynak']
            } for f in findings])
            st.dataframe(findings_df, use_container_width=True)

            st.markdown("---")

            for i, finding in enumerate(findings, 1):
                css = risk_css_class(finding['risk_seviyesi'])
                st.markdown(f"""
                <div class="finding-card {css}">
                    <div class="finding-title">
                        <span class="risk-badge {css}">{finding['risk_seviyesi']}</span>
                        BULGU #{i}: {finding['baslik']}
                    </div>
                    <div class="finding-body">
                        <p><b>📌 Bulgu:</b> {finding['aciklama']}</p>
                        <p><b>🔍 Kök Neden Analizi:</b> {finding['kok_neden']}</p>
                        <p><b>💼 İş Etkisi:</b> {finding['is_etkisi']}</p>
                        <p style="color:#475569;font-size:0.78rem;">Etkilenen Kayıt: <b style="color:#94a3b8">{finding['etkilenen']:,}</b> &nbsp;|&nbsp; Kaynak: {finding['kaynak']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SEKME 4: AKSİYON PLANLARI
    # ══════════════════════════════════════════
    with tab4:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">✅</div>
            <h2>Düzeltici Aksiyon Planları</h2>
        </div>
        """, unsafe_allow_html=True)

        if not action_plans:
            st.info("Aksiyon planı gerektiren bulgu bulunamadı.")
        else:
            # Excel export için tablo
            plans_df = pd.DataFrame(action_plans)
            st.markdown("**Aksiyon Planı Özet Tablosu**")
            st.dataframe(plans_df, use_container_width=True)

            st.markdown("---")

            for plan in action_plans:
                css = risk_css_class(plan['risk_seviyesi'])
                priority_color = {
                    'P1 – Acil': '#ef4444',
                    'P2 – Yüksek': '#f59e0b',
                    'P3 – Orta': '#3b82f6',
                    'P4 – Düşük': '#10b981'
                }.get(plan['oncelik'], '#6366f1')

                st.markdown(f"""
                <div class="action-card">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
                        <h4 style="margin:0;">{plan['bulgu']}</h4>
                        <span style="background:{priority_color}22;border:1px solid {priority_color}55;color:{priority_color};padding:3px 10px;border-radius:20px;font-size:0.72rem;font-weight:700;">
                            {plan['oncelik']}
                        </span>
                    </div>
                    <p style="color:#cbd5e1;font-size:0.87rem;margin:0 0 10px 0;">{plan['aksiyon']}</p>
                    <div class="action-meta">
                        <span>🏢 <b>Sorumlu Birim:</b> {plan['birim']}</span>
                        <span>⚙️ <b>Uygulama Zorluğu:</b> {plan['zorluk']}</span>
                        <span><span class="risk-badge {css}">{plan['risk_seviyesi']}</span></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # SEKME 5: YÖNETİCİ ÖZETİ
    # ══════════════════════════════════════════
    with tab5:
        es = exec_summary
        risk_colors = {
            'KRİTİK': '#ef4444', 'YÜKSEK': '#f59e0b',
            'ORTA': '#3b82f6', 'DÜŞÜK': '#10b981'
        }
        rc = risk_colors.get(es['genel_risk'], '#6366f1')

        st.markdown(f"""
        <div class="exec-summary">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:16px;margin-bottom:24px;">
                <div>
                    <div class="audit-badge">İÇ DENETİM YÖNETİCİ ÖZETİ</div>
                    <h2>İç Denetim Analitik Değerlendirme Raporu</h2>
                    <div class="subtitle">Tarih: {es['tarih']} &nbsp;|&nbsp; Kayıt Sayısı: {es['toplam_kayit']:,} &nbsp;|&nbsp; Ortalama Risk Skoru: {es['ort_risk']}/100</div>
                </div>
                <div style="text-align:center;background:rgba(99,102,241,0.1);border:1px solid #4338ca;border-radius:12px;padding:16px 24px;">
                    <div style="font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;color:#818cf8;margin-bottom:4px;">GENEL RİSK</div>
                    <div style="font-size:2rem;font-weight:800;color:{rc};font-family:'IBM Plex Mono';">{es['genel_risk']}</div>
                </div>
            </div>

            <div class="exec-section">
                <h3>1. Genel Risk Değerlendirmesi</h3>
                <p>{es['genel_yorum']}<br><br>
                İncelenen {es['toplam_kayit']:,} kayıt içerisinde <b style="color:#ef4444;">{es['kritik_sayi']:,} kritik</b> ve
                <b style="color:#f59e0b;">{es['yuksek_sayi']:,} yüksek</b> riskli kayıt tespit edilmiştir.
                Ortalama risk skoru {es['ort_risk']}/100 olarak hesaplanmıştır.</p>
            </div>

            <div class="exec-section">
                <h3>2. Kritik Kontrol Zafiyetleri</h3>
                <p>{'<br>'.join([f"• <b>{f['baslik']}</b>: {f['aciklama']}" for f in es['kritik_bulgular']]) if es['kritik_bulgular'] else 'Kritik seviyede kontrol zafiyeti tespit edilmemiştir.'}</p>
            </div>

            <div class="exec-section">
                <h3>3. Öncelikli Denetim Bulguları</h3>
                <p>{'<br>'.join([f"• <b>{f['baslik']}</b>: {f['is_etkisi']}" for f in es['yuksek_bulgular']]) if es['yuksek_bulgular'] else '• Yüksek riskli bulgu sayısı yönetilebilir düzeydedir.'}</p>
            </div>

            <div class="exec-section">
                <h3>4. Öncelikli Aksiyon Alanları</h3>
                <p>{'<br>'.join([f"• {a}" for a in es['oncelikli_alanlar']])}</p>
            </div>

            <div class="exec-section">
                <h3>5. Sonraki Dönem Denetim Odak Alanları</h3>
                <p>{'<br>'.join([f"• {a}" for a in es['sonraki_adimlar']])}</p>
            </div>

            <div style="margin-top:20px;padding-top:16px;border-top:1px solid rgba(99,102,241,0.2);">
                <p style="font-size:0.78rem;color:#475569;margin:0;">
                    Bu rapor, IIA Uluslararası İç Denetim Standartları (IPPF) çerçevesinde 
                    otomatik veri analitiği yöntemleriyle üretilmiştir. 
                    Son karar yetkisi, sorumlu iç denetçiye aittir.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # İndirilebilir özet
        summary_text = f"""
İÇ DENETİM ANALİTİK DEĞERLENDİRME RAPORU
==========================================
Tarih: {es['tarih']}
Toplam Kayıt: {es['toplam_kayit']:,}
Ortalama Risk Skoru: {es['ort_risk']}/100
Genel Risk Seviyesi: {es['genel_risk']}

1. GENEL RİSK DEĞERLENDİRMESİ
{es['genel_yorum']}
Kritik Kayıt: {es['kritik_sayi']:,} | Yüksek Riskli: {es['yuksek_sayi']:,}

2. KRİTİK KONTROL ZAFİYETLERİ
{''.join([chr(10) + '• ' + f['baslik'] + ': ' + f['aciklama'] for f in es['kritik_bulgular']]) if es['kritik_bulgular'] else 'Kritik seviyede bulgu tespit edilmemiştir.'}

3. ÖNCELİKLİ BULGULAR
{''.join([chr(10) + '• ' + f['baslik'] for f in es['yuksek_bulgular']]) if es['yuksek_bulgular'] else '• Yüksek riskli bulgu yönetilebilir düzeyde.'}

4. AKSIYON ALANLARI
{''.join([chr(10) + '• ' + a for a in es['oncelikli_alanlar']])}

5. SONRAKI ADIMLAR
{''.join([chr(10) + '• ' + a for a in es['sonraki_adimlar']])}

---
IIA IPPF Standartlarına uygun otomatik analitik raporu.
        """
        st.download_button(
            label="📥 Yönetici Özetini İndir (.txt)",
            data=summary_text,
            file_name=f"ic_denetim_yonetici_ozeti_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )


def _render_feature_cards():
    """Başlangıç sayfasında özellik kartları göster."""
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:8px;">
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">🧪</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Veri Kalite Kontrolleri</div>
            <div style="color:#64748b;font-size:0.82rem;">Eksik veri, mükerrer kayıt, negatif tutar, aykırı değer, yuvarlama analizi</div>
        </div>
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">🎯</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Senaryo Motoru</div>
            <div style="color:#64748b;font-size:0.82rem;">Eşik ihlali, yoğunlaşma, mesai dışı işlem, SoD ihlali tespiti</div>
        </div>
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">📊</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Risk Skorlama</div>
            <div style="color:#64748b;font-size:0.82rem;">Her kayıt için 0–100 arası birleşik risk skoru (Düşük → Kritik)</div>
        </div>
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">🔎</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Denetim Bulguları</div>
            <div style="color:#64748b;font-size:0.82rem;">Otomatik bulgu üretimi, kök neden analizi, iş etkisi değerlendirmesi</div>
        </div>
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">✅</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Aksiyon Planları</div>
            <div style="color:#64748b;font-size:0.82rem;">Sorumlu birim, öncelik ve uygulama zorluğu içeren düzeltici aksiyonlar</div>
        </div>
        <div style="background:#1a2235;border:1px solid #1e2a42;border-radius:10px;padding:20px;">
            <div style="font-size:1.5rem;margin-bottom:8px;">📌</div>
            <div style="font-weight:600;color:#f1f5f9;margin-bottom:6px;">Yönetici Özeti</div>
            <div style="color:#64748b;font-size:0.82rem;">IIA standartlarına uygun kurumsal yönetici özeti, indirilebilir format</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def _generate_demo_data() -> pd.DataFrame:
    """Demo amaçlı gerçekçi ERP benzeri veri üret."""
    np.random.seed(42)
    n = 500

    vendors = ['Tedarikçi A AŞ', 'Lojistik B Ltd', 'Teknoloji C GmbH',
               'Danışmanlık D Inc', 'Malzeme E Koop', 'Servis F SRL',
               'İnşaat G Ort', 'Temizlik H Firm']
    users = ['ahmet.kaya', 'fatma.demir', 'mehmet.yilmaz',
             'zeynep.arslan', 'ali.celik', 'ayse.sahin']
    categories = ['Satınalma', 'Hizmet Alımı', 'Kira', 'BT Harcaması',
                  'Seyahat', 'Danışmanlık', 'Bakım-Onarım']
    statuses = ['Onaylandı', 'Beklemede', 'Onaylandı', 'Reddedildi',
                'Onaylandı', 'Onaylandı']

    # Normal işlemler
    amounts = np.abs(np.random.lognormal(mean=9, sigma=1.5, size=n))

    # Anomali enjekte et
    amounts[10:15] = 49999  # Eşik altı
    amounts[50:55] = np.random.choice([-1, -5000, -12000], size=5)  # Negatif
    amounts[100] = amounts[100] * 20  # Aykırı değer
    amounts[200:210] = 5000  # Tekrarlayan

    dates = pd.date_range('2024-01-01', periods=n, freq='h') + \
            pd.to_timedelta(np.random.randint(0, 8760, n), unit='h')

    df = pd.DataFrame({
        'Belge_No': [f'DOC{str(i).zfill(5)}' for i in range(n)],
        'Tarih': dates[:n],
        'Tedarikci': np.random.choice(vendors, n, p=[0.4,0.15,0.1,0.1,0.1,0.05,0.05,0.05]),
        'Kullanici': np.random.choice(users, n),
        'Kategori': np.random.choice(categories, n),
        'Tutar': amounts[:n].round(2),
        'Onay_Durumu': np.random.choice(statuses, n)
    })

    # Mükerrer ekle
    df = pd.concat([df, df.iloc[20:23]], ignore_index=True)

    return df


if __name__ == '__main__':
    main()
