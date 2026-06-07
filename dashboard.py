import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import pickle
import base64
from pathlib import Path
from pymongo import MongoClient
import certifi

BASE_DIR = Path(__file__).parent

st.set_page_config(
    page_title="Churn Intelligence · Arca Continental",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_logo_b64():
    try:
        with open(BASE_DIR / 'assets' / 'arcacontinental.png', 'rb') as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_b64()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #ECEEF2; color: #1a1a1a; }
.stApp { background: #ECEEF2; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg,#0a0c10 0%,#141720 100%) !important; border-right: 2px solid #B00000; }
section[data-testid="stSidebar"] * { color: #c8cdd8 !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 12px; padding: 10px 12px; border-bottom: 1px solid #1e2530; display: block; cursor: pointer; letter-spacing: 0.5px; text-transform: uppercase; font-weight: 500; }
section[data-testid="stSidebar"] .stRadio label:hover { color: white !important; background: rgba(176,0,0,0.15) !important; }

.page-header { margin-bottom: 24px; padding-bottom: 16px; border-bottom: 2px solid #d0d5dd; }
.page-title { font-size: 20px; font-weight: 700; color: #0a0c10; margin-bottom: 2px; letter-spacing: 0.5px; text-transform: uppercase; }
.page-sub { font-size: 11px; color: #8a8f9a; font-weight: 400; letter-spacing: 0.3px; }

/* KPI */
.kpi-card { background: white; border-radius: 0; padding: 18px 20px; border: 1px solid #d0d5dd; border-top: 3px solid #d0d5dd; position: relative; }
.kpi-card.danger { border-top: 3px solid #B00000; }
.kpi-card.warning { border-top: 3px solid #d97706; }
.kpi-card.success { border-top: 3px solid #059669; }
.kpi-card.neutral { border-top: 3px solid #3b5bdb; }
.kpi-label { font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; color: #8a8f9a; margin-bottom: 8px; font-weight: 600; }
.kpi-val { font-size: 30px; font-weight: 700; color: #0a0c10; font-family: 'JetBrains Mono', monospace; line-height: 1; }
.kpi-val.red { color: #B00000; }
.kpi-val.amber { color: #d97706; }
.kpi-val.green { color: #059669; }
.kpi-val.blue { color: #3b5bdb; }
.kpi-delta { font-size: 10px; color: #8a8f9a; margin-top: 6px; letter-spacing: 0.3px; }
.kpi-delta.up { color: #B00000; font-weight: 600; }

/* CARD — sin border-radius, header pegado */
.card { background: white; border: 1px solid #d0d5dd; margin-bottom: 14px; }
.card-header { padding: 11px 16px; border-bottom: 2px solid #ECEEF2; display: flex; align-items: center; justify-content: space-between; background: #f8f9fb; }
.card-title { font-size: 10px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #374151; margin: 0; }
.card-badge { font-size: 9px; font-weight: 700; padding: 2px 7px; letter-spacing: 0.8px; text-transform: uppercase; border: 1px solid; }
.badge-danger { background: #fef2f2; color: #B00000; border-color: #B00000; }
.badge-info { background: #eff6ff; color: #3b5bdb; border-color: #3b5bdb; }
.badge-warn { background: #fffbeb; color: #d97706; border-color: #d97706; }
.card-body { padding: 16px; background: white; }
.card-body-flush { background: white; overflow: hidden; }

/* TABLE */
.html-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.html-table th { background: #0a0c10; color: white; padding: 9px 14px; text-align: left; font-size: 10px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
.html-table td { padding: 9px 14px; border-bottom: 1px solid #f0f2f5; color: #2d3748; vertical-align: middle; }
.html-table tr:last-child td { border-bottom: none; }
.html-table tr:hover td { background: #f8f9fb; }
.html-table tr:nth-child(even) td { background: #fafbfc; }
.html-table tr:nth-child(even):hover td { background: #f3f4f6; }

/* RISK BADGES */
.risk-alto { display: inline-block; padding: 2px 7px; background: #fef2f2; color: #B00000; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; border: 1px solid #B00000; }
.risk-medio { display: inline-block; padding: 2px 7px; background: #fffbeb; color: #d97706; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; border: 1px solid #d97706; }
.risk-bajo { display: inline-block; padding: 2px 7px; background: #f0fdf4; color: #059669; font-size: 10px; font-weight: 700; letter-spacing: 0.5px; border: 1px solid #059669; }

/* INSIGHTS */
.insight-item { display: flex; gap: 12px; align-items: flex-start; padding: 11px 0; border-bottom: 1px solid #f0f2f5; }
.insight-item:last-child { border-bottom: none; }
.insight-idx { font-family: 'JetBrains Mono', monospace; font-size: 9px; color: #B00000; font-weight: 700; min-width: 22px; background: #fef2f2; padding: 3px 5px; text-align: center; border: 1px solid #B00000; margin-top: 1px; }
.insight-label { font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: #8a8f9a; margin-bottom: 2px; font-weight: 700; }
.insight-text { font-size: 12px; color: #2d3748; line-height: 1.5; }

/* DROW */
.drow { display: flex; justify-content: space-between; align-items: center; padding: 9px 0; border-bottom: 1px solid #f5f5f5; }
.drow:last-child { border-bottom: none; }
.drow-label { font-size: 12px; color: #6b7280; }
.drow-val { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 600; color: #0a0c10; }

/* ACTION */
.action-item { background: #f8f9fb; border-left: 3px solid #e4e7ec; padding: 10px 14px; margin-bottom: 8px; }
.action-tag { font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: #B00000; font-weight: 700; margin-bottom: 3px; }
.action-text { font-size: 12px; color: #374151; line-height: 1.5; }

/* NOTA */
.nota { background: #f8f9fb; border-left: 3px solid #B00000; padding: 8px 12px; font-size: 11px; color: #64748b; margin-top: 6px; }
.nota strong { color: #374151; }

/* TIMELINE */
.timeline { position: relative; padding-left: 24px; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: #e4e7ec; }
.tl-item { position: relative; margin-bottom: 16px; }
.tl-dot { position: absolute; left: -20px; top: 3px; width: 10px; height: 10px; border: 2px solid white; }
.tl-dot.danger { background: #B00000; box-shadow: 0 0 0 2px #B00000; }
.tl-dot.warning { background: #d97706; box-shadow: 0 0 0 2px #d97706; }
.tl-dot.neutral { background: #9ca3af; box-shadow: 0 0 0 2px #9ca3af; }
.tl-month { font-size: 9px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #8a8f9a; margin-bottom: 2px; }
.tl-text { font-size: 12px; color: #2d3748; }

/* OC STAT */
.oc-stat { text-align: center; padding: 14px; background: white; border: 1px solid #d0d5dd; border-top: 3px solid #d0d5dd; }
.oc-val { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; line-height: 1; margin-bottom: 4px; }
.oc-label { font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: #8a8f9a; font-weight: 700; }

/* BUTTON */
div[data-testid="stButton"] button { background: #0a0c10; color: white; border: none; border-radius: 0; font-family: 'Inter', sans-serif; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; padding: 12px 24px; width: 100%; font-weight: 700; }
div[data-testid="stButton"] button:hover { background: #B00000; }
div[data-testid="stSelectbox"] label { color: #374151 !important; font-size: 10px !important; font-weight: 700 !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
.sidebar-section { font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #4a5568 !important; margin-bottom: 6px; margin-top: 20px; display: block; border-bottom: 1px solid #1e2530; padding-bottom: 4px; }

/* Animations */
@keyframes fadeInUp { from { opacity:0; transform:translateY(12px); } to { opacity:1; transform:translateY(0); } }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.5;} }
.kpi-card { animation: fadeInUp 0.4s ease both; }
.badge-danger { animation: pulse 2.5s ease infinite; }
</style>
""", unsafe_allow_html=True)

FONT = dict(family='Inter', color='#374151', size=12)
GRID = dict(showgrid=True, gridcolor='#f0f2f5', gridwidth=1, zeroline=False)
NOGRID = dict(showgrid=False, zeroline=False)
BL = dict(
    plot_bgcolor='white', paper_bgcolor='white', font=FONT,
    margin=dict(l=0,r=0,t=8,b=0),
    hoverlabel=dict(bgcolor='#0a0c10', font_size=12, font_family='Inter', font_color='white', bordercolor='#0a0c10')
)

@st.cache_resource
def get_mongo():
    c = MongoClient("mongodb+srv://a00840850_db_user:churnhunters2026@churn.u9yenik.mongodb.net/?appName=Churn", tlsCAFile=certifi.where())
    return c["churn_db"]["predicciones"]

@st.cache_resource
def get_model():
    with open(BASE_DIR / 'model' / 'model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data
def get_clientes():
    test = pd.read_csv(BASE_DIR / 'data' / 'sales_churn_test.csv')
    cli = pd.read_csv(BASE_DIR / 'data' / 'Clientes.csv')
    cool = pd.read_csv(BASE_DIR / 'data' / 'Coolers.csv')
    sub = pd.read_csv(BASE_DIR / 'data' / 'preds_submission_final.csv')
    cl = cool.sort_values("calmonth").groupby("customer_id").last().reset_index()
    df = test.merge(cli, on="customer_id", how="left").merge(cl[["customer_id","num_coolers","num_doors"]], on="customer_id", how="left")
    df = df.merge(sub[["customer_id","target","risk_level"]], on="customer_id", how="left").fillna(0)
    alto = df[df["risk_level"]=="alto"].head(70)
    medio = df[df["risk_level"]=="medio"].head(10)
    bajo = df[df["risk_level"]=="bajo"].head(120)
    return pd.concat([alto, medio, bajo]).reset_index(drop=True)

@st.cache_data
def get_eda():
    train = pd.read_csv(BASE_DIR / 'data' / 'sales_churn_train.csv')
    cli = pd.read_csv(BASE_DIR / 'data' / 'Clientes.csv')
    cool = pd.read_csv(BASE_DIR / 'data' / 'Coolers.csv')
    cl = cool.sort_values('calmonth').groupby('customer_id').last().reset_index()
    df = train.merge(cli, on='customer_id', how='left').merge(cl[['customer_id','num_coolers','num_doors']], on='customer_id', how='left').fillna(0)
    ds = df.sort_values(['customer_id','calmonth'])
    ds['prev'] = ds.groupby('customer_id')['uni_boxes_sold_m'].shift(1)
    ds['tendencia'] = ds['uni_boxes_sold_m'] - ds['prev']
    df['tendencia'] = ds['tendencia'].fillna(0).values
    mes = df.groupby('calmonth')['target'].mean().reset_index()
    mes['calmonth'] = mes['calmonth'].astype(str)
    mes = mes[mes['calmonth'] != '202401']
    sub = df.groupby('comercial_subchannel_d')['target'].mean().sort_values(ascending=False).reset_index()
    sub.columns = ['Subcanal','Churn']
    terr = df.groupby('territory_d')['target'].mean().sort_values(ascending=False).head(15).reset_index()
    terr.columns = ['Territorio','Churn']
    sz = df.groupby('rtm_customer_size_d')['target'].mean().sort_values(ascending=False).reset_index()
    sz.columns = ['Tamaño','Churn']
    df['cg'] = pd.cut(df['num_coolers'], bins=[0,1,2,5,100], labels=['1','2','3-5','6+'])
    cool_g = df.groupby('cg')['target'].mean().reset_index()
    cool_g.columns = ['Coolers','Churn']
    tend = df.groupby('target')['tendencia'].mean().reset_index()
    tend['label'] = tend['target'].map({0:'No churn',1:'Churn'})
    dist = df.groupby('territory_d').agg(total=('customer_id','count'), cr=('target','mean')).sort_values('total', ascending=False).head(10).reset_index()
    comp = pd.DataFrame({'Métrica':['Transacciones/mes','Cajas/mes'],'No churn':[95.5,250.1],'Churn':[0.04,0.0]})
    return mes, sub, terr, sz, cool_g, tend, dist, comp

@st.cache_data
def get_mongo_data():
    col = get_mongo()
    datos = list(col.find({}, {'_id': 0}).limit(1000))
    if not datos: return pd.DataFrame()
    df = pd.DataFrame(datos)
    df['risk_level'] = df['risk_level'].fillna('bajo').astype(str)
    df['churn_proba'] = df['churn_proba'].astype(float)
    return df

model = get_model()
df_cli = get_clientes()
SIZE_MAP = {'Mini':0,'Pequeño':1,'Mediano':2,'Gigante':3}

# SIDEBAR
with st.sidebar:
    if logo_b64:
        st.markdown(f'<img src="data:image/png;base64,{logo_b64}" style="width:130px;margin-bottom:16px;padding:8px 10px;background:white;">', unsafe_allow_html=True)
    else:
        st.markdown('<p style="font-size:14px;font-weight:700;color:white;letter-spacing:1px;">ARCA CONTINENTAL</p>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-section">Módulos</span>', unsafe_allow_html=True)
    pagina = st.radio("", ["Vista ejecutiva", "Análisis exploratorio", "Análisis individual", "Centro operativo"], label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="sidebar-section">Modelo activo</span>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#6b7280;line-height:2.2;">Random Forest + SMOTE<br>AUC 0.9987 · 5M registros<br>Canal Tradicional · MX<br>2024 – 2026</p>', unsafe_allow_html=True)

# ══ VISTA EJECUTIVA ══
if pagina == "Vista ejecutiva":
    st.markdown('<div class="page-header"><div class="page-title">Vista ejecutiva</div><div class="page-sub">Resumen de riesgo de churn · Canal tradicional · Actualización mensual</div></div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown('<div class="kpi-card neutral"><div class="kpi-label">Base de clientes</div><div class="kpi-val blue">371,727</div><div class="kpi-delta">Canal tradicional · México</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="kpi-card danger"><div class="kpi-label">En riesgo alto</div><div class="kpi-val red">2,519</div><div class="kpi-delta up">▲ Acción requerida</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="kpi-card warning"><div class="kpi-label">Tasa de churn</div><div class="kpi-val amber">0.9%</div><div class="kpi-delta">Mensual · Promedio 2024–2026</div></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="kpi-card danger"><div class="kpi-label">Ingreso en riesgo</div><div class="kpi-val red">$12 MM</div><div class="kpi-delta up">MXN mensuales</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3,2])

    with col_l:
        # Importancia — barras HTML animadas sin Plotly
        imp = [
            ('Cajas vendidas', 43.3),
            ('Promedio/transacción', 24.5),
            ('N° transacciones', 23.6),
            ('Cajas/puerta', 6.0),
            ('Tamaño cliente', 1.9),
            ('N° coolers', 0.5),
        ]
        colors = ['#B00000','#c43030','#d46060','#e49090','#f0b8b8','#f8dcdc']
        bars_html = '<div class="card"><div class="card-header"><span class="card-title">Drivers de churn — importancia en el modelo</span><span class="card-badge badge-info">Random Forest</span></div><div class="card-body">'
        for i, (name, val) in enumerate(imp):
            pct = val / 45 * 100
            bars_html += f'<div style="margin-bottom:10px;"><div style="display:flex;justify-content:space-between;margin-bottom:4px;"><span style="font-size:12px;color:#374151;font-weight:500;">{name}</span><span style="font-family:JetBrains Mono;font-size:11px;font-weight:700;color:{colors[i]};">{val}%</span></div><div style="background:#ECEEF2;height:7px;"><div style="height:7px;width:{pct:.1f}%;background:{colors[i]};"></div></div></div>'
        bars_html += '</div></div>'
        st.markdown(bars_html, unsafe_allow_html=True)

        df_mongo = get_mongo_data()
        if not df_mongo.empty:
            df_alto = df_mongo[df_mongo['risk_level']=='alto'].sort_values('churn_proba', ascending=False).head(8).reset_index(drop=True)
            rows_html = ""
            for i, (_, row) in enumerate(df_alto.iterrows()):
                pct = round(float(row['churn_proba'])*100,1)
                mxn = f"${round(pct/100*4760):,}"
                rows_html += f'<tr><td style="font-family:JetBrains Mono;font-size:11px;color:#6b7280;">{i+1}</td><td style="font-family:JetBrains Mono;font-size:11px;">{str(row["customer_id"])[:18]}...</td><td style="font-family:JetBrains Mono;font-weight:700;color:#B00000;">{pct}%</td><td><span class="risk-alto">Alto</span></td><td style="font-family:JetBrains Mono;font-size:12px;color:#059669;font-weight:600;">{mxn}</td></tr>'
            st.markdown(f'<div class="card"><div class="card-header"><span class="card-title">Top clientes · Impacto económico estimado</span><span class="card-badge badge-danger">Riesgo alto</span></div><div class="card-body-flush"><table class="html-table"><thead><tr><th>#</th><th>Cliente ID</th><th>Prob.</th><th>Nivel</th><th>Ingreso estimado</th></tr></thead><tbody>{rows_html}</tbody></table><p class="nota" style="margin:10px 14px;"><strong>Nota:</strong> Ingreso estimado sobre valor promedio por cliente del canal tradicional.</p></div></div>', unsafe_allow_html=True)

    with col_r:
        if not df_mongo.empty:
            alto = len(df_mongo[df_mongo['risk_level']=='alto'])
            medio = len(df_mongo[df_mongo['risk_level']=='medio'])
            bajo = len(df_mongo[df_mongo['risk_level']=='bajo'])
            total = alto + medio + bajo
            pct_alto = round(alto/total*100,1)

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pct_alto,
                number={'suffix':'%','font':{'family':'JetBrains Mono','size':32,'color':'#B00000'}},
                title={'text':'<span style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#8a8f9a;">Índice de riesgo global</span>'},
                gauge={
                    'axis':{'range':[0,5],'tickfont':{'size':10,'color':'#8a8f9a'},'tickcolor':'#e4e7ec'},
                    'bar':{'color':'#B00000','thickness':0.28},
                    'bgcolor':'white','borderwidth':0,
                    'steps':[
                        {'range':[0,1],'color':'#f0fdf4'},
                        {'range':[1,2.5],'color':'#fffbeb'},
                        {'range':[2.5,5],'color':'#fef2f2'},
                    ],
                    'threshold':{'line':{'color':'#B00000','width':3},'thickness':0.8,'value':pct_alto}
                }
            ))
            gauge.update_layout(paper_bgcolor='white', font=FONT, height=190, margin=dict(l=20,r=20,t=30,b=0))
            st.markdown('<div class="card"><div class="card-header"><span class="card-title">Índice de riesgo global</span></div><div class="card-body">', unsafe_allow_html=True)
            st.plotly_chart(gauge, use_container_width=True, config={'displayModeBar':False})
            st.markdown(f'''
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:4px;">
                <div style="text-align:center;padding:10px;background:#fef2f2;border:1px solid #fecaca;">
                    <div style="font-family:JetBrains Mono;font-size:18px;font-weight:700;color:#B00000;">{round(alto/total*100,1)}%</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Alto</div>
                </div>
                <div style="text-align:center;padding:10px;background:#fffbeb;border:1px solid #fde68a;">
                    <div style="font-family:JetBrains Mono;font-size:18px;font-weight:700;color:#d97706;">{round(medio/total*100,3)}%</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Medio</div>
                </div>
                <div style="text-align:center;padding:10px;background:#f0fdf4;border:1px solid #86efac;">
                    <div style="font-family:JetBrains Mono;font-size:18px;font-weight:700;color:#059669;">{round(bajo/total*100,1)}%</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:2px;">Bajo</div>
                </div>
            </div>''', unsafe_allow_html=True)
            st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <div class="card-header"><span class="card-title">Hallazgos ejecutivos</span></div>
            <div class="card-body">
                <div class="insight-item"><div class="insight-idx">01</div><div><div class="insight-label">Señal temprana</div><div class="insight-text">Clientes en churn caen <strong>22 cajas</strong> el mes previo — ventana de intervención disponible.</div></div></div>
                <div class="insight-item"><div class="insight-idx">02</div><div><div class="insight-label">Subcanal crítico</div><div class="insight-text"><strong>Hogares</strong> tiene 3.4% de churn — 3.5x el promedio. Prioridad de retención inmediata.</div></div></div>
                <div class="insight-item"><div class="insight-idx">03</div><div><div class="insight-label">Segmento vulnerable</div><div class="insight-text">Clientes <strong>Mini</strong> tienen 3.5% de churn — 100x más que clientes Gigante.</div></div></div>
                <div class="insight-item"><div class="insight-idx">04</div><div><div class="insight-label">Territorio</div><div class="insight-text"><strong>Reynosa</strong> lidera en churn rate (1.3%). El riesgo no depende del tamaño del territorio.</div></div></div>
                <div class="insight-item"><div class="insight-idx">05</div><div><div class="insight-label">Coolers</div><div class="insight-text">Correlación -0.02. El cooler no retiene al cliente si el volumen de compra cae.</div></div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ══ ANÁLISIS EXPLORATORIO ══
elif pagina == "Análisis exploratorio":
    st.markdown('<div class="page-header"><div class="page-title">Análisis exploratorio</div><div class="page-sub">Comportamiento histórico del churn · Canal tradicional · 2024–2026</div></div>', unsafe_allow_html=True)
    mes, sub, terr, sz, cool_g, tend, dist, comp = get_eda()

    # Evolución mensual — área con gradiente, más rica
    st.markdown('<div class="card"><div class="card-header"><span class="card-title">Evolución mensual del churn</span><span class="card-badge badge-info">Serie de tiempo</span></div>', unsafe_allow_html=True)
    meses_names = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    def fmt_mes(m):
        s = str(int(m)); y,mo = s[:4],int(s[4:])
        return f"{meses_names[mo-1]} {y}"
    mes_f = mes.iloc[1:].copy()
    mes_f['label'] = mes_f['calmonth'].apply(fmt_mes)
    media = (mes_f['target']*100).mean()

    fig_mes = go.Figure()
    fig_mes.add_trace(go.Scatter(
        x=mes_f['label'], y=(mes_f['target']*100).round(2),
        mode='lines+markers',
        line=dict(color='#B00000', width=3, shape='spline'),
        marker=dict(size=6, color='white', line=dict(color='#B00000', width=2.5)),
        fill='tozeroy',
        fillcolor='rgba(176,0,0,0.1)',
        hovertemplate='<b>%{x}</b><br>Churn: %{y:.2f}%<extra></extra>',
        name=''
    ))
    fig_mes.add_hline(y=media, line_dash='dot', line_color='#d97706', line_width=1.5,
        annotation_text=f"Media: {media:.2f}%", annotation_position="right",
        annotation_font=dict(size=10, color='#d97706'))
    fig_mes.update_layout(**BL, height=220,
        xaxis=dict(**NOGRID, tickangle=45, tickfont=dict(size=10, color='#6b7280'), type='category'),
        yaxis=dict(**GRID, title='% Churn', tickfont=dict(size=10, color='#6b7280'), ticksuffix='%'),
        hovermode='x unified')
    st.plotly_chart(fig_mes, use_container_width=True, config={'displayModeBar':False})
    st.markdown('<p class="nota">El churn se mantiene estable entre <strong>0.8% y 1.1%</strong>. La línea punteada indica la media. No hay estacionalidad marcada — el riesgo requiere monitoreo mensual continuo.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


    # ── Mapa coroplético México ──
    import json as _json
    TERR_ESTADO = {
        'Aguascalientes':   'Aguascalientes',
        'Zacatecas':        'Zacatecas',
        'Mesa Central':     'Guanajuato',
        'San Luis Potosi':  'San Luis Potosí',
        'Durango':          'Durango',
        'Hermosillo':       'Sonora',
        'Mexicali':         'Baja California',
        'Obregon':          'Sonora',
        'Culiacan':         'Sinaloa',
        'La Paz':           'Baja California Sur',
        'Mazatlan':         'Sinaloa',
        'Monterrey':        'Nuevo León',
        'Nuevo Leon':       'Nuevo León',
        'Matamoros':        'Tamaulipas',
        'Reynosa':          'Tamaulipas',
        'Laredo':           'Tamaulipas',
        'Piedras negras':   'Coahuila',
        'Monclova':         'Coahuila',
        'Saltillo':         'Coahuila',
        'Comarca Lagunera': 'Coahuila',
        'Delicias':         'Chihuahua',
        'Chihuahua':        'Chihuahua',
        'Juarez':           'Chihuahua',
        'Jalisco':          'Jalisco',
        'Guadalajara':      'Jalisco',
    }
    with open(BASE_DIR / 'assets' / 'mexico.geojson') as f:
        mx_geojson = _json.load(f)
    # Ver qué nombre tiene la propiedad del estado
    _name_key = 'name'

    terr_churn = terr.copy()
    terr_churn['estado'] = terr_churn['Territorio'].map(lambda t: TERR_ESTADO.get(t, t))
    terr_churn['churn_pct'] = (terr_churn['Churn']*100).round(2)
    # Agrupar por estado
    estado_df = terr_churn.groupby('estado').agg(
        churn_pct=('churn_pct','mean'),
        territorios=('Territorio', lambda x: ', '.join(x))
    ).reset_index()
    estado_df['churn_pct'] = estado_df['churn_pct'].round(2)
    estado_df['texto'] = estado_df.apply(
        lambda r: f"<b>{r['estado']}</b><br>Churn promedio: {r['churn_pct']}%<br>Territorios: {r['territorios']}", axis=1)

    fig_mapa = go.Figure(go.Choropleth(
        geojson=mx_geojson,
        featureidkey='properties.name',
        locations=estado_df['estado'],
        z=estado_df['churn_pct'],
        text=estado_df['texto'],
        hoverinfo='text',
        colorscale=[[0,'#f0fdf4'],[0.35,'#fef9c3'],[0.65,'#fecaca'],[1,'#B00000']],
        marker_line_color='white', marker_line_width=1,
        colorbar=dict(
            title=dict(text='% Churn', font=dict(size=11, color='#374151')),
            tickfont=dict(size=10, color='#374151'),
            thickness=12, len=0.7, ticksuffix='%'
        ),
        zmin=0, zmax=estado_df['churn_pct'].max()
    ))
    fig_mapa.update_geos(
        visible=False,
        fitbounds='locations',
        bgcolor='white'
    )
    fig_mapa.update_layout(
        plot_bgcolor='white', paper_bgcolor='white',
        font=FONT, height=440,
        margin=dict(l=0,r=0,t=0,b=0),
        hoverlabel=dict(bgcolor='#0f1115', font_size=12, font_family='Inter', font_color='white', bordercolor='#0f1115'),
        geo=dict(bgcolor='white')
    )
    st.markdown('<div class="card"><div class="card-header"><span class="card-title">Churn por estado · Mapa de México</span><span class="card-badge badge-warn">Hover para detalle</span></div>', unsafe_allow_html=True)
    st.plotly_chart(fig_mapa, use_container_width=True, config={'displayModeBar': False})
    st.markdown('<p class="nota">El mapa muestra el churn rate promedio por estado. Varios territorios operativos pueden pertenecer al mismo estado.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Churn por subcanal comercial</span><span class="card-badge badge-danger">Hogares: 3.4%</span></div>', unsafe_allow_html=True)
        fig_sub = go.Figure(go.Bar(
            x=sub['Subcanal'], y=(sub['Churn']*100).round(2),
            marker_color=['#B00000' if i==0 else '#d46060' if i==1 else '#e8a0a0' if i==2 else '#f0c8c8' for i in range(len(sub))],
            text=(sub['Churn']*100).round(1).apply(lambda x: f"{x}%"),
            textposition='outside', textfont=dict(size=10, color='#374151'), width=0.6))
        fig_sub.update_layout(**BL, height=260,
            xaxis=dict(**NOGRID, tickangle=45, tickfont=dict(size=9, color='#4b5563')),
            yaxis=dict(**GRID, title='% Churn', tickfont=dict(size=10, color='#6b7280'), ticksuffix='%', range=[0, float(sub['Churn'].max())*130]))
        st.plotly_chart(fig_sub, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota"><strong>Hogares</strong> duplica al segundo subcanal. Minisuper y Proximidad son los más estables.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Churn por tamaño de cliente</span><span class="card-badge badge-danger">Mini: 3.5%</span></div>', unsafe_allow_html=True)
        fig_sz = go.Figure(go.Bar(
            x=sz['Tamaño'], y=(sz['Churn']*100).round(3),
            marker_color=['#B00000','#f97316','#fca5a5','#bbf7d0','#059669'][:len(sz)],
            text=(sz['Churn']*100).round(2).apply(lambda x: f"{x}%"),
            textposition='outside', textfont=dict(size=11, color='#374151'), width=0.5))
        fig_sz.update_layout(**BL, height=210,
            xaxis=dict(**NOGRID, tickfont=dict(size=11, color='#4b5563')),
            yaxis=dict(**GRID, title='% Churn', tickfont=dict(size=10, color='#6b7280'), ticksuffix='%', range=[0, float(sz['Churn'].max())*135]))
        st.plotly_chart(fig_sz, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota">Los clientes <strong>Mini</strong> tienen 100x más churn que los Gigante. Focalizar retención en este segmento.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Caída de cajas · mes previo al churn</span><span class="card-badge badge-danger">Señal clave</span></div>', unsafe_allow_html=True)
        fig_tend = go.Figure(go.Bar(
            x=tend['label'], y=tend['tendencia'].round(1),
            marker_color=['#059669','#B00000'],
            text=tend['tendencia'].round(1).apply(lambda x: f"{x:+.1f} cajas"),
            textposition='outside', textfont=dict(size=12, family='JetBrains Mono', color='#374151'), width=0.45))
        fig_tend.update_layout(**BL, height=220,
            xaxis=dict(**NOGRID, tickfont=dict(size=12, color='#4b5563')),
            yaxis=dict(**GRID, title='Variación promedio (cajas)', tickfont=dict(size=10, color='#6b7280')))
        st.plotly_chart(fig_tend, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota">Los clientes que abandonan caen <strong>22 cajas</strong> en promedio el mes previo. Esta señal permite actuar antes de que el churn ocurra.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Churn por cantidad de coolers</span></div>', unsafe_allow_html=True)
        fig_cool = go.Figure(go.Bar(
            x=cool_g['Coolers'], y=(cool_g['Churn']*100).round(2),
            marker_color='#e8a060',
            text=(cool_g['Churn']*100).round(2).apply(lambda x: f"{x}%"),
            textposition='outside', textfont=dict(size=11, color='#374151'), width=0.45))
        fig_cool.update_layout(**BL, height=200,
            xaxis=dict(**NOGRID, title='N° de coolers', tickfont=dict(size=11, color='#4b5563')),
            yaxis=dict(**GRID, title='% Churn', tickfont=dict(size=10, color='#6b7280'), ticksuffix='%'))
        st.plotly_chart(fig_cool, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota">Tener más coolers no reduce el riesgo. El comportamiento de compra es más determinante que la infraestructura instalada.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Churn por territorio · top 15</span><span class="card-badge badge-warn">Reynosa: 1.3%</span></div>', unsafe_allow_html=True)
        fig_terr = go.Figure(go.Bar(
            x=(terr['Churn']*100).round(2), y=terr['Territorio'],
            orientation='h',
            marker_color=['#B00000' if i<2 else '#d46060' if i<4 else '#e8a0a0' if i<7 else '#f0c8c8' for i in range(len(terr))],
            text=(terr['Churn']*100).round(1).apply(lambda x: f"{x}%"),
            textposition='inside', textfont=dict(size=10, color='white'), width=0.65))
        fig_terr.update_layout(**BL, height=320,
            xaxis=dict(**NOGRID, showticklabels=False, range=[0, float(terr['Churn'].max())*135]),
            yaxis=dict(**NOGRID, tickfont=dict(size=11, color='#4b5563')))
        st.plotly_chart(fig_terr, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota"><strong>Reynosa y Moctezuma</strong> tienen el mayor churn rate. El territorio explica menos del 0.01% de la variación — el riesgo es transversal.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        rows_html = ""
        for _, row in dist.iterrows():
            cr = round(row['cr']*100, 2)
            color = '#B00000' if cr > 1.1 else '#d97706' if cr > 0.8 else '#059669'
            rows_html += f'<tr><td>{row["territory_d"]}</td><td style="font-family:JetBrains Mono;">{int(row["total"]):,}</td><td style="font-family:JetBrains Mono;color:{color};font-weight:600;">{cr}%</td></tr>'
        st.markdown(f'<div class="card"><div class="card-header"><span class="card-title">Clientes y churn por territorio · top 10</span></div><div class="card-body-flush"><table class="html-table"><thead><tr><th>Territorio</th><th>Clientes</th><th>Churn rate</th></tr></thead><tbody>{rows_html}</tbody></table><p class="nota" style="margin:10px 14px;"><strong>Guadalajara</strong> concentra la mayor base (618k) con 1.1% de churn. <strong>Durango</strong> es el territorio más estable con 0.28%.</p></div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Correlación de variables con churn</span></div>', unsafe_allow_html=True)
        corr = pd.DataFrame({'Variable':['N° transacciones','Cajas vendidas','N° puertas','N° coolers'],'r':[-0.104,-0.068,-0.029,-0.022]}).sort_values('r')
        fig_corr = go.Figure(go.Bar(
            x=corr['r'], y=corr['Variable'], orientation='h',
            marker_color=['#B00000','#f97316','#fca5a5','#fecaca'],
            text=corr['r'].apply(lambda x: f"{x:.3f}"),
            textposition='inside', textfont=dict(size=11, color='white'), width=0.5))
        fig_corr.update_layout(**BL, height=170,
            xaxis=dict(**NOGRID, showticklabels=False, range=[-0.14, 0]),
            yaxis=dict(**NOGRID, tickfont=dict(size=11, color='#4b5563')))
        st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota">A más transacciones, menor riesgo. Las transacciones son el predictor individual más fuerte (r = -0.104).</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card"><div class="card-header"><span class="card-title">Comportamiento promedio · churn vs no churn</span></div>', unsafe_allow_html=True)
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(name='No churn', x=comp['Métrica'], y=comp['No churn'],
            marker_color='#059669', text=comp['No churn'], textposition='outside',
            textfont=dict(size=11, color='#374151'), width=0.38))
        fig_comp.add_trace(go.Bar(name='Churn', x=comp['Métrica'], y=comp['Churn'],
            marker_color='#B00000', text=comp['Churn'], textposition='outside',
            textfont=dict(size=11, color='#374151'), width=0.38))
        fig_comp.update_layout(**BL, height=220, barmode='group',
            xaxis=dict(**NOGRID, tickfont=dict(size=12, color='#4b5563')),
            yaxis=dict(**GRID, tickfont=dict(size=10, color='#6b7280')),
            legend=dict(font=dict(size=11, color='#374151'), bgcolor='white', bordercolor='#e4e7ec', borderwidth=1))
        st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar':False})
        st.markdown('<p class="nota">Los clientes en churn tienen prácticamente <strong>cero actividad</strong> — la clave es anticiparlo el mes anterior con la señal de caída de cajas.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══ ANÁLISIS INDIVIDUAL ══
elif pagina == "Análisis individual":
    st.markdown('<div class="page-header"><div class="page-title">Análisis individual</div><div class="page-sub">Score de churn · Factores de riesgo · Acción de retención</div></div>', unsafe_allow_html=True)

    risk_labels = []
    for _, row in df_cli.iterrows():
        rl = str(row['risk_level'])
        if rl == 'alto': indicator = '[ALTO]'
        elif rl == 'medio': indicator = '[MEDIO]'
        else: indicator = '[BAJO]'
        risk_labels.append(f"{_ + 1}. {indicator} {str(row['customer_id'])[:22]}...")

    seleccion = st.selectbox("Selecciona un cliente del dataset de evaluación", risk_labels)
    idx = int(seleccion.split(".")[0]) - 1
    cli = df_cli.iloc[idx]

    col_d, col_r = st.columns([1,1])

    with col_d:
        size_label = str(cli['rtm_customer_size_d']) if str(cli['rtm_customer_size_d']) in SIZE_MAP else 'Mini'
        trans = int(cli['num_transacciones'])
        cajas = float(round(cli['uni_boxes_sold_m'], 2))
        cools = int(cli['num_coolers'])
        doors = int(cli['num_doors'])

        st.markdown(f"""
        <div class="card">
            <div class="card-header"><span class="card-title">Perfil del cliente</span></div>
            <div class="card-body">
                <div class="drow"><span class="drow-label">Transacciones este mes</span><span class="drow-val">{trans}</span></div>
                <div class="drow"><span class="drow-label">Cajas vendidas</span><span class="drow-val">{cajas}</span></div>
                <div class="drow"><span class="drow-label">N° de coolers</span><span class="drow-val">{cools}</span></div>
                <div class="drow"><span class="drow-label">N° de puertas</span><span class="drow-val">{doors}</span></div>
                <div class="drow"><span class="drow-label">Clasificación</span><span class="drow-val">{size_label}</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        prom_normal = max(cajas * 1.4, 20)
        tl_html = '<div class="card"><div class="card-header"><span class="card-title">Timeline de deterioro</span><span class="card-badge badge-warn">Simulado</span></div><div class="card-body"><div class="timeline">'
        for month, desc, cls in [
            ("3 meses atrás", f"{prom_normal:.0f} cajas · Comportamiento normal", "neutral"),
            ("2 meses atrás", f"{prom_normal*0.75:.0f} cajas · Leve descenso", "neutral"),
            ("Mes anterior", f"{prom_normal*0.4:.0f} cajas · Caída significativa", "warning"),
            ("Este mes", f"{cajas} cajas · Nivel actual registrado", "danger"),
        ]:
            tl_html += f'<div class="tl-item"><div class="tl-dot {cls}"></div><div class="tl-month">{month}</div><div class="tl-text">{desc}</div></div>'
        tl_html += '</div></div></div>'
        st.markdown(tl_html, unsafe_allow_html=True)

        ver = st.button("Ver score de riesgo")

    with col_r:
        if ver:
            proba = float(cli['target']) if 'target' in cli.index and float(cli['target']) > 0 else 0.0
            risk_level_raw = str(cli['risk_level']) if 'risk_level' in cli.index else 'bajo'
            risk = "Alto" if risk_level_raw == 'alto' else "Medio" if risk_level_raw == 'medio' else "Bajo"
            pct = round(proba*100, 1)
            color = "#B00000" if risk == "Alto" else "#d97706" if risk == "Medio" else "#059669"
            prom_cajas = cajas / (trans + 1)

            components.html(f'''
            <style>
            @import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap");
            body{{margin:0;padding:0;background:white;font-family:Inter,sans-serif;}}
            .gauge-card{{background:white;border:1px solid #d0d5dd;padding:0;}}
            .gauge-header{{padding:11px 16px;border-bottom:2px solid #ECEEF2;background:#f8f9fb;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#374151;}}
            .gauge-body{{padding:20px;text-align:center;}}
            </style>
            <div class="gauge-card">
              <div class="gauge-header">Score de riesgo</div>
              <div class="gauge-body">
                <canvas id="gc" width="300" height="170" style="display:block;margin:0 auto;"></canvas>
                <div style="font-family:JetBrains Mono,monospace;font-size:52px;font-weight:700;color:{color};margin-top:-8px;" id="gn">0%</div>
                <div style="font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:#8a8f9a;margin-top:6px;">Nivel: <strong style="color:{color};">{risk}</strong></div>
              </div>
            </div>
            <script>
            (function(){{
              const c=document.getElementById("gc");
              if(!c)return;
              const x=c.getContext("2d");
              const W=300,H=170,cx=150,cy=160,R=128,r=85;
              const target={pct},col="{color}";
              let cur=0;
              function rad(d){{return d*Math.PI/180;}}
              function draw(v){{
                x.clearRect(0,0,W,H);
                [[0,40,"#dcfce7"],[40,70,"#fef9c3"],[70,100,"#fee2e2"]].forEach(([s,e,fc])=>{{
                  x.beginPath();x.arc(cx,cy,R,rad(180+s*1.8),rad(180+e*1.8));
                  x.arc(cx,cy,r,rad(180+e*1.8),rad(180+s*1.8),true);
                  x.fillStyle=fc;x.fill();
                }});
                for(let i=0;i<=10;i++){{
                  const a=rad(180+i*18);
                  x.beginPath();x.moveTo(cx+(R-2)*Math.cos(a),cy+(R-2)*Math.sin(a));
                  x.lineTo(cx+(R+5)*Math.cos(a),cy+(R+5)*Math.sin(a));
                  x.strokeStyle="#d0d5dd";x.lineWidth=1.5;x.stroke();
                }}
                const a=rad(180+v*1.8);
                const nx=cx+(R-14)*Math.cos(a);
                const ny=cy+(R-14)*Math.sin(a);
                const lx=cx+8*Math.cos(a+Math.PI/2);
                const ly=cy+8*Math.sin(a+Math.PI/2);
                const rx=cx+8*Math.cos(a-Math.PI/2);
                const ry=cy+8*Math.sin(a-Math.PI/2);
                x.beginPath();x.moveTo(lx,ly);x.lineTo(nx,ny);x.lineTo(rx,ry);
                x.fillStyle=col;x.fill();
                x.beginPath();x.arc(cx,cy,9,0,Math.PI*2);x.fillStyle=col;x.fill();
                x.beginPath();x.arc(cx,cy,4,0,Math.PI*2);x.fillStyle="white";x.fill();
                x.font="bold 10px JetBrains Mono,monospace";x.fillStyle="#9ca3af";x.textAlign="center";
                x.fillText("0",cx-R+8,cy+14);x.fillText("50",cx,cy-R-6);x.fillText("100",cx+R-8,cy+14);
              }}
              function anim(){{
                cur+=(target-cur)*0.09;draw(cur);
                document.getElementById("gn").textContent=Math.round(cur)+"%";
                if(Math.abs(target-cur)>0.1)requestAnimationFrame(anim);
                else{{draw(target);document.getElementById("gn").textContent=target+"%";}}
              }}
              setTimeout(anim,100);
            }})();
            </script>
            ''', height=290)

            factores = []
            if trans < 8: factores.append(("Baja frecuencia", f"{trans} transacciones — el promedio del canal es mayor a 15."))
            if cajas < 15: factores.append(("Bajo volumen", f"{cajas} cajas vendidas — bajo el umbral de retención."))
            if prom_cajas < 2: factores.append(("Ticket reducido", f"Promedio {round(prom_cajas,1)} cajas/transacción — señal de desenganche."))
            if not factores: factores.append(("Perfil estable", "Indicadores dentro de rangos normales del canal."))

            factores_html = '<div class="card"><div class="card-header"><span class="card-title">Factores explicativos</span></div><div class="card-body">'
            for tag, txt in factores:
                factores_html += f'<div class="action-item"><div class="action-tag">{tag}</div><div class="action-text">{txt}</div></div>'
            factores_html += '</div></div>'
            st.markdown(factores_html, unsafe_allow_html=True)

            if proba > 0.4:
                st.markdown('<div class="card"><div class="card-header"><span class="card-title">Llamada de reenganche · Automatizada</span><span class="card-badge badge-danger">Activada</span></div><div class="card-body">', unsafe_allow_html=True)
                st.audio(str(BASE_DIR / 'data' / 'llamada_cliente.mp3'))
                st.markdown('</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="card"><div class="card-header"><span class="card-title">Resultado</span></div><div class="card-body" style="text-align:center;padding:60px 20px;"><p style="color:#9ca3af;font-size:13px;letter-spacing:0.5px;">Selecciona un cliente y presiona calcular</p></div></div>', unsafe_allow_html=True)

# ══ CENTRO OPERATIVO ══
elif pagina == "Centro operativo":
    st.markdown('<div class="page-header"><div class="page-title">Centro operativo</div><div class="page-sub">Protocolo de retención · Equipo comercial · Canal tradicional</div></div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown('<div class="oc-stat" style="border-top-color:#B00000;"><div class="oc-val" style="color:#B00000;">2,519</div><div class="oc-label">Contactar hoy</div></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="oc-stat" style="border-top-color:#d97706;"><div class="oc-val" style="color:#d97706;">19</div><div class="oc-label">Visita esta semana</div></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="oc-stat" style="border-top-color:#059669;"><div class="oc-val" style="color:#059669;">~882</div><div class="oc-label">Retención esperada</div></div>', unsafe_allow_html=True)
    with c4: st.markdown('<div class="oc-stat" style="border-top-color:#059669;"><div class="oc-val" style="color:#059669;">$4.2MM</div><div class="oc-label">Recuperación est.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card" style="border-top:3px solid #B00000;">
            <div class="card-header"><span class="card-title" style="color:#B00000;">Riesgo alto · 2,519 clientes</span></div>
            <div class="card-body">
                <div class="action-item" style="border-left-color:#B00000;"><div class="action-tag">Tiempo de respuesta</div><div class="action-text">Contacto en las próximas <strong>24 horas</strong> por el ejecutivo de cuenta asignado.</div></div>
                <div class="action-item" style="border-left-color:#B00000;"><div class="action-tag">Oferta de retención</div><div class="action-text">Descuento del <strong>15%</strong> en el próximo pedido o extensión de crédito sin costo.</div></div>
                <div class="action-item" style="border-left-color:#B00000;"><div class="action-tag">Llamada de reenganche</div><div class="action-text">Activar mensaje de voz automatizado como primer contacto antes de la visita.</div></div>
                <div class="action-item" style="border-left-color:#B00000;"><div class="action-tag">Seguimiento</div><div class="action-text">Revisión semanal del volumen de compra durante <strong>4 semanas</strong>.</div></div>
            </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card" style="border-top:3px solid #d97706;">
            <div class="card-header"><span class="card-title" style="color:#d97706;">Riesgo medio · 19 clientes</span></div>
            <div class="card-body">
                <div class="action-item" style="border-left-color:#d97706;"><div class="action-tag">Tiempo de respuesta</div><div class="action-text">Visita del promotor de ruta en los próximos <strong>7 días</strong>.</div></div>
                <div class="action-item" style="border-left-color:#d97706;"><div class="action-tag">Oferta de retención</div><div class="action-text">Promoción de volumen: compra <strong>10 cajas, obtén 1 gratis</strong>.</div></div>
                <div class="action-item" style="border-left-color:#d97706;"><div class="action-tag">Notificación interna</div><div class="action-text">Alerta al ejecutivo de zona con perfil y score del cliente.</div></div>
                <div class="action-item" style="border-left-color:#d97706;"><div class="action-tag">Seguimiento</div><div class="action-text">Revisión quincenal del indicador de transacciones.</div></div>
            </div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card" style="border-top:3px solid #059669;">
            <div class="card-header"><span class="card-title" style="color:#059669;">Riesgo bajo · 197,385 clientes</span></div>
            <div class="card-body">
                <div class="action-item" style="border-left-color:#059669;"><div class="action-tag">Monitoreo</div><div class="action-text">Seguimiento mensual automatizado sin intervención directa.</div></div>
                <div class="action-item" style="border-left-color:#059669;"><div class="action-tag">Fidelización</div><div class="action-text">Invitación a programa de lealtad si mantiene volumen por <strong>3 meses</strong>.</div></div>
                <div class="action-item" style="border-left-color:#059669;"><div class="action-tag">Alerta automática</div><div class="action-text">Notificación si el score supera <strong>40%</strong> en el siguiente ciclo mensual.</div></div>
                <div class="action-item" style="border-left-color:#059669;"><div class="action-tag">Re-evaluación</div><div class="action-text">Actualización mensual del score con el modelo.</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    df_mongo = get_mongo_data()
    if not df_mongo.empty:
        df_op = df_mongo[df_mongo['risk_level']=='alto'].sort_values('churn_proba', ascending=False).head(15).reset_index(drop=True)
        rows_html = ""
        for i, (_, row) in enumerate(df_op.iterrows()):
            pct = round(float(row['churn_proba'])*100,1)
            ingreso = round(pct/100*4760)
            accion = "Ejecutivo + Llamada de reenganche" if pct > 90 else "Ejecutivo de cuenta" if pct > 80 else "Promotor de zona"
            rows_html += f'<tr><td style="font-family:JetBrains Mono;font-size:11px;color:#6b7280;font-weight:600;">{i+1}</td><td style="font-family:JetBrains Mono;font-size:11px;">{str(row["customer_id"])[:20]}...</td><td style="font-family:JetBrains Mono;font-weight:700;color:#B00000;">{pct}%</td><td><span class="risk-alto">Alto</span></td><td style="font-family:JetBrains Mono;font-size:12px;color:#059669;font-weight:600;">${ingreso:,}</td><td style="font-size:12px;color:#374151;">{accion}</td></tr>'
        st.markdown(f'<div class="card"><div class="card-header"><span class="card-title">Lista operativa · Clientes de contacto prioritario</span><span class="card-badge badge-danger">Acción requerida hoy</span></div><div class="card-body-flush"><table class="html-table"><thead><tr><th>#</th><th>Cliente ID</th><th>Score</th><th>Nivel</th><th>Ingreso en riesgo</th><th>Acción recomendada</th></tr></thead><tbody>{rows_html}</tbody></table></div></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-header"><span class="card-title">Proyección de recuperación</span></div>
        <div class="card-body">
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;align-items:center;">
                <div style="text-align:center;padding:14px;background:#fef2f2;border:1px solid #fecaca;border-top:3px solid #B00000;">
                    <div style="font-family:JetBrains Mono;font-size:22px;font-weight:700;color:#B00000;">2,519</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Clientes en riesgo</div>
                </div>
                <div style="text-align:center;font-size:20px;color:#d1d5db;font-weight:300;">→</div>
                <div style="text-align:center;padding:14px;background:#fffbeb;border:1px solid #fde68a;border-top:3px solid #d97706;">
                    <div style="font-family:JetBrains Mono;font-size:22px;font-weight:700;color:#d97706;">35%</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Tasa de retención</div>
                </div>
                <div style="text-align:center;font-size:20px;color:#d1d5db;font-weight:300;">→</div>
                <div style="text-align:center;padding:14px;background:#f0fdf4;border:1px solid #86efac;border-top:3px solid #059669;">
                    <div style="font-family:JetBrains Mono;font-size:22px;font-weight:700;color:#059669;">$4.2 MM</div>
                    <div style="font-size:9px;color:#8a8f9a;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px;">Recuperación MXN</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
