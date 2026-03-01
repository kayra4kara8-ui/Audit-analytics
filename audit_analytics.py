"""
╔══════════════════════════════════════════════════════════════════════════════╗
║   İÇ DENETİM VERİ ANALİTİĞİ PLATFORMU  ·  Professional Edition  v3.0      ║
║   IIA IPPF · COSO · ISO 31000 Uyumlu                                        ║
║   SAP / Oracle / Netsis / Logo / Mikro / Generic ERP Desteği               ║
╚══════════════════════════════════════════════════════════════════════════════╝

MODÜLLER:
  M0  – Sayfa Konfigürasyonu & Tema
  M1  – Evrensel Kolon Tanıma (3-Katmanlı)
  M2  – Veri Kalitesi & Kontrol Testleri (7 Kontrol)
  M3  – Denetim Senaryo Motoru (8 Senaryo)
  M4  – Risk Skorlama Motoru (Çok Değişkenli)
  M5  – Benford Yasası Analizi
  M6  – Pareto (80/20) Analizi
  M7  – Zaman Serisi & Trend Analizi
  M8  – Ağ Analizi (Vendor-User İlişkileri)
  M9  – Denetim Bulguları Üretici
  M10 – Aksiyon Planı Üretici
  M11 – Görselleştirme Motoru (Plotly)
  M12 – Yönetici Özeti (IIA Uyumlu)
  M13 – Export & Raporlama
  M14 – Sidebar & Filtreler
  M15 – Ana Uygulama Döngüsü
"""

# ──────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────────────────────────────────────
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from collections import Counter
import warnings
import io
import math
import re
try:
    from docx import Document as DocxDocument
    from docx.shared import Pt, RGBColor, Inches, Cm
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# M0 – SAYFA KONFIGÜRASYONU & TEMA
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="İç Denetim Analitik Platformu",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Renk Paleti & Tasarım Sistemi ───────────────────────────────────────────
# Tema: "Kurumsal Obsidyen" – Koyu lacivert zemin, platin aksan, keskin kırmızı uyarılar
# Font: DM Serif Display (başlıklar) + DM Sans (gövde) + JetBrains Mono (sayılar/kod)
# ─────────────────────────────────────────────────────────────────────────────

CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── CSS Değişkenleri ── */
:root {
  --c-bg:          #060b14;
  --c-surface:     #0c1524;
  --c-surface2:    #111e30;
  --c-surface3:    #162438;
  --c-border:      #1c2e44;
  --c-border2:     #243850;
  --c-text:        #dce8f5;
  --c-text2:       #8aa4be;
  --c-text3:       #4a6480;
  --c-accent:      #4f9cf9;
  --c-accent2:     #1a6ed8;
  --c-gold:        #d4a847;
  --c-gold2:       #f0c96a;
  --c-critical:    #e03e3e;
  --c-critical2:   #ff6b6b;
  --c-high:        #d97706;
  --c-high2:       #fbbf24;
  --c-medium:      #2563eb;
  --c-medium2:     #60a5fa;
  --c-low:         #059669;
  --c-low2:        #34d399;
  --c-purple:      #7c3aed;
  --c-purple2:     #a78bfa;
  --c-cyan:        #0891b2;
  --c-cyan2:       #22d3ee;
  --r-sm:  6px;
  --r-md:  10px;
  --r-lg:  14px;
  --r-xl:  20px;
  --shadow: 0 4px 24px rgba(0,0,0,0.4);
  --shadow-lg: 0 8px 48px rgba(0,0,0,0.6);
}

/* ── Genel Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
  font-family: 'DM Sans', sans-serif !important;
  background: var(--c-bg) !important;
  color: var(--c-text) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--c-bg); }
::-webkit-scrollbar-thumb { background: var(--c-border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--c-text3); }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
  background: var(--c-surface) !important;
  border-right: 1px solid var(--c-border) !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--c-surface2);
  border-radius: var(--r-md);
  padding: 4px;
  gap: 3px;
  border: 1px solid var(--c-border);
  margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
  border-radius: var(--r-sm);
  font-weight: 500;
  font-size: 0.83rem;
  color: var(--c-text2);
  letter-spacing: 0.2px;
  padding: 8px 16px;
  transition: all 0.15s;
}
.stTabs [aria-selected="true"] {
  background: var(--c-surface3) !important;
  color: var(--c-text) !important;
  box-shadow: 0 1px 6px rgba(0,0,0,0.3);
}

/* ── Expander ── */
details[data-testid="stExpander"] {
  background: var(--c-surface2);
  border: 1px solid var(--c-border) !important;
  border-radius: var(--r-md) !important;
  margin-bottom: 8px;
  overflow: hidden;
}
details[data-testid="stExpander"] summary {
  font-weight: 500;
  font-size: 0.88rem;
  padding: 12px 16px;
}

/* ── Metric ── */
[data-testid="metric-container"] {
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  padding: 14px 18px;
}
[data-testid="stMetricLabel"] { font-size: 0.72rem !important; font-weight: 600 !important;
  letter-spacing: 0.8px !important; text-transform: uppercase !important;
  color: var(--c-text2) !important; }
[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important;
  font-size: 1.6rem !important; font-weight: 600 !important; color: var(--c-text) !important; }

/* ── Buttons ── */
.stButton > button {
  background: var(--c-accent2) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  font-weight: 600 !important;
  font-size: 0.85rem !important;
  letter-spacing: 0.3px !important;
  padding: 10px 20px !important;
  transition: all 0.2s !important;
}
.stButton > button:hover { background: var(--c-accent) !important; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(79,156,249,0.3) !important; }

/* ── Download button ── */
.stDownloadButton > button {
  background: var(--c-surface3) !important;
  color: var(--c-accent) !important;
  border: 1px solid var(--c-border2) !important;
  border-radius: var(--r-sm) !important;
  font-weight: 600 !important;
  font-size: 0.82rem !important;
}

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
  background: var(--c-surface2) !important;
  border: 2px dashed var(--c-border2) !important;
  border-radius: var(--r-lg) !important;
}

/* ── DataFrame ── */
[data-testid="stDataFrame"] { border-radius: var(--r-md); overflow: hidden; }
iframe { background: transparent !important; }

/* ── Alerts ── */
[data-testid="stAlert"] { border-radius: var(--r-md) !important; font-size: 0.87rem; }

/* ── Plotly containers ── */
[data-testid="stPlotlyChart"] { border-radius: var(--r-md); }

/* ── Divider ── */
hr { border-color: var(--c-border) !important; margin: 24px 0 !important; }

/* ═══════════════════════════════════════════════════════
   ÖZEL BİLEŞENLER
═══════════════════════════════════════════════════════ */

/* ── Masthead / Header ── */
.masthead {
  position: relative;
  background: linear-gradient(135deg, #08111f 0%, #0d1f3a 40%, #091528 100%);
  border: 1px solid var(--c-border2);
  border-radius: var(--r-xl);
  padding: 32px 40px;
  margin-bottom: 28px;
  overflow: hidden;
}
.masthead::before {
  content: '';
  position: absolute;
  top: -80px; right: -80px;
  width: 300px; height: 300px;
  background: radial-gradient(circle, rgba(79,156,249,0.06) 0%, transparent 70%);
  pointer-events: none;
}
.masthead::after {
  content: '';
  position: absolute;
  bottom: -60px; left: 30%;
  width: 200px; height: 200px;
  background: radial-gradient(circle, rgba(212,168,71,0.04) 0%, transparent 70%);
  pointer-events: none;
}
.masthead-eyebrow {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 10px;
}
.masthead-pill {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(79,156,249,0.1);
  border: 1px solid rgba(79,156,249,0.25);
  color: var(--c-accent);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
}
.masthead-pill::before { content: '●'; font-size: 0.5rem; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

.masthead-standard {
  display: inline-flex; align-items: center; gap: 6px;
  background: rgba(212,168,71,0.08);
  border: 1px solid rgba(212,168,71,0.2);
  color: var(--c-gold);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.68rem;
  font-weight: 600;
  letter-spacing: 1px;
}
.masthead h1 {
  font-family: 'DM Serif Display', serif;
  font-size: 2rem;
  font-weight: 400;
  color: var(--c-text);
  margin: 0 0 6px 0;
  letter-spacing: -0.5px;
  line-height: 1.15;
}
.masthead h1 em {
  font-style: italic;
  color: var(--c-accent);
}
.masthead-sub {
  font-size: 0.88rem;
  color: var(--c-text2);
  font-weight: 400;
  display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
}
.masthead-sub span { display: flex; align-items: center; gap: 5px; }
.masthead-sep { color: var(--c-border2); }

/* ── KPI Grid ── */
.kpi-row {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}
.kpi-card {
  position: relative;
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  padding: 18px 20px 16px;
  overflow: hidden;
  transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: var(--c-border2); transform: translateY(-2px); }
.kpi-card::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  border-radius: var(--r-lg) var(--r-lg) 0 0;
}
.kpi-card.accent::after   { background: linear-gradient(90deg,var(--c-accent),var(--c-cyan2)); }
.kpi-card.critical::after { background: linear-gradient(90deg,var(--c-critical),var(--c-critical2)); }
.kpi-card.high::after     { background: linear-gradient(90deg,var(--c-high),var(--c-high2)); }
.kpi-card.ok::after       { background: linear-gradient(90deg,var(--c-low),var(--c-low2)); }
.kpi-card.gold::after     { background: linear-gradient(90deg,var(--c-gold),var(--c-gold2)); }
.kpi-eyebrow {
  font-size: 0.67rem; font-weight: 700;
  letter-spacing: 1.2px; text-transform: uppercase;
  color: var(--c-text3); margin-bottom: 8px;
  display: flex; align-items: center; justify-content: space-between;
}
.kpi-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.75rem; font-weight: 600;
  line-height: 1; letter-spacing: -0.5px;
}
.kpi-card.accent   .kpi-value { color: var(--c-accent); }
.kpi-card.critical .kpi-value { color: var(--c-critical2); }
.kpi-card.high     .kpi-value { color: var(--c-high2); }
.kpi-card.ok       .kpi-value { color: var(--c-low2); }
.kpi-card.gold     .kpi-value { color: var(--c-gold2); }
.kpi-sub {
  font-size: 0.74rem; color: var(--c-text3);
  margin-top: 6px; font-weight: 400;
}
.kpi-trend {
  font-size: 0.72rem; font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

/* ── Section Başlığı ── */
.sec-header {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px 0;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--c-border);
}
.sec-icon {
  width: 34px; height: 34px;
  background: var(--c-surface3);
  border: 1px solid var(--c-border2);
  border-radius: var(--r-sm);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.95rem;
  flex-shrink: 0;
}
.sec-title { font-family: 'DM Serif Display', serif; font-size: 1.15rem;
  font-weight: 400; color: var(--c-text); letter-spacing: -0.2px; }
.sec-subtitle { font-size: 0.78rem; color: var(--c-text3); margin-top: 1px; }
.sec-badge {
  margin-left: auto;
  background: var(--c-surface3);
  border: 1px solid var(--c-border);
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.68rem;
  font-weight: 600;
  color: var(--c-text2);
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.5px;
}

/* ── Bulgu Kartı ── */
.finding-card {
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-left: 3px solid;
  border-radius: 0 var(--r-md) var(--r-md) 0;
  padding: 18px 22px;
  margin-bottom: 10px;
  transition: border-color 0.15s;
}
.finding-card:hover { border-color: var(--c-border2); }
.finding-card.critical { border-left-color: var(--c-critical); }
.finding-card.high     { border-left-color: var(--c-high); }
.finding-card.medium   { border-left-color: var(--c-medium); }
.finding-card.low      { border-left-color: var(--c-low); }

.finding-header {
  display: flex; align-items: flex-start;
  justify-content: space-between; gap: 12px;
  margin-bottom: 10px;
}
.finding-source {
  font-size: 0.67rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; color: var(--c-text3); margin-bottom: 4px;
}
.finding-title {
  font-size: 0.93rem; font-weight: 600; color: var(--c-text);
  line-height: 1.4;
}
.finding-body {
  font-size: 0.83rem; color: var(--c-text2);
  line-height: 1.65;
}
.finding-body b { color: var(--c-text); font-weight: 600; }
.finding-meta {
  display: flex; gap: 16px; flex-wrap: wrap;
  margin-top: 10px; padding-top: 10px;
  border-top: 1px solid var(--c-border);
  font-size: 0.75rem; color: var(--c-text3);
}
.finding-meta strong { color: var(--c-text2); }

/* ── Risk Badge ── */
.rbadge {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 0.68rem; font-weight: 700;
  letter-spacing: 0.5px; text-transform: uppercase;
  white-space: nowrap; flex-shrink: 0;
}
.rbadge.critical { background:rgba(224,62,62,.12); color:var(--c-critical2); border:1px solid rgba(224,62,62,.25); }
.rbadge.high     { background:rgba(217,119,6,.12);  color:var(--c-high2);    border:1px solid rgba(217,119,6,.25); }
.rbadge.medium   { background:rgba(37,99,235,.12);  color:var(--c-medium2);  border:1px solid rgba(37,99,235,.25); }
.rbadge.low      { background:rgba(5,150,105,.12);  color:var(--c-low2);     border:1px solid rgba(5,150,105,.25); }

/* ── Aksiyon Kartı ── */
.action-card {
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  padding: 18px 22px;
  margin-bottom: 10px;
  transition: border-color 0.15s;
}
.action-card:hover { border-color: var(--c-border2); }
.action-header {
  display: flex; align-items: flex-start;
  justify-content: space-between; gap: 12px;
  margin-bottom: 10px;
}
.action-title { font-size: 0.9rem; font-weight: 600; color: var(--c-text); line-height: 1.4; }
.action-body  { font-size: 0.83rem; color: var(--c-text2); line-height: 1.6; }
.action-chips {
  display: flex; gap: 8px; flex-wrap: wrap;
  margin-top: 12px; padding-top: 10px;
  border-top: 1px solid var(--c-border);
}
.chip {
  display: inline-flex; align-items: center; gap: 4px;
  background: var(--c-surface3);
  border: 1px solid var(--c-border2);
  padding: 3px 10px; border-radius: 20px;
  font-size: 0.72rem; color: var(--c-text2);
  font-weight: 500;
}

/* ── Priority Badge ── */
.pbadge {
  display: inline-block; padding: 3px 10px; border-radius: 20px;
  font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px;
  text-transform: uppercase;
}
.pbadge.p1 { background:rgba(224,62,62,.15); color:#ff8a8a; border:1px solid rgba(224,62,62,.3); }
.pbadge.p2 { background:rgba(217,119,6,.15); color:#fbbf24; border:1px solid rgba(217,119,6,.3); }
.pbadge.p3 { background:rgba(37,99,235,.15); color:#93c5fd; border:1px solid rgba(37,99,235,.3); }
.pbadge.p4 { background:rgba(5,150,105,.15); color:#6ee7b7; border:1px solid rgba(5,150,105,.3); }

/* ── Yönetici Özeti ── */
.exec-wrap {
  background: linear-gradient(160deg,#080f1c 0%,#0e1a2d 50%,#08111e 100%);
  border: 1px solid var(--c-border2);
  border-radius: var(--r-xl);
  overflow: hidden;
}
.exec-top {
  padding: 32px 36px;
  border-bottom: 1px solid var(--c-border);
  display: flex; align-items: center; justify-content: space-between;
  gap: 24px; flex-wrap: wrap;
}
.exec-title-block {}
.exec-overline {
  font-size: 0.67rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--c-gold); margin-bottom: 6px;
}
.exec-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.6rem; font-weight: 400;
  color: var(--c-text); letter-spacing: -0.3px;
  margin: 0 0 4px 0;
}
.exec-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem; color: var(--c-text3);
  display: flex; gap: 16px; flex-wrap: wrap;
}
.exec-risk-box {
  text-align: center;
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--c-border2);
  border-radius: var(--r-lg);
  padding: 16px 28px;
  min-width: 140px;
}
.exec-risk-label {
  font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--c-text3); margin-bottom: 6px;
}
.exec-risk-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.6rem; font-weight: 700; letter-spacing: -0.5px;
}
.exec-body { padding: 28px 36px; }
.exec-section { margin-bottom: 28px; }
.exec-section:last-child { margin-bottom: 0; }
.exec-section-title {
  font-size: 0.7rem; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--c-accent);
  margin-bottom: 10px;
  display: flex; align-items: center; gap: 8px;
}
.exec-section-title::after {
  content: ''; flex: 1; height: 1px;
  background: linear-gradient(90deg,var(--c-border2),transparent);
}
.exec-section-body {
  font-size: 0.87rem; color: var(--c-text2);
  line-height: 1.75; margin: 0;
}
.exec-section-body b { color: var(--c-text); font-weight: 600; }
.exec-bullet {
  display: flex; align-items: flex-start; gap: 10px;
  font-size: 0.85rem; color: var(--c-text2);
  margin-bottom: 8px; line-height: 1.6;
}
.exec-bullet::before {
  content: '▸';
  color: var(--c-accent);
  flex-shrink: 0; margin-top: 1px;
  font-size: 0.75rem;
}
.exec-finding-item {
  background: rgba(255,255,255,0.02);
  border: 1px solid var(--c-border);
  border-left: 3px solid;
  border-radius: 0 var(--r-sm) var(--r-sm) 0;
  padding: 12px 16px; margin-bottom: 8px;
  font-size: 0.83rem;
}
.exec-finding-item.critical { border-left-color: var(--c-critical); }
.exec-finding-item.high     { border-left-color: var(--c-high); }
.exec-finding-item b { color: var(--c-text); font-weight: 600; display: block; margin-bottom: 2px; }
.exec-finding-item span { color: var(--c-text2); }
.exec-footer {
  padding: 16px 36px;
  border-top: 1px solid var(--c-border);
  font-size: 0.74rem; color: var(--c-text3);
  display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;
}
.exec-footer a { color: var(--c-text3); text-decoration: none; }

/* ── Kolon Haritası (Sidebar) ── */
.cm-table { width: 100%; font-size: 0.74rem; border-collapse: collapse; margin-top: 8px; }
.cm-table tr { border-bottom: 1px solid var(--c-border); }
.cm-table tr:last-child { border-bottom: none; }
.cm-table td { padding: 5px 4px; }
.cm-role { color: var(--c-text2); font-weight: 600; }
.cm-col  { color: var(--c-accent); font-family: 'JetBrains Mono',monospace; font-size:0.7rem; }
.cm-conf { color: var(--c-text3); font-size: 0.65rem; }

/* ── Info / Warning / Error Kutular ── */
.info-box {
  background: rgba(79,156,249,.07);
  border: 1px solid rgba(79,156,249,.2);
  border-radius: var(--r-md);
  padding: 14px 18px; color: #7dbfff;
  font-size: 0.85rem; margin-bottom: 16px; line-height: 1.6;
}
.warn-box {
  background: rgba(217,119,6,.07);
  border: 1px solid rgba(217,119,6,.2);
  border-radius: var(--r-md);
  padding: 14px 18px; color: #fbbf24;
  font-size: 0.85rem; margin-bottom: 16px; line-height: 1.6;
}

/* ── Feature Grid (Landing) ── */
.feat-grid {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 12px; margin-top: 20px;
}
.feat-card {
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-radius: var(--r-lg);
  padding: 20px;
  transition: border-color 0.2s, transform 0.2s;
}
.feat-card:hover { border-color: var(--c-border2); transform: translateY(-2px); }
.feat-icon  { font-size: 1.4rem; margin-bottom: 10px; }
.feat-title { font-weight: 600; color: var(--c-text); font-size: 0.9rem; margin-bottom: 6px; }
.feat-desc  { color: var(--c-text3); font-size: 0.78rem; line-height: 1.6; }

/* ── Stat Table ── */
.stat-grid {
  display: grid; grid-template-columns: repeat(2,1fr); gap: 8px;
}
.stat-item {
  background: var(--c-surface3);
  border: 1px solid var(--c-border);
  border-radius: var(--r-sm);
  padding: 10px 14px;
}
.stat-label { font-size: 0.68rem; color: var(--c-text3); font-weight: 600;
  letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 3px; }
.stat-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.95rem; color: var(--c-text); font-weight: 500;
}

/* ── Scenario Card ── */
.scenario-card {
  background: var(--c-surface2);
  border: 1px solid var(--c-border);
  border-radius: var(--r-md);
  padding: 16px 20px;
  margin-bottom: 10px;
}
.scenario-header {
  display: flex; align-items: center; gap: 10px;
  margin-bottom: 8px;
}
.scenario-title { font-weight: 600; font-size: 0.9rem; color: var(--c-text); }
.scenario-body  { font-size: 0.82rem; color: var(--c-text2); line-height: 1.6; }
.scenario-stats {
  display: flex; gap: 16px; margin-top: 10px;
  padding-top: 10px; border-top: 1px solid var(--c-border);
  font-size: 0.75rem; color: var(--c-text3);
}
.scenario-stats strong { color: var(--c-text2); }

/* ── Sidebar Sections ── */
.sb-section { margin-bottom: 20px; }
.sb-label {
  font-size: 0.67rem; font-weight: 700; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--c-text3);
  margin-bottom: 8px; display: block;
}
.sb-logo {
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--c-border);
  margin-bottom: 16px;
}
.sb-logo-eyebrow {
  font-size: 0.6rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--c-accent);
  margin-bottom: 3px;
}
.sb-logo-title {
  font-family: 'DM Serif Display', serif;
  font-size: 1.05rem; color: var(--c-text); font-weight: 400;
}
.sb-logo-sub {
  font-size: 0.68rem; color: var(--c-text3); margin-top: 2px;
  font-family: 'JetBrains Mono', monospace;
}

/* ── Benford Chart Label ── */
.benford-note {
  background: var(--c-surface3);
  border: 1px solid var(--c-border);
  border-radius: var(--r-sm);
  padding: 10px 14px;
  font-size: 0.78rem; color: var(--c-text2);
  margin-top: 8px; line-height: 1.5;
}

/* ── Timeline ── */
.timeline-item {
  display: flex; gap: 14px;
  padding: 12px 0;
  border-bottom: 1px solid var(--c-border);
}
.timeline-item:last-child { border-bottom: none; }
.timeline-dot {
  width: 8px; height: 8px;
  border-radius: 50%; flex-shrink: 0;
  margin-top: 6px;
}
.timeline-dot.critical { background: var(--c-critical); box-shadow: 0 0 6px var(--c-critical); }
.timeline-dot.high     { background: var(--c-high); }
.timeline-dot.medium   { background: var(--c-medium); }
.timeline-dot.low      { background: var(--c-low); }
.timeline-content { flex: 1; }
.timeline-title { font-size: 0.83rem; font-weight: 600; color: var(--c-text); margin-bottom: 2px; }
.timeline-sub   { font-size: 0.74rem; color: var(--c-text3); }

/* ── Data Overview Grid ── */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(4,1fr);
  gap: 10px; margin-bottom: 16px;
}
.ov-card {
  background: var(--c-surface3);
  border: 1px solid var(--c-border);
  border-radius: var(--r-sm);
  padding: 12px 14px;
}
.ov-label { font-size: 0.67rem; text-transform: uppercase; letter-spacing: 0.8px;
  font-weight: 700; color: var(--c-text3); margin-bottom: 4px; }
.ov-value {
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.1rem; font-weight: 600; color: var(--c-text);
}

/* ── Benford Table ── */
.bf-table { width:100%; font-size:0.78rem; border-collapse:collapse; }
.bf-table th { background:var(--c-surface3); color:var(--c-text2); font-weight:600;
  padding:8px 12px; text-align:left; font-size:0.7rem; letter-spacing:0.5px; text-transform:uppercase; }
.bf-table td { padding:7px 12px; border-bottom:1px solid var(--c-border); color:var(--c-text2); }
.bf-table tr:hover td { background:rgba(255,255,255,0.02); }
.bf-dev-low  { color:var(--c-low2); font-weight:600; font-family:'JetBrains Mono',monospace; }
.bf-dev-mid  { color:var(--c-high2); font-weight:600; font-family:'JetBrains Mono',monospace; }
.bf-dev-high { color:var(--c-critical2); font-weight:600; font-family:'JetBrains Mono',monospace; }

/* ── Scrollable Table Container ── */
.scroll-table { overflow-x:auto; border-radius:var(--r-md); }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ─── Plotly Ortak Tema ────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(17,30,48,0.5)",
    font=dict(family="DM Sans", color="#8aa4be", size=12),
    xaxis=dict(gridcolor="#1c2e44", zerolinecolor="#1c2e44", linecolor="#1c2e44"),
    yaxis=dict(gridcolor="#1c2e44", zerolinecolor="#1c2e44", linecolor="#1c2e44"),
    colorway=["#4f9cf9","#22d3ee","#a78bfa","#fbbf24","#34d399","#ff6b6b","#f472b6","#fb923c"],
    margin=dict(l=28, r=28, t=48, b=28),
    hoverlabel=dict(
        bgcolor="#0c1524", bordercolor="#1c2e44",
        font_family="DM Sans", font_size=12,
    ),
    legend=dict(
        bgcolor="rgba(12,21,36,0.8)", bordercolor="#1c2e44",
        borderwidth=1, font_size=11,
    ),
)
COLOR_RISK = {
    "Kritik": "#e03e3e", "Yüksek": "#d97706",
    "Orta":   "#2563eb", "Düşük":  "#059669",
}

