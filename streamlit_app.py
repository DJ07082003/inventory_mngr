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

mapping_table = pd.DataFrame({"Product":["Prod1","Prod1","Prod1","Prod2","Prod2","Prod3","Prod3"], 
                        "Part":["Part1","Part2","Part3","Part1","Part2","Part1","Part3"], 
                        "Quantity":[5,4,2,2,3,3,1]})


if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

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

# Dummy user credentials
registered_users = {
    "akshay": ["Akshay12",+919876543210],
    "umesh": ["Umesh12",919876543210],
    "pratik": ["Pratik12",+919876543210]
}

# Function to generate bill and deduct from inventory
def generate_bill(products):
    for product in products:
        pass

if 'loginclicked' not in st.session_state:
    st.session_state.loginclicked = False

def loginclicked1():
    st.session_state.loginclicked = True

if 'forgotpwdclicked' not in st.session_state:
    st.session_state.forgotpwdclicked = False

def forgotpwdclicked1():
    st.session_state.forgotpwdclicked = True

if 'clrinvclicked' not in st.session_state:
    st.session_state.clrinvclicked = False

def clrinvclicked1():
    st.session_state.clrinvclicked = True

if 'clrbillclicked' not in st.session_state:
    st.session_state.clrbillclicked = False

def clrbillclicked1():
    st.session_state.clrbillclicked = True

if 'chckinvclicked' not in st.session_state:
    st.session_state.chckinvclicked = False

def chckinvclicked1():
    st.session_state.chckinvclicked = True

if 'chckbillclicked' not in st.session_state:
    st.session_state.chckbillclicked = False

def chckbillclicked1():
    st.session_state.chckbillclicked = True

def main():
    st.title("Inventory Management System")

    # Login page
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login = st.sidebar.button("Login", on_click=loginclicked1)
    forgot_password = st.sidebar.button("Forgot Password", on_click=forgotpwdclicked1)

    clear_inventory = st.sidebar.button("Clear Inventory", on_click=clrinvclicked1)
    clear_billing = st.sidebar.button("Clear Billing", on_click=clrbillclicked1)


    if st.session_state.loginclicked:
            # if username <> "":
        if username in registered_users and registered_users[username][0] == password:

            conn = sqlite3.connect("inventory_{user}.db".format(user=username))
            cursor = conn.cursor()

            cmd1 = "CREATE TABLE IF NOT EXISTS inventory_{user}(invoice_no TEXT, parts TEXT, quantity INTEGER, purchase_date DATE)".format(user=username)
            cursor.execute(cmd1)

            cmd2 = "CREATE TABLE IF NOT EXISTS billing_{user}(invoice_no TEXT, product TEXT, quantity INTEGER, bill_date DATE)".format(user=username)
            cursor.execute(cmd2)

            cmd3 = "CREATE TABLE IF NOT EXISTS mapping_{user}(product TEXT, part TEXT, quantity INTEGER)".format(user=username)
            cursor.execute(cmd3)

            cursor.execute("select count(1) from mapping_{user}".format(user=username))
            res = cursor.fetchall()
            if res[0][0] < 1:
                for i in range(mapping_table.shape[0]):
                    cursor.execute('INSERT INTO mapping_{user} VALUES("{prd}","{prt}",{q})'.format(user=username,prd=mapping_table['Product'][i],prt=mapping_table['Part'][i],q=mapping_table['Quantity'][i]))
                conn.commit()

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


            st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'collapsed'
            st.sidebar.success("Logged in as {}".format(username))
            # st.sidebar.write("Registration page coming soon...")
            st.write("Welcome, {}".format(username))
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Inventory","Orders","Analysis","Reports","Billing","Mapping"])

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
                product = st.selectbox("Product",mapping_table['Product'].unique())
                quantity = st.number_input("Quantity ", min_value=1, step=1)
                bill_date = st.date_input("Bill Date")

                # uploaded_file = st.file_uploader("Upload csv file ", type='csv')

                if st.button("Add to Billing"):
                    add_billing(invoice_no, product, quantity, bill_date, uploaded_file, username)
                    st.success("Added to billing!")

            with tab6:
                # st.table(pd.DataFrame({"Product":"Prod1", "Part":"Part1", "Quantity":5},
                #                         {"Product":"Prod1", "Part":"Part2", "Quantity":4},
                #                         {"Product":"Prod1", "Part":"Part3", "Quantity":2},
                #                         {"Product":"Prod2", "Part":"Part1", "Quantity":2},
                #                         {"Product":"Prod2", "Part":"Part2", "Quantity":3},
                #                         {"Product":"Prod3", "Part":"Part1", "Quantity":3},
                #                         {"Product":"Prod3", "Part":"Part3", "Quantity":1}
                #                         ))
                st.table(mapping_table)

            if st.session_state.clrinvclicked:
                cursor.execute("delete from inventory_{user}".format(user=username))
                conn.commit()
                st.session_state.clrinvclicked = False

            if st.session_state.clrbillclicked:
                cursor.execute("delete from billing_{user}".format(user=username))
                conn.commit()
                st.session_state.clrbillclicked = False



        if (username in ("")):
            pass
        elif (username not in (registered_users)):
            st.sidebar.error("Invalid username.")
        elif password in (""):
            st.sidebar.error("Please check your credentials.")
        elif password != (registered_users[username][0]):
            st.sidebar.error("Password doesn't match. Please try again.")
        else:
            pass

# if forgot_password:
    if st.session_state.forgotpwdclicked:

        st.title("Credential Reset Page")

        registered_phone_number = "1234567890"  # Assume this is the registered phone number

        phone_number = st.text_input("Enter Registered Phone Number")

        if st.button("Send OTP"):
            if phone_number == registered_phone_number:
                otp = generate_otp()
                send_otp_via_sms(phone_number, otp)
                st.success("OTP sent successfully. Check your phone messages.")
                otp_input = st.text_input("Enter OTP")

                if otp_input:
                    if otp_input == otp:
                        username = st.sidebar.text_input("Username")
                        new_pswrd = st.text_input("New Password")
                        confirm_pswrd = st.text_input("Confirm Password")
                        if new_pswrd == confirm_pswrd:
                            registered_users[username][0] = new_pswrd
                        st.success("OTP verified. You can now reset your credentials.")
                        # Add functionality to reset credentials here
                    else:
                        st.error("Invalid OTP. Please try again.")
            else:
                st.error("Invalid phone number. Please enter the registered phone number.")

if __name__ == "__main__":
    main()

