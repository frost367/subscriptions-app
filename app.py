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

def short_name(email):
    return email.split("@")[0][:8]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Tajawal',sans-serif!important;direction:rtl;}
.stApp{background:#f0f2f8;}
.block-container{padding:0.8rem!important;max-width:460px!important;margin:auto;}

.app-header{background:linear-gradient(135deg,#3730a3,#6d28d9);border-radius:20px;padding:18px 20px;margin-bottom:14px;color:white;}
.app-header h2{color:white!important;margin:0;font-size:21px;}
.app-header p{color:#c4b5fd;margin:4px 0 0;font-size:13px;}

.stTabs [data-baseweb="tab-list"]{background:white;border-radius:14px;padding:5px;gap:4px;box-shadow:0 2px 8px #0001;}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:#6b7280;font-weight:700;font-size:13px;padding:7px 12px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#3730a3,#6d28d9)!important;color:white!important;}

.stExpander{background:white!important;border:1.5px solid #ede9fe!important;border-radius:16px!important;margin-bottom:10px!important;box-shadow:0 2px 10px #6d28d909!important;}
div[data-testid="stExpander"] summary{font-family:Tajawal!important;font-size:14px!important;color:#1e1b4b!important;font-weight:700!important;padding:12px!important;}

.client-box{background:linear-gradient(135deg,#3730a3,#6d28d9);border-radius:14px;padding:10px 6px;text-align:center;color:white;cursor:pointer;min-height:80px;display:flex;flex-direction:column;justify-content:center;align-items:center;box-shadow:0 4px 12px #6d28d933;}
.client-box.warn{background:linear-gradient(135deg,#b45309,#d97706);}
.client-box.danger{background:linear-gradient(135deg,#991b1b,#dc2626);}
.client-box.empty{background:#f3f4f6;border:2px dashed #d1d5db;color:#9ca3af;box-shadow:none;}
.client-box b{font-size:13px;display:block;margin-bottom:4px;}
.client-box span{font-size:11px;opacity:0.9;}

.info-popup{background:white;border-radius:18px;padding:20px;border:1.5px solid #ede9fe;box-shadow:0 4px 20px #6d28d922;margin-top:10px;}
.info-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;color:#374151;}
.info-row:last-child{border-bottom:none;}
.info-label{color:#9ca3af;font-size:13px;}

.alert-r{background:#fff1f2;border:2px solid #fca5a5;border-radius:14px;padding:14px;margin:8px 0;color:#991b1b;}
.alert-w{background:#fffbeb;border:2px solid #fcd34d;border-radius:14px;padding:14px;margin:8px 0;color:#92400e;}

.stButton>button{background:linear-gradient(135deg,#3730a3,#6d28d9)!important;color:white!important;border:none!important;border-radius:14px!important;font-weight:700!important;font-size:15px!important;padding:12px!important;width:100%!important;font-family:Tajawal!important;box-shadow:0 4px 14px #6d28d933!important;}
.stTextInput input,.stNumberInput input,.stDateInput input{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:12px!important;font-family:Tajawal!important;font-size:15px!important;padding:10px!important;}
.stTextarea textarea{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:12px!important;font-family:Tajawal!important;font-size:14px!important;}
label{color:#4b5563!important;font-family:Tajawal!important;font-size:14px!important;font-weight:600!important;}
hr{border-color:#ede9fe!important;margin:10px 0!important;}
</style>
""", unsafe_allow_html=True)

if "data" not in st.session_state:
    st.session_state.data = load()
if "selected" not in st.session_state:
    st.session_state.selected = None  # (ei, ci)

data = st.session_state.data
today_str = datetime.today().strftime("%d/%m/%Y")
total_clients = sum(len(e.get("clients",[])) for e in data.get("emails",[]))

st.markdown(f"""
<div class="app-header">
  <h2>📋 مدير الاشتراكات</h2>
  <p>📅 {today_str} &nbsp;·&nbsp; 👥 {total_clients} زبون</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📧  الإيميلات", "🔔  تنبيهات", "➕  إضافة"])

# ══════════════════════════════════
with tab1:
    search = st.text_input("", placeholder="🔍 ابحث عن إيميل...")
    emails_list = data.get("emails", [])
    if search:
        emails_list = [e for e in emails_list if search.lower() in e["email"].lower()]

    if not emails_list:
        st.info("لا توجد إيميلات — أضف من تبويب ➕")

    for ei, em in enumerate(emails_list):
        clients = em.get("clients", [])
        dl_list = [days_left(c.get("end","")) for c in clients]

        if any(d <= 0 for d in dl_list):        icon = "🔴"
        elif any(0 < d <= 2 for d in dl_list):  icon = "🟡"
        elif clients:                            icon = "🟢"
        else:                                    icon = "⚪"

        min_dl = min(dl_list) if dl_list else 0
        label  = f"{icon}  {em['email']}   ·   {len(clients)}/5   ·   ⏳{min_dl} يوم"

        with st.expander(label):
            # ── 5 boxes grid ──────────────────────────
            cols = st.columns(5)
            for slot in range(5):
                with cols[slot]:
                    if slot < len(clients):
                        c   = clients[slot]
                        dl  = days_left(c.get("end",""))
                        cls = "danger" if dl<=0 else ("warn" if dl<=2 else "")
                        box_label = short_name(c.get("email", c.get("name","?")))
                        st.markdown(f"""
<div class="client-box {cls}">
  <b>{box_label}</b>
  <span>{dl}d</span>
</div>""", unsafe_allow_html=True)
                        if st.button("⬆", key=f"open_{ei}_{slot}", help="عرض التفاصيل"):
                            if st.session_state.selected == (ei, slot):
                                st.session_state.selected = None
                            else:
                                st.session_state.selected = (ei, slot)
                    else:
                        st.markdown("""
<div class="client-box empty">
  <b>+</b>
  <span>فارغ</span>
</div>""", unsafe_allow_html=True)

            # ── popup detail ──────────────────────────
            sel = st.session_state.selected
            if sel and sel[0] == ei and sel[1] < len(clients):
                ci = sel[1]
                c  = clients[ci]
                dl = days_left(c.get("end",""))

                if dl <= 0:   status = "⛔ منتهي";      scol = "#dc2626"
                elif dl <= 2: status = f"⚠️ {dl} يوم";   scol = "#d97706"
                else:         status = f"✅ {dl} يوم";   scol = "#16a34a"

                st.markdown(f"""
<div class="info-popup">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
    <span style="font-weight:900;font-size:16px;color:#1e1b4b;">👤 {c.get('email','—').split('@')[0]}</span>
    <span style="color:{scol};font-weight:700;font-size:14px;">{status}</span>
  </div>
  <div class="info-row"><span class="info-label">📧 الإيميل</span><span>{c.get('email','—')}</span></div>
  <div class="info-row"><span class="info-label">📅 البداية</span><span>{c.get('start','—')}</span></div>
  <div class="info-row"><span class="info-label">📅 النهاية</span><span>{c.get('end','—')}</span></div>
  <div class="info-row"><span class="info-label">💰 السعر</span><span>{c.get('price','—')} دج</span></div>
  <div class="info-row"><span class="info-label">💳 الدفع</span><span>{'✅ دفع' if c.get('paid')=='نعم' else '❌ لم يدفع'}</span></div>
</div>""", unsafe_allow_html=True)

                # notes
                note_key = f"note_{ei}_{ci}"
                current_note = c.get("note","")
                new_note = st.text_area("📝 ملاحظة", value=current_note, key=note_key,
                                        placeholder="أضف ملاحظة هنا...", height=80)
                bcol1, bcol2 = st.columns(2)
                with bcol1:
                    if st.button("💾 حفظ الملاحظة", key=f"savenote_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"][ci]["note"] = new_note
                        save(data); st.session_state.data = data
                        st.success("✅ تم حفظ الملاحظة")
                with bcol2:
                    if st.button("🗑 حذف الزبون", key=f"del_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].pop(ci)
                        save(data); st.session_state.data = data
                        st.session_state.selected = None; st.rerun()

            st.divider()

            # ── add client ────────────────────────────
            if len(clients) < 5:
                st.markdown("**➕ إضافة زبون**")
                ce  = st.text_input("📧 إيميل الزبون", key=f"ce_{ei}", placeholder="client@gmail.com")
                cp  = st.number_input("💰 السعر (دج)", min_value=0, key=f"cp_{ei}")
                cs  = st.date_input("📅 البداية",  key=f"cs_{ei}",  value=datetime.today())
                ced = st.date_input("📅 النهاية",  key=f"ced_{ei}", value=datetime.today()+timedelta(days=30))
                cpaid = st.radio("💳 هل دفع؟", ["نعم","لا"], key=f"cpaid_{ei}", horizontal=True)
                if st.button("✅ إضافة", key=f"addcl_{ei}"):
                    if ce.strip():
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].append({
                            "email":ce.strip(), "name":ce.strip().split("@")[0],
                            "start":cs.strftime("%Y-%m-%d"),
                            "end":ced.strftime("%Y-%m-%d"),
                            "price":str(cp), "paid":cpaid, "note":""
                        })
                        save(data); st.session_state.data = data
                        st.success("✅ تم!"); st.rerun()
                    else:
                        st.error("أدخل إيميل الزبون!")
            else:
                st.warning("⚠️ الحد الأقصى 5 زبائن")

            st.divider()
            if st.button("🗑 حذف هذا الإيميل", key=f"demail_{ei}"):
                ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                data["emails"].pop(ri)
                save(data); st.session_state.data = data
                st.session_state.selected = None; st.rerun()

# ══════════════════════════════════
with tab2:
    st.markdown("### 🔔 التنبيهات")
    found = False
    for em in data.get("emails",[]):
        for c in em.get("clients",[]):
            dl = days_left(c.get("end",""))
            if dl <= 0:
                st.markdown(f"""<div class="alert-r">⛔ <b>انتهى!</b> &nbsp; {c.get('email','')} &nbsp;|&nbsp; 📧 {em['email']} &nbsp;|&nbsp; 📅 {c.get('end','')}</div>""", unsafe_allow_html=True)
                found = True
            elif dl <= 2:
                st.markdown(f"""<div class="alert-w">⚠️ <b>ينتهي خلال {dl} يوم!</b> &nbsp; {c.get('email','')} &nbsp;|&nbsp; 📧 {em['email']} &nbsp;|&nbsp; 📅 {c.get('end','')}</div>""", unsafe_allow_html=True)
                found = True
    if not found:
        st.success("✅ كل الاشتراكات بخير!")

# ══════════════════════════════════
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
            st.error("أدخل الإيميل أولاً!")
