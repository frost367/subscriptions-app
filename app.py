import streamlit as st
import json
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="دفتر الفائدة", page_icon="💰", layout="centered")

PROFIT_FILE = "profit_data.json"

def load():
    if Path(PROFIT_FILE).exists():
        with open(PROFIT_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"products":[], "sales":[]}

def save(data):
    with open(PROFIT_FILE,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Tajawal',sans-serif!important;direction:rtl;}
.stApp{background:#f0fdf4;}
.block-container{padding:0.8rem!important;max-width:460px!important;margin:auto;}
.profit-header{background:linear-gradient(135deg,#065f46,#059669);border-radius:20px;padding:18px 20px;margin-bottom:12px;}
.profit-header h2{color:white!important;margin:0 0 10px;font-size:20px;}
.stats-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}
.stat-card{background:rgba(255,255,255,0.2);border-radius:12px;padding:8px 6px;text-align:center;}
.stat-card .num{font-size:20px;font-weight:900;color:white;}
.stat-card .lbl{font-size:10px;color:#a7f3d0;margin-top:2px;}
.stTabs [data-baseweb="tab-list"]{background:white;border-radius:14px;padding:5px;gap:4px;box-shadow:0 2px 8px #0001;}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:#6b7280;font-weight:700;font-size:12px;padding:6px 8px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#065f46,#059669)!important;color:white!important;}
.prod-card{background:white;border-radius:14px;padding:13px 16px;margin-bottom:8px;border:1.5px solid #d1fae5;box-shadow:0 2px 8px #05966911;}
.sale-card{background:white;border-radius:14px;padding:12px 16px;margin-bottom:8px;border:1.5px solid #d1fae5;display:flex;justify-content:space-between;align-items:center;}
.month-card{background:white;border-radius:16px;padding:14px;margin-bottom:10px;border:1.5px solid #d1fae5;box-shadow:0 2px 10px #05966909;}
.m-stat{background:#ecfdf5;border-radius:10px;padding:8px;text-align:center;}
.m-stat .n{font-size:18px;font-weight:900;color:#065f46;}
.m-stat .l{font-size:10px;color:#059669;}
.stButton>button{background:linear-gradient(135deg,#065f46,#059669)!important;color:white!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:10px!important;width:100%!important;font-family:Tajawal!important;}
.stTextInput input,.stNumberInput input,.stDateInput input,.stSelectbox select{background:white!important;color:#064e3b!important;border:1.5px solid #a7f3d0!important;border-radius:11px!important;font-family:Tajawal!important;font-size:14px!important;padding:9px!important;}
label{color:#374151!important;font-family:Tajawal!important;font-size:13px!important;font-weight:600!important;}
hr{border-color:#d1fae5!important;margin:8px 0!important;}
</style>
""", unsafe_allow_html=True)

if "pdata" not in st.session_state:
    st.session_state.pdata = load()

pdata = st.session_state.pdata

# ── إحصائيات ───────────────────────────
all_sales    = pdata.get("sales",[])
cur_month    = datetime.today().strftime("%Y-%m")
month_sales  = [s for s in all_sales if s.get("date","").startswith(cur_month)]
total_rev    = sum(s.get("sell_price",0)*s.get("qty",1) for s in month_sales)
total_cost   = sum(s.get("cost_price",0)*s.get("qty",1) for s in month_sales)
total_profit = total_rev - total_cost
total_qty    = sum(s.get("qty",1) for s in month_sales)

st.markdown(f"""
<div class="profit-header">
  <h2>💰 دفتر الفائدة &nbsp;<span style="font-size:12px;opacity:.7;">{datetime.today().strftime('%d/%m/%Y')}</span></h2>
  <div class="stats-row">
    <div class="stat-card"><div class="num">{total_qty}</div><div class="lbl">مبيعات الشهر</div></div>
    <div class="stat-card"><div class="num">{total_rev}</div><div class="lbl">دج إيراد</div></div>
    <div class="stat-card"><div class="num">{total_profit}</div><div class="lbl">دج فائدة</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📦 المنتجات","🧾 مبيعات اليوم","📊 الشهري","➕ منتج جديد"])

# ══════ TAB 1 — المنتجات ══════
with tab1:
    st.markdown("### 📦 قائمة المنتجات")
    products = pdata.get("products",[])
    if not products:
        st.info("لا توجد منتجات — أضف من تبويب ➕")
    for pi, p in enumerate(products):
        profit_unit = p.get("sell_price",0) - p.get("cost_price",0)
        st.markdown(f"""
<div class="prod-card">
  <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
    <b style="font-size:15px;color:#065f46;">📦 {p.get('name','—')}</b>
    <span style="background:#ecfdf5;color:#065f46;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:700;">+{profit_unit} دج/وحدة</span>
  </div>
  <div style="color:#6b7280;font-size:13px;line-height:2;">
    💸 التكلفة: {p.get('cost_price',0)} دج &nbsp;·&nbsp;
    💰 البيع: {p.get('sell_price',0)} دج
  </div>
</div>""", unsafe_allow_html=True)
        if st.button(f"🗑 حذف {p.get('name','')}", key=f"delprod_{pi}"):
            pdata["products"].pop(pi)
            save(pdata); st.session_state.pdata=pdata; st.rerun()

# ══════ TAB 2 — مبيعات اليوم ══════
with tab2:
    st.markdown("### 🧾 تسجيل مبيعة اليوم")
    products = pdata.get("products",[])
    if not products:
        st.warning("أضف منتجاً أولاً من تبويب ➕")
    else:
        prod_names = [p["name"] for p in products]
        sel_prod = st.selectbox("📦 اختر المنتج", prod_names)
        sel_p    = next(p for p in products if p["name"]==sel_prod)
        qty      = st.number_input("🔢 الكمية المباعة", min_value=1, value=1)
        sale_date = st.date_input("📅 التاريخ", value=datetime.today())

        profit_preview = (sel_p.get("sell_price",0) - sel_p.get("cost_price",0)) * qty
        rev_preview    = sel_p.get("sell_price",0) * qty

        st.markdown(f"""
<div style="background:#ecfdf5;border-radius:12px;padding:12px;margin:10px 0;border:1.5px solid #6ee7b7;">
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center;">
    <div><div style="font-size:18px;font-weight:900;color:#065f46;">{rev_preview} دج</div><div style="font-size:11px;color:#059669;">الإيراد</div></div>
    <div><div style="font-size:18px;font-weight:900;color:#065f46;">{profit_preview} دج</div><div style="font-size:11px;color:#059669;">الفائدة</div></div>
  </div>
</div>""", unsafe_allow_html=True)

        if st.button("✅ تسجيل المبيعة"):
            pdata["sales"].append({
                "product":  sel_prod,
                "qty":      qty,
                "sell_price": sel_p.get("sell_price",0),
                "cost_price": sel_p.get("cost_price",0),
                "date":     sale_date.strftime("%Y-%m-%d")
            })
            save(pdata); st.session_state.pdata=pdata
            st.success(f"✅ تم تسجيل {qty}x {sel_prod}!"); st.rerun()

    st.markdown("---")
    st.markdown("#### 📋 مبيعات اليوم")
    today_str  = datetime.today().strftime("%Y-%m-%d")
    today_sales = [s for s in pdata.get("sales",[]) if s.get("date","")==today_str]
    if not today_sales:
        st.info("لا توجد مبيعات اليوم بعد")
    for s in today_sales:
        p  = s.get("sell_price",0)*s.get("qty",1)
        pr = (s.get("sell_price",0)-s.get("cost_price",0))*s.get("qty",1)
        st.markdown(f"""
<div class="sale-card">
  <span>📦 {s.get('product','')} × {s.get('qty',1)}</span>
  <span style="color:#065f46;font-weight:700;">{p} دج &nbsp;|&nbsp; +{pr} دج</span>
</div>""", unsafe_allow_html=True)

# ══════ TAB 3 — الشهري ══════
with tab3:
    st.markdown("### 📊 ملخص شهري")
    all_months = sorted(set(s.get("date","")[:7] for s in pdata.get("sales",[])), reverse=True)
    if not all_months:
        st.info("لا توجد بيانات بعد")
    for m in all_months:
        m_sales  = [s for s in pdata.get("sales",[]) if s.get("date","").startswith(m)]
        m_rev    = sum(s.get("sell_price",0)*s.get("qty",1) for s in m_sales)
        m_cost   = sum(s.get("cost_price",0)*s.get("qty",1) for s in m_sales)
        m_profit = m_rev - m_cost
        m_qty    = sum(s.get("qty",1) for s in m_sales)
        st.markdown(f"""
<div class="month-card">
  <div style="font-weight:700;color:#065f46;font-size:15px;margin-bottom:8px;">📅 {m}</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
    <div class="m-stat"><div class="n">{m_qty}</div><div class="l">مباع</div></div>
    <div class="m-stat"><div class="n">{m_rev}</div><div class="l">دج إيراد</div></div>
    <div class="m-stat"><div class="n">{m_profit}</div><div class="l">دج فائدة</div></div>
  </div>
</div>""", unsafe_allow_html=True)

# ══════ TAB 4 — منتج جديد ══════
with tab4:
    st.markdown("### ➕ إضافة منتج جديد")
    p_name = st.text_input("📦 اسم المنتج", placeholder="مثال: Netflix 1 شهر")
    p_cost = st.number_input("💸 سعر التكلفة (دج)", min_value=0)
    p_sell = st.number_input("💰 سعر البيع (دج)",   min_value=0)
    if p_sell > p_cost:
        st.markdown(f"""
<div style="background:#ecfdf5;border-radius:12px;padding:10px;border:1.5px solid #6ee7b7;text-align:center;">
  <b style="color:#065f46;font-size:16px;">الفائدة لكل وحدة: {p_sell-p_cost} دج ✅</b>
</div>""", unsafe_allow_html=True)
    if st.button("💾 حفظ المنتج"):
        if p_name.strip():
            pdata["products"].append({"name":p_name.strip(),"cost_price":p_cost,"sell_price":p_sell})
            save(pdata); st.session_state.pdata=pdata
            st.success(f"✅ تم إضافة {p_name}"); st.rerun()
        else:
            st.error("أدخل اسم المنتج!")
