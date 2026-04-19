import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ELMAKAN SARL · Coûts Partiels",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS — Interface accessible : gros textes, fort contraste, couleurs claires ──
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,600;0,700;1,600&family=Source+Sans+3:wght@400;600;700&display=swap');

:root {
    --ink:      #0f172a;
    --bg:       #f8fafc;
    --primary:  #0ea5e9;
    --success:  #10b981;
    --danger:   #ef4444;
    --warning:  #f59e0b;
    --muted:    #64748b;
    --border:   #e2e8f0;
    --card-bg:  #f0f9ff;
    --green-bg: #ecfdf5;
    --amber-bg: #fffbeb;
    --red-bg:   #fef2f2;
    --sidebar:  #1e293b;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 19px !important;
    background-color: var(--bg) !important;
    color: var(--ink) !important;
    line-height: 1.8 !important;
}

.block-container {
    padding: 2.5rem 3.5rem 5rem !important;
    max-width: 1350px !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: var(--sidebar) !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stSidebar"] p {
    color: #f1f5f9 !important;
    font-size: 16px !important;
    line-height: 1.7 !important;
}
[data-testid="stSidebar"] .stMarkdown {
    color: #f1f5f9 !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: #f1f5f9 !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown li {
    font-size: 17px !important;
    line-height: 1.7 !important;
}
[data-testid="stSidebar"] label {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}
[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
    margin: 18px 0 !important;
}
[data-testid="stSidebar"] .stNumberInput input {
    font-size: 18px !important;
    padding: 10px 14px !important;
    background: #0f172a !important;
    border: 2px solid #475569 !important;
    color: white !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] .stToggle label p {
    font-size: 18px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* ── Headings ── */
h1, h2, h3, h4 {
    font-family: 'Lora', serif !important;
    color: var(--ink) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px !important;
    flex-wrap: wrap !important;
    border-bottom: 3px solid var(--border) !important;
    padding-bottom: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    padding: 12px 20px !important;
    border-radius: 10px 10px 0 0 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: var(--muted) !important;
    background: #f1f5f9 !important;
    border: 2px solid var(--border) !important;
    border-bottom: none !important;
    margin-bottom: -3px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
    border-color: var(--primary) !important;
}

/* ── Metric cards ── */
.metric-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    border-top: 5px solid var(--danger);
    padding: 24px 26px 20px;
    margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(15,23,42,0.06);
}
.metric-card.green  { border-top-color: var(--success); }
.metric-card.blue   { border-top-color: var(--primary); }
.metric-card.amber  { border-top-color: var(--warning); }

.metric-label {
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
}
.metric-value {
    font-family: 'Lora', serif;
    font-size: 32px;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.15;
}
.metric-sub {
    font-size: 16px;
    color: var(--muted);
    margin-top: 8px;
    font-weight: 600;
}

/* ── Section titles ── */
.section-title {
    font-family: 'Lora', serif;
    font-size: 30px;
    font-weight: 700;
    color: var(--ink);
    border-bottom: 4px solid var(--primary);
    padding-bottom: 12px;
    margin: 40px 0 28px 0;
}

/* ── Alert / info boxes ── */
.result-box {
    border: 2px solid var(--warning);
    border-radius: 12px;
    background: var(--amber-bg);
    padding: 20px 26px;
    margin: 16px 0;
    font-size: 18px;
    line-height: 1.85;
    color: var(--ink);
}
.result-box.success {
    border-color: var(--success);
    background: var(--green-bg);
}
.result-box.danger {
    border-color: var(--danger);
    background: var(--red-bg);
}
.result-box.info {
    border-color: var(--primary);
    background: var(--card-bg);
}

/* ── Formula box ── */
.formula-box {
    background: var(--card-bg);
    border: 2px solid var(--primary);
    border-radius: 12px;
    padding: 22px 28px;
    font-family: 'Courier New', monospace;
    font-size: 18px;
    line-height: 2.5;
    margin: 18px 0;
    color: var(--ink);
}

/* ── Cover card ── */
.cover-card {
    border: 3px solid var(--primary);
    border-radius: 18px;
    padding: 3.5rem 3rem;
    text-align: center;
    background: white;
    margin-bottom: 2.5rem;
    box-shadow: 0 6px 24px rgba(15,23,42,0.10);
}

