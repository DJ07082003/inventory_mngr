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

conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

cmd1 = "CREATE TABLE IF NOT EXISTS inventory(product TEXT, parts TEXT, quantity INTEGER, purchase_date DATE)"
cursor.execute(cmd1)

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


# Function to extract item names, quantities, and purchase date from bill text
# def extract_info_from_bill(bill_text):
#     # Define patterns for item names, quantities, and date
#     item_name_pattern = r"[\w\s]+"
#     quantity_pattern = r"\d+"
#     date_pattern = r"\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}"

#     # Extract item names, quantities, and date from bill text
#     item_names = re.findall(item_name_pattern, bill_text, flags=re.IGNORECASE)
#     quantities = re.findall(quantity_pattern, bill_text)
#     dates = re.findall(date_pattern, bill_text)

#     # Assuming each item has a corresponding quantity and purchase date
#     if len(item_names) == len(quantities) and len(item_names) == len(dates):
#         return list(zip(item_names, quantities, dates))
#     else:
#         return None

# Dummy user credentials
registered_users = {
    "user1": "Lovely1",
    "user2": "Lovely2"
}

# # Dummy inventory data
# inventory_data = pd.DataFrame({
#     "Product": [],
#     "Parts": [],
#     "Quantity": [],
#     "Date": [],
#     "Purchase_Date": []
# })

# Create the SQL connection to pets_db as specified in your secrets file.
# conn = st.connection('inventory1_db', type='sql')

# Insert some data with conn.session.
# with conn.session as s:
#     s.execute('CREATE TABLE IF NOT EXISTS pet_owners (person TEXT, pet TEXT);')
#     s.execute('DELETE FROM pet_owners;')
#     pet_owners = {'jerry': 'fish', 'barbara': 'cat', 'alex': 'puppy'}
#     for k in pet_owners:
#         s.execute(
#             'INSERT INTO pet_owners (person, pet) VALUES (:owner, :pet);',
#             params=dict(owner=k, pet=pet_owners[k])
#         )
#     s.commit()

# # Query and display the data you inserted
# pet_owners = conn.query('select * from pet_owners')
# st.dataframe(pet_owners)

# with conn.session as s:
#     s.execute('CREATE TABLE IF NOT EXISTS inventory_data (Product TEXT, Parts TEXT, Quantity INTEGER);')
#     s.commit()

# Query and display the data you inserted
# pet_owners = conn.query('select * from inventory_data')
# st.dataframe(pet_owners)


# inventory_data = pd.DataFrame(columns = ["Product", "Parts", "Quantity","Date","Purchase_Date"])

# Function to add inventory input
def add_inventory(product, parts, quantity, purchase_date, uploaded_file):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d %H:%M:%S")
    if uploaded_file is not None:
        upload_df = pd.read_csv(uploaded_file)
        upload_df = upload_df[["product", "parts", "quantity", "purchase_date"]]
        # st.write(upload_df)

        for i in range(upload_df.shape[0]):
            cursor.execute('INSERT INTO inventory VALUES("{prd}","{prt}",{q},"{prdt}")'.format(prd=upload_df['product'][i],prt=upload_df['parts'][i],q=upload_df['quantity'][i],prdt=upload_df['purchase_date'][i]))
        conn.commit()
    else:
        cursor.execute('INSERT INTO inventory VALUES("{prd}","{prt}",{q},"{prdt}")'.format(prd=product,prt=parts,q=quantity,prdt=purchase_date))
        conn.commit()

    cursor.execute("select * from inventory")
    res = cursor.fetchall()
    st.table(pd.DataFrame(res, columns=["product", "parts", "quantity", "purchase_date"]))

    # inventory_data = pd.concat([inventory_data,pd.DataFrame({"Product":[product],
    #                 "Parts":[parts],
    #                 "Quantity":[quantity],
    #                 "Date":[current_date],
    #                 "Purchase_Date":[purchase_date]})],ignore_index=True)
    
    # with conn.session as s:
    #     s.execute('INSERT INTO inventory_data (Product, Parts) VALUES (prd, prt);'.format(prd=product,prt=parts))
    #     s.commit()

    # st.table(conn.query('select * from inventory_data'))
    # st.table(inventory_data)
    # print(inventory_data)
    # return inventory_data
    # inventory_data = pd.DataFrame({"Product":[product],
    #                 "Parts":[parts],
    #                 "Quantity":[quantity],
    #                 "Date":[current_date],
    #                 "Purchase_Date":[purchase_date]})
    # inventory_data["Product"].extend(product)
    # inventory_data["Parts"].extend(parts)
    # inventory_data["Quantity"].extend(quantity)
    # inventory_data["Date"].extend(current_date)
    # inventory_data["Purchase_Date"].extend(purchase_date)