# ══════════════════════════════════════════════════════════════════════════════
# M1 – EVRENSEl KOLON TANIMA  (3-Katmanlı Strateji)
# ══════════════════════════════════════════════════════════════════════════════
# Katman 1 : Anahtar-kelime puanlama (Türkçe + İngilizce + SAP + Oracle + Netsis + Logo)
# Katman 2 : Veri tipi çıkarımı (sayısal, datetime, string)
# Katman 3 : İstatistiksel ince ayar (varyans, kardinalite, aralık)
# ─────────────────────────────────────────────────────────────────────────────

COLUMN_KW: dict[str, list[str]] = {
    # ── TUTAR ──
    "amount": [
        "tutar","amount","fiyat","price","total","net","gross","deger","değer",
        "bedel","sum","toplam","debit","credit","borc","borç","alacak","wrbtr",
        "dmbtr","netwr","brwrd","value","cost","maliyet","odeme","ödeme","payment",
        "invoice_amount","invoice_value","para","tl","usd","eur","gbp","ytl",
        "miktar_tutar","brut","brüt","net_tutar","odenen","ödenen","tahsilat",
        "tahsil","alim","alım","satis_tutari","satış_tutarı","harcama","gider",
        "gelir","revenue","expense","spending","harcamalar","maliyeti","bedeli",
        "toplamtutar","geneltoplam","satirtoplami","kalemtutari","faturatutari",
        "meblag","meblağ","siparis_tutari","po_value","line_amount",
    ],
    # ── TARİH ──
    "date": [
        "tarih","date","timestamp","time","zaman","gun","gün","bldat","budat",
        "cpudt","erdat","created","modified","updated","dt","period","donem",
        "dönem","ay","month","year","yil","yıl","tarihi","datetime","hareket",
        "olusturma","oluşturma","giris","giriş","kayit_tarihi","islem_tarihi",
        "belge_tarihi","fatura_tarihi","vade_tarihi","vade","due_date","post_date",
        "entry_date","transaction_date","posting_date","doc_date","value_date",
        "muhasebe_tarihi","muhasebetarihi","odeme_tarihi","tahakkuk","accrual",
        "bitis","bitiş","baslangic","başlangıç","start_date","end_date",
    ],
    # ── TEDARİKÇİ / KARŞI TARAF ──
    "vendor": [
        "tedarikci","tedarikçi","vendor","supplier","satici","satıcı","musteri",
        "müşteri","customer","client","lifnr","kunnr","partner","firma","company",
        "karsi","karşı","counterparty","account_name","isim","name","ad","title",
        "sirket","şirket","kurum","institution","payee","alici","alıcı","bayi",
        "distribütor","distributor","alt_tedarikci","alt_müşteri","cari","cari_adi",
        "cari_unvani","cari_unvanı","unvan","vendor_name","supplier_name",
        "customer_name","company_name","firm_name","party_name","karsi_taraf",
        "saticikodu","saticiadi","tedarikcikodu","tedarikciad","businesspartner",
    ],
    # ── KULLANICI / PERSONEL ──
    "user": [
        "kullanici","kullanıcı","user","personel","employee","ernam","aenam",
        "usnam","uname","operator","girenkisi","giren","olusturan","oluşturan",
        "created_by","entered_by","author","agent","staff","preparer","düzenleyen",
        "kaydeden","kayd_eden","giren_kisi","islem_yapan","islemi_yapan",
        "giris_yapan","giriş_yapan","username","user_id","emp_id","personel_no",
        "personel_id","sicil","sicil_no","prepared_by","processed_by","maker",
        "initiator","requester","talep_eden","submitter","creator","recorder",
    ],
    # ── ONAYLAYAN ──
    "approver": [
        "onaylayan","approver","approved_by","onay_yapan","manager","mudur",
        "müdür","supervisor","reviewer","checker","controller","yetkili",
        "onaylayan_kisi","onay_veren","authorize","authorizer","approver_name",
        "approved_user","amiri","amir","yönetici","yonetici","checker_name",
        "second_approver","ust_onay","üst_onay","imzalayan","imza","signer",
    ],
    # ── BELGE NUMARASI ──
    "doc_id": [
        "belge","document","docnum","belnr","vbeln","ebeln","invoice","fatura",
        "siparis","siparış","order","id","no","num","number","ref","kod","code",
        "ticket","serial","seri","fis","fiş","evrak","makbuz","receipt","voucher",
        "belge_no","fatura_no","siparis_no","order_no","invoice_no","doc_no",
        "ref_no","reference","referans","kayit_no","islem_no","hareket_no",
        "muhasebe_no","journal_no","entry_no","transaction_id","txn_id","po_no",
        "po_number","payment_ref","odeme_ref","chq_no","check_no","dekont_no",
    ],
    # ── KATEGORİ / TİP ──
    "category": [
        "kategori","category","tip","type","tur","tür","sinif","sınıf","hesap",
        "account","gl","cost_type","maliyet","hkont","matyp","class","grup",
        "group","bolum","bölüm","section","segment","kalem","item_type","nature",
        "gl_account","hesap_kodu","hesap_adi","masraf_turu","masraf_türü",
        "gider_turu","gider_türü","harcama_turu","harcama_türü","expense_type",
        "cost_category","muhasebe_hesabi","hesap_planı","chart_of_accounts",
        "account_type","invoice_type","fatura_turu","payment_type","odeme_turu",
    ],
    # ── DURUM / ONAY DURUMU ──
    "status": [
        "onay","approval","status","durum","state","approved","accepted","rejected",
        "pending","bekle","tamamla","complete","aktif","active","statü","statu",
        "onay_durumu","approval_status","islem_durumu","payment_status","odeme_durumu",
        "kayit_durumu","belge_durumu","doc_status","workflow_status","stage",
        "aşama","asama","step","adim","adım","flag","isaretli","checked",
        "verifed","validated","posted","booked","muhasebeleşti","reversed",
    ],
    # ── DEPARTMAN / BİRİM ──
    "department": [
        "departman","department","birim","unit","bolum","bölüm","division","branch",
        "sube","şube","merkez","center","profit_center","kostl","cost_center",
        "cc","maliyet_merkezi","masraf_yeri","butce_birimi","bütçe_birimi",
        "org_unit","organization","organizasyon","plant","fabrika","tesis",
        "lokasyon","location","site","bolge","bölge","region","subsidiary",
        "company_code","sirket_kodu","şirket_kodu","bukrs","buket",
    ],
    # ── AÇIKLAMA ──
    "description": [
        "aciklama","açıklama","description","desc","detail","note","not","comment",
        "yorum","explanation","text","metin","narration","konu","subject","memo",
        "narrative","islem_aciklama","hareket_aciklama","fatura_aciklama",
        "siparis_aciklama","belge_aciklama","stext","ltext","item_text","header",
        "line_item","kalem_aciklamasi","transaction_description","remarks",
    ],
    # ── PARA BİRİMİ ──
    "currency": [
        "para_birimi","currency","doviz","döviz","waers","tcurr","lcurr",
        "curr","cur","fx","foreign","yabanci","yabancı","kur","exchange",
    ],
    # ── MİKTAR / ADET ──
    "quantity": [
        "adet","quantity","qty","miktar","menge","miktari","miktarı","units",
        "pieces","pcs","count","sayi","sayı","number_of","amount_of",
    ],
}

ROLE_TR: dict[str, str] = {
    "amount":      "Tutar",
    "date":        "Tarih",
    "vendor":      "Karşı Taraf",
    "user":        "Kullanıcı",
    "approver":    "Onaylayan",
    "doc_id":      "Belge No",
    "category":    "Kategori",
    "status":      "Durum",
    "department":  "Departman",
    "description": "Açıklama",
    "currency":    "Para Birimi",
    "quantity":    "Miktar",
}


def _normalize(s: str) -> str:
    """Kolon adını normalize et: küçük harf, boşluk/nokta/tire → alt çizgi."""
    s = s.lower().strip()
    s = re.sub(r"[\s\.\-\/\\]+", "_", s)
    # Türkçe karakter normalizasyonu
    s = s.replace("ı","i").replace("ğ","g").replace("ü","u") \
         .replace("ş","s").replace("ö","o").replace("ç","c")
    return s


def _score_col(col_norm: str, keywords: list[str]) -> float:
    score = 0.0
    for kw in keywords:
        kw_n = _normalize(kw)
        if kw_n == col_norm:
            score += 12         # tam eşleşme – en yüksek
        elif col_norm.startswith(kw_n):
            score += 7          # önek
        elif col_norm.endswith(kw_n):
            score += 6          # sonek
        elif kw_n in col_norm:
            score += 4          # içeriyor
        # Kısmi eşleşme (en az 4 char)
        elif len(kw_n) >= 4 and kw_n[:4] in col_norm:
            score += 1.5
    return score


def detect_columns(df: pd.DataFrame) -> dict[str, str]:
    """
    Evrensel 3-Katmanlı Kolon Tanıma Motoru.

    Dönüş:
        {rol: gerçek_sütun_adı}  –  tanınan tüm roller için
    """
    # Normalize haritası: normalize_ad → orijinal_ad
    norm_map: dict[str, str] = {_normalize(c): c for c in df.columns}
    mapping: dict[str, str] = {}
    used: set[str] = set()

    # ── KATMAN 1: Anahtar-Kelime Puanlama ──────────────────────────────────
    for role, kws in COLUMN_KW.items():
        best_col, best_score = None, 0.0
        for nk, ok in norm_map.items():
            if ok in used:
                continue
            sc = _score_col(nk, kws)
            if sc > best_score:
                best_score, best_col = sc, ok
        if best_col and best_score > 0:
            mapping[role] = best_col
            used.add(best_col)

    # ── KATMAN 2: Veri Tipi Fallback ────────────────────────────────────────
    num_cols = [c for c in df.columns
                if pd.api.types.is_numeric_dtype(df[c]) and c not in used]
    dt_cols  = [c for c in df.columns
                if pd.api.types.is_datetime64_any_dtype(df[c]) and c not in used]
    str_cols = [c for c in df.columns
                if df[c].dtype == object and c not in used]

    # Tutar fallback → en yüksek varyans
    if "amount" not in mapping and num_cols:
        best = max(num_cols, key=lambda c: float(df[c].std()) if df[c].std() > 0 else 0)
        mapping["amount"] = best
        used.add(best)
        num_cols = [c for c in num_cols if c != best]

    # Miktar fallback → ikinci sayısal sütun
    if "quantity" not in mapping and num_cols:
        mapping["quantity"] = num_cols[0]
        used.add(num_cols[0])

    # Tarih fallback → datetime sütun
    if "date" not in mapping:
        if dt_cols:
            mapping["date"] = dt_cols[0]
            used.add(dt_cols[0])
        else:
            # String içinden tarih dene
            for c in str_cols:
                try:
                    sample = df[c].dropna().head(20).astype(str)
                    parsed = pd.to_datetime(sample, infer_datetime_format=True, errors="coerce")
                    if parsed.notna().sum() >= len(sample) * 0.7:
                        mapping["date"] = c
                        used.add(c)
                        str_cols = [x for x in str_cols if x != c]
                        break
                except Exception:
                    pass

    # String sütunlardan kalan rolleri ata
    role_fallback = ["vendor","user","approver","category","doc_id",
                     "department","description","status","currency"]
    for role in role_fallback:
        if role not in mapping and str_cols:
            mapping[role] = str_cols.pop(0)

    # ── KATMAN 3: İstatistiksel İnce Ayar ───────────────────────────────────
    # doc_id → en yüksek kardinaliteli string
    if "doc_id" not in mapping:
        remaining_str = [c for c in df.columns if df[c].dtype == object and c not in used]
        if remaining_str:
            best = max(remaining_str, key=lambda c: df[c].nunique())
            mapping["doc_id"] = best

    # Tutar sütununun gerçekten sayısal olduğundan emin ol
    if "amount" in mapping:
        amt_test = _to_numeric_safe(df, mapping["amount"])
        if amt_test.notna().sum() < len(df) * 0.3:
            # Bu sütun sayısal değil, yeniden ara
            del mapping["amount"]
            for c in df.columns:
                if c not in used:
                    test = _to_numeric_safe(df, c)
                    if test.notna().sum() > len(df) * 0.5:
                        mapping["amount"] = c
                        break

    return mapping


