import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image
import pytesseract
from datetime import datetime
import re
from twilio.rest import Client
import random
import string
import sqlite3
import streamlit_authenticator as stauth

st.set_page_config(page_title="Inventory Management System", page_icon=":bar_chart:", layout="wide")

# Dummy user credentials
# registered_users = {
#     "akshay": ["Akshay12",+919876543210],
#     "umesh": ["Umesh12",919876543210],
#     "pratik": ["Pratik12",+919876543210]
# }

names = ["Akshay", "Umesh", "Pratik"]
usernames = ["akshay", "umesh", "pratik"]
passwords = ["Akshay12", "Umesh12", "Pratik12"]

hashed_passwords = stauth.utilities.hasher.Hasher(passwords).generate()

common_conn = sqlite3.connect("creds.db")
common_cursor = common_conn.cursor()

cmd = "CREATE TABLE IF NOT EXISTS credentials (names TEXT, usernames TEXT, passwords TEXT)"
common_cursor.execute(cmd)

def get_creds():
    common_cursor.execute("select * from credentials")
    res = common_cursor.fetchall()
    credf = pd.DataFrame(res, columns=["names", "usernames", "pwds"])
    return credf

credf = get_creds()

for i,j in enumerate(usernames):
    if j not in list(credf["usernames"]):
        common_cursor.execute('INSERT INTO credentials VALUES("{name}","{uname}","{hash_pwd}")'.format(name=names[i],uname=usernames[i],hash_pwd=hashed_passwords[i]))
        common_conn.commit()

credf = get_creds()

names = list(credf["names"])
usernames = list(credf["usernames"])
passwords = list(credf["pwds"])

temp_dict = {}
for k,i in enumerate(usernames):
    temp_dict[i] = {"email": "", "name": names[k], "password": passwords[k]}

credentials = {}
credentials["usernames"] = temp_dict

st.title("Inventory Management System")

authenticator = stauth.Authenticate(credentials, "Inventory Management App", "abc123", cookie_expiry_days=30.0)
name, authentication_status, username = authenticator.login("main")

## Additional functions

# Function to generate OTP
def generate_otp(length=6):
    return ''.join(random.choices(string.digits, k=length))

# Function to send OTP via SMS
def send_otp_via_sms(phone_number, otp):
    # Twilio credentials
    account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
    auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
    twilio_phone_number = 'YOUR_TWILIO_PHONE_NUMBER'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP for credential reset: {otp}',
        from_=twilio_phone_number,
        to=phone_number
    )

    return message.sid

# Function to generate bill and deduct from inventory
def generate_bill(products):
    for product in products:
        pass0

if 'clrinvclicked' not in st.session_state:
    st.session_state.clrinvclicked = False

def clrinvclicked1():
    st.session_state.clrinvclicked = True

if 'clrbillclicked' not in st.session_state:
    st.session_state.clrbillclicked = False

def clrbillclicked1():
    st.session_state.clrbillclicked = True

if 'clrmapclicked' not in st.session_state:
    st.session_state.clrmapclicked = False

def clrmapclicked1():
    st.session_state.clrmapclicked = True

if 'chckinvclicked' not in st.session_state:
    st.session_state.chckinvclicked = False

def chckinvclicked1():
    st.session_state.chckinvclicked = True

if 'chckbillclicked' not in st.session_state:
    st.session_state.chckbillclicked = False

def chckbillclicked1():
    st.session_state.chckbillclicked = True

if 'chckmapclicked' not in st.session_state:
    st.session_state.chckmapclicked = False

def chckmapclicked1():
    st.session_state.chckmapclicked = True

