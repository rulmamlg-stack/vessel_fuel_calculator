import streamlit as st

st.set_page_config(page_title="Kalkulator Konsumsi BBM Kapal", layout="centered")

st.title("🚢 Kalkulator Konsumsi Bahan Bakar Kapal")

# --- Identitas Kapal ---
st.header("Identitas Kapal")
nama_kapal = st.text_input("Nama Kapal")
jenis_kapal = st.selectbox("Jenis Kapal", ["Tanker", "Cargo", "Tugboat", "Ferry", "Lainnya"])
gt_dwt = st.number_input("GT / DWT", min_value=0.0, step=100.0)
jenis_bbm = st.selectbox("Jenis Bahan Bakar", ["HSD", "MFO", "LNG", "Solar"])

# --- Data Perjalanan ---
st.header("Data Perjalanan")
jarak = st.number_input("Jarak Tempuh (NM)", min_value=0.0, step=1.0)
kecepatan = st.number_input("Kecepatan Rata-rata (knots)", min_value=0.1, step=0.1)
waktu_standby = st.number_input("Waktu Standby / Manuver (jam)", min_value=0.0, step=0.5)
safety_margin = st.slider("Safety Margin (%)", 0, 30, 10)

# --- Mesin Utama ---
st.header("Mesin Utama (Main Engine)")
me_rate = st.number_input("Konsumsi per Jam ME (liter/jam)", min_value=0.0, step=0.1)
me_load = st.slider("Load Mesin (%)", 0, 100, 85)

# --- Mesin Bantu ---
st.header("Mesin Bantu (Auxiliary Engine)")
ae_count = st.number_input("Jumlah Mesin Bantu", min_value=0, step=1)
ae_rate = st.number_input("Konsumsi per Mesin per Jam AE (liter/jam)", min_value=0.0, step=0.1)
ae_hours = st.number_input("Total Jam Operasi AE (jam)", min_value=0.0, step=0.5)

# --- Bunker ---
st.header("Bunker On Board (Opsional)")
rob_awal = st.number_input("Stok BBM Awal (liter)", min_value=0.0, step=100.0)

# --- Perhitungan ---
if st.button("Hitung Konsumsi"):
    # Waktu tempuh berlayar
    waktu_berlayar = jarak / kecepatan if kecepatan > 0 else 0

    # Konsumsi mesin utama
    konsumsi_me = me_rate * (me_load/100) * waktu_berlayar

    # Konsumsi mesin bantu
    konsumsi_ae = ae_rate * ae_count * ae_hours

    # Total konsumsi
    konsumsi_total = (konsumsi_me + konsumsi_ae) * (1 + safety_margin/100)

    # Sisa BBM
    rob_sisa = rob_awal - konsumsi_total if rob_awal > 0 else None

    # --- Hasil Output ---
    st.subheader("📊 Hasil Perhitungan")
    st.write(f"⏱️ Waktu Berlayar: **{waktu_berlayar:.2f} jam**")
    st.write(f"⚙️ Konsumsi Mesin Utama: **{konsumsi_me:,.2f} liter**")
    st.write(f"⚙️ Konsumsi Mesin Bantu: **{konsumsi_ae:,.2f} liter**")
    st.write(f"🔥 Konsumsi Total (+ Safety {safety_margin}%): **{konsumsi_total:,.2f} liter**")

    if rob_sisa is not None:
        st.write(f"⛽ Sisa BBM (ROB): **{rob_sisa:,.2f} liter**")