# ─── Sayısal Dönüşüm Yardımcısı ──────────────────────────────────────────────
def _to_numeric_safe(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Para birimi sembolleri, binlik ayraçlar, Türkçe ondalık (,) dahil
    herhangi bir formattaki sayı sütununu güvenle float'a dönüştür.
    """
    s = df[col].astype(str).str.strip()
    # Para birimi ve boşluk temizle
    s = s.str.replace(r"[₺\$€£¥₩\s]", "", regex=True)
    # Parantezli negatif: (1.234,56) → -1234.56
    s = s.apply(lambda x: "-" + x[1:-1] if x.startswith("(") and x.endswith(")") else x)
    # Binlik ayraç tespiti: 1.234,56 → Türkçe; 1,234.56 → İngilizce
    def _fix(x):
        if re.search(r"\d\.\d{3},", x):   # Türkçe format
            return x.replace(".", "").replace(",", ".")
        elif re.search(r"\d,\d{3}\.", x):  # İngilizce format
            return x.replace(",", "")
        else:
            return x.replace(",", ".")
    s = s.apply(_fix)
    return pd.to_numeric(s, errors="coerce")


def _parse_dates_safe(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Tarih sütununu güvenle parse et, hatalı değerleri NaT yap."""
    df = df.copy()
    try:
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
    except Exception:
        try:
            df[col] = pd.to_datetime(df[col], format="mixed", errors="coerce")
        except Exception:
            pass
    return df


# ══════════════════════════════════════════════════════════════════════════════
# M2 – VERİ KALİTESİ & KONTROL TESTLERİ
# ══════════════════════════════════════════════════════════════════════════════

def run_data_quality(df: pd.DataFrame, col_map: dict) -> list[dict]:
    """
    7 temel denetim kalite kontrolünü çalıştırır.
    Her kontrol IIA standartlarına uygun yapılandırılmış dict döndürür.
    """
    total = len(df)
    results: list[dict] = []

    # ── KT-01: Eksik Veri Analizi ─────────────────────────────────────────
    miss     = df.isnull().sum()
    miss_pct = (miss / total * 100).round(2)
    crit_cols = miss[miss_pct > 10]
    warn_cols = miss[(miss_pct > 2) & (miss_pct <= 10)]
    any_miss  = df.isnull().any(axis=1).sum()
    results.append({
        "id":       "KT-01",
        "kontrol":  "Eksik Veri Analizi",
        "bulgu":    (f"{len(crit_cols)} sütunda %10 üzeri, {len(warn_cols)} sütunda "
                     f"%2–10 arası eksik veri. Toplam {any_miss:,} kayıt en az bir boş alan içeriyor."),
        "etki":     int(any_miss),
        "risk":     "Yüksek" if len(crit_cols) >= 2 else ("Orta" if len(crit_cols) > 0 or len(warn_cols) > 3 else "Düşük"),
        "detay":    miss_pct[miss_pct > 0].round(1).to_dict(),
        "kategori": "Veri Bütünlüğü",
    })

    # ── KT-02: Mükerrer Belge Numarası ────────────────────────────────────
    if "doc_id" in col_map:
        dup_mask = df.duplicated(subset=[col_map["doc_id"]], keep=False)
        dup_n    = int(dup_mask.sum())
        results.append({
            "id":       "KT-02",
            "kontrol":  "Mükerrer Belge Numarası",
            "bulgu":    f"{dup_n:,} kayıt aynı belge numarasını ({col_map['doc_id']}) paylaşıyor. Bu, fatura iptali, sistem hatası veya kasıtlı mükerrer kayıt işaretçisidir.",
            "etki":     dup_n,
            "risk":     "Kritik" if dup_n > 5 else ("Yüksek" if dup_n > 0 else "Düşük"),
            "detay":    {},
            "kategori": "Mükerrerlik",
        })

    # ── KT-03: Tam Satır Mükerreri ────────────────────────────────────────
    full_dup = int(df.duplicated().sum())
    results.append({
        "id":       "KT-03",
        "kontrol":  "Tam Satır Mükerrerlik",
        "bulgu":    f"{full_dup:,} satır, diğer bir satırın birebir kopyası. Sistematik veri aktarım hatası veya çift kayıt riski.",
        "etki":     full_dup,
        "risk":     "Kritik" if full_dup > 10 else ("Yüksek" if full_dup > 0 else "Düşük"),
        "detay":    {},
        "kategori": "Mükerrerlik",
    })

    # ── KT-04: Negatif & Sıfır Tutar ─────────────────────────────────────
    if "amount" in col_map:
        amt  = _to_numeric_safe(df, col_map["amount"])
        neg  = int((amt < 0).sum())
        zero = int((amt == 0).sum())
        neg_total = float(amt[amt < 0].sum()) if neg > 0 else 0
        results.append({
            "id":       "KT-04",
            "kontrol":  "Negatif & Sıfır Tutar Kontrolü",
            "bulgu":    (f"{neg:,} negatif tutar (toplam {neg_total:,.2f}), "
                         f"{zero:,} sıfır değerli kayıt. "
                         "Negatif tutarlar ters kayıt veya iade süreçlerine işaret edebilir."),
            "etki":     neg + zero,
            "risk":     "Yüksek" if neg > 10 else ("Orta" if neg > 0 else "Düşük"),
            "detay":    {"negatif_adet": neg, "negatif_toplam": round(neg_total, 2), "sıfır_adet": zero},
            "kategori": "Tutar Doğruluğu",
        })

    # ── KT-05: Aykırı Değer Analizi (IQR + Z-score) ──────────────────────
    if "amount" in col_map:
        amt = _to_numeric_safe(df, col_map["amount"]).dropna()
        if len(amt) > 4:
            Q1, Q3 = amt.quantile(.25), amt.quantile(.75)
            IQR    = Q3 - Q1
            lo, hi = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
            iqr_out  = int(((amt < lo) | (amt > hi)).sum())
            z        = (amt - amt.mean()) / (amt.std() + 1e-9)
            z_out    = int((z.abs() > 3).sum())
            extreme  = int((z.abs() > 5).sum())
            results.append({
                "id":       "KT-05",
                "kontrol":  "Aykırı Değer Analizi (IQR / Z-score)",
                "bulgu":    (f"IQR yöntemi: {iqr_out:,} aykırı değer. "
                             f"Z-score (>3σ): {z_out:,}, aşırı (>5σ): {extreme:,}. "
                             "Bu tutarlar bütçe aşımı, usulsüz ödeme veya sistem hatasını işaret edebilir."),
                "etki":     max(iqr_out, z_out),
                "risk":     "Kritik" if extreme > 3 else ("Yüksek" if max(iqr_out, z_out) > 20 else "Orta"),
                "detay":    {"IQR_sınır_alt": round(lo, 2), "IQR_sınır_üst": round(hi, 2),
                              "IQR_aykırı": iqr_out, "Z_aykırı": z_out, "aşırı_aykırı": extreme},
                "kategori": "Tutar Doğruluğu",
            })

    # ── KT-06: Şüpheli Yuvarlama Deseni ──────────────────────────────────
    if "amount" in col_map:
        amt     = _to_numeric_safe(df, col_map["amount"]).dropna()
        nonzero = amt[amt > 0]
        if len(nonzero) > 0:
            r100  = int((nonzero % 100 == 0).sum())
            r500  = int((nonzero % 500 == 0).sum())
            r1000 = int((nonzero % 1000 == 0).sum())
            r10k  = int((nonzero % 10000 == 0).sum())
            pct   = r100 / len(nonzero) * 100
            results.append({
                "id":       "KT-06",
                "kontrol":  "Şüpheli Yuvarlama Deseni",
                "bulgu":    (f"Tutarların %{pct:.1f}'i 100'ün katı. "
                             f"1.000'in katı: {r1000:,}, 10.000'in katı: {r10k:,}. "
                             "Yüksek yuvarlama oranı sahte veya tahmini veri girişine işaret eder."),
                "etki":     r100,
                "risk":     "Yüksek" if pct > 35 else ("Orta" if pct > 18 else "Düşük"),
                "detay":    {"%100_katı": round(pct, 1), "1000_katı": r1000,
                              "10000_katı": r10k, "500_katı": r500},
                "kategori": "Sahte İşlem Riski",
            })

    # ── KT-07: Tarih Tutarsızlıkları ─────────────────────────────────────
    if "date" in col_map:
        df2    = _parse_dates_safe(df, col_map["date"])
        nat    = int(df2[col_map["date"]].isna().sum())
        now    = pd.Timestamp.now()
        future = int((df2[col_map["date"]] > now).sum())
        very_old = int((df2[col_map["date"]] < pd.Timestamp("2000-01-01")).sum())
        weekend  = int(df2[col_map["date"]].dt.dayofweek.isin([5, 6]).sum()) \
            if df2[col_map["date"]].dtype == "datetime64[ns]" else 0
        results.append({
            "id":       "KT-07",
            "kontrol":  "Tarih Tutarsızlıkları",
            "bulgu":    (f"{nat:,} geçersiz tarih (NaT), {future:,} gelecek tarihli, "
                         f"{very_old:,} 2000 öncesi, {weekend:,} hafta sonu kayıt."),
            "etki":     nat + future + very_old,
            "risk":     "Yüksek" if (nat + future) > 10 else ("Orta" if (nat + future) > 0 else "Düşük"),
            "detay":    {"geçersiz": nat, "gelecek": future,
                          "2000_öncesi": very_old, "hafta_sonu": weekend},
            "kategori": "Veri Bütünlüğü",
        })

    return results


# ══════════════════════════════════════════════════════════════════════════════
# M3 – DENETİM SENARYO MOTORU
# ══════════════════════════════════════════════════════════════════════════════

def run_scenarios(df: pd.DataFrame, col_map: dict) -> list[dict]:
    """
    8 denetim risk senaryosunu otomatik çalıştırır.
    Her senaryo IIA uyumlu risk gerekçesi ve kanıt tablosu içerir.
    """
    scenarios: list[dict] = []
    amt = _to_numeric_safe(df, col_map["amount"]) if "amount" in col_map else None

    # ── SC-01: Olağandışı İşlem Yoğunluğu ───────────────────────────────
    if "date" in col_map:
        df2 = _parse_dates_safe(df.copy(), col_map["date"])
        dc  = df2.groupby(df2[col_map["date"]].dt.date).size()
        if len(dc) > 3:
            mean, std = dc.mean(), dc.std() or 1
            threshold = mean + 2 * std
            spikes    = dc[dc > threshold]
            scenarios.append({
                "id":        "SC-01",
                "senaryo":   "Olağandışı İşlem Yoğunluğu",
                "aciklama":  (f"{len(spikes)} günde günlük işlem sayısı istatistiksel "
                              f"ortalamanın (μ={mean:.1f}) 2 standart sapma üstüne çıktı."),
                "risk_gere": "Yoğun işlem günleri; toplu veri manipülasyonu, sistem açığı istismarı veya onay atlama girişimini işaret edebilir.",
                "risk":      "Yüksek" if len(spikes) > 3 else "Orta",
                "etki":      int(spikes.sum()),
                "ornek":     dc.nlargest(10).reset_index().rename(columns={0: "İşlem Sayısı"}),
                "kategori":  "İşlem Analizi",
            })

    # ── SC-02: Karşı Taraf Yoğunlaşması ─────────────────────────────────
    if "vendor" in col_map and amt is not None:
        va = df.assign(_a=amt.fillna(0)).groupby(col_map["vendor"])["_a"].agg(["sum","count","mean"])
        va.columns = ["Toplam Tutar", "İşlem Sayısı", "Ortalama Tutar"]
        va = va.sort_values("Toplam Tutar", ascending=False)
        total_amt = va["Toplam Tutar"].sum()
        top1_pct  = va["Toplam Tutar"].iloc[0] / (total_amt + 1e-9) * 100
        top3_pct  = va["Toplam Tutar"].iloc[:3].sum() / (total_amt + 1e-9) * 100
        # HHI (Herfindahl-Hirschman Index)
        shares = va["Toplam Tutar"] / (total_amt + 1e-9)
        hhi    = float((shares ** 2).sum() * 10000)
        scenarios.append({
            "id":        "SC-02",
            "senaryo":   "Karşı Taraf Yoğunlaşması (Concentration Risk)",
            "aciklama":  (f"En büyük karşı taraf toplam tutarın %{top1_pct:.1f}'ini, "
                          f"ilk 3 karşı taraf %{top3_pct:.1f}'ini oluşturuyor. "
                          f"HHI Endeksi: {hhi:.0f} (yüksek yoğunlaşma: >2500)."),
            "risk_gere": "Aşırı yoğunlaşma; bağımlılık riski, gizli ilişki, rekabetçi ihale süreçlerini atlatma veya komisyon/rüşvet düzenlemelerini işaret edebilir.",
            "risk":      "Kritik" if top1_pct > 50 else ("Yüksek" if top1_pct > 30 else "Orta"),
            "etki":      len(va[va["Toplam Tutar"] > va["Toplam Tutar"].mean() * 3]),
            "ornek":     va.head(10).reset_index(),
            "kategori":  "Yoğunlaşma Riski",
            "hhi":       hhi,
        })

    # ── SC-03: Mesai Dışı Saat İşlemleri ────────────────────────────────
    if "date" in col_map:
        df2 = _parse_dates_safe(df.copy(), col_map["date"])
        try:
            h   = df2[col_map["date"]].dt.hour
            off = ((h < 8) | (h > 18)) & h.notna()
            off_n = int(off.sum())
            if off_n > 0:
                off_df = df2[off].copy()
                off_df["Saat"] = h[off]
                hour_dist = h[off].value_counts().sort_index()
                scenarios.append({
                    "id":        "SC-03",
                    "senaryo":   "Mesai Dışı Saat İşlemleri",
                    "aciklama":  (f"{off_n:,} işlem standart çalışma saatleri (08:00–18:00) dışında "
                                  "gerçekleştirilmiş. En yoğun mesai dışı saat: "
                                  f"{int(hour_dist.idxmax())}:00."),
                    "risk_gere": "Mesai dışı işlemler; yetkisiz sistem erişimi, gözetim dışı veri değişikliği veya iç kontrollerin devre dışı bırakılmasını işaret edebilir.",
                    "risk":      "Yüksek" if off_n > 20 else "Orta",
                    "etki":      off_n,
                    "ornek":     off_df.head(15),
                    "kategori":  "Erişim Riski",
                })
        except Exception:
            pass

    # ── SC-04: Eşik Altı Yapılandırma (Structuring) ──────────────────────
    if amt is not None:
        threshold_hits = []
        for thresh in [5_000, 10_000, 25_000, 50_000, 100_000, 500_000]:
            lo, hi    = thresh * 0.88, thresh
            band_mask = (amt > lo) & (amt < hi)
            below_n   = int(band_mask.sum())
            if below_n >= 3:
                threshold_hits.append((thresh, below_n))

        if threshold_hits:
            thresh, below_n = max(threshold_hits, key=lambda x: x[1])
            lo = thresh * 0.88
            scenarios.append({
                "id":        "SC-04",
                "senaryo":   f"Eşik Altı Yapılandırma – {thresh:,} TL Eşiği",
                "aciklama":  (f"{below_n:,} işlem {thresh:,} TL onay eşiğinin "
                              f"%88–%100 bandında ({lo:,.0f}–{thresh:,} TL arası). "
                              "Bu desen kasıtlı eşik aşındırmasına (structuring) işaret eder."),
                "risk_gere": "Onay eşiğinin hemen altında tutulan işlemler, üst onay gereksinimini atlatmak için tutarların bilinçli olarak bölündüğünü gösterebilir.",
                "risk":      "Kritik" if below_n > 15 else "Yüksek",
                "etki":      below_n,
                "ornek":     df.assign(_a=amt)[(amt > lo) & (amt < thresh)].head(15),
                "kategori":  "Yetki Atlatma",
            })

    # ── SC-05: Görevler Ayrılığı (SoD) İhlali ───────────────────────────
    if "user" in col_map and "approver" in col_map:
        mask = df[col_map["user"]].notna() & df[col_map["approver"]].notna()
        sod_mask = mask & (df[col_map["user"]] == df[col_map["approver"]])
        sod_n    = int(sod_mask.sum())
        if sod_n > 0:
            sod_users = df.loc[sod_mask, col_map["user"]].value_counts().head(10)
            scenarios.append({
                "id":        "SC-05",
                "senaryo":   "Görevler Ayrılığı (SoD) İhlali",
                "aciklama":  (f"{sod_n:,} kayıtta aynı kişi hem işlemi oluşturan hem de onaylayan "
                              f"rolündedir. {sod_users.index[0] if len(sod_users) else 'N/A'} "
                              f"en fazla ihlal yapan kullanıcı ({sod_users.iloc[0] if len(sod_users) else 0} kez)."),
                "risk_gere": "Görevler ayrılığı ihlali COSO iç kontrol çerçevesinin temel gereksinimlerinden biridir. Tek kişinin hem oluşturma hem onay yetkisine sahip olması usulsüzlük riskini kritik düzeyde artırır.",
                "risk":      "Kritik",
                "etki":      sod_n,
                "ornek":     df[sod_mask].head(15),
                "kategori":  "SoD / Yetki",
                "sod_users": sod_users,
            })

    # ── SC-06: Tekrarlayan Sabit Tutar Deseni ───────────────────────────
    if amt is not None:
        rounded = amt[amt > 0].round(2)
        vc      = rounded.value_counts()
        rep     = vc[vc > 5]
        if len(rep) > 0:
            top_val  = float(rep.index[0])
            top_freq = int(rep.iloc[0])
            scenarios.append({
                "id":        "SC-06",
                "senaryo":   "Tekrarlayan Sabit Tutar Deseni",
                "aciklama":  (f"{len(rep)} farklı tutar değeri 5'ten fazla tekrarlandı. "
                              f"En sık tutar: {top_val:,.2f} TL ({top_freq} kez). "
                              f"Bu durum toplu veri girişi veya kopyala-yapıştır hatasını gösterebilir."),
                "risk_gere": "Aynı tutarın farklı işlemlerde sistematik biçimde tekrarlanması; sahte fatura üretimi, otomatik sistem hatası veya veri kalıplarını gizleme girişimini işaret edebilir.",
                "risk":      "Yüksek" if len(rep) > 10 else "Orta",
                "etki":      int(rep.sum()),
                "ornek":     rep.head(10).reset_index().rename(columns={"index": "Tutar", col_map["amount"]: "Tekrar Sayısı"}),
                "kategori":  "Sahte İşlem Riski",
            })

    # ── SC-07: Kullanıcı Yoğunlaşması ───────────────────────────────────
    if "user" in col_map and amt is not None:
        ua = df.assign(_a=amt.fillna(0)).groupby(col_map["user"])["_a"].agg(["sum","count"])
        ua.columns = ["Toplam Tutar", "İşlem Sayısı"]
        ua = ua.sort_values("Toplam Tutar", ascending=False)
        total_amt = ua["Toplam Tutar"].sum()
        top1_user_pct = ua["Toplam Tutar"].iloc[0] / (total_amt + 1e-9) * 100
        if top1_user_pct > 30:
            scenarios.append({
                "id":        "SC-07",
                "senaryo":   "Kullanıcı/Personel Yoğunlaşması",
                "aciklama":  (f"Tek kullanıcı ({ua.index[0]}) toplam tutarın "
                              f"%{top1_user_pct:.1f}'ini ve {int(ua.iloc[0]['İşlem Sayısı']):,} "
                              "işlemi gerçekleştirmiş. Bu anormal bir yoğunlaşmadır."),
                "risk_gere": "Belirli bir kullanıcıda aşırı işlem yükü, yetki sınırlarının aşılması veya diğer kullanıcı hesaplarının kötüye kullanılmasını işaret edebilir.",
                "risk":      "Yüksek" if top1_user_pct > 50 else "Orta",
                "etki":      int(ua.iloc[0]["İşlem Sayısı"]),
                "ornek":     ua.head(10).reset_index(),
                "kategori":  "Yoğunlaşma Riski",
            })

    # ── SC-08: Hafta Sonu & Tatil Günü İşlemleri ────────────────────────
    if "date" in col_map:
        df2 = _parse_dates_safe(df.copy(), col_map["date"])
        try:
            dow     = df2[col_map["date"]].dt.dayofweek
            weekend = (dow >= 5) & dow.notna()
            wknd_n  = int(weekend.sum())
            if wknd_n > 0:
                scenarios.append({
                    "id":        "SC-08",
                    "senaryo":   "Hafta Sonu & Tatil Günü İşlemleri",
                    "aciklama":  (f"{wknd_n:,} işlem hafta sonunda (Cumartesi/Pazar) "
                                  "gerçekleştirilmiş. Bu durum otomatik işlemler veya "
                                  "yetkisiz sistem erişimine işaret edebilir."),
                    "risk_gere": "Hafta sonu işlemleri çoğu kurumda kısıtlı onay mekanizmasıyla yürütülür. İzin dışı dönemde gerçekleştirilen yüksek tutarlı işlemler iç kontrol riskini artırır.",
                    "risk":      "Orta" if wknd_n < 20 else "Yüksek",
                    "etki":      wknd_n,
                    "ornek":     df2[weekend].head(15),
                    "kategori":  "Erişim Riski",
                })
        except Exception:
            pass

    return scenarios

# ══════════════════════════════════════════════════════════════════════════════
# M4 – RİSK SKORLAMA MOTORU
# ══════════════════════════════════════════════════════════════════════════════
# Ağırlıklı çok-değişkenli skor modeli:
#   Tutar Etkisi    : 35 puan  (normalize edilmiş mutlak değer)
#   Anomali Seviyesi: 30 puan  (Z-score bazlı)
#   İşlem Frekansı  : 15 puan  (vendor bazlı)
#   Kullanıcı Riski : 10 puan  (user bazlı)
#   Zaman Riski     :  5 puan  (mesai dışı / hafta sonu)
#   Kontrol Uyarısı :  5 puan  (yuvarlak tutar / eşik altı)
# ─────────────────────────────────────────────────────────────────────────────

def compute_risk_scores(df: pd.DataFrame, col_map: dict) -> pd.DataFrame:
    """
    Her kayıt için 0–100 arası birleşik risk skoru hesaplar.
    Risk seviyesi: Düşük (<25) | Orta (25–49) | Yüksek (50–74) | Kritik (≥75)
    """
    df  = df.copy()
    n   = len(df)
    s   = pd.Series(0.0, index=df.index)

    # ── Bileşen 1: Tutar Etkisi (35p) ────────────────────────────────────
    if "amount" in col_map:
        amt = _to_numeric_safe(df, col_map["amount"]).fillna(0).abs()
        cap = amt.quantile(0.99) + 1e-9
        s  += (amt / cap).clip(0, 1) * 35

    # ── Bileşen 2: Anomali (Z-score) (30p) ───────────────────────────────
    if "amount" in col_map:
        amt = _to_numeric_safe(df, col_map["amount"]).fillna(0)
        z   = (amt - amt.mean()).abs() / (amt.std() + 1e-9)
        cap_z = z.quantile(0.99) + 1e-9
        s  += (z / cap_z).clip(0, 1) * 30

    # ── Bileşen 3: Vendor Frekansı (15p) ─────────────────────────────────
    if "vendor" in col_map:
        freq     = df[col_map["vendor"]].map(df[col_map["vendor"]].value_counts())
        freq_max = freq.max() + 1e-9
        s       += (freq / freq_max) * 15

    # ── Bileşen 4: Kullanıcı Riski (10p) ─────────────────────────────────
    if "user" in col_map:
        freq     = df[col_map["user"]].map(df[col_map["user"]].value_counts())
        freq_max = freq.max() + 1e-9
        s       += (freq / freq_max) * 10

    # ── Bileşen 5: Zaman Riski (5p) ──────────────────────────────────────
    if "date" in col_map:
        df2 = _parse_dates_safe(df, col_map["date"])
        try:
            h   = df2[col_map["date"]].dt.hour.fillna(12)
            dow = df2[col_map["date"]].dt.dayofweek.fillna(0)
            off_hour = ((h < 8) | (h > 18)).astype(float)
            weekend  = (dow >= 5).astype(float)
            s += (off_hour * 3 + weekend * 2).clip(0, 5)
        except Exception:
            pass

    # ── Bileşen 6: Kontrol Uyarısı (5p) ──────────────────────────────────
    if "amount" in col_map:
        amt    = _to_numeric_safe(df, col_map["amount"]).fillna(0)
        # Yuvarlak tutar: 2p
        round_flag = ((amt.abs() % 100 == 0) & (amt != 0)).astype(float) * 2
        # Eşik altı: 3p
        struct_flag = pd.Series(0.0, index=df.index)
        for thresh in [5000, 10000, 25000, 50000, 100000]:
            struct_flag = struct_flag.where(
                ~((amt > thresh * 0.88) & (amt < thresh)),
                3.0
            )
        s += (round_flag + struct_flag).clip(0, 5)

    df["risk_skoru"]    = s.clip(0, 100).round(2)
    df["risk_seviyesi"] = df["risk_skoru"].apply(
        lambda v: "Kritik" if v >= 75 else ("Yüksek" if v >= 50 else ("Orta" if v >= 25 else "Düşük"))
    )
    return df


# ══════════════════════════════════════════════════════════════════════════════
# M5 – BENFORD YASASI ANALİZİ
# ══════════════════════════════════════════════════════════════════════════════
# Benford Yasası: Doğal veri setlerinde ilk rakamların beklenen frekans dağılımı.
# Önemli sapma → yapay / manipüle edilmiş veriye işaret eder.
# ─────────────────────────────────────────────────────────────────────────────

BENFORD_EXPECTED = {
    1: 30.10, 2: 17.61, 3: 12.49, 4: 9.69,
    5: 7.92,  6: 6.69,  7: 5.80,  8: 5.12, 9: 4.58,
}

def run_benford_analysis(df: pd.DataFrame, col_map: dict) -> dict:
    """
    Tutar sütununa Benford Yasası uygular.
    Döndürür: {digit: {observed, expected, deviation, chi_sq}}
    """
    if "amount" not in col_map:
        return {}

    amt     = _to_numeric_safe(df, col_map["amount"]).dropna()
    amt_pos = amt[amt > 0]
    if len(amt_pos) < 50:
        return {}

    # İlk rakamı çıkar
    first_digits = amt_pos.astype(str).str.replace(r"^0+\.", "", regex=True) \
                                      .str.replace(r"[^1-9]", "", regex=True) \
                                      .str[0].astype(int, errors="ignore")
    first_digits = first_digits[first_digits.between(1, 9)]
    total = len(first_digits)
    if total == 0:
        return {}

    obs_counts = Counter(first_digits.tolist())
    results    = {}
    chi_sq     = 0.0

    for d in range(1, 10):
        obs_count = obs_counts.get(d, 0)
        obs_pct   = obs_count / total * 100
        exp_pct   = BENFORD_EXPECTED[d]
        deviation = obs_pct - exp_pct
        exp_count = total * exp_pct / 100
        chi_sq   += ((obs_count - exp_count) ** 2) / (exp_count + 1e-9)

        results[d] = {
            "gozlemlenen": round(obs_pct, 2),
            "beklenen":    exp_pct,
            "sapma":       round(deviation, 2),
            "adet":        obs_count,
        }

    # Kritiklik değerlendirmesi (ki-kare df=8, α=0.05 → 15.51)
    results["chi_sq"]   = round(chi_sq, 2)
    results["anormal"]  = chi_sq > 15.51
    results["toplam_n"] = total
    return results


# ══════════════════════════════════════════════════════════════════════════════
# M6 – PARETO (80/20) ANALİZİ
# ══════════════════════════════════════════════════════════════════════════════

def run_pareto_analysis(df: pd.DataFrame, col_map: dict) -> dict:
    """
    Vendor / User bazlı Pareto analizi.
    Toplam tutarın %80'ini kimin oluşturduğunu tespit eder.
    """
    result = {}

    if "vendor" in col_map and "amount" in col_map:
        amt   = _to_numeric_safe(df, col_map["amount"]).fillna(0)
        va    = df.assign(_a=amt).groupby(col_map["vendor"])["_a"].sum().sort_values(ascending=False)
        total = va.sum()
        cumulative = va.cumsum() / (total + 1e-9) * 100
        vendors_80 = int((cumulative <= 80).sum()) + 1
        result["vendor"] = {
            "data":       va,
            "cumulative": cumulative,
            "vendors_80": vendors_80,
            "total":      float(total),
            "top_vendor": str(va.index[0]) if len(va) > 0 else "",
            "top_pct":    float(va.iloc[0] / (total + 1e-9) * 100) if len(va) > 0 else 0,
        }

    if "user" in col_map and "amount" in col_map:
        amt   = _to_numeric_safe(df, col_map["amount"]).fillna(0)
        ua    = df.assign(_a=amt).groupby(col_map["user"])["_a"].sum().sort_values(ascending=False)
        total = ua.sum()
        cumulative = ua.cumsum() / (total + 1e-9) * 100
        users_80 = int((cumulative <= 80).sum()) + 1
        result["user"] = {
            "data":     ua,
            "cumulative": cumulative,
            "users_80": users_80,
            "total":    float(total),
            "top_user": str(ua.index[0]) if len(ua) > 0 else "",
            "top_pct":  float(ua.iloc[0] / (total + 1e-9) * 100) if len(ua) > 0 else 0,
        }

    return result


# ══════════════════════════════════════════════════════════════════════════════
# M9 – DENETİM BULGULARI ÜRETİCİ
# ══════════════════════════════════════════════════════════════════════════════

_ROOT_CAUSES = {
    "Eksik":       "Veri girişinde zorunlu alan (mandatory field) kısıtlamalarının veya sistem entegrasyon doğrulama kontrollerinin yetersizliği.",
    "Mükerrer":    "ERP sisteminde benzersiz belge numarası kısıtlaması (unique constraint) eksikliği veya onay sürecindeki kontrol boşluğu.",
    "Negatif":     "Ters kayıt ve iade prosedürlerinde yeterli kontrol mekanizmasının bulunmaması; negatif değer giriş politikasının tanımlanmamış olması.",
    "Aykırı":      "Tutar bazlı onay limiti matrisinin güncellenmemiş olması; aykırı değer tespitine yönelik istatistiksel izleme mekanizmasının eksikliği.",
    "Yuvarlama":   "Veri doğrulama kurallarının yetersizliği; tahmini veya sahte veri girişini engelleyen kontrol mekanizmasının bulunmaması.",
    "Tarih":       "Sistem tarih/saat kontrolü konfigürasyon hatası veya geriye dönük muhasebe kaydı konusunda yeterli onay sürecinin olmaması.",
    "Yoğunlaşma":  "Alternatif teklif (en az 3 teklif) politikasının uygulanmaması; tedarikçi çeşitlendirme hedeflerinin satınalma prosedürüne yansıtılmamış olması.",
    "Mesai":       "Zaman bazlı sistem erişim politikasının tanımlanmamış veya teknik olarak uygulanmamış olması; erişim kayıt ve izleme sisteminin yetersizliği.",
    "Eşik":        "Birikimli işlem tutarlarını izleyen kontrol mekanizmasının bulunmaması; onay eşiklerinin bireysel işlem bazında değil toplam bazda değerlendirilmemesi.",
    "SoD":         "Rol bazlı erişim kontrolü (RBAC) politikasının yetersiz tanımlanmış olması; görevler ayrılığı matrisinin güncel tutulmaması ve periyodik inceleme yapılmaması.",
    "Tekrarlayan": "Çift ödeme/kayıt tespiti için kural motoru eksikliği; veri girişinde tutar bazlı otomatik doğrulama kontrolünün bulunmaması.",
    "Olağandışı":  "Anomali tespiti ve gerçek zamanlı işlem izleme kapasitesinin bulunmaması; günlük işlem limiti kontrol mekanizmasının tanımlanmamış olması.",
    "Kullanıcı":   "Kullanıcı yetki profillerinin işlem hacmiyle orantılı olarak tanımlanmamış olması; aşırı yetki birikiminin (privilege accumulation) önlenmesine yönelik kontrol eksikliği.",
    "Hafta Sonu":  "Hafta sonu/tatil günü sistem erişiminde çok faktörlü doğrulama (MFA) ve yönetici onayı zorunluluğunun bulunmaması.",
    "Benford":     "Finansal verinin Benford Yasası beklentisinden anlamlı sapması; manuel veri manipülasyonu, sistem hatası veya sahte kayıt girişine işaret eden istatistiksel uyarı.",
    "Pareto":      "Tedarikçi/kullanıcı yoğunlaşmasının kabul edilebilir sınırların üzerinde olması; risk tabanlı tedarikçi yönetim sürecinin yeterince uygulanmaması.",
}

_IMPACTS = {
    "Kritik": "Maddi finansal kayıp, uyumsuzluk cezası, itibar hasarı ve yasal sorumluluk riski yüksektir.",
    "Yüksek": "Operasyonel verimlilik kaybı ve finansal raporlama güvenilirliğine olumsuz etki riski bulunmaktadır.",
    "Orta":   "Kontrol zafiyetinin sürmesi halinde orta vadede risk profili artabilir; izleme kapsamına alınmalıdır.",
    "Düşük":  "Mevcut durumda sınırlı etki; iyileştirme fırsatı olarak değerlendirilmelidir.",
}


def _infer_root_cause(text: str) -> str:
    for kw, cause in _ROOT_CAUSES.items():
        if kw.lower() in text.lower():
            return cause
    return "İlgili süreçte yeterli iç kontrol mekanizmasının bulunmaması; süreç tasarımında kontrol boşluklarının varlığı."


def generate_findings(quality: list, scenarios: list,
                      df: pd.DataFrame, benford: dict, pareto: dict) -> list[dict]:
    """
    Kalite kontrolleri + senaryolar + Benford + Pareto'dan
    IIA uyumlu yapılandırılmış bulgular üretir.
    """
    prio   = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3}
    findings: list[dict] = []

    # ── Kalite Bulguları ──
    for q in quality:
        if q["etki"] > 0 and q["risk"] in ("Kritik", "Yüksek", "Orta"):
            findings.append({
                "id":        q["id"],
                "baslik":    f"[{q['id']}] {q['kontrol']}",
                "bulgu":     q["bulgu"],
                "kok_neden": _infer_root_cause(q["kontrol"]),
                "is_etkisi": f"{q['etki']:,} etkilenen kayıt. {_IMPACTS.get(q['risk'], '')}",
                "risk":      q["risk"],
                "etki":      q["etki"],
                "kaynak":    "Veri Kalitesi Modülü",
                "kategori":  q.get("kategori", "Veri Bütünlüğü"),
            })

    # ── Senaryo Bulguları ──
    for s in scenarios:
        if s["etki"] > 0:
            findings.append({
                "id":        s["id"],
                "baslik":    f"[{s['id']}] {s['senaryo']}",
                "bulgu":     s["aciklama"],
                "kok_neden": _infer_root_cause(s["senaryo"]),
                "is_etkisi": f"{s['etki']:,} etkilenen kayıt. {_IMPACTS.get(s['risk'], '')}",
                "risk":      s["risk"],
                "etki":      s["etki"],
                "kaynak":    "Senaryo Motoru",
                "kategori":  s.get("kategori", "Denetim Senaryosu"),
            })

    # ── Benford Bulgusu ──
    if benford.get("anormal"):
        findings.append({
            "id":        "BF-01",
            "baslik":    "[BF-01] Benford Yasası – Anormal Dağılım",
            "bulgu":     (f"Ki-kare istatistiği {benford.get('chi_sq', 0):.2f} "
                          f"(kritik değer: 15.51, α=0.05). {benford.get('toplam_n', 0):,} "
                          "tutar değeri Benford beklentisinden istatistiksel olarak anlamlı biçimde sapıyor."),
            "kok_neden": _ROOT_CAUSES["Benford"],
            "is_etkisi": f"Tüm veri setinin güvenilirliğini etkileyen sistemik bir sapma söz konusu olabilir. {_IMPACTS['Yüksek']}",
            "risk":      "Yüksek",
            "etki":      benford.get("toplam_n", 0),
            "kaynak":    "Benford Analizi",
            "kategori":  "Sahte İşlem Riski",
        })

    # ── Pareto Bulgusu ──
    if "vendor" in pareto:
        p = pareto["vendor"]
        if p["vendors_80"] <= max(3, int(len(pareto["vendor"]["data"]) * 0.1)):
            findings.append({
                "id":        "PA-01",
                "baslik":    "[PA-01] Aşırı Tedarikçi Yoğunlaşması (Pareto)",
                "bulgu":     (f"Toplam tutarın %80'i yalnızca {p['vendors_80']} tedarikçiden "
                              f"oluşuyor (toplam tedarikçi sayısı: {len(p['data'])}). "
                              f"En büyük tedarikçi payı: %{p['top_pct']:.1f}."),
                "kok_neden": _ROOT_CAUSES["Pareto"],
                "is_etkisi": f"Tedarikçi bağımlılığı ve rekabetçi fiyatlandırma riski. {_IMPACTS['Yüksek']}",
                "risk":      "Yüksek" if p["top_pct"] > 40 else "Orta",
                "etki":      p["vendors_80"],
                "kaynak":    "Pareto Analizi",
                "kategori":  "Yoğunlaşma Riski",
            })

    # ── Kritik Risk Yoğunluğu ──
    if "risk_seviyesi" in df.columns:
        crit_pct = (df["risk_seviyesi"] == "Kritik").mean() * 100
        if crit_pct > 5:
            findings.append({
                "id":        "RS-01",
                "baslik":    "[RS-01] Kritik Risk Yoğunluğu",
                "bulgu":     (f"Kayıtların %{crit_pct:.1f}'i (n={int((df['risk_seviyesi']=='Kritik').sum()):,}) "
                              "kritik risk skoruna sahip. Bu oran kabul edilebilir %5 eşiğinin üzerindedir."),
                "kok_neden": "Kontrol ortamında sistemik zafiyetler veya yüksek riskli işlem profilinin varlığı.",
                "is_etkisi": f"{int((df['risk_seviyesi']=='Kritik').sum()):,} kayıt. {_IMPACTS['Kritik']}",
                "risk":      "Kritik",
                "etki":      int((df["risk_seviyesi"] == "Kritik").sum()),
                "kaynak":    "Risk Skorlama",
                "kategori":  "Risk Profili",
            })

    findings.sort(key=lambda x: (prio.get(x["risk"], 4), -x["etki"]))
    return findings


# ══════════════════════════════════════════════════════════════════════════════
# M10 – AKSİYON PLANI ÜRETİCİ
# ══════════════════════════════════════════════════════════════════════════════

