import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="مدير الاشتراكات", page_icon="📋", layout="centered")

DATA_FILE = "data.json"

def load():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"emails": []}

def save(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def days_left(date_str):
    try:
        return (datetime.strptime(date_str, "%Y-%m-%d").date() - datetime.today().date()).days
    except:
        return 0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700;900&display=swap');
html,body,[class*="css"]{font-family:'Tajawal',sans-serif!important;direction:rtl;}
.stApp{background:#0a0a14;}
.block-container{padding:0.8rem!important;max-width:460px!important;margin:auto;}
.stTabs [data-baseweb="tab-list"]{background:#1a1a2e;border-radius:12px;padding:4px;gap:3px;}
.stTabs [data-baseweb="tab"]{border-radius:8px;color:#94a3b8;font-weight:700;font-size:14px;padding:6px 10px;}
.stTabs [aria-selected="true"]{background:#7c3aed!important;color:white!important;}
.stButton>button{background:linear-gradient(135deg,#7c3aed,#a855f7)!important;color:white!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:15px!important;padding:10px!important;width:100%!important;font-family:Tajawal!important;}
.stTextInput input,.stNumberInput input,.stDateInput input{background:#1e1e3a!important;color:#f1f5f9!important;border:1.5px solid #7c3aed66!important;border-radius:10px!important;font-family:Tajawal!important;font-size:15px!important;}
.stExpander{border:1px solid #7c3aed44!important;border-radius:14px!important;background:#13131f!important;margin-bottom:8px!important;}
label{color:#94a3b8!important;font-family:Tajawal!important;}
h1{color:#a855f7!important;text-align:center;}
.stSuccess,.stError,.stWarning,.stInfo{border-radius:10px!important;font-family:Tajawal!important;}
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = load()
data = st.session_state.data

st.markdown("# 📋 مدير الاشتراكات")

tab1, tab2, tab3 = st.tabs(["📧 الإيميلات", "🔔 تنبيهات", "➕ إضافة"])

with tab1:
    search = st.text_input("", placeholder="🔍 ابحث عن إيميل أو زبون...")
    emails_list = data.get("emails", [])
    if search:
        emails_list = [e for e in emails_list
                       if search.lower() in e["email"].lower()
                       or any(search.lower() in c.get("email","").lower() for c in e.get("clients",[]))]

    if not emails_list:
        st.info("لا توجد إيميلات — أضف من تبويب ➕")
    else:
        for ei, em in enumerate(emails_list):
            clients = em.get("clients", [])
            dl_list = [days_left(c.get("end","")) for c in clients]
            min_dl  = min(dl_list) if dl_list else 999

            if any(d <= 0 for d in dl_list):   icon = "🔴"
            elif any(0 < d <= 2 for d in dl_list): icon = "🟡"
            else: icon = "🟢"

            days_txt = f"{min_dl} يوم" if clients else "فارغ"
            label = f"{icon}  {em['email']}  ·  {len(clients)}/5  ·  ⏳{days_txt}"

            with st.expander(label):
                st.caption(f"🛠 {em.get('service','—')}   📅 بداية الاشتراك: {em.get('start','—')}")

                if not clients:
                    st.caption("— لا يوجد زبائن بعد —")

                for ci, c in enumerate(clients):
                    dl = days_left(c.get("end",""))
                    if dl <= 0:
                        status = "🔴 منتهي"
                        color  = "#ef4444"
                    elif dl <= 2:
                        status = f"🟡 باقي {dl} يوم"
                        color  = "#f59e0b"
                    else:
                        status = f"🟢 باقي {dl} يوم"
                        color  = "#22c55e"

                    paid = "✅ دفع" if c.get("paid") == "نعم" else "❌ لم يدفع"

                    st.markdown(f"""
<div style="background:#1e1e3a;border-radius:12px;padding:12px 14px;margin:6px 0;border-right:4px solid {color};">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
  <span style="font-weight:700;font-size:15px;color:#e2e8f0;">👤 {c.get('name','—')}</span>
  <span style="font-size:13px;font-weight:700;color:{color};">{status}</span>
</div>
<div style="color:#94a3b8;font-size:13px;line-height:2;">
  📧 {c.get('email','—')}<br>
  📅 {c.get('start','—')} &nbsp;←&nbsp; {c.get('end','—')}<br>
  💰 {c.get('price','—')} دج &nbsp;&nbsp; {paid}
</div>
</div>""", unsafe_allow_html=True)

                    if st.button(f"🗑 حذف  {c.get('name','')}", key=f"del_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].pop(ci)
                        save(data); st.session_state.data = data; st.rerun()

                st.divider()

                if len(clients) < 5:
                    st.markdown("**➕ إضافة زبون**")
                    cn    = st.text_input("👤 اسم الزبون",    key=f"cn_{ei}")
                    ce    = st.text_input("📧 إيميل الزبون",  key=f"ce_{ei}")
                    cp    = st.number_input("💰 السعر دج", min_value=0, key=f"cp_{ei}")
                    cs    = st.date_input("📅 البداية",  key=f"cs_{ei}",  value=datetime.today())
                    ced   = st.date_input("📅 النهاية",  key=f"ced_{ei}", value=datetime.today()+timedelta(days=30))
                    cpaid = st.radio("💳 هل دفع؟", ["نعم","لا"], key=f"cpaid_{ei}", horizontal=True)

                    if st.button("✅ إضافة الزبون", key=f"addcl_{ei}"):
                        if cn.strip():
                            ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                            data["emails"][ri]["clients"].append({
                                "name":cn.strip(), "email":ce.strip(),
                                "start":cs.strftime("%Y-%m-%d"),
                                "end":ced.strftime("%Y-%m-%d"),
                                "price":str(cp), "paid":cpaid
                            })
                            save(data); st.session_state.data = data
                            st.success("✅ تم إضافة الزبون!"); st.rerun()
                        else:
                            st.error("أدخل اسم الزبون!")
                else:
                    st.warning("⚠️ الحد الأقصى 5 زبائن")

                st.divider()
                if st.button("🗑 حذف هذا الإيميل كاملاً", key=f"demail_{ei}"):
                    ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                    data["emails"].pop(ri)
                    save(data); st.session_state.data = data; st.rerun()

with tab2:
    st.markdown("### 🔔 التنبيهات")
    found = False
    for em in data.get("emails", []):
        for c in em.get("clients", []):
            dl = days_left(c.get("end",""))
            if dl <= 0:
                st.error(f"⛔ انتهى الاشتراك!  |  👤 {c.get('name','')}  |  📧 {em['email']}  |  📅 {c.get('end','')}")
                found = True
            elif dl <= 2:
                st.warning(f"⚠️ ينتهي خلال {dl} يوم!  |  👤 {c.get('name','')}  |  📧 {em['email']}  |  📅 {c.get('end','')}")
                found = True
    if not found:
        st.success("✅ كل الاشتراكات بخير! لا توجد تنبيهات.")

with tab3:
    st.markdown("### ➕ إضافة إيميل جديد")
    new_email = st.text_input("📧 الإيميل الكامل", placeholder="example@gmail.com")
    new_pass  = st.text_input("🔑 كلمة المرور", type="password")
    new_serv  = st.text_input("🛠 اسم الخدمة",  placeholder="Netflix / Spotify ...")
    new_start = st.date_input("📅 تاريخ بداية الاشتراك السنوي", value=datetime.today())

    if st.button("💾 حفظ الإيميل"):
        if new_email.strip():
            if any(e["email"]==new_email.strip() for e in data["emails"]):
                st.error("⚠️ هذا الإيميل موجود مسبقاً!")
            else:
                data["emails"].append({
                    "email":   new_email.strip(),
                    "password": new_pass,
                    "service":  new_serv,
                    "start":    new_start.strftime("%Y-%m-%d"),
                    "clients":  []
                })
                save(data); st.session_state.data = data
                st.success(f"✅ تم إضافة {new_email}"); st.rerun()
        else:
            st.error("أدخل الإيميل أولاً!").badge-red    { background:#7f1d1d; color:#fca5a5; padding:3px 10px; border-radius:20px; font-size:13px; }
.alert-red  { background:#7f1d1d; border:1px solid #ef4444; border-radius:10px; padding:12px 16px; margin:6px 0; color:#fca5a5; font-weight:700; }
.alert-warn { background:#78350f; border:1px solid #f59e0b; border-radius:10px; padding:12px 16px; margin:6px 0; color:#fde68a; font-weight:700; }
h1,h2,h3 { color:#a855f7 !important; }
.stButton>button { background:linear-gradient(135deg,#7c3aed,#a855f7) !important; color:white !important; border:none !important; border-radius:10px !important; font-weight:700 !important; width:100%; }
.stTextInput>div>input, .stNumberInput>div>input { background:#1e1e3a !important; color:#f1f5f9 !important; border:1px solid #7c3aed55 !important; border-radius:8px !important; }
label { color:#94a3b8 !important; }
hr { border-color:#7c3aed33 !important; }
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = load()

data = st.session_state.data

st.markdown("<h1 style='text-align:center;font-size:28px;'>📋 مدير الاشتراكات</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📧 الإيميلات", "🔔 التنبيهات", "➕ إضافة"])

with tab1:
    search = st.text_input("🔍 بحث بالإيميل", placeholder="ابحث عن إيميل...")
    emails = data.get("emails", [])
    if search:
        emails = [e for e in emails if search.lower() in e["email"].lower()
                  or any(search.lower() in c.get("email","").lower() for c in e.get("clients",[]))]
    if not emails:
        st.info("لا توجد إيميلات — أضف من تبويب ➕ إضافة")
    else:
        for ei, em in enumerate(emails):
            clients = em.get("clients", [])
            alerts = sum(1 for c in clients if days_left(c.get("end","")) <= 0)
            warns  = sum(1 for c in clients if 0 < days_left(c.get("end","")) <= 2)
            if alerts:  badge = f"<span class='badge-red'>⛔ {alerts} منتهي</span>"
            elif warns: badge = f"<span class='badge-yellow'>⚠️ {warns} قريب</span>"
            else:       badge = f"<span class='badge-green'>✅ نشط</span>"
            with st.expander(f"📧 {em['email']}   —   {len(clients)}/5 زبائن   {badge}"):
                for ci, c in enumerate(clients):
                    dl = days_left(c.get("end",""))
                    card_class = "danger" if dl<=0 else ("warning" if dl<=2 else "")
                    if dl<=0:   status_html = "<span class='badge-red'>⛔ منتهي</span>"
                    elif dl<=2: status_html = f"<span class='badge-yellow'>⚠️ باقي {dl} يوم</span>"
                    else:       status_html = f"<span class='badge-green'>✅ باقي {dl} يوم</span>"
                    st.markdown(f"""
                    <div class='client-card {card_class}'>
                      <b style='color:#e2e8f0;font-size:15px;'>👤 {c.get("name","—")}</b> &nbsp;&nbsp;{status_html}<br/>
                      <span style='color:#94a3b8;font-size:13px;'>
                      📧 {c.get("email","—")} &nbsp;|&nbsp;
                      📅 {c.get("start","—")} ← {c.get("end","—")} &nbsp;|&nbsp;
                      💰 {c.get("price","—")} دج &nbsp;|&nbsp;
                      {"✅ دفع" if c.get("paid")=="نعم" else "❌ لم يدفع"}
                      </span>
                    </div>""", unsafe_allow_html=True)
                    if st.button("🗑 حذف", key=f"del_{ei}_{ci}"):
                        real_ei = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][real_ei]["clients"].pop(ci)
                        save(data); st.rerun()
                    st.markdown("---")
                if len(clients) < 5:
                    st.markdown("**➕ إضافة زبون:**")
                    c1,c2,c3 = st.columns(3)
                    with c1: cn  = st.text_input("اسم الزبون",   key=f"cn_{ei}")
                    with c2: ce  = st.text_input("إيميل الزبون", key=f"ce_{ei}")
                    with c3: cp  = st.number_input("السعر دج", min_value=0, key=f"cp_{ei}")
                    c4,c5 = st.columns(2)
                    with c4: cs  = st.date_input("البداية", key=f"cs_{ei}",  value=datetime.today())
                    with c5: ced = st.date_input("النهاية", key=f"ced_{ei}", value=datetime.today()+timedelta(days=30))
                    cpaid = st.radio("هل دفع؟", ["نعم","لا"], key=f"cpaid_{ei}", horizontal=True)
                    if st.button("✅ إضافة الزبون", key=f"addcl_{ei}"):
                        if cn:
                            real_ei = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                            data["emails"][real_ei]["clients"].append({
                                "name":cn,"email":ce,
                                "start":cs.strftime("%Y-%m-%d"),
                                "end":ced.strftime("%Y-%m-%d"),
                                "price":str(cp),"paid":cpaid
                            })
                            save(data); st.success("✅ تم"); st.rerun()
                else:
                    st.warning("⚠️ الحد الأقصى 5 زبائن")
                if st.button("🗑 حذف هذا الإيميل", key=f"demail_{ei}"):
                    real_ei = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                    data["emails"].pop(real_ei)
                    save(data); st.rerun()

with tab2:
    st.markdown("### 🔔 التنبيهات")
    found = False
    for em in data.get("emails",[]):
        for c in em.get("clients",[]):
            dl = days_left(c.get("end",""))
            if dl <= 0:
                st.markdown(f"""<div class='alert-red'>⛔ <b>انتهى!</b> {c.get("name","")} | {em["email"]} | {c.get("end","")}</div>""", unsafe_allow_html=True)
                found = True
            elif dl <= 2:
                st.markdown(f"""<div class='alert-warn'>⚠️ <b>ينتهي خلال {dl} يوم!</b> {c.get("name","")} | {em["email"]} | {c.get("end","")}</div>""", unsafe_allow_html=True)
                found = True
    if not found:
        st.success("✅ كل الاشتراكات بخير!")

with tab3:
    st.markdown("### ➕ إضافة إيميل جديد")
    new_email = st.text_input("الإيميل", placeholder="example@gmail.com")
    new_pass  = st.text_input("كلمة المرور", type="password")
    new_serv  = st.text_input("اسم الخدمة", placeholder="Netflix...")
    new_start = st.date_input("تاريخ بداية الاشتراك", value=datetime.today())
    if st.button("💾 حفظ الإيميل"):
        if new_email:
            if any(e["email"]==new_email for e in data["emails"]):
                st.error("هذا الإيميل موجود مسبقاً!")
            else:
                data["emails"].append({"email":new_email,"password":new_pass,
                    "service":new_serv,"start":new_start.strftime("%Y-%m-%d"),"clients":[]})
                save(data); st.success(f"✅ تم إضافة {new_email}"); st.rerun()
        else:
            st.error("أدخل الإيميل أولاً")