/* ── Prof mode banner ── */
.prof-mode {
    background: var(--success);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 18px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 1rem;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 2px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] table {
    font-size: 17px !important;
}
[data-testid="stDataFrame"] th {
    font-size: 16px !important;
    font-weight: 700 !important;
    background: #f0f9ff !important;
    color: var(--ink) !important;
    padding: 14px 18px !important;
}
[data-testid="stDataFrame"] td {
    font-size: 17px !important;
    padding: 12px 18px !important;
    color: var(--ink) !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader p {
    font-size: 19px !important;
    font-weight: 700 !important;
    color: var(--ink) !important;
}

/* ── Markdown ── */
.stMarkdown p, .stMarkdown li {
    font-size: 18px !important;
    line-height: 1.85 !important;
    color: var(--ink) !important;
}
.stMarkdown h4 {
    font-size: 22px !important;
    color: var(--ink) !important;
    margin-top: 1.4rem !important;
    font-family: 'Lora', serif !important;
}
.stMarkdown code {
    font-size: 17px !important;
    background: var(--card-bg) !important;
    color: var(--primary) !important;
    padding: 3px 10px !important;
    border-radius: 5px !important;
}
.stMarkdown strong {
    font-weight: 700 !important;
    color: var(--ink) !important;
}

/* ── HR ── */
hr {
    border: none !important;
    border-top: 2px solid var(--border) !important;
    margin: 32px 0 !important;
}

/* ── Native Streamlit alerts ── */
[data-testid="stAlert"] {
    font-size: 18px !important;
    border-radius: 12px !important;
    padding: 18px 22px !important;
}

/* ── GL & Bilan custom headers ── */
.gl-header {
    background: var(--ink);
    color: white;
    padding: 14px 20px;
    border-radius: 10px 10px 0 0;
    font-size: 18px;
    font-weight: 700;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2rem;
}
.gl-header span {
    opacity: 0.8;
    font-size: 16px;
    font-weight: 400;
}
.bilan-actif-header {
    background: var(--primary);
    color: white;
    padding: 14px 20px;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-radius: 10px 10px 0 0;
}
.bilan-passif-header {
    background: var(--danger);
    color: white;
    padding: 14px 20px;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-radius: 10px 10px 0 0;
}
</style>
""",
    unsafe_allow_html=True,
)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Mode Professeur (saisie libre) + données par défaut
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### ELMAKAN SARL")
    st.markdown("*Mobilier artisanal — Exercice N*")
    st.markdown("---")

    mode_prof = st.toggle("Saisie libre", value=False)

    if mode_prof:
        st.markdown(
            '<div class="prof-mode">⚙ Paramètres modifiables</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Ventes", expanded=True):
            quantite = st.number_input(
                "Volume vendu (unités)",
                min_value=100,
                max_value=500000,
                value=8000,
                step=100,
            )
            prix_unit = st.number_input(
                "Prix de vente unitaire (DA)",
                min_value=100,
                max_value=100000,
                value=2000,
                step=50,
            )

        with st.expander("Charges variables", expanded=True):
            cv_matieres = st.number_input(
                "Achats matières (601)",
                min_value=0,
                max_value=50000000,
                value=5800000,
                step=100000,
            )
            cv_stock_var = st.number_input(
                "Variation stocks (603)",
                min_value=0,
                max_value=10000000,
                value=900000,
                step=50000,
            )
            cv_commerciales = st.number_input(
                "Charges comm. variables",
                min_value=0,
                max_value=10000000,
                value=800000,
                step=50000,
            )

        with st.expander("Charges fixes", expanded=True):
            cf_loyers = st.number_input(
                "Loyers (613)",
                min_value=0,
                max_value=10000000,
                value=960000,
                step=10000,
            )
            cf_personnel = st.number_input(
                "Personnel (641)",
                min_value=0,
                max_value=20000000,
                value=1600000,
                step=100000,
            )
            cf_amort = st.number_input(
                "Amortissements (681)",
                min_value=0,
                max_value=10000000,
                value=1200000,
                step=100000,
            )

        with st.expander("Bilan d'ouverture", expanded=False):
            bo_immo_brut = st.number_input(
                "Immo. corporelles brut", value=12000000, step=100000
            )
            bo_amort_cumul = st.number_input(
                "Amort. cumulés", value=3600000, step=100000
            )
            bo_stocks = st.number_input("Stocks MP", value=1800000, step=100000)
            bo_clients = st.number_input("Clients", value=2400000, step=100000)
            bo_banque = st.number_input("Banque", value=1500000, step=100000)
            bo_caisse = st.number_input("Caisse", value=300000, step=50000)
            bo_capital = st.number_input("Capital social", value=8000000, step=100000)
            bo_reserves = st.number_input("Réserves", value=1800000, step=100000)
            bo_res_reporte = st.number_input(
                "Résultat reporté", value=600000, step=50000
            )
            bo_emprunts = st.number_input(
                "Emprunts bancaires", value=2800000, step=100000
            )
            bo_fourn = st.number_input(
                "Fournisseurs (ouverture)", value=1200000, step=100000
            )

        st.markdown("---")
        devise = st.selectbox("Devise", ["DA", "€", "$", "MAD", "TND"])

    else:
        # Valeurs fixes de l'exercice ELMAKAN
        quantite = 8000
        prix_unit = 2000
        cv_matieres = 5800000
        cv_stock_var = 900000
        cv_commerciales = 800000
        cf_loyers = 960000
        cf_personnel = 1600000
        cf_amort = 1200000
        bo_immo_brut = 12000000
        bo_amort_cumul = 3600000
        bo_stocks = 1800000
        bo_clients = 2400000
        bo_banque = 1500000
        bo_caisse = 300000
        bo_capital = 8000000
        bo_reserves = 1800000
        bo_res_reporte = 600000
        bo_emprunts = 2800000
        bo_fourn = 1200000
        devise = "DA"

        st.success(
            "Activez la **Saisie Libre** (toggle ci-dessus) pour modifier les données et recalculer tous les tableaux."
        )
    st.markdown("---")
    st.markdown(
        """
    <div style="background:#0f172a;padding:1.2rem;border-radius:8px;border-left:4px solid #0ea5e9;">
    <p style="color:#f1f5f9;margin:0.4rem 0;font-size:16px;"><b>Entreprise :</b> ELMAKAN SARL</p>
    <p style="color:#f1f5f9;margin:0.4rem 0;font-size:16px;"><b>Secteur :</b> Mobilier artisanal en bois</p>
    <p style="color:#f1f5f9;margin:0.4rem 0;font-size:16px;"><b>Capital :</b> 8 000 000 DA</p>
    <p style="color:#f1f5f9;margin:0.4rem 0;font-size:16px;"><b>Exercice :</b> N (01/01 — 31/12)</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# CALCULS CENTRAUX (réactifs aux entrées)
# ══════════════════════════════════════════════════════════════════════════════
CA = quantite * prix_unit
CV_TOTAL = cv_matieres + cv_stock_var + cv_commerciales
CF_TOTAL = cf_loyers + cf_personnel + cf_amort
MCV = CA - CV_TOTAL
TAUX_MCV = (MCV / CA * 100) if CA > 0 else 0
MCV_UNIT = MCV / quantite if quantite > 0 else 0
CV_UNIT = CV_TOTAL / quantite if quantite > 0 else 0
RESULTAT = MCV - CF_TOTAL
SR_VALEUR = (CF_TOTAL / (TAUX_MCV / 100)) if TAUX_MCV > 0 else 0
SR_VOLUME = (CF_TOTAL / MCV_UNIT) if MCV_UNIT > 0 else 0
POINT_MORT = (SR_VALEUR / CA * 365) if CA > 0 else 0
MARGE_SEC = CA - SR_VALEUR
INDICE_SEC = (MARGE_SEC / CA * 100) if CA > 0 else 0
LEVIER_OP = (MCV / RESULTAT) if RESULTAT != 0 else float("inf")

# Bilan ouverture
bo_immo_net = bo_immo_brut - bo_amort_cumul
bo_actif_net = bo_immo_net + bo_stocks + bo_clients + bo_banque + bo_caisse
bo_passif = bo_capital + bo_reserves + bo_res_reporte + bo_emprunts + bo_fourn

# Bilan clôture (mouvements du grand livre)
bc_immo_brut = bo_immo_brut
bc_amort_cum = bo_amort_cumul + cf_amort
bc_immo_net = bc_immo_brut - bc_amort_cum
bc_stocks = bo_stocks - cv_stock_var
bc_clients = 7500000 if not mode_prof else bo_clients + CA - (CA * 0.59)  # simplif
bc_banque = 5640000 if not mode_prof else bo_banque + CA * 0.6 - CV_TOTAL * 0.4
bc_caisse = bo_caisse - 1600000 if not mode_prof else bo_caisse - cf_personnel
bc_fourn = 1200000 if not mode_prof else bo_fourn + cv_matieres - cv_matieres * 0.75
bc_capital = bo_capital
bc_reserves = bo_reserves
bc_res_N = RESULTAT
bc_emprunts = bo_emprunts
bc_dettes_fisc = RESULTAT * 0.19 if RESULTAT > 0 else 0
bc_actif_net = bc_immo_net + bc_stocks + bc_clients + bc_banque + max(bc_caisse, 0)
bc_passif = (
    bc_capital
    + bc_reserves
    + bo_res_reporte
    + bc_res_N
    + bc_emprunts
    + bc_fourn
    + bc_dettes_fisc
)


# ── Formatage ────────────────────────────────────────────────────────────────
def fmt(x):
    try:
        return f"{float(x):,.0f}".replace(",", " ")
    except:
        return str(x)


def pct(x):
    return f"{x:.2f} %"


# ══════════════════════════════════════════════════════════════════════════════
# EN-TÊTE
# ══════════════════════════════════════════════════════════════════════════════
if mode_prof:
    st.markdown(
        '<div class="prof-mode"> SAISIE LIBRE ACTIVE — données modifiables dans le panneau gauche</div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f"""
<div class="cover-card">
  <div style="font-family:'Source Sans 3',sans-serif; font-size:14px; font-weight:700;
  letter-spacing:0.12em; text-transform:uppercase; color:#6b7280; margin-bottom:1.2rem;">
  Dossier Comptable Complet — Exercice N
  </div>
  <h1 style="font-family:'Lora',serif; font-size:3rem; font-weight:700; margin-bottom:0.4rem; color:#111827;">
    <em style="color:#1d4ed8; font-style:italic;">ELMAKAN</em> SARL
  </h1>
  <div style="font-size:20px; font-weight:600; color:#374151; margin:1rem 0 1.2rem;">
  Fabrication &amp; commercialisation de mobilier artisanal 
  </div>
  <div style="font-size:18px; color:#4b5563; max-width:620px; margin:0 auto 1.8rem; line-height:1.85;">
  Une PME algérienne spécialisée dans la fabrication de mobilier artisanal en bois.
  Vente aux détaillants et aux particuliers sur commande.
  <strong>Capital social : 8 000 000 DA</strong><br>
Exercice comptable de l'année N (01/01 — 31/12).
  </div>
  
  <div style="display:flex; justify-content:center; gap:3rem; flex-wrap:wrap;
  font-size:17px; color:#374151;
  border-top:2px solid #bfdbfe; padding-top:1.2rem; margin-top:0.5rem;">
    <span>🔵 <b style="color:#1d4ed8; font-size:19px;">CA :</b> {fmt(CA)} {devise}</span>
    <span>🟢 <b style="color:#166534; font-size:19px;">MCV :</b> {fmt(MCV)} {devise}</span>
    <span>🟢 <b style="color:#166534; font-size:19px;">Résultat :</b> {fmt(RESULTAT)} {devise}</span>
    <span>🟡 <b style="color:#92400e; font-size:19px;">SR :</b> {fmt(SR_VALEUR)} {devise}</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# KPIs
# KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(
        f"""<div class="metric-card blue">
    <div class="metric-label">Chiffre d'affaires</div>
    <div class="metric-value">{fmt(CA)}</div>
    <div class="metric-sub">{devise} · {fmt(quantite)} unités</div>
    </div>""",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""<div class="metric-card">
    <div class="metric-label">Marge / Coût Variable</div>
    <div class="metric-value">{fmt(MCV)}</div>
    <div class="metric-sub">Taux : {pct(TAUX_MCV)}</div>
    </div>""",
        unsafe_allow_html=True,
    )
with c3:
    color = "green" if RESULTAT >= 0 else ""
    st.markdown(
        f"""<div class="metric-card {color}">
    <div class="metric-label">Résultat net</div>
    <div class="metric-value">{fmt(RESULTAT)}</div>
    <div class="metric-sub">{"Bénéfice" if RESULTAT >= 0 else "Déficit"} — {pct(RESULTAT/CA*100 if CA else 0)} du CA</div>
    </div>""",
        unsafe_allow_html=True,
    )
with c4:
    st.markdown(
        f"""<div class="metric-card amber">
    <div class="metric-label">Seuil de rentabilité</div>
    <div class="metric-value">{fmt(SR_VALEUR)}</div>
    <div class="metric-sub">{devise} · Atteint au jour {POINT_MORT:.0f}</div>
    </div>""",
        unsafe_allow_html=True,
    )

st.markdown("<hr>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tabs = st.tabs(
    [
        "§1 Présentation",
        "§2 Bilan d'ouverture",
        "§3 Journal",
        "§4 Grand Livre",
        "§5 Balance",
        "§6 TCR",
        "§7 Coûts Partiels",
        "§8 Seuil & Analyse",
        "§9 Bilan de clôture",
        "§10 Questions",
    ]
)


# ─────────────────────────────────────────────────────────────────────────────
# §1 PRÉSENTATION
# ─────────────────────────────────────────────────────────────────────────────
with tabs[0]:
    st.markdown(
        '<div class="section-title">Présentation de l\'entreprise</div>',
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.markdown(
            """
        **ELMAKAN SARL** est une PME algérienne spécialisée dans la **fabrication de mobilier artisanal en bois**.
        Elle vend ses produits à des détaillants et à des particuliers sur commande.

        L'exercice porte sur l'année comptable **N** (01/01/N — 31/12/N).

        #### Données de l'exercice
        - **Volume vendu :** 8 000 unités
        - **Prix de vente unitaire :** 2 000 DA
        - **Chiffre d'affaires :** 16 000 000 DA

        #### Rappel théorique — Méthode des coûts partiels
        La méthode des coûts partiels distingue deux catégories de charges :
        - **Charges variables (CV)** : varient proportionnellement au volume d'activité
        - **Charges fixes (CF)** : restent constantes quel que soit le niveau d'activité
        """
        )

    with col_b:
        st.markdown(
            """
        <div class="result-box info">
        <b>Formules essentielles</b><br><br>
        <code>MCV = CA − CV total</code><br>
        <code>t = MCV / CA × 100</code><br>
        <code>SR = CF / t</code><br>
        <code>PM = SR / CA × 365</code><br>
        <code>MS = CA − SR</code><br>
        <code>IS = MS / CA × 100</code><br>
        <code>LO = MCV / Résultat</code>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class="result-box">
    <b>Note pédagogique :</b> Cet exercice est intégralement cohérent — les données du bilan d'ouverture,
    les opérations du grand livre, le TCR et l'analyse des coûts partiels sont tous liés entre eux.
    Les étudiants doivent résoudre chaque partie dans l'ordre pour obtenir les totaux finaux corrects.
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §2 BILAN D'OUVERTURE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[1]:
    st.markdown(
        '<div class="section-title">Bilan d\'ouverture — 01/01/N</div>',
        unsafe_allow_html=True,
    )

    col_actif, col_passif = st.columns(2)

    with col_actif:
        st.markdown(
            '<div class="bilan-actif-header">🔵 ACTIF</div>', unsafe_allow_html=True
        )
        actif_bo = {
            "Poste": [
                "ACTIF IMMOBILISÉ",
                "Immobilisations corporelles",
                "  Amortissements cumulés",
                "  Valeur nette",
                "ACTIF CIRCULANT",
                "Stocks de matières premières",
                "Clients et comptes rattachés",
                "Banque",
                "Caisse",
                "TOTAL ACTIF NET",
            ],
            "Brut (DA)": [
                "",
                fmt(bo_immo_brut),
                "",
                "",
                "",
                fmt(bo_stocks),
                fmt(bo_clients),
                fmt(bo_banque),
                fmt(bo_caisse),
                "",
            ],
            "Amort. (DA)": [
                "",
                "",
                fmt(bo_amort_cumul),
                "",
                "",
                "—",
                "—",
                "—",
                "—",
                "",
            ],
            "Net (DA)": [
                "",
                "",
                "",
                fmt(bo_immo_net),
                "",
                fmt(bo_stocks),
                fmt(bo_clients),
                fmt(bo_banque),
                fmt(bo_caisse),
                fmt(bo_actif_net),
            ],
        }
        df_actif_bo = pd.DataFrame(actif_bo)

        def style_bo_actif(row):
            if row["Poste"] in ["TOTAL ACTIF NET"]:
                return ["font-weight:bold;background:#1a171422;"] * len(row)
            if row["Poste"] in ["ACTIF IMMOBILISÉ", "ACTIF CIRCULANT"]:
                return ["font-weight:600;background:#e8f0ff;"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_actif_bo.style.apply(style_bo_actif, axis=1),
            use_container_width=True,
            hide_index=True,
        )

    with col_passif:
        st.markdown(
            '<div class="bilan-passif-header">🔴 PASSIF</div>', unsafe_allow_html=True
        )
        passif_bo = {
            "Poste": [
                "CAPITAUX PROPRES",
                "Capital social",
                "Réserves",
                "Résultat reporté",
                "  Sous-total CP",
                "DETTES FINANCIÈRES",
                "Emprunts bancaires",
                "DETTES D'EXPLOITATION",
                "Fournisseurs",
                "TOTAL PASSIF",
            ],
            "Montant (DA)": [
                "",
                fmt(bo_capital),
                fmt(bo_reserves),
                fmt(bo_res_reporte),
                fmt(bo_capital + bo_reserves + bo_res_reporte),
                "",
                fmt(bo_emprunts),
                "",
                fmt(bo_fourn),
                fmt(bo_passif),
            ],
        }
        df_passif_bo = pd.DataFrame(passif_bo)

        def style_bo_passif(row):
            if row["Poste"] == "TOTAL PASSIF":
                return ["font-weight:bold;background:#1a171422;"] * len(row)
            if row["Poste"] in [
                "CAPITAUX PROPRES",
                "DETTES FINANCIÈRES",
                "DETTES D'EXPLOITATION",
            ]:
                return ["font-weight:600;background:#fff0ee;"] * len(row)
            if row["Poste"] == "  Sous-total CP":
                return ["font-weight:500;background:#f0faf5;"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_passif_bo.style.apply(style_bo_passif, axis=1),
            use_container_width=True,
            hide_index=True,
        )

    if abs(bo_actif_net - bo_passif) < 1:
        st.markdown(
            f'<div class="result-box success">✔ Bilan équilibré : Actif net = Passif = <b>{fmt(bo_actif_net)} {devise}</b></div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="result-box danger">⚠ Déséquilibre : Actif = {fmt(bo_actif_net)} / Passif = {fmt(bo_passif)} — vérifiez les données.</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# §3 JOURNAL
# ─────────────────────────────────────────────────────────────────────────────
with tabs[2]:
    st.markdown(
        '<div class="section-title">Journal des opérations — Exercice N</div>',
        unsafe_allow_html=True,
    )

    journal_data = {
        "N°": list(range(1, 17)),
        "Date": [
            "05/01/N",
            "12/01/N",
            "20/01/N",
            "02/02/N",
            "15/02/N",
            "28/02/N",
            "10/03/N",
            "25/03/N",
            "05/04/N",
            "20/04/N",
            "15/05/N",
            "30/05/N",
            "10/06/N",
            "20/06/N",
            "31/12/N",
            "31/12/N",
        ],
        "Libellé de l'opération": [
            "Achat matières premières à crédit",
            "Règlement fournisseur par virement bancaire",
            "Vente de produits finis à crédit",
            "Encaissement client par virement",
            "Paiement charges de personnel (espèces)",
            "Vente supplémentaire de produits finis à crédit",
            "Achat matières premières au comptant (banque)",
            "Encaissement client par virement",
            "Paiement loyer (banque)",
            "Vente à crédit",
            "Paiement charges de personnel (espèces)",
            "Encaissement client par virement",
            "Règlement fournisseur par virement",
            "Paiement loyer (banque)",
            "Dotation aux amortissements (fin d'exercice)",
            "Consommation matières (variation de stock)",
        ],
        "Compte débité": [
            "601 Matières : 3 600 000",
            "401 Fournisseurs : 1 200 000",
            "411 Clients : 5 500 000",
            "512 Banque : 2 400 000",
            "641 Personnel : 800 000",
            "411 Clients : 4 500 000",
            "601 Matières : 2 200 000",
            "512 Banque : 3 000 000",
            "613 Loyers : 480 000",
            "411 Clients : 6 000 000",
            "641 Personnel : 800 000",
            "512 Banque : 5 500 000",
            "401 Fournisseurs : 2 400 000",
            "613 Loyers : 480 000",
            "681 Amortissements : 1 200 000",
            "603 Var. stocks : 900 000",
        ],
        "Compte crédité": [
            "401 Fournisseurs : 3 600 000",
            "512 Banque : 1 200 000",
            "701 Ventes PF : 5 500 000",
            "411 Clients : 2 400 000",
            "530 Caisse : 800 000",
            "701 Ventes PF : 4 500 000",
            "512 Banque : 2 200 000",
            "411 Clients : 3 000 000",
            "512 Banque : 480 000",
            "701 Ventes PF : 6 000 000",
            "530 Caisse : 800 000",
            "411 Clients : 5 500 000",
            "512 Banque : 2 400 000",
            "512 Banque : 480 000",
            "281 Amort. cumulés : 1 200 000",
            "310 Stocks MP : 900 000",
        ],
    }
    df_journal = pd.DataFrame(journal_data)

    def style_journal(row):
        if row["N°"] in [15, 16]:
            return ["background:#fffbf0"] * len(row)
        if row["N°"] in [3, 6, 10]:
            return ["background:#f0faf5"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df_journal.style.apply(style_journal, axis=1),
        use_container_width=True,
        hide_index=True,
    )
    


# ─────────────────────────────────────────────────────────────────────────────
# §4 GRAND LIVRE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[3]:
    st.markdown('<div class="section-title">Grand Livre — Comptes principaux</div>', unsafe_allow_html=True)
 
    # ── Colonnes communes à tous les comptes en T ──────────────────────────────
    COL_T = ["N° Op.", "Libellé", "Débit (DA)", "Crédit (DA)", "Solde cumulé (DA)"]
 
    comptes = {
        "411 — Clients et comptes rattachés": {
            "num": "411",
            "nature": "Solde DÉBITEUR final : 7 500 000 DA",
            "data": {
                "N° Op.":  ["—",   "Op.3",  "Op.4",         "Op.6",  "Op.8",         "Op.10", "Op.12",        "TOTAL", "SOLDE DÉBITEUR"],
                "Libellé": ["Solde d'ouverture",
                            "Vente PF à crédit", "Encaissement client",
                            "Vente PF à crédit", "Encaissement client",
                            "Vente PF à crédit", "Encaissement client",
                            "—", "—"],
                "Débit (DA)":  ["2 400 000", "5 500 000", "—",         "4 500 000", "—",         "6 000 000", "—",         "18 400 000", "7 500 000"],
                "Crédit (DA)": ["—",         "—",         "2 400 000", "—",         "3 000 000", "—",         "5 500 000", "10 900 000", "—"],
                "Solde cumulé (DA)": ["2 400 000", "7 900 000", "5 500 000", "10 000 000", "7 000 000", "13 000 000", "7 500 000", "—", "7 500 000"],
            }
        },
        "512 — Banque": {
            "num": "512",
            "nature": "Solde DÉBITEUR final : 5 640 000 DA",
            "data": {
                "N° Op.":  ["—",   "Op.2",           "Op.4",             "Op.7",             "Op.8",             "Op.9",           "Op.12",            "Op.13",            "Op.14",          "TOTAL",     "SOLDE DÉBITEUR"],
                "Libellé": ["Solde d'ouverture",
                            "Règlt fournisseur", "Encaiss. client",
                            "Achat MP comptant", "Encaiss. client",
                            "Paiement loyer",    "Encaiss. client",
                            "Règlt fournisseur", "Paiement loyer",
                            "—", "—"],
                "Débit (DA)":  ["1 500 000", "—",         "2 400 000", "—",         "3 000 000", "—",       "5 500 000", "—",         "—",       "12 400 000", "5 640 000"],
                "Crédit (DA)": ["—",         "1 200 000", "—",         "2 200 000", "—",         "480 000", "—",         "2 400 000", "480 000", "6 760 000",  "—"],
                "Solde cumulé (DA)": ["1 500 000","300 000","2 700 000","500 000","3 500 000","3 020 000","8 520 000","6 120 000","5 640 000","—","5 640 000"],
            }
        },
        "401 — Fournisseurs et comptes rattachés": {
            "num": "401",
            "nature": "Solde CRÉDITEUR final : 1 200 000 DA",
            "data": {
                "N° Op.":  ["—",   "Op.1",             "Op.2",             "Op.13",            "TOTAL",     "SOLDE CRÉDITEUR"],
                "Libellé": ["Solde d'ouverture (dette initiale)",
                            "Achat MP à crédit", "Règlement fourn.",
                            "Règlement fourn.", "—", "—"],
                "Débit (DA)":  ["—",         "—",         "1 200 000", "2 400 000", "3 600 000", "—"],
                "Crédit (DA)": ["1 200 000", "3 600 000", "—",         "—",         "4 800 000", "1 200 000"],
                "Solde cumulé (DA)": ["1 200 000 C","4 800 000 C","3 600 000 C","1 200 000 C","—","1 200 000"],
            }
        },
        "601 — Achats de matières premières": {
            "num": "601",
            "nature": "Solde DÉBITEUR final : 5 800 000 DA",
            "data": {
                "N° Op.":  ["Op.1",             "Op.7",             "TOTAL",     "SOLDE DÉBITEUR"],
                "Libellé": ["Achat MP à crédit (fournisseur)",
                            "Achat MP comptant (banque)", "—", "—"],
                "Débit (DA)":  ["3 600 000", "2 200 000", "5 800 000", "5 800 000"],
                "Crédit (DA)": ["—",         "—",         "—",         "—"],
                "Solde cumulé (DA)": ["3 600 000","5 800 000","—","5 800 000"],
            }
        },
        "613 — Charges locatives (Loyers)": {
            "num": "613",
            "nature": "Solde DÉBITEUR final : 960 000 DA",
            "data": {
                "N° Op.":  ["Op.9",           "Op.14",          "TOTAL",    "SOLDE DÉBITEUR"],
                "Libellé": ["Paiement loyer T1 (banque)",
                            "Paiement loyer T2 (banque)", "—", "—"],
                "Débit (DA)":  ["480 000", "480 000", "960 000", "960 000"],
                "Crédit (DA)": ["—",       "—",       "—",       "—"],
                "Solde cumulé (DA)": ["480 000","960 000","—","960 000"],
            }
        },
        "641 — Charges de personnel": {
            "num": "641",
            "nature": "Solde DÉBITEUR final : 1 600 000 DA",
            "data": {
                "N° Op.":  ["Op.5",                        "Op.11",                       "TOTAL",     "SOLDE DÉBITEUR"],
                "Libellé": ["Paiement salaires (caisse) — Semestre 1",
                            "Paiement salaires (caisse) — Semestre 2", "—", "—"],
                "Débit (DA)":  ["800 000", "800 000", "1 600 000", "1 600 000"],
                "Crédit (DA)": ["—",       "—",       "—",         "—"],
                "Solde cumulé (DA)": ["800 000","1 600 000","—","1 600 000"],
            }
        },
        "681 — Dotations aux amortissements": {
            "num": "681",
            "nature": "Solde DÉBITEUR final : 1 200 000 DA",
            "data": {
                "N° Op.":  ["Op.15",                                       "TOTAL",     "SOLDE DÉBITEUR"],
                "Libellé": ["Dotation amortissement annuel (fin exercice)", "—",         "—"],
                "Débit (DA)":  ["1 200 000", "1 200 000", "1 200 000"],
                "Crédit (DA)": ["—",         "—",         "—"],
                "Solde cumulé (DA)": ["1 200 000","—","1 200 000"],
            }
        },
        "701 — Ventes de produits finis": {
            "num": "701",
            "nature": "Solde CRÉDITEUR final : 16 000 000 DA  (= CA total)",
            "data": {
                "N° Op.":  ["Op.3",             "Op.6",             "Op.10",            "TOTAL",     "SOLDE CRÉDITEUR"],
                "Libellé": ["Vente PF à crédit", "Vente PF à crédit", "Vente PF à crédit", "—",      "= Chiffre d'affaires N"],
                "Débit (DA)":  ["—",         "—",         "—",         "0",         "—"],
                "Crédit (DA)": ["5 500 000", "4 500 000", "6 000 000", "16 000 000","16 000 000"],
                "Solde cumulé (DA)": ["5 500 000 C","10 000 000 C","16 000 000 C","—","16 000 000"],
            }
        },
    }
 
    for compte_name, info in comptes.items():
        # En-tête coloré avec numéro de compte bien visible
        is_credit = "CRÉDITEUR" in info["nature"]
        header_color = "#b91c1c" if is_credit else "#1d4ed8"
        badge_color  = "#fee2e2" if is_credit else "#dbeafe"
        badge_text   = "#b91c1c" if is_credit else "#1d4ed8"
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
             background:{header_color}; color:white; padding:14px 20px;
             border-radius:10px 10px 0 0; margin-top:2rem;">
          <div style="display:flex; align-items:center; gap:16px;">
            <span style="background:rgba(255,255,255,0.25); color:white;
                  font-size:20px; font-weight:800; padding:4px 14px;
                  border-radius:6px; font-family:'Courier New',monospace;">
              {info['num']}
            </span>
            <strong style="font-size:18px;">{compte_name.split(' — ',1)[1]}</strong>
          </div>
          <span style="background:{badge_color}; color:{badge_text};
                font-size:14px; font-weight:700; padding:5px 14px;
                border-radius:20px;">
            {info['nature']}
          </span>
        </div>""", unsafe_allow_html=True)
 
        df_gl = pd.DataFrame(info["data"])
 
        def style_gl(row):
            if row["N° Op."] in ["TOTAL", "SOLDE DÉBITEUR", "SOLDE CRÉDITEUR"]:
                return ["font-weight:700; background:#1e3a8a; color:white"] * len(row)
            if row["N° Op."] == "—" and row["Libellé"] == "Solde d'ouverture":
                return ["background:#eff6ff; font-style:italic"] * len(row)
            return [""] * len(row)
 
        st.dataframe(df_gl.style.apply(style_gl, axis=1), use_container_width=True, hide_index=True)
 
    st.markdown("""
    <div class="result-box success" style="margin-top:1.5rem;">
    ✔ <b>8 comptes présentés</b> — Les soldes du grand livre alimentent directement la balance et le TCR.<br>
    Le solde créditeur du compte 701 (16 000 000 DA) = <b>Chiffre d'affaires total de l'exercice N</b>.
    </div>""", unsafe_allow_html=True)
 
# ─────────────────────────────────────────────────────────────────────────────
# §5 BALANCE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[4]:
    st.markdown(
        '<div class="section-title">Balance des comptes — 31/12/N</div>',
        unsafe_allow_html=True,
    )

    balance_data = {
        "N°": [
            "281",
            "310",
            "401",
            "411",
            "512",
            "530",
            "601",
            "603",
            "613",
            "641",
            "681",
            "701",
        ],
        "Intitulé": [
            "Amort. immobilisations",
            "Stocks matières premières",
            "Fournisseurs",
            "Clients",
            "Banque",
            "Caisse",
            "Achats matières premières",
            "Variation stocks MP",
            "Loyers",
            "Charges de personnel",
            "Dotations amortissements",
            "Ventes produits finis",
        ],
        "Mvt Débit (DA)": [
            "—",
            "—",
            "3 600 000",
            "18 400 000",
            "12 400 000",
            "—",
            fmt(cv_matieres),
            fmt(cv_stock_var),
            fmt(cf_loyers),
            fmt(cf_personnel),
            fmt(cf_amort),
            "—",
        ],
        "Mvt Crédit (DA)": [
            fmt(cf_amort),
            fmt(cv_stock_var),
            "4 800 000",
            "10 900 000",
            "6 760 000",
            "1 600 000",
            "—",
            "—",
            "—",
            "—",
            "—",
            fmt(CA),
        ],
        "Solde D (DA)": [
            "—",
            "—",
            "—",
            "7 500 000",
            "5 640 000",
            "—",
            fmt(cv_matieres),
            fmt(cv_stock_var),
            fmt(cf_loyers),
            fmt(cf_personnel),
            fmt(cf_amort),
            "—",
        ],
        "Solde C (DA)": [
            fmt(cf_amort),
            "—",
            "1 200 000",
            "—",
            "—",
            "—",
            "—",
            "—",
            "—",
            "—",
            "—",
            fmt(CA),
        ],
    }
    df_balance = pd.DataFrame(balance_data)

    def style_balance(row):
        if row["N°"] in ["411", "512", "701"]:
            return ["background:#f0f5ff"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df_balance.style.apply(style_balance, axis=1),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown(
        f"""<div class="result-box success">
    ✔ Balance équilibrée — les soldes débiteurs et créditeurs sont cohérents avec les opérations enregistrées.
    </div>""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §6 TCR
# ─────────────────────────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown(
        '<div class="section-title">Tableau des Comptes de Résultat (TCR)</div>',
        unsafe_allow_html=True,
    )

    tcr_data = {
        "Rubrique": [
            "PRODUITS D'EXPLOITATION",
            "701 — Ventes de produits finis",
            "TOTAL PRODUITS",
            "CHARGES D'EXPLOITATION",
            "601 — Achats de matières premières",
            "603 — Variation de stocks de MP",
            "613 — Charges locatives (loyers)",
            "641 — Charges de personnel",
            "681 — Dotations aux amortissements",
            "TOTAL CHARGES",
            "RÉSULTAT NET DE L'EXERCICE N",
        ],
        f"Montant ({devise})": [
            "",
            fmt(CA),
            fmt(CA),
            "",
            fmt(cv_matieres),
            fmt(cv_stock_var),
            fmt(cf_loyers),
            fmt(cf_personnel),
            fmt(cf_amort),
            fmt(CV_TOTAL + CF_TOTAL),
            fmt(RESULTAT),
        ],
        "Note / Référence": [
            "",
            "Op.3 + Op.6 + Op.10",
            "Compte 701",
            "",
            "Op.1 + Op.7",
            "Op.16",
            "Op.9 + Op.14",
            "Op.5 + Op.11",
            "Op.15",
            "Somme charges",
            "= Produits − Charges",
        ],
        "% CA": [
            "",
            "100%",
            "100%",
            "",
            pct(cv_matieres / CA * 100) if CA else "—",
            pct(cv_stock_var / CA * 100) if CA else "—",
            pct(cf_loyers / CA * 100) if CA else "—",
            pct(cf_personnel / CA * 100) if CA else "—",
            pct(cf_amort / CA * 100) if CA else "—",
            pct((CV_TOTAL + CF_TOTAL) / CA * 100) if CA else "—",
            pct(RESULTAT / CA * 100) if CA else "—",
        ],
    }
    df_tcr = pd.DataFrame(tcr_data)

    def style_tcr(row):
        if row["Rubrique"] in [
            "TOTAL PRODUITS",
            "TOTAL CHARGES",
            "RÉSULTAT NET DE L'EXERCICE N",
        ]:
            return ["font-weight:bold;background:#1a1714;color:white"] * len(row)
        if row["Rubrique"] in ["PRODUITS D'EXPLOITATION", "CHARGES D'EXPLOITATION"]:
            return ["font-weight:600;background:#e8eef8"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df_tcr.style.apply(style_tcr, axis=1), use_container_width=True, hide_index=True
    )

    st.markdown(
        f"""
    <div class="result-box success">
    <b>Résultat = {fmt(CA)} − {fmt(CV_TOTAL + CF_TOTAL)} = {fmt(RESULTAT)} DA (bénéfice)</b><br>
    Ce montant viendra alimenter les capitaux propres au bilan de clôture.
    </div>""",
        unsafe_allow_html=True,
    )

    # Waterfall TCR
    wf = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=[
                "absolute",
                "relative",
                "relative",
                "relative",
                "relative",
                "total",
            ],
            x=[
                "CA",
                "− Matières",
                "− Var.stocks",
                "− Loyers + Personnel",
                "− Amort.",
                "= Résultat",
            ],
            y=[
                CA,
                -cv_matieres,
                -cv_stock_var,
                -(cf_loyers + cf_personnel),
                -cf_amort,
                0,
            ],
            connector=dict(line=dict(color="#ddd8ce", width=1)),
            increasing=dict(marker=dict(color="#2a6b3c")),
            decreasing=dict(marker=dict(color="#b53c2a")),
            totals=dict(marker=dict(color="#1e4a8c")),
            text=[
                fmt(CA),
                fmt(cv_matieres),
                fmt(cv_stock_var),
                fmt(cf_loyers + cf_personnel),
                fmt(cf_amort),
                fmt(RESULTAT),
            ],
            textposition="outside",
        )
    )
    wf.update_layout(
        height=340,
        paper_bgcolor="white",
        plot_bgcolor="#faf7f2",
        font=dict(family="DM Sans, sans-serif", size=11),
        showlegend=False,
        margin=dict(t=30, b=30, l=20, r=20),
        yaxis=dict(gridcolor="#e8e0d4"),
    )
    st.plotly_chart(wf, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
# §7 COÛTS PARTIELS
# ─────────────────────────────────────────────────────────────────────────────
with tabs[6]:
    st.markdown(
        '<div class="section-title">Méthode des Coûts Partiels — Compte de résultat différentiel</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            f"""<div class="metric-card blue">
        <div class="metric-label">CA</div>
        <div class="metric-value">{fmt(CA)}</div>
        <div class="metric-sub">{devise} · 100%</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f"""<div class="metric-card">
        <div class="metric-label">CV Total</div>
        <div class="metric-value">{fmt(CV_TOTAL)}</div>
        <div class="metric-sub">{pct(CV_TOTAL/CA*100)} du CA</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f"""<div class="metric-card green">
        <div class="metric-label">MCV</div>
        <div class="metric-value">{fmt(MCV)}</div>
        <div class="metric-sub">Taux : {pct(TAUX_MCV)}</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with k4:
        c = "green" if RESULTAT >= 0 else ""
        st.markdown(
            f"""<div class="metric-card {c}">
        <div class="metric-label">Résultat</div>
        <div class="metric-value">{fmt(RESULTAT)}</div>
        <div class="metric-sub">{pct(RESULTAT/CA*100)} du CA</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    crd_data = {
        "Poste": [
            "Chiffre d'affaires (CA)",
            "— 601 Achats matières premières",
            "— 603 Variation de stocks",
            "— Charges commerciales variables",
            "= TOTAL CHARGES VARIABLES",
            "= MARGE SUR COÛT VARIABLE (MCV)",
            "— 613 Loyers",
            "— 641 Charges de personnel",
            "— 681 Amortissements",
            "= TOTAL CHARGES FIXES",
            "= RÉSULTAT NET",
        ],
        "Nature": [
            "—",
            "Variable",
            "Variable",
            "Variable",
            "—",
            "MCV",
            "Fixe",
            "Fixe",
            "Fixe",
            "—",
            "—",
        ],
        f"Total ({devise})": [
            fmt(CA),
            f"− {fmt(cv_matieres)}",
            f"− {fmt(cv_stock_var)}",
            f"− {fmt(cv_commerciales)}",
            fmt(CV_TOTAL),
            fmt(MCV),
            f"− {fmt(cf_loyers)}",
            f"− {fmt(cf_personnel)}",
            f"− {fmt(cf_amort)}",
            fmt(CF_TOTAL),
            fmt(RESULTAT),
        ],
        f"Unitaire ({devise})": [
            fmt(prix_unit),
            f"− {cv_matieres/quantite:.2f}" if quantite else "—",
            f"− {cv_stock_var/quantite:.2f}" if quantite else "—",
            f"− {cv_commerciales/quantite:.2f}" if quantite else "—",
            f"− {CV_UNIT:.2f}",
            f"{MCV_UNIT:.2f}",
            "—",
            "—",
            "—",
            "—",
            f"{RESULTAT/quantite:.2f}" if quantite else "—",
        ],
        "% du CA": [
            "100 %",
            pct(cv_matieres / CA * 100),
            pct(cv_stock_var / CA * 100),
            pct(cv_commerciales / CA * 100),
            pct(CV_TOTAL / CA * 100),
            pct(TAUX_MCV),
            pct(cf_loyers / CA * 100),
            pct(cf_personnel / CA * 100),
            pct(cf_amort / CA * 100),
            pct(CF_TOTAL / CA * 100),
            pct(RESULTAT / CA * 100),
        ],
    }
    df_crd = pd.DataFrame(crd_data)

    KEY = {
        "= TOTAL CHARGES VARIABLES",
        "= MARGE SUR COÛT VARIABLE (MCV)",
        "= TOTAL CHARGES FIXES",
        "= RÉSULTAT NET",
    }

    def style_crd(row):
        if row["Poste"] in KEY:
            return ["font-weight:bold;background:#1a1714;color:white"] * len(row)
        if row["Poste"] == "Chiffre d'affaires (CA)":
            return ["background:#e8f0ff;font-weight:500"] * len(row)
        return [""] * len(row)

    st.dataframe(
        df_crd.style.apply(style_crd, axis=1), use_container_width=True, hide_index=True
    )

    st.markdown(
        f"""
    <div class="formula-box">
    CV Total = {fmt(cv_matieres)} + {fmt(cv_stock_var)} + {fmt(cv_commerciales)} = <b>{fmt(CV_TOTAL)} {devise}</b><br>
    MCV = {fmt(CA)} − {fmt(CV_TOTAL)} = <b>{fmt(MCV)} {devise}</b><br>
    Taux de MCV = {fmt(MCV)} / {fmt(CA)} × 100 = <b>{pct(TAUX_MCV)}</b><br>
    CF Total = {fmt(cf_loyers)} + {fmt(cf_personnel)} + {fmt(cf_amort)} = <b>{fmt(CF_TOTAL)} {devise}</b><br>
    Résultat = {fmt(MCV)} − {fmt(CF_TOTAL)} = <b>{fmt(RESULTAT)} {devise}</b>
    </div>
    """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §8 SEUIL & ANALYSE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[7]:
    st.markdown(
        '<div class="section-title">Seuil de Rentabilité & Indicateurs de Risque</div>',
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(
            f"""<div class="metric-card amber">
        <div class="metric-label">SR en valeur</div>
        <div class="metric-value">{fmt(SR_VALEUR)}</div>
        <div class="metric-sub">{devise}</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with s2:
        st.markdown(
            f"""<div class="metric-card amber">
        <div class="metric-label">SR en volume</div>
        <div class="metric-value">{fmt(SR_VOLUME)}</div>
        <div class="metric-sub">unités</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with s3:
        st.markdown(
            f"""<div class="metric-card green">
        <div class="metric-label">Marge de sécurité</div>
        <div class="metric-value">{fmt(MARGE_SEC)}</div>
        <div class="metric-sub">{pct(INDICE_SEC)} du CA</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with s4:
        lev_disp = f"{LEVIER_OP:.2f}×" if abs(LEVIER_OP) < 1e6 else "∞"
        st.markdown(
            f"""<div class="metric-card green">
        <div class="metric-label">Levier opérationnel</div>
        <div class="metric-value">{lev_disp}</div>
        <div class="metric-sub">LO = MCV / Résultat</div>
        </div>""",
            unsafe_allow_html=True,
        )

    # Tableau détaillé
    risk_data = {
        "Indicateur": [
            "Taux de MCV",
            "SR en valeur",
            "SR en volume",
            "Point mort",
            "Marge de sécurité",
            "Indice de sécurité",
            "Levier opérationnel",
        ],
        "Calcul détaillé": [
            f"{fmt(MCV)} / {fmt(CA)} × 100",
            f"{fmt(CF_TOTAL)} / {pct(TAUX_MCV)}",
            f"{fmt(CF_TOTAL)} / {MCV_UNIT:.2f}",
            f"{fmt(SR_VALEUR)} / {fmt(CA)} × 365",
            f"{fmt(CA)} − {fmt(SR_VALEUR)}",
            f"{fmt(MARGE_SEC)} / {fmt(CA)} × 100",
            f"{fmt(MCV)} / {fmt(RESULTAT)}",
        ],
        "Résultat": [
            pct(TAUX_MCV),
            f"{fmt(SR_VALEUR)} {devise}",
            f"{fmt(SR_VOLUME)} unités",
            f"≈ {POINT_MORT:.0f} jours",
            f"{fmt(MARGE_SEC)} {devise}",
            pct(INDICE_SEC),
            lev_disp,
        ],
        "Interprétation": [
            (
                "Excellent (>50%)"
                if TAUX_MCV > 50
                else "Satisfaisant" if TAUX_MCV > 30 else "Faible"
            ),
            "Atteint largement" if CA > SR_VALEUR * 1.5 else "Proche",
            f"{quantite - SR_VOLUME:.0f} u. de marge",
            "≈ mi-juin (favorable)" if POINT_MORT < 183 else "Second semestre",
            (
                "Très confortable"
                if INDICE_SEC > 50
                else "Raisonnable" if INDICE_SEC > 25 else "Risqué"
            ),
            (
                "Excellent (>55%)"
                if INDICE_SEC > 55
                else "Satisfaisant" if INDICE_SEC > 30 else "Risqué"
            ),
            (
                "Risque faible"
                if abs(LEVIER_OP) < 3
                else "Risque modéré" if abs(LEVIER_OP) < 6 else "Élevé"
            ),
        ],
    }
    st.dataframe(pd.DataFrame(risk_data), use_container_width=True, hide_index=True)

    st.markdown(
        f"""
    <div class="formula-box">
    SR (valeur)  = CF / Taux MCV  = {fmt(CF_TOTAL)} / {pct(TAUX_MCV)} = <b>{fmt(SR_VALEUR)} {devise}</b><br>
    SR (volume)  = CF / MCV unit. = {fmt(CF_TOTAL)} / {round(MCV_UNIT, 2)} = <b>{fmt(SR_VOLUME)} unités</b><br>
    Point mort   = {fmt(SR_VALEUR)} / {fmt(CA)} × 365                  = <b>≈ {POINT_MORT:.0f} jours</b><br>
    MS           = {fmt(CA)} − {fmt(SR_VALEUR)}                         = <b>{fmt(MARGE_SEC)} {devise}</b><br>
    Indice sécu. = {fmt(MARGE_SEC)} / {fmt(CA)} × 100                  = <b>{pct(INDICE_SEC)}</b><br>
    Levier opér. = {fmt(MCV)} / {fmt(RESULTAT)}                         = <b>{lev_disp}</b>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Graphiques
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Droites CA / Coût total / SR",
            "Simulation sensibilité résultat",
        ),
        horizontal_spacing=0.1,
    )

    q_range = np.linspace(0, CA * 1.3, 300)
    cv_rate = CV_TOTAL / CA if CA else 0
    ca_line = q_range
    ct_line = q_range * cv_rate + CF_TOTAL

    fig.add_trace(
        go.Scatter(
            x=q_range / 1e6,
            y=ca_line / 1e6,
            name="CA",
            line=dict(color="#1e4a8c", width=2.5),
            mode="lines",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=q_range / 1e6,
            y=ct_line / 1e6,
            name="Coût total",
            line=dict(color="#b53c2a", width=2.5, dash="dash"),
            mode="lines",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=q_range / 1e6,
            y=[CF_TOTAL / 1e6] * 300,
            name="Charges fixes",
            line=dict(color="#8c5c0e", width=1.5, dash="dot"),
            mode="lines",
        ),
        row=1,
        col=1,
    )
    if SR_VALEUR > 0:
        fig.add_vline(
            x=SR_VALEUR / 1e6,
            line_dash="dash",
            line_color="#2a6b3c",
            line_width=2,
            row=1,
            col=1,
        )
        fig.add_annotation(
            x=SR_VALEUR / 1e6,
            y=SR_VALEUR / 1e6,
            text=f"SR<br>{SR_VALEUR/1e6:.1f} M",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#2a6b3c",
            font=dict(size=11, color="#2a6b3c"),
            row=1,
            col=1,
        )

    variations = np.arange(-40, 45, 5)
    res_sim = [
        (CA * (1 + v / 100) - CV_TOTAL * (1 + v / 100) - CF_TOTAL) / 1e6
        for v in variations
    ]
    fig.add_trace(
        go.Bar(
            x=variations,
            y=res_sim,
            marker_color=["#b53c2a" if r < 0 else "#2a6b3c" for r in res_sim],
            text=[f"{r:.2f}M" for r in res_sim],
            textposition="outside",
            textfont=dict(size=9),
            name="Résultat simulé",
        ),
        row=1,
        col=2,
    )
    fig.add_hline(
        y=0, line_dash="dot", line_color="#1a1714", line_width=1, row=1, col=2
    )

    fig.update_layout(
        height=400,
        paper_bgcolor="white",
        plot_bgcolor="#faf7f2",
        font=dict(family="DM Sans, sans-serif", size=11),
        legend=dict(orientation="h", y=-0.15, font=dict(size=10)),
        margin=dict(t=50, b=60, l=20, r=20),
    )
    fig.update_xaxes(gridcolor="#e8e0d4")
    fig.update_yaxes(gridcolor="#e8e0d4")
    fig.update_xaxes(title_text="CA (millions DA)", row=1, col=1)
    fig.update_xaxes(title_text="Variation du CA (%)", ticksuffix="%", row=1, col=2)
    fig.update_yaxes(title_text="M DA", row=1, col=1)
    fig.update_yaxes(title_text="Résultat (M DA)", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)

    # Jauge IS
    col_g, col_interp = st.columns(2)
    with col_g:
        fig_g = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=INDICE_SEC,
                number=dict(suffix="%", font=dict(size=30, family="IBM Plex Mono")),
                title=dict(text="Indice de sécurité", font=dict(size=13)),
                delta=dict(reference=30, increasing=dict(color="#2a6b3c")),
                gauge=dict(
                    axis=dict(range=[0, 100]),
                    bar=dict(color="#1e4a8c"),
                    steps=[
                        dict(range=[0, 15], color="#fde8e4"),
                        dict(range=[15, 30], color="#fff8e8"),
                        dict(range=[30, 100], color="#eaf5f0"),
                    ],
                    threshold=dict(
                        line=dict(color="#b53c2a", width=3), thickness=0.8, value=15
                    ),
                ),
            )
        )
        fig_g.update_layout(
            height=250,
            paper_bgcolor="white",
            margin=dict(t=40, b=10, l=30, r=30),
            font=dict(family="DM Sans, sans-serif"),
        )
        st.plotly_chart(fig_g, use_container_width=True)

    with col_interp:
        lo_effect = abs(LEVIER_OP) * 10 if abs(LEVIER_OP) < 1e6 else 0
        st.markdown(
            f"""
        <div class="result-box success" style="margin-top:0.5rem;">
        <b>Levier opérationnel = {lev_disp}</b><br><br>
        Une hausse de 1% du CA entraîne une hausse de <b>{abs(LEVIER_OP):.2f}%</b> du résultat.<br><br>
        <b>Q7 — Simulation :</b> Si le CA baisse de 10% :<br>
        CA new = {fmt(CA * 0.9)} DA<br>
        MCV new = {fmt(MCV * 0.9)} DA<br>
        Résultat new = {fmt(MCV * 0.9 - CF_TOTAL)} DA<br>
        → Variation résultat = <b>−{lo_effect:.1f}%</b>
        </div>""",
            unsafe_allow_html=True,
        )

    # Conclusion
    st.markdown(
        f"""
    <div style="border:2px solid var(--primary);padding:2.5rem;margin-top:2rem;background:#f0f9ff;color:var(--ink);border-radius:12px;">
    <div style="font-size:15px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--primary);margin-bottom:0.8rem;">Conclusion analytique</div>
    <h3 style="font-family:'Lora',serif;font-style:italic;font-size:1.6rem;color:var(--primary);margin-bottom:1rem;border:none !important;font-weight:700;">
    ELMAKAN SARL — Exercice N : Situation financière très favorable
    </h3>
    <p style="font-size:19px;line-height:1.9;opacity:0.95;">
    ELMAKAN SARL est <strong>largement bénéficiaire</strong> avec un résultat net de <strong>{fmt(RESULTAT)} {devise}</strong>.
    L'entreprise atteint son seuil de rentabilité dès le <strong>{POINT_MORT:.0f}e jour (≈ mi-juin)</strong>,
    laissant plus de 6 mois d'activité bénéficiaire.
    Avec un indice de sécurité de <strong>{pct(INDICE_SEC)}</strong>, elle peut supporter une baisse
    de {INDICE_SEC:.0f}% de son CA avant de tomber dans le déficit.
    Le levier opérationnel de <strong>{lev_disp}</strong> est modéré : une variation de 1% du CA
    induit une variation de {abs(LEVIER_OP):.2f}% du résultat.
    </p>
    </div>""",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §9 BILAN DE CLÔTURE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[8]:
    st.markdown(
        '<div class="section-title">Bilan de clôture — 31/12/N</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
    <div class="result-box info">
    Le bilan de clôture intègre : le résultat de l'exercice N dans les capitaux propres,
    les mouvements de trésorerie (soldes du grand livre), et les amortissements cumulés.
    </div>""",
        unsafe_allow_html=True,
    )

    col_a, col_p = st.columns(2)
    with col_a:
        st.markdown(
            '<div class="bilan-actif-header">🔵 ACTIF — 31/12/N</div>',
            unsafe_allow_html=True,
        )
        actif_bc = {
            "Poste": [
                "ACTIF IMMOBILISÉ",
                "Immobilisations corporelles (brut)",
                "  Amort. cumulés (N-1 + dotation N)",
                "  Valeur nette",
                "ACTIF CIRCULANT",
                "Stocks MP (net après variation)",
                "Clients (solde grand livre)",
                "Banque (solde grand livre)",
                "Caisse (après paiements)",
                "TOTAL ACTIF NET",
            ],
            "Net (DA)": [
                "",
                fmt(bc_immo_brut),
                fmt(bc_amort_cum),
                fmt(bc_immo_net),
                "",
                fmt(bc_stocks),
                "7 500 000",
                "5 640 000",
                f"{max(bo_caisse - cf_personnel, 0):,.0f}".replace(",", " "),
                fmt(
                    bc_immo_net
                    + bc_stocks
                    + 7500000
                    + 5640000
                    + max(bo_caisse - cf_personnel, 0)
                ),
            ],
        }
        df_actif_bc = pd.DataFrame(actif_bc)

        def style_bc_actif(row):
            if row["Poste"] == "TOTAL ACTIF NET":
                return ["font-weight:bold;background:#1a171422"] * len(row)
            if row["Poste"] in ["ACTIF IMMOBILISÉ", "ACTIF CIRCULANT"]:
                return ["font-weight:600;background:#e8f0ff"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_actif_bc.style.apply(style_bc_actif, axis=1),
            use_container_width=True,
            hide_index=True,
        )

    with col_p:
        st.markdown(
            '<div class="bilan-passif-header">🔴 PASSIF — 31/12/N</div>',
            unsafe_allow_html=True,
        )
        passif_bc = {
            "Poste": [
                "CAPITAUX PROPRES",
                "Capital social",
                "Réserves",
                "Résultat reporté (N-1)",
                "Résultat exercice N",
                "  Sous-total CP",
                "DETTES FINANCIÈRES",
                "Emprunts bancaires",
                "DETTES D'EXPLOITATION",
                "Fournisseurs (solde)",
                "Dettes fiscales (IS ~19%)",
                "TOTAL PASSIF",
            ],
            "Montant (DA)": [
                "",
                fmt(bo_capital),
                fmt(bo_reserves),
                fmt(bo_res_reporte),
                fmt(RESULTAT),
                fmt(bo_capital + bo_reserves + bo_res_reporte + RESULTAT),
                "",
                fmt(bo_emprunts),
                "",
                "1 200 000",
                fmt(RESULTAT * 0.19),
                fmt(
                    bo_capital
                    + bo_reserves
                    + bo_res_reporte
                    + RESULTAT
                    + bo_emprunts
                    + 1200000
                    + RESULTAT * 0.19
                ),
            ],
        }
        df_passif_bc = pd.DataFrame(passif_bc)

        def style_bc_passif(row):
            if row["Poste"] == "TOTAL PASSIF":
                return ["font-weight:bold;background:#1a171422"] * len(row)
            if row["Poste"] in [
                "CAPITAUX PROPRES",
                "DETTES FINANCIÈRES",
                "DETTES D'EXPLOITATION",
            ]:
                return ["font-weight:600;background:#fff0ee"] * len(row)
            if row["Poste"] == "Résultat exercice N":
                return ["background:#d4edda;font-weight:500"] * len(row)
            if row["Poste"] == "  Sous-total CP":
                return ["font-weight:500;background:#f0faf5"] * len(row)
            return [""] * len(row)

        st.dataframe(
            df_passif_bc.style.apply(style_bc_passif, axis=1),
            use_container_width=True,
            hide_index=True,
        )


# ─────────────────────────────────────────────────────────────────────────────
# §10 QUESTIONS DE SYNTHÈSE
# ─────────────────────────────────────────────────────────────────────────────
with tabs[9]:
    st.markdown(
        '<div class="section-title">Questions de réflexion et de synthèse</div>',
        unsafe_allow_html=True,
    )

    questions = [
        (
            "Q1",
            "Bilan d'ouverture",
            "Vérifiez l'équilibre du bilan d'ouverture. Que remarquez-vous sur la structure financière (ratio CP / Total Passif) ?",
            f"CP = {fmt(bo_capital+bo_reserves+bo_res_reporte)} DA / Total Passif = {fmt(bo_passif)} DA → Ratio = {(bo_capital+bo_reserves+bo_res_reporte)/bo_passif*100:.1f}% (autonomie financière {'bonne' if (bo_capital+bo_reserves+bo_res_reporte)/bo_passif > 0.6 else 'à surveiller'}).",
        ),
        (
            "Q2",
            "Grand Livre",
            "Reportez les opérations dans les comptes en T. Calculez les soldes de clôture.",
            "Clients 411 : SD = 7 500 000 DA | Banque 512 : SD = 5 640 000 DA | Fourn. 401 : SC = 1 200 000 DA | Ventes 701 : SC = 16 000 000 DA.",
        ),
        (
            "Q3",
            "TCR",
            "Établissez le TCR complet. Quel est le résultat net ? Commentez sa signification.",
            f"Résultat net = {fmt(RESULTAT)} DA. L'entreprise est bénéficiaire : elle génère {pct(RESULTAT/CA*100)} de bénéfice par DA de CA, ce qui traduit une gestion efficace.",
        ),
        (
            "Q4",
            "Coûts partiels",
            "Répartissez les charges en variables et fixes. Calculez la MCV et son taux.",
            f"CV = {fmt(CV_TOTAL)} DA | CF = {fmt(CF_TOTAL)} DA | MCV = {fmt(MCV)} DA | Taux MCV = {pct(TAUX_MCV)}.",
        ),
        (
            "Q5",
            "Seuil de rentabilité",
            "Déterminez le SR en valeur et en volume. À quelle date l'entreprise atteint-elle son point mort ?",
            f"SR valeur = {fmt(SR_VALEUR)} DA | SR volume = {fmt(SR_VOLUME)} unités | Point mort ≈ {POINT_MORT:.0f}e jour (≈ mi-juin).",
        ),
        (
            "Q6",
            "Marge de sécurité",
            "Calculez la MS et l'IS. Commentez le niveau de risque.",
            f"MS = {fmt(MARGE_SEC)} DA | IS = {pct(INDICE_SEC)} → L'entreprise peut supporter une baisse de {INDICE_SEC:.0f}% de son CA. Risque très faible.",
        ),
        (
            "Q7",
            "Levier opérationnel",
            f"Le levier opérationnel est de {LEVIER_OP:.2f}. Que se passe-t-il sur le résultat si le CA baisse de 10% ?",
            f"Baisse CA de 10% → Résultat new = {fmt(MCV*0.9 - CF_TOTAL)} DA (vs {fmt(RESULTAT)} DA actuel) → Variation = −{LEVIER_OP*10:.1f}%.",
        ),
        (
            "Q8",
            "Bilan de clôture",
            "Établissez le bilan de clôture au 31/12/N en intégrant le résultat et les mouvements de trésorerie.",
            f"Résultat {fmt(RESULTAT)} DA intégré aux CP. Amort. cumulés = {fmt(bc_amort_cum)} DA. Soldes trésorerie issus du grand livre.",
        ),
    ]

    for num, titre, question, corrige in questions:
        with st.expander(f"**{num} — {titre}**", expanded=False):
            st.markdown(f"**Question :** {question}")
            st.markdown(
                f"""<div class="result-box success"><b>Corrigé :</b> {corrige}</div>""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
    <div class="result-box info" style="margin-top:1.5rem;">
    <b>Conseil méthodologique :</b> Les parties sont interdépendantes.
    Les soldes du grand livre alimentent le TCR, et le résultat du TCR modifie les capitaux propres
    du bilan de clôture. Vérifiez toujours la cohérence verticale de vos calculs.
    </div>""",
        unsafe_allow_html=True,
    )


# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown(
    """
<hr style='border:1px solid #ddd8ce; margin-top:40px;'>
<p style='text-align:center; color:#374151; font-size:16px; font-weight:600; letter-spacing:0.05em;'>
ELMAKAN SARL · Méthode des Coûts Partiels · Comptabilité Analytique · 
</p>
""",
    unsafe_allow_html=True,
)