_ACTION_DB: dict[str, dict] = {
    "Mükerrer": {
        "aksiyon":    "ERP sisteminde belge numarası için benzersiz kısıtlama (UNIQUE INDEX) aktivasyonu; yükleme öncesi çift kayıt kontrol kuralı tanımlanması; mevcut mükerrer kayıtların incelenerek kapatılması.",
        "birim":      "Bilgi Teknolojileri / Finans Muhasebe",
        "sure":       "30 gün",
        "zorluk":     "Orta",
        "standart":   "COSO 2013 – Kontrol Faaliyetleri",
    },
    "Negatif": {
        "aksiyon":    "Negatif tutar giriş politikasının gözden geçirilmesi; ERP kural motoru ile negatif değer onay sürecinin tasarlanması; mevcut negatif kayıtların geçerliliğinin belge bazında doğrulanması.",
        "birim":      "Finans / İç Kontrol",
        "sure":       "14 gün",
        "zorluk":     "Düşük",
        "standart":   "COSO 2013 – Risk Değerlendirmesi",
    },
    "Aykırı": {
        "aksiyon":    "Tutar onay matrisi revizyonu (kategori ve birim bazlı eşik güncelleme); anomali tespiti için istatistiksel izleme aracı entegrasyonu; yüksek tutarlı işlemlerin ek belgeleme gereksinimine tabi tutulması.",
        "birim":      "Finans / İç Denetim / BT",
        "sure":       "45 gün",
        "zorluk":     "Yüksek",
        "standart":   "IIA Standart 2120 – Risk Yönetimi",
    },
    "Yuvarlama": {
        "aksiyon":    "Yuvarlak tutarlı işlemler için ek onay ve belge zorunluluğu getirilmesi; veri giriş kılavuzunun güncellenmesi; rastgele örnekleme ile yuvarlak tutar işlemlerinin belge bazında doğrulanması.",
        "birim":      "Finans / Operasyon / İç Kontrol",
        "sure":       "21 gün",
        "zorluk":     "Düşük",
        "standart":   "COSO 2013 – Kontrol Ortamı",
    },
    "Yoğunlaşma": {
        "aksiyon":    "Satınalma politikasına en az 3 teklif zorunluluğu eklenmesi; tedarikçi yoğunlaşma üst limiti (örn. tek tedarikçi max %30) belirlenmesi; mevcut yüksek yoğunlaşmalı tedarikçi sözleşmelerinin yeniden değerlendirilmesi.",
        "birim":      "Satınalma / Üst Yönetim / İç Kontrol",
        "sure":       "60 gün",
        "zorluk":     "Orta",
        "standart":   "ISO 31000 – Risk Azaltma",
    },
    "Mesai": {
        "aksiyon":    "ERP ve ilgili sistemlerde zaman bazlı erişim profili konfigürasyonu; mesai dışı girişlerde çok faktörlü kimlik doğrulama (MFA) zorunluluğu; tüm mesai dışı erişimlerin otomatik log ve uyarı sistemiyle izlenmesi.",
        "birim":      "Bilgi Teknolojileri / Bilgi Güvenliği",
        "sure":       "30 gün",
        "zorluk":     "Orta",
        "standart":   "ISO 27001 – Erişim Kontrolü",
    },
    "Eşik": {
        "aksiyon":    "Birikimli işlem tutarlarını izleyen kontrol mekanizması (rolling window) tasarımı; onay eşiklerinin sisteme entegre edilmesi; mevcut eşik ihlali şüpheli işlemlerin soruşturma kapsamına alınması.",
        "birim":      "Finans / Satınalma / İç Kontrol / BT",
        "sure":       "45 gün",
        "zorluk":     "Yüksek",
        "standart":   "COSO 2013 – Kontrol Faaliyetleri",
    },
    "SoD": {
        "aksiyon":    "Görevler ayrılığı matrisinin tam revizyonu; ERP'de oluşturma ve onay rollerinin teknik olarak ayrıştırılması (mutually exclusive roles); SoD ihlali yapan kullanıcı hesaplarının erişim profilinin güncellenmesi; altı aylık SoD gözden geçirme döngüsü kurulması.",
        "birim":      "BT / İnsan Kaynakları / İç Kontrol / İç Denetim",
        "sure":       "30 gün",
        "zorluk":     "Yüksek",
        "standart":   "COSO 2013 – Kontrol Faaliyetleri; IIA Standart 2130",
    },
    "Eksik": {
        "aksiyon":    "Kritik sütunlar için ERP'de zorunlu alan (mandatory field) konfigürasyonu; veri tamamlama prosedürü ve sorumlu kullanıcı atanması; eksik veriye sahip mevcut kayıtların gözden geçirilmesi.",
        "birim":      "BT / Finans / İlgili Birim Yöneticileri",
        "sure":       "21 gün",
        "zorluk":     "Düşük",
        "standart":   "COSO 2013 – Bilgi ve İletişim",
    },
    "Tarih": {
        "aksiyon":    "Sistem tarih kontrolünün güçlendirilmesi; geriye dönük belge kaydı için ikincil onay mekanizması ve belge zorunluluğu; önceki dönem kayıt girişlerinin periyodik olarak raporlanması ve denetim komitesine sunulması.",
        "birim":      "BT / Finans Muhasebe",
        "sure":       "21 gün",
        "zorluk":     "Orta",
        "standart":   "COSO 2013 – Kontrol Faaliyetleri",
    },
    "Tekrarlayan": {
        "aksiyon":    "Çift ödeme/kayıt tespit kural motoru entegrasyonu; aynı tutarın kısa sürede tekrarlanmasını engelleyen kontrol kuralı; mevcut tekrarlayan tutarlı işlemlerin belge bazında doğrulanması.",
        "birim":      "BT / Finans / Operasyon",
        "sure":       "30 gün",
        "zorluk":     "Orta",
        "standart":   "COSO 2013 – Kontrol Faaliyetleri",
    },
    "Olağandışı": {
        "aksiyon":    "Gerçek zamanlı işlem izleme ve anomali uyarı sistemi kurulumu; günlük işlem limiti tanımlanması; yoğun işlem günleri için otomatik denetim tetikleyicisi oluşturulması.",
        "birim":      "Finans / İç Denetim / BT",
        "sure":       "45 gün",
        "zorluk":     "Orta",
        "standart":   "IIA Standart 2120 – Risk Yönetimi",
    },
    "Benford": {
        "aksiyon":    "Tüm finansal verinin periyodik Benford testi programına alınması; anlamlı sapma gösteren işlem gruplarının kapsamlı soruşturma kapsamına alınması; sürekli denetim (continuous auditing) çerçevesine Benford kontrolünün eklenmesi.",
        "birim":      "İç Denetim / Finans",
        "sure":       "30 gün",
        "zorluk":     "Orta",
        "standart":   "IIA GTAG 16 – Sürekli Denetim",
    },
    "Pareto": {
        "aksiyon":    "Tedarikçi yoğunlaşma limitinin politika belgesiyle resmileştirilmesi; mevcut yüksek paylı tedarikçilerle sözleşme yenileme süreçlerinde rekabetçi ihale uygulanması; alternatif tedarikçi geliştirme programı başlatılması.",
        "birim":      "Satınalma / Üst Yönetim",
        "sure":       "90 gün",
        "zorluk":     "Yüksek",
        "standart":   "ISO 31000 – Risk Azaltma",
    },
    "Kullanıcı": {
        "aksiyon":    "Yüksek işlem hacimli kullanıcıların yetki profillerinin gözden geçirilmesi; kullanıcı bazlı tutar limiti tanımlanması; ayrıcalık birikimini (privilege accumulation) önlemek için periyodik erişim gözden geçirme döngüsü kurulması.",
        "birim":      "BT / İnsan Kaynakları / İç Kontrol",
        "sure":       "30 gün",
        "zorluk":     "Orta",
        "standart":   "ISO 27001 – Kimlik ve Erişim Yönetimi",
    },
    "Hafta Sonu": {
        "aksiyon":    "Hafta sonu/tatil günü sistem erişimlerinde MFA ve yönetici onayı zorunluluğu; hafta sonu işlemlerinin otomatik olarak ertesi iş günü denetim raporuna yansıtılması.",
        "birim":      "BT / Bilgi Güvenliği",
        "sure":       "21 gün",
        "zorluk":     "Düşük",
        "standart":   "ISO 27001 – Erişim Kontrolü",
    },
}

PRIO_LABEL  = {"Kritik":"P1 – Acil","Yüksek":"P2 – Yüksek","Orta":"P3 – Orta","Düşük":"P4 – Düşük"}
PRIO_CLASS  = {"P1 – Acil":"p1","P2 – Yüksek":"p2","P3 – Orta":"p3","P4 – Düşük":"p4"}


def generate_action_plans(findings: list) -> list[dict]:
    """
    Her önemli bulgu için somut, standart referanslı aksiyon planı üretir.
    """
    plans: list[dict] = []
    for f in findings:
        if f["risk"] not in ("Kritik", "Yüksek", "Orta"):
            continue
        # Aksiyon veritabanında eşleşme ara
        action = None
        for kw, val in _ACTION_DB.items():
            if kw.lower() in f["baslik"].lower() or kw.lower() in f["bulgu"].lower():
                action = val
                break
        if action is None:
            action = {
                "aksiyon":  "İlgili sürecin kapsamlı incelenmesi; kontrol açığını kapatan prosedür ve politika belgesi oluşturulması; uygulama etkinliğinin periyodik olarak değerlendirilmesi.",
                "birim":    "İç Kontrol / İlgili Süreç Sahibi / Yönetim",
                "sure":     "45 gün",
                "zorluk":   "Orta",
                "standart": "COSO 2013 – Kontrol Ortamı",
            }
        plans.append({
            "bulgu_id":  f["id"],
            "bulgu":     f["baslik"],
            "aksiyon":   action["aksiyon"],
            "birim":     action["birim"],
            "sure":      action["sure"],
            "oncelik":   PRIO_LABEL.get(f["risk"], "P3 – Orta"),
            "zorluk":    action["zorluk"],
            "standart":  action["standart"],
            "risk":      f["risk"],
        })
    return plans

# ══════════════════════════════════════════════════════════════════════════════
# M11 – GÖRSELLEŞTİRME MOTORU
# ══════════════════════════════════════════════════════════════════════════════

def _base_fig(**kwargs) -> go.Figure:
    """PLOT_LAYOUT temasını uygulayan temel figure üreticisi."""
    fig = go.Figure(**kwargs)
    fig.update_layout(**PLOT_LAYOUT)
    return fig


def fig_risk_distribution(df: pd.DataFrame) -> go.Figure:
    counts = df["risk_seviyesi"].value_counts().reindex(
        ["Kritik","Yüksek","Orta","Düşük"], fill_value=0
    )
    colors = [COLOR_RISK.get(r, "#4f9cf9") for r in counts.index]
    fig = _base_fig()
    fig.add_trace(go.Bar(
        x=counts.index,
        y=counts.values,
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v:,}" for v in counts.values],
        textposition="outside",
        textfont=dict(color="#dce8f5", size=13, family="JetBrains Mono"),
        hovertemplate="<b>%{x}</b><br>Kayıt: %{y:,}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Risk Seviyesi Dağılımı", font_size=14, font_color="#dce8f5"),
        height=300,
        xaxis_title="", yaxis_title="Kayıt Sayısı",
        showlegend=False,
    )
    return fig


def fig_risk_histogram(df: pd.DataFrame) -> go.Figure:
    fig = _base_fig()
    fig.add_trace(go.Histogram(
        x=df["risk_skoru"],
        nbinsx=25,
        marker=dict(
            color=df["risk_skoru"],
            colorscale=[[0,"#059669"],[0.33,"#2563eb"],[0.66,"#d97706"],[1,"#e03e3e"]],
            showscale=True,
            colorbar=dict(
                title=dict(text="Risk", font=dict(size=11)),   # ← changed
                tickvals=[0,25,50,75,100],
                ticktext=["0","25","50","75","100"],
                thickness=12, len=0.8,
                tickfont=dict(size=10),                        # ← changed
            ),
        ),
        hovertemplate="Skor: %{x:.0f}<br>Kayıt: %{y:,}<extra></extra>",
    ))
    fig.add_vline(x=25, line_dash="dash", line_color="#2563eb",   annotation_text="Orta", annotation_font_size=10)
    fig.add_vline(x=50, line_dash="dash", line_color="#d97706",   annotation_text="Yüksek", annotation_font_size=10)
    fig.add_vline(x=75, line_dash="dash", line_color="#e03e3e",   annotation_text="Kritik", annotation_font_size=10)
    fig.update_layout(
        title=dict(text="Risk Skoru Dağılımı (0–100)", font_size=14, font_color="#dce8f5"),
        height=300,
        xaxis_title="Risk Skoru",
        yaxis_title="Kayıt Sayısı",
        showlegend=False,
    )
    return fig


def fig_time_trend(df: pd.DataFrame, col_map: dict) -> go.Figure:
    df2 = _parse_dates_safe(df.copy(), col_map["date"])
    df2["_m"] = df2[col_map["date"]].dt.to_period("M").astype(str)
    m = df2.groupby("_m").agg(
        Sayı    =("risk_skoru", "count"),
        OrtRisk =("risk_skoru", "mean"),
        KritikN =("risk_seviyesi", lambda x: (x == "Kritik").sum()),
    ).reset_index()

    fig = make_subplots(
        specs=[[{"secondary_y": True}]],
        subplot_titles=["Aylık İşlem & Risk Trendi"],
    )
    fig.add_trace(go.Bar(
        x=m["_m"], y=m["Sayı"],
        name="İşlem Sayısı",
        marker_color="rgba(79,156,249,0.35)",
        marker_line_color="rgba(79,156,249,0.7)",
        marker_line_width=1,
        hovertemplate="%{x}<br>İşlem: %{y:,}<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=m["_m"], y=m["OrtRisk"],
        name="Ort. Risk Skoru",
        mode="lines+markers",
        line=dict(color="#e03e3e", width=2.5),
        marker=dict(size=7, symbol="circle", color="#e03e3e",
                    line=dict(color="#0c1524", width=1.5)),
        hovertemplate="%{x}<br>Ort. Risk: %{y:.1f}<extra></extra>",
    ), secondary_y=True)
    fig.add_trace(go.Scatter(
        x=m["_m"], y=m["KritikN"],
        name="Kritik Kayıt",
        mode="lines+markers",
        line=dict(color="#f59e0b", width=1.5, dash="dot"),
        marker=dict(size=5),
        hovertemplate="%{x}<br>Kritik: %{y:,}<extra></extra>",
    ), secondary_y=True)
    layout = {**PLOT_LAYOUT}
    layout.pop("xaxis", None); layout.pop("yaxis", None)
    fig.update_layout(**layout, height=340,
                      legend=dict(orientation="h", y=1.1, x=0),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(17,30,48,0.5)")
    fig.update_yaxes(title_text="İşlem Sayısı",  secondary_y=False,
                     gridcolor="#1c2e44", zerolinecolor="#1c2e44")
    fig.update_yaxes(title_text="Risk Skoru / Kritik Adet", secondary_y=True,
                     gridcolor="#1c2e44", zerolinecolor="#1c2e44")
    return fig


def fig_vendor_concentration(df: pd.DataFrame, col_map: dict) -> go.Figure:
    amt = _to_numeric_safe(df, col_map["amount"]).fillna(0)
    vc  = df.assign(_a=amt).groupby(col_map["vendor"])["_a"].sum().nlargest(12)
    max_v = vc.max() + 1e-9

    colors = [
        f"rgba({int(224 + (79-224)*v/max_v)},{int(62 + (156-62)*v/max_v)},{int(62 + (249-62)*v/max_v)},0.8)"
        for v in vc.values
    ]
    colors_bar = [COLOR_RISK["Kritik"] if v > max_v*0.4 else
                  (COLOR_RISK["Yüksek"] if v > max_v*0.2 else
                   (COLOR_RISK["Orta"] if v > max_v*0.1 else COLOR_RISK["Düşük"]))
                  for v in vc.values]

    fig = _base_fig()
    fig.add_trace(go.Bar(
        y=vc.index.astype(str),
        x=vc.values,
        orientation="h",
        marker_color=colors_bar,
        marker_line_width=0,
        text=[f"  {v:,.0f}" for v in vc.values],
        textposition="outside",
        textfont=dict(color="#8aa4be", size=10, family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>Toplam: %{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Karşı Taraf Yoğunlaşması – Top 12", font_size=14, font_color="#dce8f5"),
        height=400,
        yaxis=dict(autorange="reversed", gridcolor="#1c2e44", zerolinecolor="#1c2e44"),
        xaxis=dict(gridcolor="#1c2e44", zerolinecolor="#1c2e44"),
        showlegend=False,
    )
    return fig


def fig_risk_heatmap(df: pd.DataFrame, col_map: dict) -> go.Figure:
    cat_col = col_map.get("category") or col_map.get("department") or col_map.get("vendor")
    if not cat_col:
        return None
    top  = df[cat_col].value_counts().nlargest(10).index
    sub  = df[df[cat_col].isin(top)]
    heat = sub.groupby([cat_col, "risk_seviyesi"]).size().unstack(fill_value=0)
    heat = heat.reindex(columns=["Kritik","Yüksek","Orta","Düşük"], fill_value=0)

    fig = _base_fig()
    fig.add_trace(go.Heatmap(
        z=heat.values,
        x=heat.columns,
        y=heat.index.astype(str),
        colorscale=[
            [0.0,  "#0c1524"],
            [0.15, "#162438"],
            [0.4,  "#1a4a8a"],
            [0.7,  "#b45309"],
            [1.0,  "#991b1b"],
        ],
        text=heat.values,
        texttemplate="%{text}",
        textfont=dict(size=12, color="white", family="JetBrains Mono"),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z}<extra></extra>",
        showscale=True,
        colorbar=dict(thickness=12, len=0.8, tickfont_size=10),
    ))
    fig.update_layout(
        title=dict(text="Risk Isı Haritası (Kategori × Risk Seviyesi)", font_size=14, font_color="#dce8f5"),
        height=400,
    )
    return fig


def fig_pareto_chart(pareto: dict, entity: str = "vendor") -> go.Figure:
    if entity not in pareto:
        return None
    p  = pareto[entity]
    va = p["data"].head(20)
    cu = p["cumulative"].loc[va.index]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=va.index.astype(str), y=va.values,
        name="Tutar",
        marker_color=[
            "#e03e3e" if v > va.max()*0.4 else
            "#d97706" if v > va.max()*0.2 else
            "#2563eb" for v in va.values
        ],
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Tutar: %{y:,.0f}<extra></extra>",
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=va.index.astype(str), y=cu.values,
        name="Kümülatif %",
        mode="lines+markers",
        line=dict(color="#22d3ee", width=2),
        marker=dict(size=6),
        hovertemplate="%{x}<br>Kümülatif: %{y:.1f}%<extra></extra>",
    ), secondary_y=True)
    fig.add_hline(y=80, line_dash="dash", line_color="#fbbf24", secondary_y=True,
                  annotation_text="%80 Eşiği", annotation_font_size=10)

    layout = {**PLOT_LAYOUT}
    layout.pop("xaxis", None); layout.pop("yaxis", None)
    fig.update_layout(**layout, height=340,
                      title=dict(text="Pareto Analizi (80/20 Kuralı)", font_size=14, font_color="#dce8f5"),
                      legend=dict(orientation="h", y=1.05),
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(17,30,48,0.5)")
    fig.update_yaxes(title_text="Tutar", secondary_y=False,
                     gridcolor="#1c2e44", zerolinecolor="#1c2e44")
    fig.update_yaxes(title_text="Kümülatif %", range=[0,105], secondary_y=True,
                     gridcolor="#1c2e44", zerolinecolor="#1c2e44")
    fig.update_xaxes(tickangle=-35, gridcolor="#1c2e44")
    return fig


def fig_benford_chart(benford: dict) -> go.Figure:
    if not benford or "chi_sq" not in benford:
        return None
    digits   = list(range(1, 10))
    observed = [benford[d]["gozlemlenen"] for d in digits]
    expected = [benford[d]["beklenen"]    for d in digits]
    deviations = [benford[d]["sapma"]    for d in digits]

    bar_colors = [
        "#e03e3e" if abs(d) > 5 else ("#d97706" if abs(d) > 2 else "#059669")
        for d in deviations
    ]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Gözlemlenen vs Beklenen (%)", "Sapma (Gözlemlenen − Beklenen)"],
        column_widths=[0.6, 0.4],
    )
    # Sol: karşılaştırma
    fig.add_trace(go.Bar(
        x=[str(d) for d in digits], y=observed, name="Gözlemlenen",
        marker_color="rgba(79,156,249,0.7)", marker_line_width=0,
        hovertemplate="Rakam %{x}<br>Gözlemlenen: %{y:.1f}%<extra></extra>",
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=[str(d) for d in digits], y=expected, name="Benford Beklentisi",
        mode="lines+markers",
        line=dict(color="#fbbf24", width=2, dash="dot"),
        marker=dict(size=7, color="#fbbf24"),
        hovertemplate="Rakam %{x}<br>Beklenen: %{y:.1f}%<extra></extra>",
    ), row=1, col=1)
    # Sağ: sapma
    fig.add_trace(go.Bar(
        x=[str(d) for d in digits], y=deviations, name="Sapma",
        marker_color=bar_colors, marker_line_width=0,
        hovertemplate="Rakam %{x}<br>Sapma: %{y:+.1f}%<extra></extra>",
        showlegend=False,
    ), row=1, col=2)
    fig.add_hline(y=0, line_color="#1c2e44", row=1, col=2)

    layout = {**PLOT_LAYOUT}
    layout.pop("xaxis", None); layout.pop("yaxis", None)
    chi_sq = benford.get("chi_sq", 0)
    status = "⚠️ ANORMAl" if chi_sq > 15.51 else "✅ NORMAL"
    fig.update_layout(
        **layout, height=320,
        title=dict(text=f"Benford Yasası Analizi  ·  χ²={chi_sq:.2f}  {status}",
                   font_size=14, font_color="#dce8f5"),
        legend=dict(orientation="h", y=1.08),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,30,48,0.5)",
    )
    for ax in ["xaxis","yaxis","xaxis2","yaxis2"]:
        fig.update_layout(**{ax: dict(gridcolor="#1c2e44", zerolinecolor="#1c2e44")})
    return fig


def fig_scatter_risk(df: pd.DataFrame, col_map: dict) -> go.Figure:
    """Tutar vs Risk Skoru scatter plot – Kritik noktaları büyük işaret."""
    if "amount" not in col_map:
        return None
    amt   = _to_numeric_safe(df, col_map["amount"]).fillna(0)
    color_map = {"Kritik":"#e03e3e","Yüksek":"#d97706","Orta":"#2563eb","Düşük":"#059669"}

    fig = _base_fig()
    for level in ["Düşük","Orta","Yüksek","Kritik"]:
        mask = df["risk_seviyesi"] == level
        fig.add_trace(go.Scatter(
            x=amt[mask].values,
            y=df.loc[mask, "risk_skoru"].values,
            mode="markers",
            name=level,
            marker=dict(
                color=color_map[level],
                size=8 if level == "Kritik" else 5,
                opacity=0.8 if level in ("Kritik","Yüksek") else 0.5,
                symbol="diamond" if level == "Kritik" else "circle",
                line=dict(color="#0c1524", width=0.5),
            ),
            hovertemplate="Tutar: %{x:,.0f}<br>Risk: %{y:.1f}<extra>" + level + "</extra>",
        ))
    fig.update_layout(
        title=dict(text="Tutar vs Risk Skoru Dağılımı", font_size=14, font_color="#dce8f5"),
        height=340,
        xaxis_title="Tutar",
        yaxis_title="Risk Skoru",
        legend=dict(orientation="h", y=1.08),
    )
    return fig


def fig_user_risk(df: pd.DataFrame, col_map: dict) -> go.Figure:
    """Kullanıcı bazlı risk profil grafiği."""
    if "user" not in col_map:
        return None
    ug = df.groupby(col_map["user"]).agg(
        OrtRisk  =("risk_skoru",    "mean"),
        MaxRisk  =("risk_skoru",    "max"),
        Islem    =("risk_skoru",    "count"),
        KritikN  =("risk_seviyesi", lambda x: (x=="Kritik").sum()),
    ).nlargest(12, "MaxRisk")

    fig = _base_fig()
    fig.add_trace(go.Bar(
        x=ug.index.astype(str), y=ug["OrtRisk"],
        name="Ort. Risk",
        marker_color=[
            "#e03e3e" if v >= 75 else "#d97706" if v >= 50 else "#2563eb" if v >= 25 else "#059669"
            for v in ug["OrtRisk"]
        ],
        hovertemplate="<b>%{x}</b><br>Ort. Risk: %{y:.1f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=ug.index.astype(str), y=ug["MaxRisk"],
        name="Max Risk",
        mode="markers",
        marker=dict(symbol="diamond", size=10, color="#fbbf24"),
        hovertemplate="<b>%{x}</b><br>Max Risk: %{y:.1f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Kullanıcı Risk Profili (Top 12)", font_size=14, font_color="#dce8f5"),
        height=320,
        xaxis_tickangle=-30,
        legend=dict(orientation="h", y=1.08),
    )
    return fig


