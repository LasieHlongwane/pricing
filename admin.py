# admin.py
import streamlit as st
import pandas as pd
import os
from utils import generate_activation_key, send_activation_email
from products import PRODUCTS

ORDERS_CSV = "orders/orders.csv"
st.set_page_config(page_title="LAC Admin", layout="wide")
st.title("LAC Admin — Approve Orders")

# Admin auth
admin_password = st.secrets["admin"]["password"]
pwd = st.text_input("Enter admin password", type="password")
if pwd != admin_password:
    st.warning("Enter the admin password to continue.")
    st.stop()

if not os.path.exists(ORDERS_CSV):
    st.info("No orders yet.")
else:
    df = pd.read_csv(ORDERS_CSV)
    pending = df[df['status'] == 'pending']
    if pending.empty:
        st.info("No pending orders.")
    else:
        for idx, row in pending.iterrows():
            st.markdown("---")
            st.write(f"**Order ID:** {row['order_id']}")
            st.write(f"Product: {row['product']}")
            st.write(f"Name: {row['name']}")
            st.write(f"Email: {row['email']}")
            st.write(f"Phone: {row['phone']}")
            st.write(f"Business: {row['business']}")
            if row['proof_filename']:
                proof_path = os.path.join("orders", "proofs", row['proof_filename'])
                if os.path.exists(proof_path):
                    st.write("Proof of payment uploaded:")
                    st.write(f"- {proof_path}")
                    # For images you can display: st.image(proof_path)
                else:
                    st.write("No proof file found in folder.")
            approve = st.button(f"Approve {row['order_id']}", key=row['order_id'])
            if approve:
                activation_key = generate_activation_key()
                product_link = PRODUCTS.get(row['product'], {}).get("link", "https://yourapp.streamlit.app")
                # send email
                send_activation_email(
                    to_email=row['email'],
                    name=row['name'],
                    product=row['product'],
                    activation_key=activation_key,
                    product_link=product_link,
                    smtp_user=st.secrets["email"]["user"],
                    smtp_pass=st.secrets["email"]["password"]
                )
                # update CSV
                df.loc[idx, 'status'] = 'approved'
                df.loc[idx, 'activation_key'] = activation_key
                df.to_csv(ORDERS_CSV, index=False)
                st.success(f"{row['order_id']} approved & email sent to {row['email']}")
