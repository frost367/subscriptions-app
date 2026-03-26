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
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Tajawal', sans-serif !important;
    direction: rtl;
}
.stApp { background: #f0f2f8; }
.block-container { padding: 1rem !important; max-width: 460px !important; margin: auto; }

/* header */
.app-header {
    background: linear-gradient(135deg, #3730a3, #6d28d9);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 16px;
    color: white;
    text-align: right;
}
.app-header h2 { color: white !important; margin: 0; font-size: 22px; }
.app-header p  { color: #c4b5fd; margin: 4px 0 0; font-size: 13px; }

/* tabs */
.stTabs [data-baseweb="tab-list"] {
    background: white;
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
    box-shadow: 0 2px 8px #0001;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #6b7280;
    font-weight: 700;
    font-size: 13px;
    padding: 7px 12px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#3730a3,#6d28d9) !important;
    color: white !important;
}

/* email card */
.em-card {
    background: white;
    border-radius: 18px;
    padding: 16px;
    margin-bottom: 10px;
    box-shadow: 0 2px 12px #6d28d911;
    border: 1.5px solid #ede9fe;
}

/* client card */
.cl-card {
    background: #fafafa;
    border-radius: 14px;
    padding: 13px 15px;
    margin: 8px 0;
    border: 1.5px solid #ede9fe;
    box-shadow: 0 1px 6px #0001;
}

/* badges */
.b-green  { background:#dcfce7; color:#166534; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
.b-yellow { background:#fef9c3; color:#854d0e; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }
.b-red    { background:#fee2e2; color:#991b1b; padding:3px 12px; border-radius:20px; font-size:12px; font-weight:700; }

/* alert boxes */
.alert-r { background:#fff1f2; border:2px solid #fca5a5; border-radius:14px; padding:14px; margin:8px 0; color:#991b1b; }
.alert-w { background:#fffbeb; border:2px solid #fcd34d; border-radius:14px; padding:14px; margin:8px 0; color:#92400e; }

/* buttons */
.stButton>button {
    background: linear-gradient(135deg,#3730a3,#6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 12px !important;
    width: 100% !important;
    font-family: Tajawal !important;
    box-shadow: 0 4px 14px #6d28d933 !important;
}
.stButton>button:hover { opacity: 0.92; transform: translateY(-1px); }

/* inputs */
.stTextInput input, .stNumberInput input, .stDateInput input {
    background: white !important;
    color: #1e1b4b !important;
    border: 1.5px solid #ddd6fe !important;
    border-radius: 12px !important;
    font-family: Tajawal !important;
    font-size: 15px !important;
    padding: 10px !important;
    box-shadow: 0 1px 4px #0001 !important;
}
.stTextInput input:focus { border-color: #6d28d9 !important; }

label { color: #4b5563 !important; font-family: Tajawal !important; font-size: 14px !important; font-weight: 600 !important; }

/* expander */
.stExpander {
    background: white !important;
    border: 1.5px solid #ede9fe !important;
    border-radius: 16px !important;
    margin-bottom: 10px !important;
    box-shadow: 0 2px 10px #6d28d909 !important;
}
div[data-testid="stExpander"] summary {
    font-family: Tajawal !important;
    font-size: 15px !important;
    color: #1e1b4b !important;
    font-weight: 700 !important;
    padding: 12px !important;
}

/* search */
.stTextInput input[placeholder*="بحث"] {
    background: white !important;
    border-radius: 14px !important;
    padding-right: 14px !important;
}

hr { border-color: #ede9fe !important; margin: 10px 0 !important; }
.stSuccess { background:#f0fdf4 !important; border:1.5px solid #86efac !important; border-radius:12px !important; color:#166534 !important; }
.stError   { background:#fff1f2 !important; border:1.5px solid #fca5a5 !important; border-radius:12px !important; color:#991b1b !important; }
.stWarning { background:#fffbeb !important; border:1.5px solid #fcd34d !important; border-radius:12px !important; color:#92400e !important; }
.stInfo    { background:#eff6ff !important; border:1.5px solid #93c5fd !important; border-radius:12px !important; color:#1e40af !important; }
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = load()
data = st.session_state.data

# header
today_str = datetime.today().strftime("%A، %d %B %Y")
total_clients = sum(len(e.get("clients",[])) for e in data.get("emails",[]))
st.markdown(f"""
<div class="app-header">
  <h2>📋 مدير الاشتراكات</h2>
  <p>📅 {today_str} &nbsp;·&nbsp; 👥 {total_clients} زبون نشط</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📧  الإيميلات", "🔔  تنبيهات", "➕  إضافة"])

# ══════════════════════════════════
with tab1:
    search = st.text_input("", placeholder="🔍  ابحث عن إيميل أو زبون...")
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

            if any(d <= 0 for d in dl_list):        icon = "🔴"
            elif any(0 < d <= 2 for d in dl_list):  icon = "🟡"
            else:                                    icon = "🟢"

            days_txt = f"⏳ {min_dl} يوم" if clients else "فارغ"
            label = f"{icon}  {em['email']}   ·   {len(clients)}/5   ·   {days_txt}"

            with st.expander(label):
                st.caption(f"🛠 {em.get('service','—')}   |   📅 بداية الاشتراك: {em.get('start','—')}")

                if not clients:
                    st.caption("— لا يوجد زبائن بعد —")

                for ci, c in enumerate(clients):
                    dl = days_left(c.get("end",""))
                    if dl <= 0:
                        badge_html = "<span class='b-red'>⛔ منتهي</span>"
                        border_color = "#ef4444"
                    elif dl <= 2:
                        badge_html = f"<span class='b-yellow'>⚠️ {dl} يوم</span>"
                        border_color = "#f59e0b"
                    else:
                        badge_html = f"<span class='b-green'>✅ {dl} يوم</span>"
                        border_color = "#6d28d9"

                    paid_icon = "✅ دفع" if c.get("paid") == "نعم" else "❌ لم يدفع"

                    st.markdown(f"""
<div class="cl-card" style="border-right:4px solid {border_color};">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
    <span style="font-weight:700;font-size:15px;color:#1e1b4b;">👤 {c.get('name','—')}</span>
    {badge_html}
  </div>
  <div style="color:#6b7280;font-size:13px;line-height:2.2;">
    📧&nbsp; {c.get('email','—')}<br>
    📅&nbsp; {c.get('start','—')} &nbsp;←&nbsp; {c.get('end','—')}<br>
    💰&nbsp; {c.get('price','—')} دج &nbsp;&nbsp;·&nbsp;&nbsp; {paid_icon}
  </div>
</div>""", unsafe_allow_html=True)

                    if st.button(f"🗑  حذف  {c.get('name','')}", key=f"del_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].pop(ci)
                        save(data); st.session_state.data = data; st.rerun()

                st.divider()
                if len(clients) < 5:
                    st.markdown("**➕ إضافة زبون جديد**")
                    cn    = st.text_input("👤 اسم الزبون",    key=f"cn_{ei}")
                    ce    = st.text_input("📧 إيميل الزبون",  key=f"ce_{ei}")
                    cp    = st.number_input("💰 السعر (دج)", min_value=0, key=f"cp_{ei}")
                    cs    = st.date_input("📅 البداية",  key=f"cs_{ei}",  value=datetime.today())
                    ced   = st.date_input("📅 النهاية",  key=f"ced_{ei}", value=datetime.today()+timedelta(days=30))
                    cpaid = st.radio("💳 هل دفع؟", ["نعم","لا"], key=f"cpaid_{ei}", horizontal=True)
                    if st.button("✅  إضافة الزبون", key=f"addcl_{ei}"):
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
                    st.warning("⚠️ الحد الأقصى 5 زبائن لهذا الإيميل")

                st.divider()
                if st.button("🗑  حذف هذا الإيميل كاملاً", key=f"demail_{ei}"):
                    ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                    data["emails"].pop(ri)
                    save(data); st.session_state.data = data; st.rerun()

# ══════════════════════════════════
with tab2:
    st.markdown("### 🔔 التنبيهات")
    found = False
    for em in data.get("emails", []):
        for c in em.get("clients", []):
            dl = days_left(c.get("end",""))
            if dl <= 0:
                st.markdown(f"""<div class="alert-r">
⛔ <b>انتهى الاشتراك!</b><br>
👤 {c.get('name','')} &nbsp;|&nbsp; 📧 {em['email']}<br>
📅 انتهى في: <b>{c.get('end','')}</b>
</div>""", unsafe_allow_html=True)
                found = True
            elif dl <= 2:
                st.markdown(f"""<div class="alert-w">
⚠️ <b>ينتهي خلال {dl} يوم!</b><br>
👤 {c.get('name','')} &nbsp;|&nbsp; 📧 {em['email']}<br>
📅 ينتهي في: <b>{c.get('end','')}</b>
</div>""", unsafe_allow_html=True)
                found = True
    if not found:
        st.success("✅ كل الاشتراكات بخير! لا توجد تنبيهات.")

# ══════════════════════════════════
with tab3:
    st.markdown("### ➕ إضافة إيميل جديد")
    new_email = st.text_input("📧 الإيميل الكامل", placeholder="example@gmail.com")
    new_pass  = st.text_input("🔑 كلمة المرور", type="password")
    new_serv  = st.text_input("🛠 اسم الخدمة",  placeholder="Netflix / Spotify ...")
    new_start = st.date_input("📅 تاريخ بداية الاشتراك السنوي", value=datetime.today())
    if st.button("💾  حفظ الإيميل"):
        if new_email.strip():
            if any(e["email"]==new_email.strip() for e in data["emails"]):
                st.error("⚠️ هذا الإيميل موجود مسبقاً!")
            else:
                data["emails"].append({
                    "email":    new_email.strip(),
                    "password": new_pass,
                    "service":  new_serv,
                    "start":    new_start.strftime("%Y-%m-%d"),
                    "clients":  []
                })
                save(data); st.session_state.data = data
                st.success(f"✅ تم إضافة {new_email}"); st.rerun()
        else:
            st.error("أدخل الإيميل أولاً!")