def fig_weekday_heatmap(df: pd.DataFrame, col_map: dict) -> go.Figure:
    """Haftanın günü × saat risk yoğunluk haritası."""
    if "date" not in col_map:
        return None
    df2 = _parse_dates_safe(df.copy(), col_map["date"])
    try:
        df2["_dow"] = df2[col_map["date"]].dt.dayofweek
        df2["_h"]   = df2[col_map["date"]].dt.hour
        pivot = df2.groupby(["_dow","_h"])["risk_skoru"].mean().unstack(fill_value=0)

        day_names = ["Pzt","Sal","Çar","Per","Cum","Cmt","Paz"]
        y_labels  = [day_names[i] for i in pivot.index]

        fig = _base_fig()
        fig.add_trace(go.Heatmap(
            z=pivot.values,
            x=[f"{h:02d}:00" for h in pivot.columns],
            y=y_labels,
            colorscale=[[0,"#0c1524"],[0.3,"#162438"],[0.6,"#b45309"],[1,"#991b1b"]],
            hovertemplate="<b>%{y}  %{x}</b><br>Ort. Risk: %{z:.1f}<extra></extra>",
            showscale=True,
            colorbar=dict(thickness=10, len=0.8, tickfont_size=10),
        ))
        fig.update_layout(
            title=dict(text="Zaman Bazlı Risk Yoğunluk Haritası", font_size=14, font_color="#dce8f5"),
            height=320,
            xaxis_title="Saat", yaxis_title="",
        )
        return fig
    except Exception:
        return None


# ══════════════════════════════════════════════════════════════════════════════
# M12 – YÖNETİCİ ÖZETİ  (IIA IPPF Uyumlu – %100 Streamlit Native)
# ══════════════════════════════════════════════════════════════════════════════

def render_executive_summary(df: pd.DataFrame, col_map: dict,
                              findings: list, scenarios: list,
                              quality: list, action_plans: list) -> None:
    """
    Kurumsal, IIA uyumlu Yönetici Özeti.
    Tüm içerik Streamlit native bileşenlerle render edilir – HTML div sorunu yok.
    """
    total   = len(df)
    crit_n  = int((df["risk_seviyesi"] == "Kritik").sum())
    high_n  = int((df["risk_seviyesi"] == "Yüksek").sum())
    med_n   = int((df["risk_seviyesi"] == "Orta").sum())
    low_n   = int((df["risk_seviyesi"] == "Düşük").sum())
    avg_s   = float(df["risk_skoru"].mean())
    max_s   = float(df["risk_skoru"].max())

    # ── Genel risk seviyesi ──
    if avg_s >= 60 or crit_n / (total or 1) > .15:
        genel_risk, risk_color, risk_css = "KRİTİK", "#e03e3e", "critical"
        verdict = (
            "Analiz sonuçları, incelenen veri setinde iç kontrol ortamının kritik düzeyde zayıfladığını "
            "ortaya koymaktadır. Birden fazla sistemik kontrol zafiyeti tespit edilmiş olup yönetim "
            "kurulunun acil bilgilendirilmesi ve öncelikli kapatma aksiyonu başlatılması önerilmektedir."
        )
    elif avg_s >= 40 or (crit_n + high_n) / (total or 1) > .25:
        genel_risk, risk_color, risk_css = "YÜKSEK", "#d97706", "high"
        verdict = (
            "Veri analizi, önemli kontrol zafiyetleri ve yüksek riskli işlem örüntüleri tespit etmiştir. "
            "Mevcut bulgular, öncelikli aksiyon planlaması ve yakın dönem denetim takibi gerektirmektedir. "
            "Yönetim kuruluna raporlanması önerilmektedir."
        )
    elif avg_s >= 25:
        genel_risk, risk_color, risk_css = "ORTA", "#2563eb", "medium"
        verdict = (
            "Belirli süreç alanlarında kontrol iyileştirme ihtiyacı bulunmaktadır. Bulgular genel itibarıyla "
            "yönetilebilir düzeyde olmakla birlikte, tanımlanan aksiyon planlarının zamanında uygulanması "
            "ve izleme döneminde periyodik gözden geçirme yapılması önerilmektedir."
        )
    else:
        genel_risk, risk_color, risk_css = "DÜŞÜK", "#059669", "low"
        verdict = (
            "Analiz edilen veri seti, makul düzeyde kontrol bütünlüğü sergilemektedir. Tespit edilen düşük "
            "riskli bulgular izleme kapsamına alınmalı; sürekli denetim (continuous auditing) mekanizmaları "
            "aracılığıyla düzenli izleme sürdürülmelidir."
        )

    kritik_b = [f for f in findings if f["risk"] == "Kritik"][:4]
    yuksek_b = [f for f in findings if f["risk"] == "Yüksek"][:4]
    p1_plans = [p for p in action_plans if "P1" in p["oncelik"]]

    # Öncelik alanları
    sc_text = " ".join(s["senaryo"].lower() for s in scenarios)
    q_text  = " ".join(q["kontrol"].lower() for q in quality)
    combined = sc_text + " " + q_text
    focus_areas = []
    if "eşik" in combined or "structuring" in combined:
        focus_areas.append("Tutar onay limitleri ve eşik yönetim politikasının kapsamlı revizyonu")
    if "yoğunlaşma" in combined or "concentration" in combined:
        focus_areas.append("Tedarikçi çeşitlendirme ve yoğunlaşma riski yönetimi")
    if "sod" in combined or "görevler" in combined:
        focus_areas.append("Görevler ayrılığı matrisinin tam revizyonu ve RBAC politika güncellemesi")
    if "mesai" in combined or "hafta" in combined:
        focus_areas.append("Erişim kontrolü güçlendirmesi ve zaman bazlı kısıtlama konfigürasyonu")
    if "benford" in combined:
        focus_areas.append("Finansal veri bütünlüğü soruşturması ve sürekli Benford izlemesi")
    if "mükerrer" in combined:
        focus_areas.append("Sistem düzeyinde mükerrer kayıt kontrol mekanizması kurulumu")
    if not focus_areas:
        focus_areas = [
            "Veri kalite yönetim süreçlerinin güçlendirilmesi",
            "Anomali tespiti ve sürekli izleme kapasitesinin artırılması",
        ]

    sonraki_adimlar = [
        f"Kritik ve yüksek öncelikli {len(p1_plans)} aksiyon için 30 gün içinde kapatma planı hazırlanması",
        "Denetim Komitesi'ne kısa, orta ve uzun vadeli kapatma takvimi sunulması",
        "Tespit edilen yüksek riskli süreçler için kontrol tasarım etkinlik testi yapılması",
        "Sürekli denetim (continuous auditing) ve anomali izleme altyapısının kurulması",
        "Risk bazlı iç denetim planının güncellenmesi ve yıllık denetim programına yansıtılması",
    ]

    # ═════════════════════════════════════════════════════
    # RENDER
    # ═════════════════════════════════════════════════════

    # ── Üst Bölüm: Başlık & Risk Göstergesi ──────────────────────────────
    st.markdown(f"""
    <div class="exec-wrap">
      <div class="exec-top">
        <div class="exec-title-block">
          <div class="exec-overline">İÇ DENETİM YÖNETİCİ ÖZETİ  ·  IIA IPPF UYUMLU</div>
          <h2 class="exec-title">Analitik Değerlendirme Raporu</h2>
          <div class="exec-meta">
            <span>📅 {datetime.now().strftime('%d %B %Y')}</span>
            <span>📊 {total:,} kayıt analiz edildi</span>
            <span>📈 Ort. Risk: {avg_s:.1f} / 100</span>
            <span>🔺 Maks. Risk: {max_s:.1f} / 100</span>
          </div>
        </div>
        <div class="exec-risk-box">
          <div class="exec-risk-label">GENEL RİSK</div>
          <div class="exec-risk-value" style="color:{risk_color};">{genel_risk}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Satırı ──────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Toplam Kayıt",  f"{total:,}")
    c2.metric("Kritik",        f"{crit_n:,}",  delta=None)
    c3.metric("Yüksek",        f"{high_n:,}")
    c4.metric("Orta",          f"{med_n:,}")
    c5.metric("Düşük",         f"{low_n:,}")
    c6.metric("Ort. Risk",     f"{avg_s:.1f}")

    st.divider()

    # ── Bölüm 1: Genel Değerlendirme ────────────────────────────────────────
    st.markdown("#### 1 · Genel Risk Değerlendirmesi")
    st.info(
        f"**Genel Risk Seviyesi: {genel_risk}**\n\n"
        f"{verdict}\n\n"
        f"Analiz kapsamındaki **{total:,}** kayıt incelenmiş; **{crit_n:,}** kritik, "
        f"**{high_n:,}** yüksek, **{med_n:,}** orta ve **{low_n:,}** düşük riskli kayıt "
        f"tespit edilmiştir. Ağırlıklı ortalama risk skoru **{avg_s:.1f}/100**, "
        f"maksimum risk skoru **{max_s:.1f}/100** olarak hesaplanmıştır."
    )

    # ── Bölüm 2: Kritik Kontrol Zafiyetleri ──────────────────────────────────
    st.markdown("#### 2 · Kritik Kontrol Zafiyetleri")
    if kritik_b:
        for b in kritik_b:
            st.error(
                f"**{b['baslik']}**\n\n"
                f"📌 **Bulgu:** {b['bulgu']}\n\n"
                f"🔍 **Kök Neden:** {b['kok_neden']}\n\n"
                f"💼 **İş Etkisi:** {b['is_etkisi']}"
            )
    else:
        st.success("✅ Kritik seviyede kontrol zafiyeti tespit edilmemiştir.")

    # ── Bölüm 3: Yüksek Öncelikli Bulgular ───────────────────────────────────
    st.markdown("#### 3 · Yüksek Öncelikli Denetim Bulguları")
    if yuksek_b:
        for b in yuksek_b:
            st.warning(
                f"**{b['baslik']}**\n\n"
                f"📌 **Bulgu:** {b['bulgu']}\n\n"
                f"💼 **İş Etkisi:** {b['is_etkisi']}"
            )
    else:
        st.success("✅ Yüksek riskli bulgu sayısı yönetilebilir düzeydedir.")

    # ── Bölüm 4: Öncelikli Aksiyon Alanları ─────────────────────────────────
    st.markdown("#### 4 · Öncelikli Aksiyon Alanları")
    for i, area in enumerate(focus_areas, 1):
        st.markdown(f"**{i}.** {area}")

    if p1_plans:
        st.markdown("**Acil (P1) Aksiyonlar:**")
        for p in p1_plans[:5]:
            st.markdown(
                f"- **{p['bulgu_id']}** – {p['aksiyon'][:120]}…  "
                f"*Sorumlu: {p['birim']}  ·  Süre: {p['sure']}*"
            )

    # ── Bölüm 5: Sonraki Dönem Odak Alanları ─────────────────────────────────
    st.markdown("#### 5 · Sonraki Dönem Denetim Odak Alanları")
    for i, item in enumerate(sonraki_adimlar, 1):
        st.markdown(f"**{i}.** {item}")

    # ── Bölüm 6: Özet İstatistik ─────────────────────────────────────────────
    st.markdown("#### 6 · Denetim Özet İstatistikleri")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-item"><div class="stat-label">Toplam Bulgu</div><div class="stat-value">{len(findings)}</div></div>
          <div class="stat-item"><div class="stat-label">Kritik Bulgu</div><div class="stat-value" style="color:#e03e3e">{len(kritik_b)}</div></div>
          <div class="stat-item"><div class="stat-label">Aksiyon Planı</div><div class="stat-value">{len(action_plans)}</div></div>
          <div class="stat-item"><div class="stat-label">P1 Aksiyon</div><div class="stat-value" style="color:#e03e3e">{len(p1_plans)}</div></div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-item"><div class="stat-label">Kalite Kontrolü</div><div class="stat-value">{len(quality)}</div></div>
          <div class="stat-item"><div class="stat-label">Senaryo Sayısı</div><div class="stat-value">{len(scenarios)}</div></div>
          <div class="stat-item"><div class="stat-label">Yüksek Risk %</div><div class="stat-value" style="color:#d97706">{(crit_n+high_n)/(total or 1)*100:.1f}%</div></div>
          <div class="stat-item"><div class="stat-label">Maks. Risk Skoru</div><div class="stat-value" style="color:#e03e3e">{max_s:.1f}</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption(
        "Bu rapor IIA Uluslararası İç Denetim Standartları (IPPF), COSO 2013 İç Kontrol Çerçevesi "
        "ve ISO 31000 Risk Yönetimi Standardı çerçevesinde otomatik veri analitiği yöntemleriyle üretilmiştir. "
        "Bulgular denetim kanıtı niteliğinde değil, ön değerlendirme ve risk göstergesi niteliğindedir. "
        "Son karar ve değerlendirme yetkisi sorumlu iç denetçiye aittir."
    )

    # ── İndirme ──────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    report_txt = _build_report_text(
        total, crit_n, high_n, med_n, low_n, avg_s, max_s,
        genel_risk, verdict, kritik_b, yuksek_b, focus_areas,
        sonraki_adimlar, findings, action_plans
    )
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(
            "📥 Yönetici Özeti (.txt)",
            data=report_txt,
            file_name=f"ic_denetim_yonetici_ozeti_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )
    with col_dl2:
        csv_findings = pd.DataFrame(findings)[["id","baslik","risk","etki","kaynak","kategori"]].to_csv(index=False)
        st.download_button(
            "📥 Bulgular Listesi (.csv)",
            data=csv_findings,
            file_name=f"bulgular_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )


def _build_report_text(total, crit_n, high_n, med_n, low_n, avg_s, max_s,
                       genel_risk, verdict, kritik_b, yuksek_b,
                       focus_areas, sonraki_adimlar, findings, plans) -> str:
    sep = "═" * 70
    thin = "─" * 70
    now  = datetime.now().strftime("%d %B %Y  %H:%M")
    lines = [
        sep,
        "  İÇ DENETİM ANALİTİK DEĞERLENDİRME RAPORU",
        "  IIA IPPF · COSO 2013 · ISO 31000 Uyumlu",
        sep,
        f"  Tarih                 : {now}",
        f"  Toplam Kayıt          : {total:,}",
        f"  Genel Risk Seviyesi   : {genel_risk}",
        f"  Ortalama Risk Skoru   : {avg_s:.1f} / 100",
        f"  Maksimum Risk Skoru   : {max_s:.1f} / 100",
        thin,
        f"  Kritik : {crit_n:,}   Yüksek : {high_n:,}   Orta : {med_n:,}   Düşük : {low_n:,}",
        sep, "",
        "1. GENEL RİSK DEĞERLENDİRMESİ", thin,
        verdict, "",
        "2. KRİTİK KONTROL ZAFİYETLERİ", thin,
    ]
    if kritik_b:
        for b in kritik_b:
            lines += [f"  [{b['id']}] {b['baslik']}", f"  Bulgu    : {b['bulgu']}",
                      f"  Kök Neden: {b['kok_neden']}", f"  Etki     : {b['is_etkisi']}", ""]
    else:
        lines.append("  Kritik seviyede bulgu tespit edilmemiştir.\n")

    lines += ["3. YÜKSEK ÖNCELİKLİ BULGULAR", thin]
    if yuksek_b:
        for b in yuksek_b:
            lines += [f"  [{b['id']}] {b['baslik']}", f"  Bulgu    : {b['bulgu']}",
                      f"  Etki     : {b['is_etkisi']}", ""]
    else:
        lines.append("  Yüksek riskli bulgu yönetilebilir düzeyde.\n")

    lines += ["4. ÖNCELİKLİ AKSİYON ALANLARI", thin]
    for i, a in enumerate(focus_areas, 1):
        lines.append(f"  {i}. {a}")
    lines.append("")

    lines += ["5. SONRAKI DÖNEM ODAK ALANLARI", thin]
    for i, a in enumerate(sonraki_adimlar, 1):
        lines.append(f"  {i}. {a}")
    lines.append("")

    lines += ["6. TÜM BULGULAR", thin]
    for f in findings:
        lines.append(f"  [{f['id']}] {f['baslik']}  |  Risk: {f['risk']}  |  Etki: {f['etki']:,}")
    lines.append("")

    lines += ["7. AKSİYON PLANI ÖZETİ", thin]
    for p in plans:
        lines.append(f"  {p['oncelik']}  [{p['bulgu_id']}]  {p['birim']}  ·  {p['sure']}")
    lines += ["", sep,
              "  NOT: Bu rapor otomatik veri analitiği yöntemleriyle üretilmiştir.",
              "  Son karar yetkisi sorumlu iç denetçiye aittir.",
              sep]
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# M13 – EXPORT & RAPORLAMA
# ══════════════════════════════════════════════════════════════════════════════

def build_export_excel(df: pd.DataFrame, findings: list,
                       action_plans: list, quality: list,
                       scenarios: list) -> bytes:
    """Kapsamlı Excel rapor dosyası oluştur."""
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        # Risk Verileri
        df.to_excel(writer, sheet_name="Risk_Verileri", index=False)
        # Bulgular
        pd.DataFrame(findings)[["id","baslik","risk","etki","kok_neden","is_etkisi","kaynak","kategori"]]\
          .to_excel(writer, sheet_name="Bulgular", index=False)
        # Aksiyon Planları
        pd.DataFrame(action_plans)\
          .to_excel(writer, sheet_name="Aksiyon_Planlari", index=False)
        # Kalite Kontrolleri
        pd.DataFrame(quality)[["id","kontrol","bulgu","etki","risk","kategori"]]\
          .to_excel(writer, sheet_name="Kalite_Kontrolleri", index=False)
        # Senaryo Sonuçları
        sc_rows = [{"id": s["id"], "senaryo": s["senaryo"], "aciklama": s["aciklama"],
                    "risk": s["risk"], "etki": s["etki"], "kategori": s.get("kategori","")}
                   for s in scenarios]
        pd.DataFrame(sc_rows).to_excel(writer, sheet_name="Senaryo_Sonuclari", index=False)
    return buf.getvalue()


def _docx_set_cell_bg(cell, hex_color: str):
    """Tablo hücresine arka plan rengi ekler (python-docx yardımcı)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def _docx_header_row(table, headers: list, bg: str = "1F3864", fg: str = "FFFFFF"):
    """Tabloya koyu başlık satırı ekler."""
    row = table.rows[0]
    for i, h in enumerate(headers):
        cell = row.cells[i]
        cell.text = h
        _docx_set_cell_bg(cell, bg)
        run = cell.paragraphs[0].runs[0]
        run.bold = True
        run.font.color.rgb = RGBColor.from_string(fg)
        run.font.size = Pt(9)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER


def build_word_report(
    dataset_name: str,
    findings: list,
    plans: list,
    genel_risk: str,
    verdict: str,
    focus_areas: list,
    tracking: dict | None = None,
) -> bytes:
    """
    Profesyonel iç denetim Word raporu (.docx) oluşturur.

    tracking: {bulgu_id_aksiyon_idx: {"durum": str, "gerceklesen": str}} sözlüğü
    """
    if not DOCX_AVAILABLE:
        raise ImportError("python-docx kurulu değil. 'pip install python-docx' komutunu çalıştırın.")

    doc = DocxDocument()

    # ── Sayfa yapısı ──────────────────────────────────────────────────────────
    section = doc.sections[0]
    section.page_width  = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin   = Cm(2.5)
    section.right_margin  = Cm(2.5)
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2)

    # ── Stilleri ayarla ───────────────────────────────────────────────────────
    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Arial"
    style_normal.font.size = Pt(10)

    # ── KAPAK SAYFASI ─────────────────────────────────────────────────────────
    doc.add_paragraph()
    doc.add_paragraph()

    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_p.add_run("İÇ DENETİM ANALİTİK DEĞERLENDİRME RAPORU")
    run.bold = True
    run.font.size = Pt(20)
    run.font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = sub_p.add_run("IIA IPPF · COSO 2013 · ISO 31000 Uyumlu")
    run2.italic = True
    run2.font.size = Pt(12)
    run2.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

    doc.add_paragraph()

    # Bilgi kutusu
    info_tbl = doc.add_table(rows=4, cols=2)
    info_tbl.style = "Table Grid"
    info_data = [
        ("Rapor Tarihi", datetime.now().strftime("%d %B %Y  %H:%M")),
        ("Analiz Edilen Veri Seti", dataset_name or "Yüklenen Dosya"),
        ("Genel Risk Seviyesi", genel_risk),
        ("Rapor Türü", "Otomatik Veri Analitiği Raporu"),
    ]
    for i, (label, value) in enumerate(info_data):
        c0 = info_tbl.cell(i, 0)
        c1 = info_tbl.cell(i, 1)
        c0.text = label
        c1.text = str(value)
        _docx_set_cell_bg(c0, "D6E4F0")
        r0 = c0.paragraphs[0].runs[0]
        r0.bold = True
        r0.font.size = Pt(10)
        c1.paragraphs[0].runs[0].font.size = Pt(10)

    doc.add_page_break()

    # ── YÖNETİCİ ÖZETİ ────────────────────────────────────────────────────────
    h1 = doc.add_heading("1. Yönetici Özeti", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)

    risk_p = doc.add_paragraph()
    r = risk_p.add_run(f"Genel Risk Seviyesi: {genel_risk}")
    r.bold = True
    r.font.size = Pt(11)

    doc.add_paragraph(verdict)

    if focus_areas:
        doc.add_paragraph("Öncelikli Aksiyon Alanları:", style="Normal").runs[0].bold = True
        for i, area in enumerate(focus_areas, 1):
            p = doc.add_paragraph(f"{i}. {area}")
            p.paragraph_format.left_indent = Cm(1)

    doc.add_paragraph()

    # ── BULGULAR TABLOSU ──────────────────────────────────────────────────────
    doc.add_heading("2. Denetim Bulguları", level=1).runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    doc.add_paragraph(f"Toplam {len(findings)} bulgu tespit edilmiştir.")

    if findings:
        f_cols = ["ID", "Başlık", "Risk Seviyesi", "Etkilenen Kayıt", "Kök Neden"]
        f_tbl  = doc.add_table(rows=len(findings) + 1, cols=5)
        f_tbl.style = "Table Grid"

        # Sütun genişlikleri
        col_widths = [Cm(2), Cm(5), Cm(2.5), Cm(2.5), Cm(5.5)]
        for row in f_tbl.rows:
            for j, w in enumerate(col_widths):
                row.cells[j].width = w

        _docx_header_row(f_tbl, f_cols)

        risk_colors = {
            "Kritik": "FFB3B3", "Yüksek": "FFE0B2",
            "Orta":   "C5D8F6", "Düşük":  "C8F5DC",
        }
        for i, f in enumerate(findings, 1):
            row = f_tbl.rows[i]
            vals = [
                f.get("id", ""),
                f.get("baslik", ""),
                f.get("risk", ""),
                f"{f.get('etki', 0):,}",
                f.get("kok_neden", "")[:200],
            ]
            bg = risk_colors.get(f.get("risk", ""), "FFFFFF")
            for j, val in enumerate(vals):
                cell = row.cells[j]
                cell.text = str(val)
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                if j == 2:  # Risk sütunu renklendir
                    _docx_set_cell_bg(cell, bg)

    doc.add_paragraph()
    doc.add_page_break()

    # ── AKSİYON PLANLARI TABLOSU ──────────────────────────────────────────────
    doc.add_heading("3. Aksiyon Planları", level=1).runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    doc.add_paragraph(f"Toplam {len(plans)} aksiyon planı oluşturulmuştur.")

    if plans:
        a_cols = ["İlgili Bulgu ID", "Önerilen Aksiyon", "Sorumlu Birim", "Süre", "Öncelik"]
        a_tbl  = doc.add_table(rows=len(plans) + 1, cols=5)
        a_tbl.style = "Table Grid"
        a_col_widths = [Cm(2.5), Cm(6), Cm(3), Cm(2), Cm(2)]
        for row in a_tbl.rows:
            for j, w in enumerate(a_col_widths):
                row.cells[j].width = w

        _docx_header_row(a_tbl, a_cols)

        for i, p in enumerate(plans, 1):
            row = a_tbl.rows[i]
            vals = [
                p.get("bulgu_id", ""),
                p.get("aksiyon", "")[:250],
                p.get("birim", ""),
                p.get("sure", ""),
                p.get("oncelik", ""),
            ]
            for j, val in enumerate(vals):
                cell = row.cells[j]
                cell.text = str(val)
                cell.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_paragraph()
    doc.add_page_break()

    # ── TAKİP DURUMU TABLOSU ──────────────────────────────────────────────────
    doc.add_heading("4. Aksiyon Takip Tablosu", level=1).runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    doc.add_paragraph(
        "Bu tablo, aksiyon planlarının uygulanma durumunu takip etmek amacıyla "
        "hazırlanmıştır. 'Durum' ve 'Gerçekleşen Kapanış Tarihi' sütunları, "
        "sorumlu birimler tarafından doldurulacaktır."
    )

    if plans:
        t_cols = ["Bulgu ID", "Aksiyon", "Sorumlu", "Planlanan Kapanış", "Durum", "Gerçekleşen Kapanış"]
        t_tbl  = doc.add_table(rows=len(plans) + 1, cols=6)
        t_tbl.style = "Table Grid"
        t_col_widths = [Cm(2), Cm(5), Cm(2.5), Cm(2.5), Cm(2.5), Cm(2.5)]
        for row in t_tbl.rows:
            for j, w in enumerate(t_col_widths):
                row.cells[j].width = w

        _docx_header_row(t_tbl, t_cols)

        for i, p in enumerate(plans, 1):
            trk_key = f"{p.get('bulgu_id','')}__{i-1}"
            trk = (tracking or {}).get(trk_key, {})
            row = t_tbl.rows[i]
            vals = [
                p.get("bulgu_id", ""),
                p.get("aksiyon", "")[:150],
                p.get("birim", ""),
                p.get("sure", ""),
                trk.get("durum", "Açık"),
                trk.get("gerceklesen", ""),
            ]
            for j, val in enumerate(vals):
                cell = row.cells[j]
                cell.text = str(val)
                cell.paragraphs[0].runs[0].font.size = Pt(9)
                # Durum sütunu renklendirme
                if j == 4:
                    durum_bg = {"Kapalı": "C8F5DC", "Devam Ediyor": "FFE0B2", "Açık": "FFB3B3"}.get(val, "FFFFFF")
                    _docx_set_cell_bg(cell, durum_bg)

    # ── İMZA SAYFASI ──────────────────────────────────────────────────────────
    doc.add_page_break()
    doc.add_heading("5. Onay ve İmza", level=1).runs[0].font.color.rgb = RGBColor(0x1F, 0x38, 0x64)
    doc.add_paragraph(
        "Bu rapor, otomatik veri analitiği yöntemleriyle üretilmiş olup sorumlu "
        "iç denetçi tarafından gözden geçirilmeli ve onaylanmalıdır."
    )
    doc.add_paragraph()

    sign_tbl = doc.add_table(rows=3, cols=3)
    sign_tbl.style = "Table Grid"
    sign_headers = ["Hazırlayan (İç Denetçi)", "Onaylayan (Denetim Müdürü)", "Kabul Eden (Yönetim)"]
    for j, h in enumerate(sign_headers):
        _docx_set_cell_bg(sign_tbl.cell(0, j), "1F3864")
        sign_tbl.cell(0, j).text = h
        r = sign_tbl.cell(0, j).paragraphs[0].runs[0]
        r.bold = True
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        r.font.size = Pt(9)

    for j in range(3):
        sign_tbl.cell(1, j).text = "Ad Soyad:\n\nİmza:"
        sign_tbl.cell(1, j).paragraphs[0].runs[0].font.size = Pt(9)
        sign_tbl.cell(2, j).text = f"Tarih: {datetime.now().strftime('%d/%m/%Y')}"
        sign_tbl.cell(2, j).paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_paragraph()
    footer_p = doc.add_paragraph(
        "Bu rapor IIA Uluslararası İç Denetim Standartları (IPPF), COSO 2013 ve ISO 31000 "
        "çerçevesinde otomatik analitik yöntemlerle üretilmiştir. Bulgular ön değerlendirme "
        "niteliğindedir; son karar yetkisi sorumlu iç denetçiye aittir."
    )
    footer_p.runs[0].italic = True
    footer_p.runs[0].font.size = Pt(8)
    footer_p.runs[0].font.color.rgb = RGBColor(0x80, 0x80, 0x80)

    # ── Buffer'a yaz ──────────────────────────────────────────────────────────
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# M16 – GRC (GOVERNANCE, RISK & COMPLIANCE) KONTROL MATRİSİ
# ══════════════════════════════════════════════════════════════════════════════
# İlandan: "GRC araçlarını yöneterek erişim kontrollerini sağlamak ve
#            mevzuat uyumunu sürekli izlemek"
# ─────────────────────────────────────────────────────────────────────────────

