import streamlit as st
import json
from datetime import datetime, timedelta
from pathlib import Path

st.set_page_config(page_title="مدير الاشتراكات", page_icon="📋", layout="centered")

DATA_FILE = "data.json"

def load():
    if Path(DATA_FILE).exists():
        with open(DATA_FILE,"r",encoding="utf-8") as f:
            return json.load(f)
    return {"emails":[], "monthly":[]}

def save(data):
    with open(DATA_FILE,"w",encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def days_left(date_str):
    try:
        return (datetime.strptime(date_str,"%Y-%m-%d").date()-datetime.today().date()).days
    except:
        return 0

def short(email):
    return email.split("@")[0][:9]

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Tajawal',sans-serif!important;direction:rtl;}
.stApp{background:#f0f2f8;}
.block-container{padding:0.8rem!important;max-width:460px!important;margin:auto;}

/* header */
.app-header{background:linear-gradient(135deg,#3730a3,#6d28d9);border-radius:20px;padding:18px 20px;margin-bottom:10px;color:white;}
.app-header h2{color:white!important;margin:0 0 10px;font-size:20px;}

/* stat cards row */
.stats-row{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;margin-bottom:4px;}
.stat-card{background:rgba(255,255,255,0.15);border-radius:12px;padding:8px 6px;text-align:center;}
.stat-card .num{font-size:20px;font-weight:900;color:white;}
.stat-card .lbl{font-size:10px;color:#c4b5fd;margin-top:2px;}

/* tabs */
.stTabs [data-baseweb="tab-list"]{background:white;border-radius:14px;padding:5px;gap:4px;box-shadow:0 2px 8px #0001;}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:#6b7280;font-weight:700;font-size:12px;padding:6px 8px;}
.stTabs [aria-selected="true"]{background:linear-gradient(135deg,#3730a3,#6d28d9)!important;color:white!important;}

/* expander */
.stExpander{background:white!important;border:1.5px solid #ede9fe!important;border-radius:16px!important;margin-bottom:10px!important;box-shadow:0 2px 10px #6d28d909!important;}
div[data-testid="stExpander"] summary{font-family:Tajawal!important;font-size:13px!important;color:#1e1b4b!important;font-weight:700!important;padding:10px!important;}

/* client boxes */
.cl-box{border-radius:12px;padding:8px 4px;text-align:center;color:white;min-height:72px;display:flex;flex-direction:column;justify-content:center;align-items:center;background:linear-gradient(135deg,#3730a3,#6d28d9);box-shadow:0 3px 10px #6d28d933;cursor:pointer;}
.cl-box.warn{background:linear-gradient(135deg,#b45309,#d97706);}
.cl-box.danger{background:linear-gradient(135deg,#991b1b,#dc2626);}
.cl-box.empty{background:#f9fafb;border:2px dashed #d1d5db;color:#9ca3af;box-shadow:none;cursor:pointer;}
.cl-box b{font-size:11px;display:block;word-break:break-all;padding:0 2px;}
.cl-box span{font-size:10px;opacity:0.85;margin-top:2px;}

/* popup */
.popup{background:white;border-radius:18px;padding:16px;border:1.5px solid #ede9fe;box-shadow:0 4px 20px #6d28d922;margin:10px 0;}
.popup-row{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #f3f4f6;font-size:13px;}
.popup-row:last-child{border:none;}
.popup-lbl{color:#9ca3af;font-size:12px;}

/* monthly card */
.month-card{background:white;border-radius:16px;padding:14px;margin-bottom:10px;border:1.5px solid #ede9fe;box-shadow:0 2px 10px #6d28d909;}
.month-title{font-weight:700;color:#3730a3;font-size:15px;margin-bottom:8px;}
.month-stats{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;}
.m-stat{background:#f5f3ff;border-radius:10px;padding:8px;text-align:center;}
.m-stat .n{font-size:18px;font-weight:900;color:#3730a3;}
.m-stat .l{font-size:10px;color:#7c3aed;}

.alert-r{background:#fff1f2;border:2px solid #fca5a5;border-radius:14px;padding:12px;margin:8px 0;color:#991b1b;font-size:13px;}
.alert-w{background:#fffbeb;border:2px solid #fcd34d;border-radius:14px;padding:12px;margin:8px 0;color:#92400e;font-size:13px;}

.stButton>button{background:linear-gradient(135deg,#3730a3,#6d28d9)!important;color:white!important;border:none!important;border-radius:12px!important;font-weight:700!important;font-size:14px!important;padding:10px!important;width:100%!important;font-family:Tajawal!important;box-shadow:0 3px 12px #6d28d933!important;}
.stTextInput input,.stNumberInput input,.stDateInput input{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:11px!important;font-family:Tajawal!important;font-size:14px!important;padding:9px!important;}
.stTextarea textarea{background:white!important;color:#1e1b4b!important;border:1.5px solid #ddd6fe!important;border-radius:11px!important;font-family:Tajawal!important;font-size:13px!important;}
label{color:#4b5563!important;font-family:Tajawal!important;font-size:13px!important;font-weight:600!important;}
hr{border-color:#ede9fe!important;margin:8px 0!important;}
</style>
""", unsafe_allow_html=True)

# ── session state ─────────────────────────────────────────
if "data"     not in st.session_state: st.session_state.data     = load()
if "selected" not in st.session_state: st.session_state.selected = None
if "add_slot" not in st.session_state: st.session_state.add_slot = None

data = st.session_state.data

# ── global stats ──────────────────────────────────────────
all_clients  = [c for e in data.get("emails",[]) for c in e.get("clients",[])]
total_c      = len(all_clients)
total_profit = sum(int(c.get("price",0) or 0) for c in all_clients)
free_slots   = sum(5 - len(e.get("clients",[])) for e in data.get("emails",[]))
active_c     = sum(1 for c in all_clients if days_left(c.get("end","")) > 0)

st.markdown(f"""
<div class="app-header">
  <h2>📋 مدير الاشتراكات &nbsp;<span style="font-size:13px;opacity:.7;">{datetime.today().strftime('%d/%m/%Y')}</span></h2>
  <div class="stats-row">
    <div class="stat-card"><div class="num">{total_c}</div><div class="lbl">زبائن</div></div>
    <div class="stat-card"><div class="num">{active_c}</div><div class="lbl">نشطون</div></div>
    <div class="stat-card"><div class="num">{free_slots}</div><div class="lbl">أماكن فارغة</div></div>
    <div class="stat-card"><div class="num">{total_profit}</div><div class="lbl">دج الفائدة</div></div>
  </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📧 الإيميلات", "🔔 تنبيهات", "📊 إحصائيات", "➕ إضافة"])

# ══════════════════════════════════════════════
# TAB 1 — emails + client boxes
# ══════════════════════════════════════════════
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
        min_dl  = min(dl_list) if dl_list else 0

        if any(d <= 0 for d in dl_list):       icon = "🔴"
        elif any(0 < d <= 2 for d in dl_list): icon = "🟡"
        elif clients:                           icon = "🟢"
        else:                                   icon = "⚪"

        label = f"{icon}  {em['email']}   ·   {len(clients)}/5   ·   ⏳{min_dl}د"

        with st.expander(label):
            cols = st.columns(5)
            for slot in range(5):
                with cols[slot]:
                    if slot < len(clients):
                        c  = clients[slot]
                        dl = days_left(c.get("end",""))
                        cls = "danger" if dl<=0 else ("warn" if dl<=2 else "")
                        nm  = short(c.get("email","?"))
                        st.markdown(f"""<div class="cl-box {cls}">
<b>{nm}</b><span>{dl}d</span></div>""", unsafe_allow_html=True)
                        if st.button("👁", key=f"view_{ei}_{slot}"):
                            if st.session_state.selected == (ei, slot):
                                st.session_state.selected = None
                            else:
                                st.session_state.selected = (ei, slot)
                                st.session_state.add_slot = None
                    else:
                        st.markdown("""<div class="cl-box empty">
<b style="font-size:18px;">+</b><span>فارغ</span></div>""", unsafe_allow_html=True)
                        if st.button("➕", key=f"add_{ei}_{slot}"):
                            if st.session_state.add_slot == (ei, slot):
                                st.session_state.add_slot = None
                            else:
                                st.session_state.add_slot = (ei, slot)
                                st.session_state.selected = None

            # ── popup: view client ────────────────────
            sel = st.session_state.selected
            if sel and sel[0] == ei and sel[1] < len(clients):
                ci = sel[1]
                c  = clients[ci]
                dl = days_left(c.get("end",""))
                if dl<=0:   sc="#dc2626"; st_txt="⛔ منتهي"
                elif dl<=2: sc="#d97706"; st_txt=f"⚠️ {dl} يوم"
                else:       sc="#16a34a"; st_txt=f"✅ {dl} يوم"

                st.markdown(f"""<div class="popup">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
  <b style="font-size:15px;color:#1e1b4b;">👤 {short(c.get('email',''))}</b>
  <span style="color:{sc};font-weight:700;font-size:13px;">{st_txt}</span>
</div>
<div class="popup-row"><span class="popup-lbl">📧 الإيميل</span><span>{c.get('email','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">📅 البداية</span><span>{c.get('start','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">📅 النهاية</span><span>{c.get('end','—')}</span></div>
<div class="popup-row"><span class="popup-lbl">💰 السعر</span><span>{c.get('price','—')} دج</span></div>
<div class="popup-row"><span class="popup-lbl">💳 الدفع</span><span>{'✅ دفع' if c.get('paid')=='نعم' else '❌ لم يدفع'}</span></div>
</div>""", unsafe_allow_html=True)

                new_note = st.text_area("📝 ملاحظة", value=c.get("note",""),
                                        key=f"note_{ei}_{ci}", placeholder="اكتب ملاحظة...", height=70)
                nc1, nc2 = st.columns(2)
                with nc1:
                    if st.button("💾 حفظ", key=f"savenote_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"][ci]["note"] = new_note
                        save(data); st.session_state.data = data; st.success("✅")
                with nc2:
                    if st.button("🗑 حذف", key=f"delc_{ei}_{ci}"):
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].pop(ci)
                        save(data); st.session_state.data = data
                        st.session_state.selected = None; st.rerun()

            # ── popup: add client ─────────────────────
            asl = st.session_state.add_slot
            if asl and asl[0] == ei:
                st.markdown("---")
                st.markdown("**➕ إضافة زبون جديد**")
                ce    = st.text_input("📧 إيميل الزبون", key=f"nce_{ei}", placeholder="client@gmail.com")
                cp    = st.number_input("💰 السعر (دج)", min_value=0, key=f"ncp_{ei}")
                cs    = st.date_input("📅 البداية", key=f"ncs_{ei}",  value=datetime.today())
                ced   = st.date_input("📅 النهاية", key=f"nced_{ei}", value=datetime.today()+timedelta(days=30))
                cpaid = st.radio("💳 هل دفع؟", ["نعم","لا"], key=f"ncpaid_{ei}", horizontal=True)
                if st.button("✅ إضافة الزبون", key=f"naddcl_{ei}"):
                    if ce.strip():
                        ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                        data["emails"][ri]["clients"].append({
                            "email":ce.strip(), "name":ce.strip().split("@")[0],
                            "start":cs.strftime("%Y-%m-%d"),
                            "end":ced.strftime("%Y-%m-%d"),
                            "price":str(cp), "paid":cpaid, "note":""
                        })
                        save(data); st.session_state.data = data
                        st.session_state.add_slot = None
                        st.success("✅ تم!"); st.rerun()
                    else:
                        st.error("أدخل إيميل الزبون!")

            st.divider()
            if st.button("🗑 حذف هذا الإيميل", key=f"demail_{ei}"):
                ri = next(i for i,e in enumerate(data["emails"]) if e["email"]==em["email"])
                data["emails"].pop(ri)
                save(data); st.session_state.data = data
                st.session_state.selected = None
                st.session_state.add_slot = None; st.rerun()

# ══════════════════════════════════════════════
# TAB 2 — alerts
# ══════════════════════════════════════════════
with tab2:
    st.markdown("### 🔔 التنبيهات")
    found = False
    for em in data.get("emails",[]):
        for c in em.get("clients",[]):
            dl = days_left(c.get("end",""))
            if dl <= 0:
                st.markdown(f"""<div class="alert-r">⛔ <b>انتهى!</b> {c.get('email','')} | {em['email']} | {c.get('end','')}</div>""", unsafe_allow_html=True)
                found = True
            elif dl <= 2:
                st.markdown(f"""<div class="alert-w">⚠️ <b>ينتهي خلال {dl} يوم!</b> {c.get('email','')} | {em['email']} | {c.get('end','')}</div>""", unsafe_allow_html=True)
                found = True
    if not found:
        st.success("✅ كل الاشتراكات بخير!")

# ══════════════════════════════════════════════
# TAB 3 — monthly stats
# ══════════════════════════════════════════════
with tab3:
    st.markdown("### 📊 إحصائيات شهرية")

    monthly = data.get("monthly", [])

    # add this month if not exists
    cur_month = datetime.today().strftime("%Y-%m")
    if not any(m["month"]==cur_month for m in monthly):
        monthly.append({
            "month": cur_month,
            "sold":  len(all_clients),
            "profit": total_profit,
            "active": active_c
        })
        data["monthly"] = monthly
        save(data)

    if not monthly:
        st.info("لا توجد بيانات شهرية بعد.")
    else:
        for m in reversed(monthly):
            month_name = m.get("month","")
            sold   = m.get("sold", 0)
            profit = m.get("profit", 0)
            active = m.get("active", 0)
            st.markdown(f"""
<div class="month-card">
  <div class="month-title">📅 {month_name}</div>
  <div class="month-stats">
    <div class="m-stat"><div class="n">{sold}</div><div class="l">مباع</div></div>
    <div class="m-stat"><div class="n">{profit}</div><div class="l">دج فائدة</div></div>
    <div class="m-stat"><div class="n">{active}</div><div class="l">نشط</div></div>
  </div>
</div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**💾 تسجيل إحصائيات الشهر الحالي يدوياً**")
    if st.button("📸 حفظ إحصائيات هذا الشهر"):
        cur = datetime.today().strftime("%Y-%m")
        entry = {"month":cur, "sold":total_c, "profit":total_profit, "active":active_c}
        existing = [i for i,m in enumerate(monthly) if m["month"]==cur]
        if existing:
            data["monthly"][existing[0]] = entry
        else:
            data["monthly"].append(entry)
        save(data); st.session_state.data = data
        st.success("✅ تم حفظ إحصائيات الشهر!")

# ══════════════════════════════════════════════
# TAB 4 — add email
# ══════════════════════════════════════════════
with tab4:
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