# Function to generate bill and deduct from inventory
def generate_bill(products):
    for product in products:
        # Deduct quantity from inventory data
        # Here you can implement logic to deduct from inventory
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

if 'chckinvclicked' not in st.session_state:
    st.session_state.chckinvclicked = False

def chckinvclicked1():
    st.session_state.chckinvclicked = True

def main():
    st.title("Inventory Management System")

    # Login page
    # login = st.sidebar.checkbox("Login")
    # if login:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login = st.sidebar.button("Login", on_click=loginclicked1)
    forgot_password = st.sidebar.button("Forgot Password", on_click=forgotpwdclicked1)

    clear_inventory = st.sidebar.button("Clear Inventory", on_click=clrinvclicked1)
    check_inventory = st.button("Check Inventory", on_click=chckinvclicked1)

    if st.session_state.chckinvclicked:
        cursor.execute("select parts as parts, sum(quantity) as total_quantity from inventory group by parts")
        res1 = cursor.fetchall()
        st.table(pd.DataFrame(res1,columns=["parts", "total quantity"]))
        st.session_state.chckinvclicked = False

    if st.session_state.clrinvclicked:
        cursor.execute("delete from inventory")
        conn.commit()
        st.session_state.clrinvclicked = False

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
                            registered_users[username] = new_pswrd
                        st.success("OTP verified. You can now reset your credentials.")
                        # Add functionality to reset credentials here
                    else:
                        st.error("Invalid OTP. Please try again.")
            else:
                st.error("Invalid phone number. Please enter the registered phone number.")



    if st.session_state.loginclicked:
            # if username <> "":
        if username in registered_users and registered_users[username] == password:
            st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'collapsed'
            st.sidebar.success("Logged in as {}".format(username))
            # st.sidebar.write("Registration page coming soon...")
            st.write("Welcome, {}".format(username))
            st.write("Please input inventory details:")

            # st.title("Bill Information Extractor")

            # uploaded_file = st.file_uploader("Upload Bill Image", type=["jpg", "jpeg", "png"])

            # if uploaded_file is not None:
            #     bill_image = Image.open(uploaded_file)
            #     st.image(bill_image, caption="Uploaded Bill Image", use_column_width=True)

            #     if st.button("Extract Information"):
            #         # Perform OCR to extract text from bill image
            #         bill_text = pytesseract.image_to_string(bill_image)

            #         # Extract information from bill text
            #         info = extract_info_from_bill(bill_text)

            #         if info:
            #             st.header("Extracted Information from Bill:")
            #             for i, (item_name, quantity, date) in enumerate(info, start=1):
            #                 st.write(f"Item {i}:")
            #                 st.write(f"- Name: {item_name.strip()}")
            #                 st.write(f"- Quantity: {quantity}")
            #                 st.write(f"- Purchase Date: {date}")
            #         else:
            #             st.error("Failed to extract information from bill. Please try again or upload a clearer image.")



            product = st.text_input("Product")
            parts = st.text_input("Parts")
            quantity = st.number_input("Quantity", min_value=1, step=1)
            purchase_date = st.date_input("Purchase Date")

            uploaded_file = st.file_uploader("Upload csv file", type='csv')

            if st.button("Add to Inventory"):
                add_inventory(product, parts, quantity, purchase_date, uploaded_file)
                # add_inventory(inventory_data,product, parts, "1", "2023-04-01")
                st.success("Added to inventory!")
                # print(inventory_data)
                # st.table(inventory_data)

            # Button to generate bill
            # if st.button("Generate Bill"):
            #     selected_products = st.multiselect("Select Products for Bill", inventory_data["Product"])
            #     generate_bill(selected_products)

        if (username in ("")):
            pass
        elif (username not in (registered_users)):
            st.sidebar.error("Invalid username.")
        elif password in (""):
            st.sidebar.error("Please check your credentials.")
        elif password != (registered_users[username]):
            st.sidebar.error("Password doesn't match. Please try again.")
        else:
            pass


if __name__ == "__main__":
    main()