_GRC_CONTROLS = [
    # id, alan, kontrol, standart, test_fn
    {
        "id": "GRC-01",
        "alan": "Erişim Kontrolü",
        "kontrol": "Görevler Ayrılığı (SoD) İhlali",
        "standart": "COSO 2013 – CC8.1 / IIA PA 2320",
        "aciklama": "Aynı kullanıcı hem işlem girişi hem onayı yapamaz.",
    },
    {
        "id": "GRC-02",
        "alan": "Erişim Kontrolü",
        "kontrol": "Mesai Dışı & Hafta Sonu Erişimi",
        "standart": "ISO 27001 – A.9.4 / COBIT DSS05",
        "aciklama": "Normal çalışma saatleri dışında gerçekleşen sistem erişimi izlenmelidir.",
    },
    {
        "id": "GRC-03",
        "alan": "Finansal Uyum",
        "kontrol": "Eşik Altı Yapılandırma (Structuring)",
        "standart": "FATF Öneri 7 / AML Mevzuatı",
        "aciklama": "Onay limitinin hemen altında birden fazla ardışık işlem finansal suç riskini artırır.",
    },
    {
        "id": "GRC-04",
        "alan": "Finansal Uyum",
        "kontrol": "Benford Yasası Sapması",
        "standart": "ACFE – Sahtecilik Önleme Rehberi",
        "aciklama": "Finansal verilerin doğal dağılımdan sapması; veri manipülasyonuna işaret edebilir.",
    },
    {
        "id": "GRC-05",
        "alan": "Veri Bütünlüğü",
        "kontrol": "Mükerrer Belge / Çift Ödeme Riski",
        "standart": "COSO 2013 – CC7.2 / IIA Std. 2130",
        "aciklama": "Aynı belge numarası veya aynı içerik birden fazla kez kaydedilmiş olabilir.",
    },
    {
        "id": "GRC-06",
        "alan": "Veri Bütünlüğü",
        "kontrol": "Eksik / Boş Kritik Alan",
        "standart": "GDPR Madde 5 / KVKK Md. 4",
        "aciklama": "Zorunlu alanların boş bırakılması veri kalitesini ve yasal uyumu etkiler.",
    },
    {
        "id": "GRC-07",
        "alan": "Tedarikçi Uyumu",
        "kontrol": "Tedarikçi Yoğunlaşması (Pareto)",
        "standart": "Kamu İhale Kanunu / Şirket Satınalma Politikası",
        "aciklama": "Az sayıda tedarikçiye aşırı bağımlılık rekabet eksikliğine ve suistimal riskine yol açar.",
    },
    {
        "id": "GRC-08",
        "alan": "Operasyonel Uyum",
        "kontrol": "Negatif / Sıfır Tutar Kayıtları",
        "standart": "COSO 2013 – CC4.1 / Vergi Mevzuatı",
        "aciklama": "Mantıksal olarak geçersiz tutar değerleri; kötü amaçlı kayıt veya sistem hatasına işaret edebilir.",
    },
]


def run_grc_assessment(findings: list, scenarios: list, quality: list, df: pd.DataFrame) -> list[dict]:
    """
    Bulgular, senaryolar ve kalite testlerini GRC kontrol çerçevesiyle eşleştirir;
    her kontrol için Risk / Uyum Durumu / Kanıt sayısı döndürür.
    """
    keyword_map = {
        "GRC-01": ["sod", "görevler", "ayrılık"],
        "GRC-02": ["mesai", "hafta sonu", "hafta_sonu", "erişim"],
        "GRC-03": ["eşik", "structuring", "yapılandırma"],
        "GRC-04": ["benford", "bf-01"],
        "GRC-05": ["mükerrer", "çift", "duplicate"],
        "GRC-06": ["eksik", "boş", "missing"],
        "GRC-07": ["pareto", "yoğunlaşma", "pa-01"],
        "GRC-08": ["negatif", "sıfır", "zero"],
    }

    all_texts = (
        [f["id"].lower() + " " + f["baslik"].lower() for f in findings]
        + [s["id"].lower() + " " + s["senaryo"].lower() for s in scenarios]
        + [q["id"].lower() + " " + q["kontrol"].lower() for q in quality]
    )

    results = []
    for ctrl in _GRC_CONTROLS:
        kws = keyword_map.get(ctrl["id"], [])
        kanit_sayisi = sum(
            1 for t in all_texts if any(kw in t for kw in kws)
        )

        # Risk seviyesi: ilgili bulgulardan miras al
        related_risks = []
        for f in findings:
            txt = f["id"].lower() + f["baslik"].lower()
            if any(kw in txt for kw in kws):
                related_risks.append(f["risk"])
        for s in scenarios:
            txt = s["id"].lower() + s["senaryo"].lower()
            if any(kw in txt for kw in kws):
                related_risks.append(s["risk"])

        prio = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3}
        if related_risks:
            risk = min(related_risks, key=lambda r: prio.get(r, 4))
            durum = "❌ Uyumsuz" if risk in ("Kritik", "Yüksek") else "⚠️ Kısmen Uyumlu"
        elif kanit_sayisi == 0:
            risk = "Düşük"
            durum = "✅ Uyumlu"
        else:
            risk = "Orta"
            durum = "⚠️ Kısmen Uyumlu"

        results.append({
            **ctrl,
            "risk":         risk,
            "durum":        durum,
            "kanit_sayisi": kanit_sayisi,
        })

    return results


