# main.py

import streamlit as st
import pandas as pd
import os
import datetime
from products import PRODUCTS

# -----------------------------
# ORDER DIRECTORIES
# -----------------------------
ORDERS_DIR = "orders"
PROOFS_DIR = os.path.join(ORDERS_DIR, "proofs")

os.makedirs(PROOFS_DIR, exist_ok=True)
ORDERS_CSV = os.path.join(ORDERS_DIR, "orders.csv")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="LAC — Order Portal", layout="centered")
st.title("LAC Accounting Bots — Order & Payment")

# -----------------------------
# ORDER FORM
# -----------------------------
with st.form("order_form"):
    product = st.selectbox("Choose Product", list(PRODUCTS.keys()))
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone (WhatsApp preferred)")
    business = st.text_input("Business Name (optional)")
    submitted = st.form_submit_button("Proceed to Payment Instructions")

# -----------------------------
# AFTER FORM SUBMISSION
# -----------------------------
if submitted:
    ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_id = f"ORD-{ts}"

    st.success(f"Order received. Your order ID is {order_id}")

    example_ref = f"INV-{datetime.datetime.now().strftime('%y%m%d')}-{phone[-4:] if phone else 'XXXX'}"

    st.markdown("### Payment Instructions")
    st.markdown(f"""
    **Bank:** Tymebank  
    **Account Holder:** Hlongwane Lasie  
    **Account Number:** 51072882825  
    **Branch Code:** 678910  
    **Reference:** Please use **{example_ref}** (or the reference shown after checkout)
    """)

    st.markdown("Upload proof of payment (screenshot or PDF) or send it to WhatsApp **+27 76 611 4909**.")

    # Upload proof
    proof = st.file_uploader("Upload proof of payment (optional)", type=['png', 'jpg', 'jpeg', 'pdf'])

    proof_filename = ""
    if proof:
        proof_filename = f"{order_id}_{proof.name}"
        proof_path = os.path.join(PROOFS_DIR, proof_filename)

        with open(proof_path, "wb") as f:
            f.write(proof.getbuffer())

        st.success("Proof uploaded successfully.")

    # -----------------------------
    # SAVE ORDER TO CSV
    # -----------------------------
    order = {
        "order_id": order_id,
        "timestamp": datetime.datetime.now().isoformat(),
        "product": product,
        "name": name,
        "email": email,
        "phone": phone,
        "business": business,
        "proof_filename": proof_filename,
        "status": "pending",
        "activation_key": ""
    }

    df = pd.DataFrame([order])

    if not os.path.exists(ORDERS_CSV):
        df.to_csv(ORDERS_CSV, index=False)
    else:
        df.to_csv(ORDERS_CSV, mode='a', header=False, index=False)

    st.info("We will verify the payment and activate your product. You will receive an email once approved.")
