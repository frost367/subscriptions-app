import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="مدير الأعمال", page_icon="📋", layout="centered")

DATA_FILE   = "data.json"
PROFIT_FILE = "profit.json"

def load(f):
    if Path(f).exists():
        with open(f,"r",encoding="utf-8") as fp: return json.load(fp)
    return {}

def save(f, d):
    with open(f,"w",encoding="utf-8") as fp: json.dump(d, fp, ensure_ascii=False, indent=2)

def days_left(s):
    try: return (datetime.strptime(s,"%Y-%m-%d").date()-datetime.today().date()).days
    except: return 0

def short(e): return e.split("@")[0][:9]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Tajawal',sans-serif!important;direction:rtl;}
.stApp{background:#f0f2f8;}
.block-container{padding:0.8rem!important;max-width:460px!important;margin:auto;}
.sub-header{border-radius:20px;padding:18px 20px;margin-bottom:12px;}
.sub-header h2{color:white!important;margin:0 0 10px;font-size:20px;}
.stats-row{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:7px;}
.stats-row-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;}
.stat-card{background:rgba(255,255,255,0.18);border-radius:12px;padding:8px 6px;text-align:center;}
.stat-card .num{font-size:19px;font-weight:900;color:white;}
.stat-card .lbl{font-size:10px;color:rgba(255,255,255,0.75);margin-top:2px;}
.stTabs [data-baseweb="tab-list"]{background:white;border-radius:14px;padding:5px;gap:4px;box-shadow:0 2px 8px #0001;}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:#6b7280;font-weight:700;font-size:12px;padding:6px 8px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#3730a3,#6d28d9)!important;color:white!important;}
.stExpander{background:white!important;border:1.5px solid #ede9fe!important;border-radius:16px!important;margin-bottom:10px!important;box-shadow:0 2px 10px #0001!important;}
div[data-testid="stExpander"] summary{font-family:Tajawal!important;font-size:13px!important;color:#1e1b4b!important;font-weight:700!important;padding:10px!important;}
.cl-box{border-radius:12px;padding:8px 4px;text-align:center;color:white;min-height:72px;display:flex;flex-direction:column;justify-content:center;align-items:center;background:linear-gradient(135deg,#3730a3,#6d28d9);box-shadow:0 3px 10px #6d28d933;}
.cl-box.warn{background:linear-gradient(135deg,#b45309,#d97706);}
.cl-box.danger{background:linear-gradient(135deg,#991b1b,#dc2626);}
.cl-box.empty{background:#f9fafb;border:2px dashed #d1d5db;color:#9ca3af;box-shadow:none;}
.cl-box b{font-size:11px;display:block;word-break:break-all;padding:0 2px;}
.cl-box span{font-size:10px;opacity:.85;margin-top:2px;}
.popup{background:white;border-radius:16px;padding:14px;border:1.5px solid #ede9fe;box-shadow:0 4px 18px #6d28d920;margin:8px 0;}
.popup-row{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #f3f4f6;font-size:13px;}
.popup-row:last-child{border:none;}
.popup-lbl{color:#9ca3af;font-size:12px;}
.card{background:white;border-radius:14px;padding:13px 16px;margin-bottom:8px;border:1.5px solid #ede9fe;}
.green-card{background:white;border-radius:14px;padding:13px 16px;margin-bottom:8px;border:1.5px solid #d1fae5;}
.month-stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:8px;}
.m-stat{border-radius:10px;padding:8px;text-align:center;}
.alert-r{background:#fff1f2;border:2px solid #fca5a5;border-radius:14px;padding:12px;margin:8px 0;color:#991b1b;font-size:13px;}
.alert-w{background:#fffbeb;border:2px solid #fcd34d;border-radius:14px;padding:12px;margin:8px 0;color:#92400e;font-size:13px;}
.preview{border-radius:12px;padding:12px;margin:8px 0;text-align:center;}
.stButton>button{color:white!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:10px!important;width:100%!important;font-family:Tajawal!important;background:linear-gradient(135deg,#3730a3,#6d28d9)!important;}
.stTextInput input,.stNumberInput input,.stDateInput input{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:11px!important;font-family:Tajawal!important;font-size:14px!important;padding:9px!important;}
.stTextarea textarea{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:11px!important;font-family:Tajawal!important;font-size:13px!important;}
label{color:#374151!important;font-family:Tajawal!important;font-size:13px!important;font-weight:600!important;}
hr{border-color:#ede9fe!important;margin:8px 0!important;}
</style>
""", unsafe_allow_html=True)

for k,v in [("sdata",None),("pdata",None),("selected",None),("add_slot",None)]:
    if k not in st.session_state: st.session_state[k]=v

if st.session_state.sdata is None: st.session_state.sdata = load(DATA_FILE)   or {"emails":[]}
if st.session_state.pdata is None: st.session_state.pdata = load(PROFIT_FILE) or {"products":[],"sales":[]}

sdata = st.session_state.sdata
pdata = st.session_state.pdata

all_clients  = [c for e in sdata.get("emails",[]) for c in e.get("clients",[])]
total_c      = len(all_clients)
paid_clients = [c for c in all_clients if c.get("paid","")=="نعم"]
total_paid   = sum(int(c.get("price",0) or 0) for c in paid_clients)
free_slots   = sum(5-len(e.get("clients",[])) for e in sdata.get("emails",[]))
active_c     = sum(1 for c in all_clients if days_left(c.get("end",""))>0)
cur_month    = datetime.today().strftime("%Y-%m")
all_sales    = pdata.get("sales",[])
month_sales  = [s for s in all_sales if s.get("date","").startswith(cur_month)]
m_rev    = sum(s.get("sell_price",0)*s.get("qty",1) for s in month_sales)
m_cost   = sum(s.get("cost_price",0)*s.get("qty",1) for s in month_sales)
m_profit = m_rev-m_cost
m_qty    = sum(s.get("qty",1) for s in month_sales)

main_tab1, main_tab2 = st.tabs(["📋  الاشتراكات", "💰  دفتر الفائدة"])

# ╔═══════════════ SUBSCRIPTIONS ═══════════════╗
with main_tab1:
    st.markdown(f"""
<div class="sub-header" style="background:linear-gradient(135deg,#3730a3,#6d28d9);">
<h2>📋 الاشتراكات الشهرية <span style="font-size:12px;opacity:.7;">{datetime.today().strftime('%d/%m/%Y')}</span></h2>
<div class="stats-row">
<div class="stat-card"><div class="num">{total_c}</div><div class="lbl">زبائن</div></div>
<div class="stat-card"><div class="num">{active_c}</div><div class="lbl">نشطون</div></div>
<div class="stat-card"><div class="num">{free_slots}</div><div class="lbl">فارغة</div></div>
<div class="stat-card"><div class="num">{total_paid}</div><div class="lbl">دج</div></div>
</div></div>""", unsafe_allow_html=True)

    s1,s2,s3,s4 = st.tabs(["📧 الإيميلات","🔔 تنبيهات","📊 إحصائيات","➕ إضافة"])

    with s1:
        search = st.text_input("", placeholder="🔍 ابحث...", key="srch")
        elist = sdata.get("emails",[])
        if search: elist=[e for e in elist if search.lower() in e["email"].lower()]
        if not elist: st.info("لا توجد إيميلات — أضف من تبويب ➕")

        for ei,em in enumerate(elist):
            clients=em.get("clients",[])
            dll=[days_left(c.get("end","")) for c in clients]
            mdl=min(dll) if dll else 0
            icon="🔴" if any(d<=0 for d in dll) else ("🟡" if any(0<d<=2 for d in dll) else ("🟢" if clients else "⚪"))
            with st.expander(f"{icon}  {em['email']}  ·  {len(clients)}/5  ·  ⏳{mdl}د"):
                st.caption(f"🛠 {em.get('service','—')}  |  📅 {em.get('start','—')}")
                cols=st.columns(5)
                for slot in range(5):
                    with cols[slot]:
                        if slot<len(clients):
                            c=clients[slot]; dl=days_left(c.get("end",""))
                            cls="danger" if dl<=0 else ("warn" if dl<=2 else "")
                            st.markdown(f'<div class="cl-box {cls}"><b>{short(c.get("email","?"))}</b><span>{dl}d</span></div>',unsafe_allow_html=True)
                            if st.button("👁",key=f"v_{ei}_{slot}"):
                                st.session_state.selected=None if st.session_state.selected==(ei,slot) else (ei,slot)
                                st.session_state.add_slot=None
                        else:
                            st.markdown('<div class="cl-box empty"><b style="font-size:18px;">+</b><span>فارغ</span></div>',unsafe_allow_html=True)
                            if st.button("➕",key=f"a_{ei}_{slot}"):
                                st.session_state.add_slot=None if st.session_state.add_slot==(ei,slot) else (ei,slot)
                                st.session_state.selected=None

                sel=st.session_state.selected
                if sel and sel[0]==ei and sel[1]<len(clients):
                    ci=sel[1]; c=clients[ci]; dl=days_left(c.get("end",""))
                    sc="#dc2626" if dl<=0 else ("#d97706" if dl<=2 else "#16a34a")
                    st_txt="⛔ منتهي" if dl<=0 else (f"⚠️ {dl} يوم" if dl<=2 else f"✅ {dl} يوم")
                    st.markdown(f"""<div class="popup">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
<b style="font-size:15px;color:#1e1b4b;">👤 {short(c.get('email',''))}</b>
<span style="color:{sc};font-weight:700;font-size:13px;">{st_txt}</span></div>
<div class="popup-row"><span class="popup-lbl">📧 الإيميل</span><span>{c.get('email','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">📅 البداية</span><span>{c.get('start','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">📅 النهاية</span><span>{c.get('end','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">💰 السعر</span><span>{c.get('price','—')} دج</span></div>
<div class="popup-row"><span class="popup-lbl">💳 الدفع</span><span>{'✅ دفع' if c.get('paid')=='نعم' else '❌ لم يدفع'}</span></div>
</div>""",unsafe_allow_html=True)
                    nn=st.text_area("📝 ملاحظة",value=c.get("note",""),key=f"nt_{ei}_{ci}",height=70)
                    cc1,cc2=st.columns(2)
                    with cc1:
                        if st.button("💾 حفظ",key=f"sn_{ei}_{ci}"):
                            ri=next(i for i,e in enumerate(sdata["emails"]) if e["email"]==em["email"])
                            sdata["emails"][ri]["clients"][ci]["note"]=nn
                            save(DATA_FILE,sdata); st.session_state.sdata=sdata; st.success("✅")
                    with cc2:
                        if st.button("🗑 حذف",key=f"dc_{ei}_{ci}"):
                            ri=next(i for i,e in enumerate(sdata["emails"]) if e["email"]==em["email"])
                            sdata["emails"][ri]["clients"].pop(ci)
                            save(DATA_FILE,sdata); st.session_state.sdata=sdata
                            st.session_state.selected=None; st.rerun()

                asl=st.session_state.add_slot
                if asl and asl[0]==ei:
                    st.markdown("---")
                    st.markdown("**➕ إضافة زبون**")
                    ce=st.text_input("📧 إيميل الزبون",key=f"nce_{ei}")
                    cp=st.number_input("💰 السعر (دج)",min_value=0,key=f"ncp_{ei}")
                    cs=st.date_input("📅 البداية",key=f"ncs_{ei}",value=datetime.today())
                    # النهاية تلقائياً 30 يوم
                    ced=cs+timedelta(days=30)
                    st.info(f"📅 النهاية تلقائياً: {ced.strftime('%Y-%m-%d')} (30 يوم)")
                    cpaid=st.radio("💳 هل دفع؟",["نعم","لا"],key=f"ncp2_{ei}",horizontal=True)
                    if st.button("✅ إضافة",key=f"nadd_{ei}"):
                        if ce.strip():
                            ri=next(i for i,e in enumerate(sdata["emails"]) if e["email"]==em["email"])
                            sdata["emails"][ri]["clients"].append({
                                "email":ce.strip(),"name":ce.strip().split("@")[0],
                                "start":cs.strftime("%Y-%m-%d"),
                                "end":ced.strftime("%Y-%m-%d"),
                                "price":str(cp),"paid":cpaid,"note":""
                            })
                            save(DATA_FILE,sdata); st.session_state.sdata=sdata
                            st.session_state.add_slot=None; st.success("✅ تم!"); st.rerun()
                        else: st.error("أدخل الإيميل!")

                st.divider()
                if st.button("🗑 حذف الإيميل كاملاً",key=f"dem_{ei}"):
                    ri=next(i for i,e in enumerate(sdata["emails"]) if e["email"]==em["email"])
                    sdata["emails"].pop(ri); save(DATA_FILE,sdata)
                    st.session_state.sdata=sdata; st.session_state.selected=None
                    st.session_state.add_slot=None; st.rerun()

    with s2:
        st.markdown("### 🔔 التنبيهات")
        found=False
        for em in sdata.get("emails",[]):
            for c in em.get("clients",[]):
                dl=days_left(c.get("end",""))
                if dl<=0:
                    st.markdown(f'<div class="alert-r">⛔ <b>انتهى!</b> {c.get("email","")} | {em["email"]} | {c.get("end","")}</div>',unsafe_allow_html=True); found=True
                elif dl<=2:
                    st.markdown(f'<div class="alert-w">⚠️ <b>{dl} يوم!</b> {c.get("email","")} | {em["email"]} | {c.get("end","")}</div>',unsafe_allow_html=True); found=True
        if not found: st.success("✅ كل الاشتراكات بخير!")

    with s3:
        st.markdown("### 📊 إحصائيات الشهر الحالي")
        mn=[c for c in all_clients if c.get("start","").startswith(cur_month)]
        mp=[c for c in mn if c.get("paid","")=="نعم"]
        mps=sum(int(c.get("price",0) or 0) for c in mp)
        st.markdown(f"""<div class="card">
<div style="font-weight:700;color:#3730a3;font-size:15px;margin-bottom:10px;">📅 {cur_month}</div>
<div class="month-stats">
<div class="m-stat" style="background:#f5f3ff;"><div style="font-size:17px;font-weight:900;color:#3730a3;">{len(mn)}</div><div style="font-size:10px;color:#7c3aed;">زبائن جدد</div></div>
<div class="m-stat" style="background:#f5f3ff;"><div style="font-size:17px;font-weight:900;color:#3730a3;">{mps}</div><div style="font-size:10px;color:#7c3aed;">دج مدفوعة</div></div>
<div class="m-stat" style="background:#f5f3ff;"><div style="font-size:17px;font-weight:900;color:#3730a3;">{active_c}</div><div style="font-size:10px;color:#7c3aed;">نشطون</div></div>
</div></div>""",unsafe_allow_html=True)
        for c in mn:
            pi="✅" if c.get("paid","")=="نعم" else "❌"
            st.markdown(f'<div style="background:white;border-radius:11px;padding:9px 14px;margin:5px 0;border:1.5px solid #ede9fe;font-size:13px;display:flex;justify-content:space-between;"><span>📧 {c.get("email","—")}</span><span>{pi} {c.get("price","0")} دج</span></div>',unsafe_allow_html=True)
        if st.button("🔄 تحديث",key="ref_s"):
            st.session_state.sdata=load(DATA_FILE) or {"emails":[]}; st.rerun()

    with s4:
        st.markdown("### ➕ إضافة إيميل جديد")
        ne=st.text_input("📧 الإيميل الكامل",placeholder="example@gmail.com")
        np_=st.text_input("🔑 كلمة المرور",type="password")
        nserv=st.text_input("🛠 اسم الخدمة",placeholder="Netflix ...")
        nstart=st.date_input("📅 بداية الاشتراك السنوي",value=datetime.today())
        if st.button("💾 حفظ الإيميل",key="save_em"):
            if ne.strip():
                if any(e["email"]==ne.strip() for e in sdata["emails"]):
                    st.error("⚠️ موجود مسبقاً!")
                else:
                    sdata["emails"].append({"email":ne.strip(),"password":np_,
                        "service":nserv,"start":nstart.strftime("%Y-%m-%d"),"clients":[]})
                    save(DATA_FILE,sdata); st.session_state.sdata=sdata
                    st.success(f"✅ تم إضافة {ne}"); st.rerun()
            else: st.error("أدخل الإيميل!")

# ╔═══════════════ PROFIT ═══════════════╗
with main_tab2:
    st.markdown(f"""
<div class="sub-header" style="background:linear-gradient(135deg,#065f46,#059669);">
<h2>💰 دفتر الفائدة <span style="font-size:12px;opacity:.7;">{datetime.today().strftime('%d/%m/%Y')}</span></h2>
<div class="stats-row-3">
<div class="stat-card"><div class="num">{m_qty}</div><div class="lbl">مباع الشهر</div></div>
<div class="stat-card"><div class="num">{m_rev}</div><div class="lbl">دج إيراد</div></div>
<div class="stat-card"><div class="num">{m_profit}</div><div class="lbl">دج فائدة</div></div>
</div></div>""",unsafe_allow_html=True)
    
p1,p2,p3,p4=st.tabs(["📦 المنتجات","🧾 مبيعات اليوم","📊 الشهري","➕ منتج"])

with p1:
        st.markdown("### 📦 قائمة المنتجات")
        prods=pdata.get("products",[])
        if not prods: st.info("لا توجد منتجات — أضف من تبويب ➕")
        for pi,p in enumerate(prods):
            pu=p.get("sell_price",0)-p.get("cost_price",0)
            st.markdown(f"""<div class="green-card">
<div style="display:flex;justify-content:space-between;margin-bottom:6px;">
<b style="font-size:15px;color:#065f46;">📦 {p.get('name','—')}</b>
<span style="background:#dcfce7;color:#065f46;padding:2px 10px;border-radius:20px;font-size:12px;font-weight:700;">+{pu} دج</span></div>
<div style="color:#6b7280;font-size:13px;">💸 التكلفة: {p.get('cost_price',0)} دج · 💰 البيع: {p.get('sell_price',0)} دج</div>
</div>""",unsafe_allow_html=True)
            if st.button(f"🗑 حذف {p.get('name','')}",key=f"dp_{pi}"):
                pdata["products"].pop(pi); save(PROFIT_FILE,pdata)
                st.session_state.pdata=pdata; st.rerun()

    with p2:
        st.markdown("### 🧾 تسجيل مبيعة")
        prods=pdata.get("products",[])
        if not prods:
            st.warning("أضف منتجاً أولاً!")
        else:
            sp=st.selectbox("📦 المنتج",[p["name"] for p in prods],key="sp")
            selp=next(p for p in prods if p["name"]==sp)
            qty=st.number_input("🔢 الكمية",min_value=1,value=1,key="qty")
            sd=st.date_input("📅 التاريخ",value=datetime.today(),key="sdate")
            prv=(selp.get("sell_price",0)-selp.get("cost_price",0))*qty
            rvv=selp.get("sell_price",0)*qty
            st.markdown(f"""<div class="preview" style="background:#ecfdf5;border:1.5px solid #6ee7b7;">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center;">
<div><div style="font-size:18px;font-weight:900;color:#065f46;">{rvv} دج</div><div style="font-size:11px;color:#059669;">الإيراد</div></div>
<div><div style="font-size:18px;font-weight:900;color:#065f46;">{prv} دج</div><div style="font-size:11px;color:#059669;">الفائدة</div></div>
</div></div>""",unsafe_allow_html=True)
            if st.button("✅ تسجيل",key="regsale"):
                pdata["sales"].append({"product":sp,"qty":qty,
                    "sell_price":selp.get("sell_price",0),"cost_price":selp.get("cost_price",0),
                    "date":sd.strftime("%Y-%m-%d")})
                save(PROFIT_FILE,pdata); st.session_state.pdata=pdata
                st.success(f"✅ {qty}x {sp}"); st.rerun()
        st.markdown("---")
        st.markdown("#### 📋 مبيعات اليوم")
        tds=datetime.today().strftime("%Y-%m-%d")
        tdsl=[s for s in pdata.get("sales",[]) if s.get("date","")==tds]
        if not tdsl: st.info("لا توجد مبيعات اليوم")
        for s in tdsl:
            rv=s.get("sell_price",0)*s.get("qty",1)
            pr=(s.get("sell_price",0)-s.get("cost_price",0))*s.get("qty",1)
            st.markdown(f'<div style="background:white;border-radius:12px;padding:10px 14px;margin:5px 0;border:1.5px solid #d1fae5;font-size:13px;display:flex;justify-content:space-between;"><span>📦 {s.get("product","")} × {s.get("qty",1)}</span><span style="color:#065f46;font-weight:700;">{rv} دج | +{pr} دج</span></div>',unsafe_allow_html=True)

    with p3:
        st.markdown("### 📊 ملخص شهري")
        ams=sorted(set(s.get("date","")[:7] for s in pdata.get("sales",[])),reverse=True)
        if not ams: st.info("لا توجد بيانات بعد")
        