def main():
    # st.title("Inventory Management System")
    clear_inventory = st.sidebar.button("Clear Inventory", on_click=clrinvclicked1)
    clear_billing = st.sidebar.button("Clear Billing", on_click=clrbillclicked1)
    clear_mapping = st.sidebar.button("Clear Mapping", on_click=clrmapclicked1)

    conn = sqlite3.connect("inventory_{user}.db".format(user=username))
    cursor = conn.cursor()

    cmd1 = "CREATE TABLE IF NOT EXISTS inventory_{user}(invoice_no TEXT, parts TEXT, quantity INTEGER, purchase_date DATE)".format(user=username)
    cursor.execute(cmd1)

    cmd2 = "CREATE TABLE IF NOT EXISTS billing_{user}(invoice_no TEXT, product TEXT, quantity INTEGER, bill_date DATE)".format(user=username)
    cursor.execute(cmd2)

    cmd3 = "CREATE TABLE IF NOT EXISTS mapping_{user}(product TEXT, part TEXT, quantity INTEGER)".format(user=username)
    cursor.execute(cmd3)

    # cursor.execute("select count(1) from mapping_{user}".format(user=username))
    # res = cursor.fetchall()
    # if res[0][0] < 1:
    #     for i in range(mapping_table.shape[0]):
    #         cursor.execute('INSERT INTO mapping_{user} VALUES("{prd}","{prt}",{q})'.format(user=username,prd=mapping_table['Product'][i],prt=mapping_table['Part'][i],q=mapping_table['Quantity'][i]))
    #     conn.commit()

    # Function to add inventory input
    def add_inventory(invoice_no, parts, quantity, purchase_date, uploaded_file, username):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if uploaded_file is not None:
            upload_df = pd.read_csv(uploaded_file)
            upload_df = upload_df[["invoice_no", "parts", "quantity", "purchase_date"]]
            # st.write(upload_df)

            for i in range(upload_df.shape[0]):
                cursor.execute('INSERT INTO inventory_{user} VALUES("{prd}","{prt}",{q},"{prdt}")'.format(user=username,prd=upload_df['invoice_no'][i],prt=upload_df['parts'][i],q=upload_df['quantity'][i],prdt=upload_df['purchase_date'][i]))
            conn.commit()
        else:
            cursor.execute('INSERT INTO inventory_{user} VALUES("{prd}","{prt}",{q},"{prdt}")'.format(user=username,prd=invoice_no,prt=parts,q=quantity,prdt=purchase_date))
            conn.commit()

        cursor.execute("select * from inventory_{user}".format(user=username))
        res = cursor.fetchall()
        st.table(pd.DataFrame(res, columns=["invoice_no", "parts", "quantity", "purchase_date"]))

    # Function to add billing input
    def add_billing(invoice_no, product, quantity, bill_date, uploaded_file, username):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if uploaded_file is not None:
            upload_df = pd.read_csv(uploaded_file)
            upload_df = upload_df[["invoice_no", "parts", "quantity", "purchase_date"]]
            # st.write(upload_df)

            for i in range(upload_df.shape[0]):
                cursor.execute('INSERT INTO billing_{user} VALUES("{prd}","{prt}",{q},"{prdt}")'.format(user=username,prd=upload_df['invoice_no'][i],prt=upload_df['product'][i],q=upload_df['quantity'][i],prdt=upload_df['bill_date'][i]))
            conn.commit()
        else:
            cursor.execute('INSERT INTO billing_{user} VALUES("{prd}","{prt}",{q},"{prdt}")'.format(user=username,prd=invoice_no,prt=product,q=quantity,prdt=bill_date))
            conn.commit()

        cursor.execute("select * from billing_{user}".format(user=username))
        res = cursor.fetchall()
        st.table(pd.DataFrame(res, columns=["invoice_no", "product", "quantity", "bill_date"]))

    def add_mapping(product, part, quantity, uploaded_file, username):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d %H:%M:%S")
        
        if uploaded_file is not None:
            upload_df = pd.read_csv(uploaded_file)
            upload_df = upload_df[["Product", "Part", "Quantity"]]
            # st.write(upload_df)

            for i in range(upload_df.shape[0]):
                cursor.execute('INSERT INTO mapping_{user} VALUES("{prd}","{prt}",{q})'.format(user=username,prd=upload_df['Product'][i],prt=upload_df['Part'][i],q=upload_df['Quantity'][i]))
            conn.commit()
        else:
            cursor.execute('INSERT INTO mapping_{user} VALUES("{prd}","{prt}",{q})'.format(user=username,prd=product,prt=part,q=quantity))
            conn.commit()

        cursor.execute("select * from mapping_{user}".format(user=username))
        res = cursor.fetchall()
        mapping_table = pd.DataFrame(res, columns=["Product", "Part", "Quantity"])
        st.table(mapping_table)


    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'collapsed'
    st.sidebar.success("Logged in as {}".format(username))
    # st.sidebar.write("Registration page coming soon...")
    st.write("Welcome, {}".format(name))
    tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Overview","Inventory","Orders","Analysis","Reports","Billing","Mapping"])

    with tab1:
        check_inventory = st.button("Check Inventory", on_click=chckinvclicked1)
        if st.session_state.chckinvclicked:
            # cursor.execute("select parts as parts, sum(quantity) as total_quantity from inventory_{user} group by parts".format(user=username))
            cursor.execute(''' select aa.parts, aa.total_quantity - coalesce(ab.total_quantity,0) 
                                from (select parts as parts, sum(quantity) as total_quantity 
                                from inventory_{user} group by parts) as aa   
                                left join 
                                (select b.part as part, sum(a.quantity*b.quantity) as total_quantity from billing_{user} as a 
                                left join mapping_{user} as b 
                                on a.product = b.product 
                                group by b.part) as ab 
                                on aa.parts = ab.part '''.format(user=username))
            res1 = cursor.fetchall()
            st.table(pd.DataFrame(res1,columns=["parts", "total quantity"]))
            st.session_state.chckinvclicked = False

        st.write("Please input inventory details:")

        invoice_no = st.text_input("Invoice Number")
        parts = st.text_input("Parts")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        purchase_date = st.date_input("Purchase Date")

        uploaded_file = st.file_uploader("Upload csv file", type='csv')

        if st.button("Add to Inventory"):
            add_inventory(invoice_no, parts, quantity, purchase_date, uploaded_file, username)
            st.success("Added to inventory!")
    with tab2:
        st.write('Coming Soon...')
    with tab3:
        st.write('Coming Soon...')
    with tab4:
        st.write('Coming Soon...')
    with tab0:
        st.write('Coming Soon...')

    with tab5:
        check_bill = st.button("Show me Bills", on_click=chckbillclicked1)
        if st.session_state.chckbillclicked:
            # cursor.execute("select * from billing_{user}".format(user=username))
            cursor.execute("select * from billing_{user}".format(user=username))
            res1 = cursor.fetchall()
            st.table(pd.DataFrame(res1,columns=["Invoice Number", "Products", "Quantity", "Bill Date"]))
            st.session_state.chckbillclicked = False

        st.write("Please input billing details:")

        invoice_no = st.text_input("Invoice Number ")
        cursor.execute("select distinct product from mapping_{user}".format(user=username))
        res = cursor.fetchall()
        prod_tb = pd.DataFrame(res, columns=["Product"])
        product = st.selectbox("Product",prod_tb['Product'].unique())
        quantity = st.number_input("Quantity ", min_value=1, step=1)
        bill_date = st.date_input("Bill Date")

        # uploaded_file = st.file_uploader("Upload csv file ", type='csv')

        if st.button("Add to Billing"):
            add_billing(invoice_no, product, quantity, bill_date, uploaded_file, username)
            st.success("Added to billing!")

    with tab6:
        check_mapping = st.button("Show me Product Mapping", on_click=chckmapclicked1)
        if st.session_state.chckmapclicked:
            # cursor.execute("select * from billing_{user}".format(user=username))
            cursor.execute("select * from mapping_{user}".format(user=username))
            res1 = cursor.fetchall()
            st.table(pd.DataFrame(res1,columns=["Product", "Part", "Quantity"]))
            st.session_state.chckmapclicked = False

        st.write("Please input product mapping with parts:")

        cols=st.columns(3)
        with cols[0]:
            pr = st.text_input('Product ')
        with cols[1]:
            pt = st.text_input('Part')
        with cols[2]:
            qt = st.text_input('Quantity')

        # uploaded_file = st.file_uploader("Upload csv file ", type='csv')

        if st.button("Add to Mapping"):
            add_mapping(pr, pt, qt, uploaded_file, username)
            st.success("Added to mapping!")
        # st.table(mapping_table)

    if st.session_state.clrinvclicked:
        cursor.execute("delete from inventory_{user}".format(user=username))
        conn.commit()
        st.session_state.clrinvclicked = False

    if st.session_state.clrbillclicked:
        cursor.execute("delete from billing_{user}".format(user=username))
        conn.commit()
        st.session_state.clrbillclicked = False

    if st.session_state.clrmapclicked:
        cursor.execute("delete from mapping_{user}".format(user=username))
        conn.commit()
        st.session_state.clrmapclicked = False



## Login authentication
if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your credentials')
elif authentication_status:
    if 'sidebar_state' not in st.session_state:
        st.session_state.sidebar_state = 'expanded'
    if __name__ == "__main__":
        main()
    authenticator.logout('Logout', 'sidebar')


