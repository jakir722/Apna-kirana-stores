import streamlit as st
import json
import os

# डेटाबेस फ़ाइल
DB_FILE = "mlm_store_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"ADMIN": {"name": "Main Admin", "sponsor_id": None, "wallet": 0.0}}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ऐप की स्क्रीन का डिज़ाइन (UI)
st.title("🍵 चाय पत्ती - 7 Level MLM सिस्टम")
st.write("MRP: ₹20 | नेटवर्क कमीशन डिस्ट्रीब्यूशन: ₹5")

data = load_data()

# टैब बनाना (अलग-अलग स्क्रीन)
tab1, tab2, tab3 = st.tabs(["👤 नया मेंबर जोड़ें", "🛒 चाय पत्ती बिक्री", "💰 वॉलेट बैलेंस देखें"])

with tab1:
    st.header("नया रजिस्ट्रेशन")
    new_id = st.text_input("यूजर आईडी (Unique ID बनाएं जैसे: CUST101)").strip()
    new_name = st.text_input("मेंबर का नाम")
    sponsor_id = st.text_input("स्पॉन्सर आईडी (जिसने इस मेंबर को जोड़ा)").strip()
    
    if st.button("रजिस्टर करें"):
        if not new_id or not new_name:
            st.error("कृपया आईडी और नाम दोनों भरें!")
        elif new_id in data:
            st.error("यह आईडी पहले से मौजूद है!")
        elif sponsor_id and sponsor_id not in data:
            st.error("स्पॉन्सर आईडी गलत है या सिस्टम में नहीं है!")
        else:
            data[new_id] = {"name": new_name, "sponsor_id": sponsor_id if sponsor_id else None, "wallet": 0.0}
            save_data(data)
            st.success(f"✅ {new_name} सफलतापूर्वक जुड़ गए हैं!")

with tab2:
    st.header("चाय पत्ती सेल (कमीशन डिस्ट्रीब्यूशन)")
    buyer_id = st.text_input("खरीदारी करने वाले की आईडी डालें").strip()
    
    if st.button("बिक्री दर्ज करें (₹20)"):
        if buyer_id not in data:
            st.error("यह आईडी रजिस्टर्ड नहीं है!")
        else:
            # 7 लेवल का कमीशन स्ट्रक्चर
            comm_structure = {1: 2.00, 2: 1.00, 3: 0.70, 4: 0.50, 5: 0.40, 6: 0.20, 7: 0.20}
            current_sponsor = data[buyer_id]["sponsor_id"]
            level = 1
            logs = []
            
            while current_sponsor and level <= 7:
                amount = comm_structure[level]
                data[current_sponsor]["wallet"] += amount
                logs.append(f"लेवल {level}: {data[current_sponsor]['name']} को ₹{amount} मिले।")
                current_sponsor = data[current_sponsor]["sponsor_id"]
                level += 1
                
            save_data(data)
            st.success("🎉 बिक्री सफल! कमीशन तुरंत बांट दिया गया है।")
            for log in logs:
                st.info(log)

with tab3:
    st.header("वॉलेट का बैलेंस चेक करें")
    check_id = st.text_input("बैलेंस देखने के लिए यूजर आईडी डालें").strip()
    if st.button("बैलेंस देखें"):
        if check_id in data:
            st.metric(label=f"{data[check_id]['name']} का कुल बैलेंस", value=f"₹{data[check_id]['wallet']:.2f}")
        else:
            st.error("आईडी नहीं मिली!")