def render_grc_tab(grc_results: list, findings: list, df: pd.DataFrame):
    """GRC sekmesini render eder."""
    st.markdown("""
    <div class="sec-header">
      <div class="sec-icon">🛡️</div>
      <div>
        <div class="sec-title">GRC – Governance, Risk & Compliance</div>
        <div class="sec-subtitle">Erişim kontrolü · Mevzuat uyumu · Kontrol matrisi · Sürekli izleme</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Özet KPI ──────────────────────────────────────────────────────────────
    uyumsuz = sum(1 for g in grc_results if "Uyumsuz" in g["durum"])
    kismi   = sum(1 for g in grc_results if "Kısmen"  in g["durum"])
    uyumlu  = sum(1 for g in grc_results if g["durum"] == "✅ Uyumlu")
    uyum_pct = int(uyumlu / len(grc_results) * 100) if grc_results else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🛡️ Toplam Kontrol",   len(grc_results))
    c2.metric("❌ Uyumsuz",           uyumsuz, delta=f"-{uyumsuz}" if uyumsuz else None,
              delta_color="inverse")
    c3.metric("⚠️ Kısmen Uyumlu",     kismi)
    c4.metric("✅ Uyum Oranı",        f"%{uyum_pct}")

    st.divider()

    # ── Kontrol Matrisi Tablosu ───────────────────────────────────────────────
    st.markdown("#### 📋 GRC Kontrol Matrisi")
    grc_df = pd.DataFrame([{
        "ID":           g["id"],
        "Alan":         g["alan"],
        "Kontrol":      g["kontrol"],
        "Risk":         g["risk"],
        "Uyum Durumu":  g["durum"],
        "Kanıt Sayısı": g["kanit_sayisi"],
        "Standart":     g["standart"],
    } for g in grc_results])
    st.dataframe(grc_df, use_container_width=True, hide_index=True)

    st.divider()

    # ── Alan Bazlı Uyum Özeti ─────────────────────────────────────────────────
    st.markdown("#### 📊 Alan Bazlı Uyum Dağılımı")
    alan_grp = {}
    for g in grc_results:
        alan = g["alan"]
        alan_grp.setdefault(alan, {"Uyumlu": 0, "Kısmen": 0, "Uyumsuz": 0})
        if "Uyumsuz" in g["durum"]:   alan_grp[alan]["Uyumsuz"] += 1
        elif "Kısmen"  in g["durum"]: alan_grp[alan]["Kısmen"]  += 1
        else:                          alan_grp[alan]["Uyumlu"]  += 1

    alan_df = pd.DataFrame([
        {"Alan": a, **v} for a, v in alan_grp.items()
    ])
    fig_grc = go.Figure()
    for col_name, color in [("Uyumsuz","#e03e3e"), ("Kısmen","#d97706"), ("Uyumlu","#059669")]:
        fig_grc.add_trace(go.Bar(
            name=col_name, x=alan_df["Alan"], y=alan_df[col_name],
            marker_color=color,
        ))
    fig_grc.update_layout(
        **PLOT_LAYOUT,
        barmode="stack",
        title="Alan Bazlı GRC Uyum Durumu",
        height=350,
    )
    st.plotly_chart(fig_grc, use_container_width=True)

    st.divider()

    # ── Kontrol Detay Kartları ────────────────────────────────────────────────
    st.markdown("#### 🔍 Kontrol Detayları")
    for g in grc_results:
        css = css_class(g["risk"])
        exp_label = f"{g['durum']}  [{g['id']}]  {g['kontrol']}  — Risk: {g['risk']}"
        with st.expander(exp_label, expanded=("Uyumsuz" in g["durum"])):
            col_d1, col_d2 = st.columns([3, 1])
            with col_d1:
                st.markdown(f"**📌 Kontrol Amacı:** {g['aciklama']}")
                st.markdown(f"**📚 Standart Referans:** `{g['standart']}`")
                st.markdown(f"**🏷 Alan:** {g['alan']}")
            with col_d2:
                st.markdown(f"""
                <div class="stat-grid">
                  <div class="stat-item">
                    <div class="stat-label">Risk</div>
                    <div class="stat-value"><span class="rbadge {css}">{g['risk']}</span></div>
                  </div>
                  <div class="stat-item">
                    <div class="stat-label">Kanıt</div>
                    <div class="stat-value">{g['kanit_sayisi']}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            # İlgili bulgular
            ilgili = [f for f in findings
                      if any(kw in (f["id"] + f["baslik"]).lower()
                             for kw in ["sod","mesai","eşik","benford","mükerrer","eksik","pareto","negatif"]
                             if kw in g["kontrol"].lower() or kw in g["id"].lower())]
            if g["kanit_sayisi"] > 0:
                st.markdown(f"**⚠️ Tespit Edilen Kanıt Sayısı:** `{g['kanit_sayisi']}` ilgili bulgu/senaryo")


# ══════════════════════════════════════════════════════════════════════════════
# M17 – OPERASYONELVERİMLİLİK DEĞERLENDİRMESİ
# ══════════════════════════════════════════════════════════════════════════════
# İlandan: "İş süreçleri üzerindeki kontrolleri, operasyonel verimlilik ve
#            etkinliği … değerlendirmek"
# ─────────────────────────────────────────────────────────────────────────────

def compute_operational_efficiency(df: pd.DataFrame, col_map: dict,
                                   quality: list, scenarios: list) -> dict:
    """
    Veri setinden operasyonel verimlilik göstergelerini hesaplar.
    Returns: dict of efficiency metrics.
    """
    result: dict = {}
    total = len(df)
    if total == 0:
        return result

    # 1. Veri Kalite Skoru (0-100)
    eksik_pct    = df.isnull().sum().sum() / (total * len(df.columns)) * 100
    mukerrer_pct = df.duplicated().sum()   / total * 100
    kalite_skoru = max(0, round(100 - eksik_pct * 2 - mukerrer_pct * 3, 1))
    result["kalite_skoru"] = kalite_skoru

    # 2. Onay Oran Analizi (varsa)
    if "status" in col_map:
        s_col = col_map["status"]
        try:
            counts = df[s_col].astype(str).str.lower().value_counts()
            onaylandi = counts.get("onaylandı", 0) + counts.get("approved", 0)
            reddedildi = counts.get("reddedildi", 0) + counts.get("rejected", 0)
            bekleyen = counts.get("beklemede", 0) + counts.get("pending", 0)
            result["onay_orani"] = round(onaylandi / max(total, 1) * 100, 1)
            result["red_orani"]  = round(reddedildi / max(total, 1) * 100, 1)
            result["bekleyen"]   = int(bekleyen)
            result["onaylandi"]  = int(onaylandi)
        except Exception:
            pass

    # 3. İşlem Yoğunluğu (varsa tarih)
    if "date" in col_map:
        try:
            df2 = _parse_dates_safe(df, col_map["date"])
            date_s = df2[col_map["date"]].dropna()
            if len(date_s) > 1:
                gun_arasi = (date_s.max() - date_s.min()).days or 1
                result["gunluk_islem"] = round(total / gun_arasi, 1)
                # Hafta sonu işlem oranı
                hs_pct = (date_s.dt.dayofweek >= 5).mean() * 100
                result["haftasonu_pct"] = round(hs_pct, 1)
                # Mesai dışı oranı
                mesai_pct = ((date_s.dt.hour < 8) | (date_s.dt.hour >= 18)).mean() * 100
                result["mesai_disi_pct"] = round(mesai_pct, 1)
        except Exception:
            pass

    # 4. Kontrol Etkinlik Skoru
    # Her kritik senaryo/kalite bulgusu skoru düşürür
    kritik_n = sum(1 for q in quality   if q["risk"] == "Kritik")
    yuksek_n = sum(1 for q in quality   if q["risk"] == "Yüksek")
    kritik_n += sum(1 for s in scenarios if s["risk"] == "Kritik")
    yuksek_n += sum(1 for s in scenarios if s["risk"] == "Yüksek")
    kontrol_skoru = max(0, round(100 - kritik_n * 15 - yuksek_n * 7, 1))
    result["kontrol_skoru"] = kontrol_skoru

    # 5. Genel Verimlilik Endeksi (0-100)
    comp = [kalite_skoru, kontrol_skoru]
    result["verimlilik_endeksi"] = round(sum(comp) / len(comp), 1)

    # 6. Tutar bazlı istatistikler (varsa)
    if "amount" in col_map:
        try:
            amt = _to_numeric_safe(df, col_map["amount"]).dropna()
            result["ort_tutar"]  = float(amt.mean())
            result["toplam_tutar"] = float(amt.sum())
            result["std_tutar"]  = float(amt.std())
            result["cv_tutar"]   = round(amt.std() / amt.mean() * 100, 1) if amt.mean() != 0 else 0
        except Exception:
            pass

    return result


def render_efficiency_tab(eff: dict, df: pd.DataFrame, col_map: dict):
    """Operasyonel Verimlilik sekmesini render eder."""
    st.markdown("""
    <div class="sec-header">
      <div class="sec-icon">⚙️</div>
      <div>
        <div class="sec-title">Operasyonel Verimlilik Değerlendirmesi</div>
        <div class="sec-subtitle">Süreç etkinliği · Kontrol skoru · İşlem kalitesi · Anomali yoğunluğu</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not eff:
        st.info("Yeterli veri bulunamadı.")
        return

    # ── Ana Göstergeler ───────────────────────────────────────────────────────
    c1, c2, c3 = st.columns(3)
    vi = eff.get("verimlilik_endeksi", 0)
    vi_delta = "İyi" if vi >= 70 else ("Orta" if vi >= 50 else "Düşük")
    c1.metric("📊 Genel Verimlilik Endeksi", f"{vi}/100",
              delta=vi_delta, delta_color="normal" if vi >= 70 else "inverse")
    c2.metric("🧪 Veri Kalite Skoru",        f"{eff.get('kalite_skoru',0)}/100")
    c3.metric("🛡️ Kontrol Etkinlik Skoru",   f"{eff.get('kontrol_skoru',0)}/100")

    st.divider()

    # ── Gauge Grafikleri ──────────────────────────────────────────────────────
    col_g1, col_g2, col_g3 = st.columns(3)
    gauge_items = [
        (col_g1, "Verimlilik Endeksi", vi),
        (col_g2, "Veri Kalitesi",      eff.get("kalite_skoru", 0)),
        (col_g3, "Kontrol Etkinliği",  eff.get("kontrol_skoru", 0)),
    ]
    for col, label, val in gauge_items:
        color = "#059669" if val >= 70 else ("#d97706" if val >= 50 else "#e03e3e")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            title={"text": label, "font": {"color": "#8aa4be", "size": 13}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#4a6480"},
                "bar":  {"color": color},
                "bgcolor": "#111e30",
                "steps": [
                    {"range": [0,  50], "color": "rgba(224,62,62,0.12)"},
                    {"range": [50, 70], "color": "rgba(217,119,6,0.12)"},
                    {"range": [70,100], "color": "rgba(5,150,105,0.12)"},
                ],
                "threshold": {"line": {"color": "#ffffff", "width": 2}, "value": val},
            },
            number={"suffix": "/100", "font": {"color": color, "size": 28}},
        ))
        fig.update_layout(**{**PLOT_LAYOUT, "height": 220, "margin": dict(l=20,r=20,t=40,b=10)})
        col.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Onay Süreci Analizi ───────────────────────────────────────────────────
    if "onay_orani" in eff:
        st.markdown("#### 📋 Onay Süreci Analizi")
        oc1, oc2, oc3 = st.columns(3)
        oc1.metric("✅ Onay Oranı",    f"%{eff['onay_orani']}")
        oc2.metric("❌ Red Oranı",     f"%{eff['red_orani']}")
        oc3.metric("⏳ Bekleyen",      f"{eff.get('bekleyen',0):,} kayıt")

        fig_onay = go.Figure(go.Pie(
            labels=["Onaylandı", "Reddedildi", "Beklemede"],
            values=[
                eff.get("onaylandi", 0),
                int(len(df) * eff["red_orani"] / 100),
                eff.get("bekleyen", 0),
            ],
            marker_colors=["#059669", "#e03e3e", "#d97706"],
            hole=0.55,
            textinfo="label+percent",
        ))
        fig_onay.update_layout(**{**PLOT_LAYOUT, "height": 300,
                                  "title": "Onay Durumu Dağılımı"})
        st.plotly_chart(fig_onay, use_container_width=True)
        st.divider()

    # ── Zaman Bazlı Verimlilik ────────────────────────────────────────────────
    if "gunluk_islem" in eff:
        st.markdown("#### ⏱ Zaman Bazlı Verimlilik Göstergeleri")
        tc1, tc2, tc3 = st.columns(3)
        tc1.metric("📅 Günlük Ort. İşlem",     f"{eff['gunluk_islem']:.1f}")
        tc2.metric("🌙 Mesai Dışı İşlem",      f"%{eff.get('mesai_disi_pct',0):.1f}",
                   delta="Yüksek Risk" if eff.get("mesai_disi_pct",0) > 5 else "Normal",
                   delta_color="inverse" if eff.get("mesai_disi_pct",0) > 5 else "normal")
        tc3.metric("📅 Hafta Sonu İşlem",      f"%{eff.get('haftasonu_pct',0):.1f}",
                   delta="Yüksek Risk" if eff.get("haftasonu_pct",0) > 5 else "Normal",
                   delta_color="inverse" if eff.get("haftasonu_pct",0) > 5 else "normal")
        st.divider()

    # ── Tutar Dağılım Analizi ─────────────────────────────────────────────────
    if "ort_tutar" in eff:
        st.markdown("#### 💰 Finansal İşlem Kalitesi")
        fc1, fc2, fc3, fc4 = st.columns(4)
        fc1.metric("Toplam Tutar",  f"{eff['toplam_tutar']:,.0f}")
        fc2.metric("Ortalama",      f"{eff['ort_tutar']:,.0f}")
        fc3.metric("Std. Sapma",    f"{eff['std_tutar']:,.0f}")
        fc4.metric("Varyasyon Katsayısı", f"%{eff['cv_tutar']:.1f}",
                   help="CV > 150% ise işlem tutarları aşırı heterojen — anomali riski yüksek")

        if "amount" in col_map:
            try:
                amt = _to_numeric_safe(df, col_map["amount"]).dropna()
                fig_hist = px.histogram(
                    amt[amt > 0], nbins=50,
                    title="Pozitif Tutar Dağılımı (log ekseni)",
                    log_y=True,
                    color_discrete_sequence=["#4f9cf9"],
                )
                fig_hist.update_layout(**{**PLOT_LAYOUT, "height": 300})
                st.plotly_chart(fig_hist, use_container_width=True)
            except Exception:
                pass


# ══════════════════════════════════════════════════════════════════════════════
# M18 – YILLIK RİSK BAZLI DENETİM PLANLAYICI
# ══════════════════════════════════════════════════════════════════════════════
# İlandan: "Yıllık risk bazlı denetim planı doğrultusunda … iç denetim
#            faaliyetlerini gerçekleştirmek"
# ─────────────────────────────────────────────────────────────────────────────

_AUDIT_AREAS = [
    ("Satınalma & Tedarik",   "Tedarikçi onay, sözleşme yönetimi, fiyat karşılaştırması"),
    ("Finans & Muhasebe",     "Finansal raporlama, dönem kapanışı, mutabakat"),
    ("İnsan Kaynakları",      "Bordro, performans değerlendirme, işe alım prosedürleri"),
    ("Bilgi Teknolojileri",   "Erişim yönetimi, yedekleme, felaket kurtarma planı"),
    ("Operasyonlar",          "Üretim/hizmet kalitesi, verimlilik, kapasite kullanımı"),
    ("Hukuk & Uyum",          "Mevzuat takibi, sözleşme yükümlülükleri, lisans yönetimi"),
    ("Pazarlama & Satış",     "Hedef uyumu, müşteri verisi yönetimi, indirim politikaları"),
    ("İç Kontrol",            "Kontrol tasarım etkinliği, uygulama testi, boşluk analizi"),
]

_AUDIT_MONTHS = [
    "Ocak","Şubat","Mart","Nisan","Mayıs","Haziran",
    "Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"
]


def generate_audit_plan(findings: list, grc_results: list) -> list[dict]:
    """
    Bulgular ve GRC uyum durumuna göre yıllık denetim planı önerir.
    Her alan için tahmini ay, öncelik ve tahmini gün sayısı döndürür.
    """
    # Uyumsuz/kısmen uyumlu GRC alanlarına öncelik ver
    grc_risk = {g["alan"]: g["risk"] for g in grc_results}
    prio_map = {"Kritik": 0, "Yüksek": 1, "Orta": 2, "Düşük": 3}

    # Bulgulardan alan etiketleri çıkar
    finding_alan_risk: dict[str, str] = {}
    for f in findings:
        kat = f.get("kategori", "")
        risk = f.get("risk", "Düşük")
        finding_alan_risk[kat] = min(
            [finding_alan_risk.get(kat, "Düşük"), risk],
            key=lambda r: prio_map.get(r, 4)
        )

    plan = []
    scheduled_months = []
    month_counter = 1

    for alan, kapsam in _AUDIT_AREAS:
        # Alan riski: GRC + bulgulardan maksimum
        alan_risk_vals = []
        for gk, gr in grc_risk.items():
            if any(w in alan.lower() for w in gk.lower().split()):
                alan_risk_vals.append(gr)
        for fk, fr in finding_alan_risk.items():
            if any(w in alan.lower() for w in fk.lower().split()):
                alan_risk_vals.append(fr)

        if alan_risk_vals:
            alan_riski = min(alan_risk_vals, key=lambda r: prio_map.get(r, 4))
        else:
            alan_riski = "Düşük"

        # Öncelik & süre
        if alan_riski == "Kritik":
            oncelik, gun = "P1 – Acil", 10
        elif alan_riski == "Yüksek":
            oncelik, gun = "P2 – Yüksek", 7
        elif alan_riski == "Orta":
            oncelik, gun = "P3 – Orta", 5
        else:
            oncelik, gun = "P4 – Rutin", 3

        # Ay ataması (P1'ler önce)
        ay_idx = min(month_counter - 1, 11)
        ay = _AUDIT_MONTHS[ay_idx]
        if alan_riski in ("Kritik", "Yüksek"):
            ay = _AUDIT_MONTHS[min(ay_idx, 5)]  # İlk yarıyıl
        month_counter += 1

        plan.append({
            "alan":     alan,
            "kapsam":   kapsam,
            "oncelik":  oncelik,
            "risk":     alan_riski,
            "ay":       ay,
            "gun":      gun,
            "durum":    "Planlandı",
        })

    # P1 → P4 sıralama
    plan.sort(key=lambda x: prio_map.get(x["risk"], 4))

    # Ay yeniden ata (sıralı)
    for i, p in enumerate(plan):
        p["ay"] = _AUDIT_MONTHS[min(i, 11)]

    return plan


def render_audit_plan_tab(audit_plan: list):
    """Yıllık Denetim Planı sekmesini render eder."""
    st.markdown("""
    <div class="sec-header">
      <div class="sec-icon">📅</div>
      <div>
        <div class="sec-title">Yıllık Risk Bazlı Denetim Planı</div>
        <div class="sec-subtitle">IIA Std. 2010 uyumlu · Risk öncelikli denetim takvimi · Kaynak planlaması</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not audit_plan:
        st.info("Denetim planı oluşturulamadı.")
        return

    # ── Özet KPI ──────────────────────────────────────────────────────────────
    toplam_gun = sum(p["gun"] for p in audit_plan)
    p1_n = sum(1 for p in audit_plan if "P1" in p["oncelik"])
    p2_n = sum(1 for p in audit_plan if "P2" in p["oncelik"])
    yil  = datetime.now().year

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📋 Toplam Denetim Alanı", len(audit_plan))
    c2.metric("🚨 P1 – Acil Alan",       p1_n)
    c3.metric("⚠️ P2 – Yüksek Alan",    p2_n)
    c4.metric("⏱ Toplam Tahmini Gün",   toplam_gun)

    st.divider()

    # ── Gantt / Takvim Görünümü ───────────────────────────────────────────────
    st.markdown(f"#### 📅 {yil} Denetim Takvimi (Gantt)")

    gantt_data = []
    for p in audit_plan:
        ay_idx = _AUDIT_MONTHS.index(p["ay"])
        start  = datetime(yil, ay_idx + 1, 1)
        end    = start + timedelta(days=p["gun"])
        color  = {"Kritik":"#e03e3e","Yüksek":"#d97706","Orta":"#2563eb","Düşük":"#059669"}.get(p["risk"],"#4f9cf9")
        gantt_data.append({
            "Alan": p["alan"], "Başlangıç": start, "Bitiş": end,
            "Risk": p["risk"], "Gün": p["gun"], "Color": color,
        })

    fig_gantt = go.Figure()
    for i, row in enumerate(gantt_data):
        fig_gantt.add_trace(go.Bar(
            x=[(row["Bitiş"] - row["Başlangıç"]).days],
            y=[row["Alan"]],
            base=[(row["Başlangıç"] - datetime(yil, 1, 1)).days],
            orientation="h",
            marker_color=row["Color"],
            name=row["Risk"],
            text=f"{row['Gün']} gün",
            textposition="inside",
            showlegend=(i < 4),
            hovertemplate=(
                f"<b>{row['Alan']}</b><br>"
                f"Başlangıç: {row['Başlangıç'].strftime('%d %B')}<br>"
                f"Süre: {row['Gün']} gün<br>"
                f"Risk: {row['Risk']}<extra></extra>"
            ),
        ))

    # X ekseni ay etiketleri
    month_positions = [(datetime(yil, m, 1) - datetime(yil, 1, 1)).days for m in range(1, 13)]
    gantt_layout = {k: v for k, v in PLOT_LAYOUT.items() if k != "xaxis"}
    fig_gantt.update_layout(
        **gantt_layout,
        height=400,
        title=f"{yil} Risk Bazlı Denetim Takvimi",
        xaxis=dict(
            tickvals=month_positions,
            ticktext=_AUDIT_MONTHS,
            gridcolor="#1c2e44",
            zerolinecolor="#1c2e44",
            linecolor="#1c2e44",
        ),
        barmode="overlay",
    )
    st.plotly_chart(fig_gantt, use_container_width=True)

    st.divider()

    # ── Detay Tablo ───────────────────────────────────────────────────────────
    st.markdown("#### 📋 Denetim Planı Detayı")

    # Kullanıcı durum güncellemesi
    if "audit_plan_durum" not in st.session_state:
        st.session_state["audit_plan_durum"] = {
            p["alan"]: "Planlandı" for p in audit_plan
        }

    plan_df_rows = []
    for p in audit_plan:
        plan_df_rows.append({
            "Alan":     p["alan"],
            "Kapsam":   p["kapsam"],
            "Öncelik":  p["oncelik"],
            "Risk":     p["risk"],
            "Takvim":   p["ay"],
            "Tahmini Gün": p["gun"],
            "Durum":    st.session_state["audit_plan_durum"].get(p["alan"], "Planlandı"),
        })
    plan_df = pd.DataFrame(plan_df_rows)
    st.dataframe(plan_df, use_container_width=True, hide_index=True)

    st.divider()

    # ── Alan Durum Güncelleme ─────────────────────────────────────────────────
    st.markdown("#### ✏️ Denetim Durumu Güncelle")
    for p in audit_plan[:4]:  # İlk 4 (P1-P2) göster
        col_p1, col_p2 = st.columns([3, 1])
        with col_p1:
            st.markdown(f"**{p['alan']}** — _{p['oncelik']}_ · {p['ay']} · {p['gun']} gün")
        with col_p2:
            mevcut = st.session_state["audit_plan_durum"].get(p["alan"], "Planlandı")
            yeni = st.selectbox(
                "Durum",
                ["Planlandı", "Devam Ediyor", "Tamamlandı", "Ertelendi"],
                index=["Planlandı","Devam Ediyor","Tamamlandı","Ertelendi"].index(mevcut),
                key=f"aplan_{p['alan']}",
                label_visibility="collapsed",
            )
            st.session_state["audit_plan_durum"][p["alan"]] = yeni

    # ── Kaynak Dağılımı ───────────────────────────────────────────────────────
    st.divider()
    st.markdown("#### 📊 Ay Bazlı Kaynak Dağılımı")
    ay_gun: dict[str, int] = {}
    for p in audit_plan:
        ay_gun[p["ay"]] = ay_gun.get(p["ay"], 0) + p["gun"]

    ay_sira = {a: i for i, a in enumerate(_AUDIT_MONTHS)}
    ay_gun_sorted = dict(sorted(ay_gun.items(), key=lambda x: ay_sira.get(x[0], 99)))

    fig_ay = go.Figure(go.Bar(
        x=list(ay_gun_sorted.keys()),
        y=list(ay_gun_sorted.values()),
        marker_color="#4f9cf9",
        text=list(ay_gun_sorted.values()),
        textposition="outside",
    ))
    fig_ay.update_layout(**{**PLOT_LAYOUT, "height": 300,
                            "title": "Aylık Toplam Denetim Günü"})
    st.plotly_chart(fig_ay, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# M14 – SIDEBAR & FİLTRELER
# ══════════════════════════════════════════════════════════════════════════════

def render_sidebar(df: pd.DataFrame, col_map: dict) -> dict:
    """Profesyonel sidebar: filtreler + kolon haritası + istatistikler."""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="sb-logo">
          <div class="sb-logo-eyebrow">İÇ DENETİM ANALİTİK</div>
          <div class="sb-logo-title">Denetim Platformu</div>
          <div class="sb-logo-sub">Professional Edition v3.0</div>
        </div>
        """, unsafe_allow_html=True)

        filters: dict = {}

        # ── Risk Filtresi ──
        st.markdown('<span class="sb-label">Risk Seviyesi</span>', unsafe_allow_html=True)
        filters["risk"] = st.multiselect(
            "_rf", ["Kritik","Yüksek","Orta","Düşük"],
            default=["Kritik","Yüksek","Orta","Düşük"],
            label_visibility="collapsed",
        )

        # ── Tarih Filtresi ──
        if "date" in col_map:
            df2 = _parse_dates_safe(df, col_map["date"])
            mn  = df2[col_map["date"]].min()
            mx  = df2[col_map["date"]].max()
            if pd.notna(mn) and pd.notna(mx) and mn != mx:
                st.markdown('<span class="sb-label">Tarih Aralığı</span>', unsafe_allow_html=True)
                try:
                    rng = st.date_input(
                        "_df", (mn.date(), mx.date()),
                        min_value=mn.date(), max_value=mx.date(),
                        label_visibility="collapsed",
                    )
                    filters["date_range"] = rng
                except Exception:
                    pass

        # ── Min Risk Skoru ──
        st.markdown('<span class="sb-label">Min. Risk Skoru</span>', unsafe_allow_html=True)
        filters["min_score"] = st.slider("_sf", 0, 100, 0, label_visibility="collapsed")

        # ── Min Tutar ──
        if "amount" in col_map:
            st.markdown('<span class="sb-label">Min. Tutar</span>', unsafe_allow_html=True)
            filters["min_amount"] = st.number_input(
                "_af", value=0.0, min_value=0.0,
                format="%.2f", label_visibility="collapsed",
            )

        # ── Vendor Filtresi ──
        if "vendor" in col_map:
            vendors = ["Tümü"] + sorted(df[col_map["vendor"]].dropna().unique().tolist())
            if len(vendors) <= 50:
                st.markdown('<span class="sb-label">Karşı Taraf</span>', unsafe_allow_html=True)
                sel_vendor = st.selectbox("_vf", vendors, label_visibility="collapsed")
                filters["vendor"] = sel_vendor

        st.markdown("---")

        # ── Kolon Haritası ──
        st.markdown('<span class="sb-label">Algılanan Sütunlar</span>', unsafe_allow_html=True)
        rows = "".join(
            f"<tr><td class='cm-role'>{ROLE_TR.get(r,r)}</td>"
            f"<td class='cm-col'>{c}</td></tr>"
            for r, c in col_map.items()
        )
        st.markdown(
            f"<table class='cm-table'>{rows}</table>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        # ── Hızlı İstatistik ──
        st.markdown('<span class="sb-label">Veri Özeti</span>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;
                    color:var(--c-text2,#8aa4be);line-height:2;">
          Satır  : {len(df):,}<br>
          Sütun  : {len(df.columns)}<br>
          Eksik  : {df.isnull().sum().sum():,} hücre<br>
          Sayısal: {len(df.select_dtypes('number').columns)} sütun<br>
          Tarih  : {len(df.select_dtypes('datetime').columns)} sütun
        </div>
        """, unsafe_allow_html=True)

    return filters


def apply_filters(df: pd.DataFrame, col_map: dict, filters: dict) -> pd.DataFrame:
    """Sidebar filtrelerini uygula."""
    out = df.copy()

    if "risk" in filters and "risk_seviyesi" in out.columns:
        out = out[out["risk_seviyesi"].isin(filters["risk"])]

    if "min_score" in filters and "risk_skoru" in out.columns:
        out = out[out["risk_skoru"] >= filters["min_score"]]

    if "date_range" in filters and "date" in col_map:
        out = _parse_dates_safe(out, col_map["date"])
        try:
            r = filters["date_range"]
            if len(r) == 2:
                out = out[
                    (out[col_map["date"]].dt.date >= r[0]) &
                    (out[col_map["date"]].dt.date <= r[1])
                ]
        except Exception:
            pass

    if "min_amount" in filters and "amount" in col_map:
        amt = _to_numeric_safe(out, col_map["amount"])
        out = out[amt.fillna(0).abs() >= filters["min_amount"]]

    if "vendor" in filters and filters["vendor"] != "Tümü" and "vendor" in col_map:
        out = out[out[col_map["vendor"]] == filters["vendor"]]

    return out


# ══════════════════════════════════════════════════════════════════════════════
# YARDIMCI: CSS sınıfı / ikon
# ══════════════════════════════════════════════════════════════════════════════

def css_class(level: str) -> str:
    return {"Kritik":"critical","Yüksek":"high","Orta":"medium","Düşük":"low"}.get(level,"medium")

def risk_icon(level: str) -> str:
    return {"Kritik":"🔴","Yüksek":"🟠","Orta":"🔵","Düşük":"🟢"}.get(level,"⚪")

def risk_emoji(level: str) -> str:
    return {"Kritik":"🚨","Yüksek":"⚠️","Orta":"🔹","Düşük":"✅"}.get(level,"❓")


# ══════════════════════════════════════════════════════════════════════════════
# DEMO VERİ ÜRETİCİ
# ══════════════════════════════════════════════════════════════════════════════

def generate_demo_data() -> pd.DataFrame:
    """
    600+ kayıtlık, birden fazla anomali içeren gerçekçi ERP benzeri demo verisi.
    SAP benzeri sütun adları kullanılmıştır.
    """
    np.random.seed(2024)
    n = 620

    vendors = [
        "Teknoloji A AŞ","Lojistik B Ltd","Danışmanlık C GmbH",
        "İnşaat D Ort","Temizlik E Firm","Malzeme F Koop",
        "Servis G SRL","Yazılım H Inc","Güvenlik I Ltd",
        "Catering J AŞ","Hukuk K Bürosu","Reklam L Ajansı",
    ]
    users  = ["a.kaya","f.demir","m.yilmaz","z.arslan","a.celik","e.sahin","h.ozturk"]
    cats   = ["BT Harcaması","Danışmanlık","Kira","Seyahat","Bakım","Hizmet","Malzeme","Eğitim"]
    depts  = ["Finans","Satınalma","İK","BT","Operasyon","Yönetim"]
    statuses = ["Onaylandı","Onaylandı","Onaylandı","Beklemede","Reddedildi"]
    ccs    = ["CC-1001","CC-1002","CC-2001","CC-2002","CC-3001"]

    amounts = np.abs(np.random.lognormal(8.5, 1.9, n)).round(2)

    # Anomali enjeksiyonları
    amounts[5:14]    = np.random.uniform(9200, 9999, 9).round(2)   # SC-04
    amounts[20:27]   = np.random.uniform(24100, 24999, 7).round(2) # SC-04
    amounts[50:62]   = np.random.choice([5000,10000,25000,50000,100000],12)  # KT-06
    amounts[80:87]   = np.random.uniform(-18000, -300, 7).round(2) # KT-04
    amounts[100]     = 1_250_000                                    # KT-05 aykırı
    amounts[150]     = 875_000
    amounts[200]     = 2_100_000
    amounts[120:125] = 0                                            # KT-04 sıfır
    amounts[300:318] = 4_750.00                                     # SC-06 tekrar

    # Tarihler – hafta sonu ve mesai dışı enjeksiyonu
    dates = []
    base  = datetime(2024, 1, 1, 9, 0)
    for i in range(n):
        delta = timedelta(days=int(np.random.randint(0, 365)),
                          hours=int(np.random.randint(0, 23)),
                          minutes=int(np.random.randint(0, 59)))
        dates.append(base + delta)

    for i in [30,31,32,33,34,35]:     # Mesai dışı – SC-03
        dates[i] = dates[i].replace(hour=int(np.random.choice([1,2,3,22,23])))
    for i in [40,41,42,43]:           # Hafta sonu – SC-08
        raw = dates[i]
        diff = (5 - raw.weekday()) % 7
        dates[i] = raw + timedelta(days=diff)

    user_c = np.random.choice(users, n)
    appr_c = np.random.choice(users, n)
    for i in [10,11,12,13,14,15]:    # SoD – SC-05
        appr_c[i] = user_c[i]

    df = pd.DataFrame({
        "Belge_No":       [f"FTR-2024-{i+1:05d}" for i in range(n)],
        "Islem_Tarihi":   dates,
        "Tedarikci_Adi":  np.random.choice(vendors, n, p=[.35,.15,.1,.1,.08,.07,.05,.04,.02,.02,.01,.01]),
        "Departman":      np.random.choice(depts, n),
        "Gider_Kalemi":   np.random.choice(cats, n),
        "Maliyet_Merkezi":np.random.choice(ccs, n),
        "Kullanici":      user_c,
        "Onaylayan":      appr_c,
        "Belge_Tutari":   amounts,
        "Onay_Durumu":    np.random.choice(statuses, n, p=[.72,.12,.08,.06,.02]),
        "Aciklama":       np.random.choice([
            "Aylık hizmet bedeli","Proje danışmanlık ücreti","Malzeme tedariki",
            "Yazılım lisansı","Seyahat gideri","Ekipman bakımı","Kira ödemesi","Eğitim",
        ], n),
    })

    # Mükerrer satırlar – KT-03
    df = pd.concat([df, df.iloc[42:47].copy()], ignore_index=True)

    # Mükerrer belge no – KT-02
    df.loc[len(df)-1, "Belge_No"] = "FTR-2024-00055"
    df.loc[len(df)-2, "Belge_No"] = "FTR-2024-00055"

    # Eksik değerler – KT-01
    df.loc[60:66, "Tedarikci_Adi"] = np.nan
    df.loc[70:73, "Belge_Tutari"]  = np.nan
    df.loc[90:92, "Onaylayan"]     = np.nan

    return df.sort_values("Islem_Tarihi").reset_index(drop=True)


# ══════════════════════════════════════════════════════════════════════════════
# M15 – ANA UYGULAMA
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:

    # ── Masthead ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="masthead">
      <div class="masthead-eyebrow">
        <span class="masthead-pill">Aktif</span>
        <span class="masthead-standard">IIA IPPF · COSO 2013 · ISO 31000</span>
      </div>
      <h1>İç Denetim <em>Analitik</em> Platformu</h1>
      <div class="masthead-sub">
        <span>🔍 Otomatik Risk Skorlama</span>
        <span class="masthead-sep">·</span>
        <span>🎯 Senaryo Motoru</span>
        <span class="masthead-sep">·</span>
        <span>📊 Benford & Pareto Analizi</span>
        <span class="masthead-sep">·</span>
        <span>📌 IIA Uyumlu Raporlama</span>
        <span class="masthead-sep">·</span>
        <span>🌍 Evrensel ERP Desteği</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Dosya Yükleme ─────────────────────────────────────────────────────────
    uploaded = st.file_uploader(
        "Excel (.xlsx) veya CSV (.csv) yükleyin — sütun adları otomatik tanınır",
        type=["xlsx", "csv", "xls"],
        help=(
            "SAP · Oracle · Netsis · Logo · Mikro · İnteraktif · Eta · "
            "ve diğer ERP/muhasebe sistemleri desteklenir. "
            "Sütun adları ve sayıları ne olursa olsun sistem otomatik algılar."
        ),
    )

    if uploaded is None and not st.session_state.get("use_demo"):
        st.markdown("""
        <div class="info-box">
        <b>📂 Başlamak için veri dosyanızı yükleyin.</b><br>
        Sütun adları otomatik algılanır — ön tanımlama gerekmez.<br>
        Desteklenen: Excel (.xlsx, .xls) · CSV (.csv)
        </div>
        """, unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 3])
        with col_btn:
            if st.button("🎲 Demo Veri ile Başla", type="primary", use_container_width=True):
                st.session_state["use_demo"] = True
                st.rerun()

        # Özellik kartları
        st.markdown("""
        <div class="feat-grid">
          <div class="feat-card">
            <div class="feat-icon">🧪</div>
            <div class="feat-title">7 Kalite Kontrolü</div>
            <div class="feat-desc">Eksik veri · Mükerrer belge & satır · Negatif/sıfır tutar · Aykırı değer (IQR+Z) · Yuvarlama deseni · Tarih tutarsızlığı</div>
          </div>
          <div class="feat-card">
            <div class="feat-icon">🎯</div>
            <div class="feat-title">8 Denetim Senaryosu</div>
            <div class="feat-desc">İşlem yoğunluğu · Yoğunlaşma (HHI) · Mesai dışı · Eşik altı yapılandırma · SoD ihlali · Tekrarlayan tutar · Kullanıcı yoğunlaşması · Hafta sonu</div>
          </div>
          <div class="feat-card">
            <div class="feat-icon">📊</div>
            <div class="feat-title">Çok Değişkenli Risk Skoru</div>
            <div class="feat-desc">6 bileşenli 0–100 skor: Tutar · Z-score anomali · Vendor frekansı · Kullanıcı riski · Zaman riski · Kontrol uyarısı</div>
          </div>
          <div class="feat-card">
            <div class="feat-icon">🔢</div>
            <div class="feat-title">Benford Yasası</div>
            <div class="feat-desc">İlk rakam dağılım testi · Ki-kare istatistiği · Anormal sapma tespiti · Sahte veri uyarısı</div>
          </div>
          <div class="feat-card">
            <div class="feat-icon">📈</div>
            <div class="feat-title">Pareto Analizi</div>
            <div class="feat-desc">80/20 tedarikçi ve kullanıcı analizi · HHI yoğunlaşma endeksi · Kümülatif dağılım grafiği</div>
          </div>
          <div class="feat-card">
            <div class="feat-icon">📌</div>
            <div class="feat-title">IIA Uyumlu Raporlama</div>
            <div class="feat-desc">Standart referanslı aksiyon planları · Kök neden analizi · Yönetici özeti · Excel + TXT export</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Veri Yükleme ──────────────────────────────────────────────────────────
    try:
        if uploaded is not None:
            st.session_state["use_demo"] = False
            fname = uploaded.name.lower()
            if fname.endswith(".csv"):
                # UTF-8 dene, başarısız olursa latin-1
                try:
                    df_raw = pd.read_csv(uploaded, encoding="utf-8-sig")
                except UnicodeDecodeError:
                    uploaded.seek(0)
                    df_raw = pd.read_csv(uploaded, encoding="latin-1")
            else:
                df_raw = pd.read_excel(uploaded)
        else:
            df_raw = generate_demo_data()
            st.markdown("""
            <div class="warn-box">
            ⚠️ <b>Demo modunda çalışıyorsunuz.</b>
            Gerçek analiz için kendi veri dosyanızı yükleyin.
            </div>
            """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"❌ Dosya okunamadı: {e}")
        return

    if df_raw.empty:
        st.error("❌ Yüklenen dosya boş veya okunamadı.")
        return

    # ── Kolon Tanıma & Analiz ─────────────────────────────────────────────────
    col_map = detect_columns(df_raw)

    with st.spinner("⚙️ Denetim analizleri çalıştırılıyor…"):
        df_scored = compute_risk_scores(df_raw, col_map)
        quality   = run_data_quality(df_scored, col_map)
        scenarios = run_scenarios(df_scored, col_map)
        benford   = run_benford_analysis(df_scored, col_map)
        pareto    = run_pareto_analysis(df_scored, col_map)
        findings  = generate_findings(quality, scenarios, df_scored, benford, pareto)
        plans     = generate_action_plans(findings)
        grc_results  = run_grc_assessment(findings, scenarios, quality, df_scored)
        eff_metrics  = compute_operational_efficiency(df_scored, col_map, quality, scenarios)
        audit_plan   = generate_audit_plan(findings, grc_results)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    filters  = render_sidebar(df_scored, col_map)
    df_f     = apply_filters(df_scored, col_map, filters)

    # ── KPI Satırı ────────────────────────────────────────────────────────────
    total    = len(df_f)
    crit_n   = int((df_f["risk_seviyesi"] == "Kritik").sum())
    high_n   = int((df_f["risk_seviyesi"] == "Yüksek").sum())
    avg_risk = float(df_f["risk_skoru"].mean()) if total > 0 else 0
    high_pct = (crit_n + high_n) / (total or 1) * 100
    finding_n = len(findings)

    color5 = "critical" if high_pct > 20 else ("high" if high_pct > 10 else "ok")
    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card accent">
        <div class="kpi-eyebrow">Toplam Kayıt <span style="color:#4f9cf9;">📋</span></div>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-sub">Filtrelenmiş veri seti</div>
      </div>
      <div class="kpi-card critical">
        <div class="kpi-eyebrow">Kritik Kayıt <span style="color:#ff6b6b;">🚨</span></div>
        <div class="kpi-value">{crit_n:,}</div>
        <div class="kpi-sub">Acil aksiyon gerektirir</div>
      </div>
      <div class="kpi-card high">
        <div class="kpi-eyebrow">Ort. Risk Skoru <span style="color:#fbbf24;">📈</span></div>
        <div class="kpi-value">{avg_risk:.0f}</div>
        <div class="kpi-sub">0–100 skala</div>
      </div>
      <div class="kpi-card {color5}">
        <div class="kpi-eyebrow">Yüksek Risk % <span>⚡</span></div>
        <div class="kpi-value">{high_pct:.1f}%</div>
        <div class="kpi-sub">Kritik + Yüksek oranı</div>
      </div>
      <div class="kpi-card gold">
        <div class="kpi-eyebrow">Toplam Bulgu <span style="color:#f0c96a;">🔎</span></div>
        <div class="kpi-value">{finding_n}</div>
        <div class="kpi-sub">{len(plans)} aksiyon planı</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── SEKMELER ─────────────────────────────────────────────────────────────
    tabs = st.tabs([
        "📋 Veri Genel Görünüm",
        "📊 Risk Analizi",
        "🔢 Benford & Pareto",
        "🎯 Denetim Senaryoları",
        "🔎 Bulgular",
        "✅ Aksiyon Planları",
        "🛡️ GRC Uyum",
        "⚙️ Operasyonel Verimlilik",
        "📅 Denetim Planı",
        "📌 Yönetici Özeti",
    ])
    t_data, t_risk, t_benford, t_scenario, t_findings, t_actions, t_grc, t_eff, t_plan, t_exec = tabs

    # ══════════════════════════════════════════════════════
    # TAB 1 – VERİ GENEL GÖRÜNÜM
    # ══════════════════════════════════════════════════════
    with t_data:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">📋</div>
          <div><div class="sec-title">Veri Genel Görünüm</div>
               <div class="sec-subtitle">Ham veri önizleme, sütun istatistikleri ve kalite kontrolleri</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Genel istatistikler
        st.markdown(f"""
        <div class="overview-grid">
          <div class="ov-card"><div class="ov-label">Toplam Satır</div><div class="ov-value">{len(df_raw):,}</div></div>
          <div class="ov-card"><div class="ov-label">Toplam Sütun</div><div class="ov-value">{len(df_raw.columns)}</div></div>
          <div class="ov-card"><div class="ov-label">Eksik Hücre</div><div class="ov-value">{df_raw.isnull().sum().sum():,}</div></div>
          <div class="ov-card"><div class="ov-label">Tam Mükerrer</div><div class="ov-value">{df_raw.duplicated().sum():,}</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Kolon istatistikleri
        st.markdown("**Sütun Bilgileri**")
        col_info = pd.DataFrame({
            "Sütun":     df_raw.columns,
            "Tip":       [str(df_raw[c].dtype) for c in df_raw.columns],
            "Dolu":      [int(df_raw[c].notna().sum()) for c in df_raw.columns],
            "Boş":       [int(df_raw[c].isna().sum()) for c in df_raw.columns],
            "Boş %":     [(df_raw[c].isna().mean()*100).round(1) for c in df_raw.columns],
            "Benzersiz": [int(df_raw[c].nunique()) for c in df_raw.columns],
            "Algılanan Rol": [
                ROLE_TR.get(next((r for r, cv in col_map.items() if cv == c), ""), "—")
                for c in df_raw.columns
            ],
        })
        st.dataframe(col_info, use_container_width=True)

        st.markdown("**Ham Veri (İlk 200 Kayıt)**")
        st.dataframe(df_f.head(200), use_container_width=True, height=380)

        # Veri kalitesi kontrolleri
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">🧪</div>
          <div><div class="sec-title">Veri Kalitesi Kontrol Sonuçları</div></div>
          <div class="sec-badge">7 Kontrol</div>
        </div>
        """, unsafe_allow_html=True)

        for q in quality:
            icon = risk_icon(q["risk"])
            css  = css_class(q["risk"])
            with st.expander(
                f"{icon}  [{q['id']}]  {q['kontrol']}  —  **{q['risk']}**  ·  {q['etki']:,} kayıt",
                expanded=(q["risk"] in ("Kritik","Yüksek"))
            ):
                col_qa, col_qb = st.columns([2,1])
                with col_qa:
                    st.markdown(f"**📌 Bulgu**\n\n{q['bulgu']}")
                    st.markdown(f"**📂 Kategori:** {q['kategori']}")
                with col_qb:
                    if q["detay"]:
                        st.markdown("**Detay:**")
                        for k, v in q["detay"].items():
                            st.markdown(f"- `{k}`: **{v}**")

        st.markdown("**Sayısal Sütun İstatistikleri**")
        st.dataframe(df_raw.describe().round(3), use_container_width=True)

    # ══════════════════════════════════════════════════════
    # TAB 2 – RİSK ANALİZİ
    # ══════════════════════════════════════════════════════
    with t_risk:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">📊</div>
          <div><div class="sec-title">Risk Analizi Dashboard</div>
               <div class="sec-subtitle">Çok değişkenli risk skorlama, dağılımlar ve trend analizi</div></div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(fig_risk_distribution(df_f), use_container_width=True)
        with c2:
            st.plotly_chart(fig_risk_histogram(df_f), use_container_width=True)

        if "date" in col_map:
            try:
                st.plotly_chart(fig_time_trend(df_f, col_map), use_container_width=True)
            except Exception:
                pass

        c3, c4 = st.columns(2)
        with c3:
            if "vendor" in col_map and "amount" in col_map:
                try:
                    st.plotly_chart(fig_vendor_concentration(df_f, col_map), use_container_width=True)
                except Exception:
                    pass
        with c4:
            try:
                hm = fig_risk_heatmap(df_f, col_map)
                if hm:
                    st.plotly_chart(hm, use_container_width=True)
            except Exception:
                pass

        c5, c6 = st.columns(2)
        with c5:
            try:
                sc = fig_scatter_risk(df_f, col_map)
                if sc:
                    st.plotly_chart(sc, use_container_width=True)
            except Exception:
                pass
        with c6:
            try:
                ur = fig_user_risk(df_f, col_map)
                if ur:
                    st.plotly_chart(ur, use_container_width=True)
            except Exception:
                pass

        if "date" in col_map:
            try:
                wh = fig_weekday_heatmap(df_f, col_map)
                if wh:
                    st.plotly_chart(wh, use_container_width=True)
            except Exception:
                pass

        st.markdown("""
        <div class="sec-header" style="margin-top:8px;">
          <div class="sec-icon">⚠️</div>
          <div><div class="sec-title">En Riskli Kayıtlar (Top 30)</div></div>
        </div>
        """, unsafe_allow_html=True)
        top30 = df_f.nlargest(30, "risk_skoru")
        st.dataframe(top30, use_container_width=True, height=450)

    # ══════════════════════════════════════════════════════
    # TAB 3 – BENFORD & PARETO
    # ══════════════════════════════════════════════════════
    with t_benford:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">🔢</div>
          <div><div class="sec-title">Benford Yasası & Pareto Analizi</div>
               <div class="sec-subtitle">Finansal veri bütünlüğü testi ve yoğunlaşma analizi</div></div>
        </div>
        """, unsafe_allow_html=True)

        # ── Benford ──
        st.markdown("#### Benford Yasası (İlk Rakam Analizi)")
        if benford and "chi_sq" in benford:
            chi_sq   = benford.get("chi_sq", 0)
            is_anom  = benford.get("anormal", False)
            total_n  = benford.get("toplam_n", 0)

            if is_anom:
                st.error(
                    f"⚠️ **Anormal Dağılım Tespit Edildi**  ·  χ²={chi_sq:.2f} (kritik: 15.51)  ·  n={total_n:,}\n\n"
                    "Tutar verisi Benford Yasası beklentisinden istatistiksel olarak anlamlı biçimde sapıyor. "
                    "Bu durum manuel veri manipülasyonu, sahte kayıt veya sistematik hata işaretçisi olabilir."
                )
            else:
                st.success(
                    f"✅ **Normal Dağılım**  ·  χ²={chi_sq:.2f} (kritik: 15.51)  ·  n={total_n:,}\n\n"
                    "Tutar verisi Benford Yasası beklentisiyle genel olarak uyumludur."
                )

            try:
                bf_fig = fig_benford_chart(benford)
                if bf_fig:
                    st.plotly_chart(bf_fig, use_container_width=True)
            except Exception:
                pass

            # Tablo
            st.markdown("**Detaylı Benford Tablosu**")
            bf_rows = []
            for d in range(1, 10):
                info = benford[d]
                dev  = info["sapma"]
                bf_rows.append({
                    "İlk Rakam": d,
                    "Gözlemlenen %": info["gozlemlenen"],
                    "Beklenen %":    info["beklenen"],
                    "Sapma":         round(dev, 2),
                    "Adet":          info["adet"],
                    "Durum":         "🔴 Yüksek" if abs(dev)>5 else ("🟠 Orta" if abs(dev)>2 else "🟢 Normal"),
                })
            st.dataframe(pd.DataFrame(bf_rows), use_container_width=True)
        else:
            st.info("Benford analizi için en az 50 pozitif tutar değeri gereklidir.")

        st.markdown("---")

        # ── Pareto ──
        st.markdown("#### Pareto Analizi (80/20 Kuralı)")
        if "vendor" in pareto:
            p = pareto["vendor"]
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric(
                    "Tutarın %80'ini Oluşturan Tedarikçi Sayısı",
                    f"{p['vendors_80']}",
                    help=f"Toplam {len(p['data'])} tedarikçiden {p['vendors_80']}'i toplamın %80'ini oluşturuyor."
                )
            with col_p2:
                st.metric(
                    "En Büyük Tedarikçi Payı",
                    f"%{p['top_pct']:.1f}",
                    help=f"{p['top_vendor']} – Toplam: {p['total']:,.0f}"
                )

            try:
                pf = fig_pareto_chart(pareto, "vendor")
                if pf:
                    st.plotly_chart(pf, use_container_width=True)
            except Exception:
                pass

        if "user" in pareto:
            p = pareto["user"]
            st.markdown("**Kullanıcı Pareto Analizi**")
            col_pu1, col_pu2 = st.columns(2)
            with col_pu1:
                st.metric("Tutarın %80'ini Oluşturan Kullanıcı", f"{p['users_80']}")
            with col_pu2:
                st.metric("En Yoğun Kullanıcı Payı", f"%{p['top_pct']:.1f}")

    # ══════════════════════════════════════════════════════
    # TAB 4 – SENARYO SONUÇLARI
    # ══════════════════════════════════════════════════════
    with t_scenario:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">🎯</div>
          <div><div class="sec-title">Denetim Senaryo Motoru Sonuçları</div>
               <div class="sec-subtitle">Otomatik çalıştırılan 8 denetim risk senaryosu</div></div>
          <div class="sec-badge">{} Senaryo Çalıştı</div>
        </div>
        """.format(len(scenarios)), unsafe_allow_html=True)

        if not scenarios:
            st.info("Seçili filtreler dahilinde aktif senaryo tespit edilmedi.")
        else:
            # Özet tablo
            sc_df = pd.DataFrame([{
                "ID": s["id"],
                "Senaryo": s["senaryo"],
                "Risk": s["risk"],
                "Etkilenen": s["etki"],
                "Kategori": s.get("kategori",""),
            } for s in scenarios])
            st.dataframe(sc_df, use_container_width=True)
            st.markdown("---")

            for sc in scenarios:
                icon = risk_icon(sc["risk"])
                css  = css_class(sc["risk"])
                with st.expander(
                    f"{icon}  [{sc['id']}]  {sc['senaryo']}  —  **{sc['risk']}**  ·  {sc['etki']:,} kayıt",
                    expanded=(sc["risk"] == "Kritik")
                ):
                    col_sa, col_sb = st.columns([3,1])
                    with col_sa:
                        st.markdown(f"**📌 Senaryo Açıklaması**\n\n{sc['aciklama']}")
                        st.markdown(f"**⚠️ Denetim Riski Gerekçesi**\n\n{sc.get('risk_gere','—')}")
                    with col_sb:
                        st.markdown(f"""
                        <div class="stat-grid">
                          <div class="stat-item"><div class="stat-label">Risk</div>
                            <div class="stat-value"><span class="rbadge {css}">{sc['risk']}</span></div></div>
                          <div class="stat-item"><div class="stat-label">Etkilenen</div>
                            <div class="stat-value">{sc['etki']:,}</div></div>
                        </div>
                        """, unsafe_allow_html=True)
                        if "hhi" in sc:
                            st.markdown(f"**HHI:** `{sc['hhi']:.0f}`")
                    if isinstance(sc.get("ornek"), pd.DataFrame) and not sc["ornek"].empty:
                        st.markdown("**📎 Örnek Kanıt Tablosu (İlk 10 Kayıt):**")
                        st.dataframe(sc["ornek"].head(10), use_container_width=True)
                    if "sod_users" in sc:
                        st.markdown("**👤 SoD İhlali Yapan Kullanıcılar:**")
                        st.dataframe(sc["sod_users"].reset_index(), use_container_width=True)

    # ══════════════════════════════════════════════════════
    # TAB 5 – BULGULAR
    # ══════════════════════════════════════════════════════
    with t_findings:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">🔎</div>
          <div><div class="sec-title">Denetim Bulguları</div>
               <div class="sec-subtitle">IIA uyumlu yapılandırılmış bulgu listesi ve kök neden analizleri</div></div>
        </div>
        """, unsafe_allow_html=True)

        if not findings:
            st.info("Seçili filtreler dahilinde önemli bulgu tespit edilmedi.")
        else:
            # Özet tablo
            f_df = pd.DataFrame([{
                "ID": f["id"], "Bulgu": f["baslik"],
                "Risk": f["risk"], "Etkilenen": f["etki"],
                "Kategori": f["kategori"], "Kaynak": f["kaynak"],
            } for f in findings])
            st.dataframe(f_df, use_container_width=True)
            st.markdown("---")

            for i, f in enumerate(findings, 1):
                icon = risk_icon(f["risk"])
                css  = css_class(f["risk"])
                with st.expander(
                    f"{icon}  Bulgu #{i} · [{f['id']}]  {f['baslik']}  [{f['risk']}]",
                    expanded=(i <= 3)
                ):
                    col_fa, col_fb = st.columns([3,2])
                    with col_fa:
                        st.markdown(f"**📌 Bulgu**\n\n{f['bulgu']}")
                        st.markdown(f"**🔍 Kök Neden Analizi**\n\n{f['kok_neden']}")
                    with col_fb:
                        st.markdown(f"**💼 İş Etkisi**\n\n{f['is_etkisi']}")
                        st.markdown(f"**📁 Kaynak:** {f['kaynak']}")
                        st.markdown(f"**🏷 Kategori:** {f['kategori']}")
                        st.markdown(f"**⚠️ Etkilenen:** `{f['etki']:,}` kayıt")
                        st.markdown(f"<span class='rbadge {css}'>{f['risk']}</span>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════
    # TAB 6 – AKSİYON PLANLARI
    # ══════════════════════════════════════════════════════
    with t_actions:
        st.markdown("""
        <div class="sec-header">
          <div class="sec-icon">✅</div>
          <div><div class="sec-title">Düzeltici Aksiyon Planları</div>
               <div class="sec-subtitle">Standart referanslı, sorumlu birim ve süre içeren aksiyon planları</div></div>
        </div>
        """, unsafe_allow_html=True)

        if not plans:
            st.info("Aksiyon planı gerektiren bulgu yok.")
        else:
            # Özet tablo
            p_df = pd.DataFrame([{
                "ID": p["bulgu_id"], "Öncelik": p["oncelik"],
                "Sorumlu": p["birim"], "Süre": p["sure"],
                "Zorluk": p["zorluk"], "Standart": p["standart"],
            } for p in plans])
            st.dataframe(p_df, use_container_width=True)
            st.markdown("---")

            prio_colors = {
                "P1 – Acil": "#e03e3e", "P2 – Yüksek": "#d97706",
                "P3 – Orta": "#2563eb", "P4 – Düşük": "#059669",
            }
            prio_css_map = {
                "P1 – Acil":"p1","P2 – Yüksek":"p2","P3 – Orta":"p3","P4 – Düşük":"p4"
            }

            # ── Takip durumu session_state başlat ──
            if "action_tracking" not in st.session_state:
                st.session_state["action_tracking"] = {}

            for idx, p in enumerate(plans):
                icon = risk_emoji(p["risk"])
                pcss = prio_css_map.get(p["oncelik"],"p3")
                rcss = css_class(p["risk"])
                trk_key = f"{p.get('bulgu_id','')}__{idx}"
                if trk_key not in st.session_state["action_tracking"]:
                    st.session_state["action_tracking"][trk_key] = {
                        "durum": "Açık", "gerceklesen": ""
                    }

                with st.expander(
                    f"{icon}  [{p['bulgu_id']}]  {p['bulgu'][:80]}  [{p['oncelik']}]",
                    expanded=("P1" in p["oncelik"])
                ):
                    st.markdown(f"**🔧 Önerilen Aksiyon**\n\n{p['aksiyon']}")
                    col_a1, col_a2, col_a3, col_a4 = st.columns(4)
                    with col_a1:
                        st.markdown(f"**🏢 Sorumlu Birim**\n\n{p['birim']}")
                    with col_a2:
                        st.markdown(f"**⏱ Uygulama Süresi**\n\n{p['sure']}")
                    with col_a3:
                        st.markdown(f"**⚙️ Uygulama Zorluğu**\n\n{p['zorluk']}")
                    with col_a4:
                        st.markdown(f"**📚 Standart Referans**\n\n{p['standart']}")

                    # ── TAKİP FORMU ──────────────────────────────────────────
                    st.markdown("---")
                    st.markdown("**📋 Aksiyon Takibi**")
                    col_t1, col_t2 = st.columns(2)
                    with col_t1:
                        yeni_durum = st.selectbox(
                            "Durum",
                            ["Açık", "Devam Ediyor", "Kapalı"],
                            index=["Açık", "Devam Ediyor", "Kapalı"].index(
                                st.session_state["action_tracking"][trk_key]["durum"]
                            ),
                            key=f"durum_{trk_key}",
                        )
                        st.session_state["action_tracking"][trk_key]["durum"] = yeni_durum
                    with col_t2:
                        mevcut_gc = st.session_state["action_tracking"][trk_key].get("gerceklesen", "")
                        try:
                            gc_date_val = (
                                datetime.strptime(mevcut_gc, "%Y-%m-%d").date()
                                if mevcut_gc else datetime.now().date()
                            )
                        except Exception:
                            gc_date_val = datetime.now().date()
                        gerceklesen = st.date_input(
                            "Gerçekleşen Kapanış Tarihi",
                            value=gc_date_val,
                            key=f"gc_{trk_key}",
                        )
                        # Kapalı durumda tarihi kaydet, aksi halde boş bırak
                        if yeni_durum == "Kapalı":
                            st.session_state["action_tracking"][trk_key]["gerceklesen"] = str(gerceklesen)
                        else:
                            st.session_state["action_tracking"][trk_key]["gerceklesen"] = ""

            # ── Takip Özet Tablosu ────────────────────────────────────────────
            st.markdown("---")
            st.markdown("#### 📊 Aksiyon Takip Özeti")
            trk = st.session_state.get("action_tracking", {})
            acik     = sum(1 for v in trk.values() if v["durum"] == "Açık")
            devam    = sum(1 for v in trk.values() if v["durum"] == "Devam Ediyor")
            kapali   = sum(1 for v in trk.values() if v["durum"] == "Kapalı")
            col_ov1, col_ov2, col_ov3 = st.columns(3)
            col_ov1.metric("🔴 Açık", acik)
            col_ov2.metric("🟡 Devam Ediyor", devam)
            col_ov3.metric("🟢 Kapalı", kapali)

            if trk:
                summary_rows = []
                for idx2, p2 in enumerate(plans):
                    k = f"{p2.get('bulgu_id','')}__{idx2}"
                    tv = trk.get(k, {})
                    summary_rows.append({
                        "Bulgu ID": p2.get("bulgu_id",""),
                        "Aksiyon (Özet)": p2.get("aksiyon","")[:80],
                        "Sorumlu": p2.get("birim",""),
                        "Planlanan Süre": p2.get("sure",""),
                        "Durum": tv.get("durum","Açık"),
                        "Gerçekleşen Kapanış": tv.get("gerceklesen",""),
                    })
                st.dataframe(pd.DataFrame(summary_rows), use_container_width=True)

    # ══════════════════════════════════════════════════════
    # TAB 7 – GRC UYUM
    # ══════════════════════════════════════════════════════
    with t_grc:
        render_grc_tab(grc_results, findings, df_f)

    # ══════════════════════════════════════════════════════
    # TAB 8 – OPERASYONELVERİMLİLİK
    # ══════════════════════════════════════════════════════
    with t_eff:
        render_efficiency_tab(eff_metrics, df_f, col_map)

    # ══════════════════════════════════════════════════════
    # TAB 9 – DENETİM PLANI
    # ══════════════════════════════════════════════════════
    with t_plan:
        render_audit_plan_tab(audit_plan)

    # ══════════════════════════════════════════════════════
    # TAB 10 – YÖNETİCİ ÖZETİ
    # ══════════════════════════════════════════════════════
    with t_exec:
        render_executive_summary(df_f, col_map, findings, scenarios, quality, plans)

        # ── Aksiyon Takip Özeti (Yönetici Özeti'nde) ──
        trk = st.session_state.get("action_tracking", {})
        if trk or plans:
            st.markdown("---")
            st.markdown("#### 📌 Aksiyon Takip Durumu")
            acik_n  = sum(1 for v in trk.values() if v["durum"] == "Açık")
            devam_n = sum(1 for v in trk.values() if v["durum"] == "Devam Ediyor")
            kapali_n= sum(1 for v in trk.values() if v["durum"] == "Kapalı")
            tamamlanma = int(kapali_n / len(plans) * 100) if plans else 0
            c_t1, c_t2, c_t3, c_t4 = st.columns(4)
            c_t1.metric("🔴 Açık Aksiyon",    acik_n)
            c_t2.metric("🟡 Devam Ediyor",     devam_n)
            c_t3.metric("🟢 Kapalı Aksiyon",   kapali_n)
            c_t4.metric("✅ Tamamlanma Oranı", f"%{tamamlanma}")

        # ── Excel Export ──
        st.markdown("---")
        st.markdown("**📥 Kapsamlı Excel Raporu**")
        try:
            excel_bytes = build_export_excel(df_f, findings, plans, quality, scenarios)
            st.download_button(
                "📥 Tam Raporu Excel Olarak İndir (.xlsx)",
                data=excel_bytes,
                file_name=f"ic_denetim_raporu_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            st.warning(f"Excel export hazırlanamadı: {e}")

        # ── Word Export ──
        st.markdown("**📄 Profesyonel Word Raporu**")
        if DOCX_AVAILABLE:
            try:
                # Yönetici özeti verilerini hesapla (M12 ile aynı mantık)
                score_col = "risk_score" if "risk_score" in df_f.columns else None
                avg_s_w = df_f[score_col].mean() if score_col else 0
                total_w  = len(df_f)
                crit_n_w = len([f for f in findings if f["risk"] == "Kritik"])
                high_n_w = len([f for f in findings if f["risk"] == "Yüksek"])
                if avg_s_w >= 55 or crit_n_w / (total_w or 1) > .35:
                    genel_risk_w = "KRİTİK"
                    verdict_w = "Analiz sonuçları kritik düzeyde iç kontrol zafiyeti ortaya koymaktadır."
                elif avg_s_w >= 40 or (crit_n_w + high_n_w) / (total_w or 1) > .25:
                    genel_risk_w = "YÜKSEK"
                    verdict_w = "Önemli kontrol zafiyetleri tespit edilmiştir. Öncelikli aksiyon gereklidir."
                elif avg_s_w >= 25:
                    genel_risk_w = "ORTA"
                    verdict_w = "Belirli süreç alanlarında kontrol iyileştirme ihtiyacı bulunmaktadır."
                else:
                    genel_risk_w = "DÜŞÜK"
                    verdict_w = "Kontrol ortamı makul düzeyde bütünlük sergilemektedir."

                sc_text_w = " ".join(s["senaryo"].lower() for s in scenarios)
                q_text_w  = " ".join(q["kontrol"].lower() for q in quality)
                combined_w = sc_text_w + " " + q_text_w
                focus_w = []
                if "eşik" in combined_w: focus_w.append("Tutar onay limitleri ve eşik yönetim politikası revizyonu")
                if "yoğunlaşma" in combined_w: focus_w.append("Tedarikçi çeşitlendirme ve yoğunlaşma riski yönetimi")
                if "sod" in combined_w: focus_w.append("Görevler ayrılığı matrisinin tam revizyonu")
                if "mesai" in combined_w or "hafta" in combined_w: focus_w.append("Erişim kontrolü güçlendirmesi")
                if not focus_w: focus_w = ["Veri kalite yönetim süreçlerinin güçlendirilmesi"]

                dataset_name = getattr(uploaded, "name", "Demo Verisi") if uploaded else "Demo Verisi"
                word_bytes = build_word_report(
                    dataset_name=dataset_name,
                    findings=findings,
                    plans=plans,
                    genel_risk=genel_risk_w,
                    verdict=verdict_w,
                    focus_areas=focus_w,
                    tracking=st.session_state.get("action_tracking", {}),
                )
                st.download_button(
                    "📄 Tam Raporu Word Olarak İndir (.docx)",
                    data=word_bytes,
                    file_name=f"ic_denetim_raporu_{datetime.now().strftime('%Y%m%d_%H%M')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            except Exception as e:
                st.warning(f"Word raporu hazırlanamadı: {e}")
        else:
            st.info("Word raporu için: `pip install python-docx`")


# ─── Giriş Noktası ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
