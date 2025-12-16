import streamlit as st
from fpdf import FPDF
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="YouParcel Quote Generator", page_icon="📦")
st.title("📦 YouParcel Quote Generator")
st.markdown("Fill in the details below to generate a professional PDF quotation.")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    # REMOVED: File Uploader
    # ADDED: Info message
    st.info("✅ Using Company Logo from system.")
    
    st.header("1. Quote Metadata")
    quote_ref = st.text_input("Quote Reference", "YPDEC25BB019IMP")
    quote_date = st.text_input("Date", "December 16, 2025")
    validity = st.text_input("Validity", "30 Days")
    
    st.header("2. Prepared By")
    prep_name = st.text_input("Name", "Kaan Gul")
    prep_title = st.text_input("Title", "Director of Logistics | YouParcel")
    prep_phone = st.text_input("Phone", "(201) 782-6081")
    prep_email = st.text_input("Email", "kaan@youparcel.com")

# --- MAIN FORM INPUTS ---
st.subheader("Shipment Details")
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Origin (POL)", "Istanbul / Ambarli, Turkey")
    dest = st.text_input("Destination (POD)", "New York, NY")
with col2:
    term = st.text_input("Term", "Port to Door")
    equipment = st.text_input("Equipment", "40' High Cube")

st.subheader("Ocean Freight Options")
c1_def = ["MSC", "EXCLUDED", "$1,816.80", "+$50 PS +$25 AMS", "$1,891.80*", "ISPS Included"]
c2_def = ["COSCO", "EXCLUDED", "$1,274.40", "+$50 PS +$25 AMS", "$1,349.40*", "ETS Included"]
c3_def = ["CMA", "INCLUDED", "$1,680.00", "+$50 PS +$32 AMS", "$1,762.00", "Best Value"]

carriers = []
# Carrier 1
with st.expander("Carrier Option 1", expanded=True):
    c1, c2, c3 = st.columns(3)
    n1 = c1.text_input("Carrier 1 Name", c1_def[0])
    s1 = c2.selectbox("Carrier 1 Locals", ["EXCLUDED", "INCLUDED"], index=0)
    f1 = c3.text_input("Carrier 1 Freight", c1_def[2])
    c4, c5, c6 = st.columns(3)
    su1 = c4.text_input("Carrier 1 Surcharges", c1_def[3])
    t1 = c5.text_input("Carrier 1 Total", c1_def[4])
    r1 = c6.text_input("Carrier 1 Remark", c1_def[5])
    carriers.append((n1, s1, f1, su1, t1, r1))

# Carrier 2
with st.expander("Carrier Option 2", expanded=False):
    c1, c2, c3 = st.columns(3)
    n2 = c1.text_input("Carrier 2 Name", c2_def[0])
    s2 = c2.selectbox("Carrier 2 Locals", ["EXCLUDED", "INCLUDED"], index=0)
    f2 = c3.text_input("Carrier 2 Freight", c2_def[2])
    c4, c5, c6 = st.columns(3)
    su2 = c4.text_input("Carrier 2 Surcharges", c2_def[3])
    t2 = c5.text_input("Carrier 2 Total", c2_def[4])
    r2 = c6.text_input("Carrier 2 Remark", c2_def[5])
    carriers.append((n2, s2, f2, su2, t2, r2))

# Carrier 3
with st.expander("Carrier Option 3", expanded=False):
    c1, c2, c3 = st.columns(3)
    n3 = c1.text_input("Carrier 3 Name", c3_def[0])
    s3 = c2.selectbox("Carrier 3 Locals", ["EXCLUDED", "INCLUDED"], index=1)
    f3 = c3.text_input("Carrier 3 Freight", c3_def[2])
    c4, c5, c6 = st.columns(3)
    su3 = c4.text_input("Carrier 3 Surcharges", c3_def[3])
    t3 = c5.text_input("Carrier 3 Total", c3_def[4])
    r3 = c6.text_input("Carrier 3 Remark", c3_def[5])
    carriers.append((n3, s3, f3, su3, t3, r3))

st.subheader("Inland Delivery")
del_addr = st.text_input("Delivery Address", "108 Boston Post Rd, Orange, CT 06477")
c1, c2, c3 = st.columns(3)
base_rate = c1.text_input("Base Trucking Rate", "$1,290.00")
toll = c2.text_input("Toll Fee", "$200.00")
total_del = c3.text_input("Total Delivery Cost", "$1,490.00")

# --- PDF CLASS ---
class PDF(FPDF):
    def header(self):
        # UPDATED LOGIC: Look for 'logo.png' in the same folder
        logo_path = "logo.png" 
        
        if os.path.exists(logo_path):
            self.image(logo_path, x=10, y=10, w=28)
        else:
            # Fallback if file isn't uploaded to GitHub yet
            self.set_font("Arial", "B", 10)
            self.set_xy(10, 10)
            self.set_text_color(255, 0, 0)
            self.cell(30, 10, "LOGO MISSING", 0, 0)

        self.set_xy(110, 10)
        self.set_font("Arial", "B", 12)
        self.set_text_color(80, 80, 80)
        self.cell(0, 5, "YouParcel", 0, 1, "R")
        self.set_font("Arial", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 5, "20 Farinella Dr, East Hanover, NJ 07039", 0, 1, "R")
        self.cell(0, 5, "P: (201) 366-0444 | E: info@youparcel.com", 0, 1, "R")
        self.cell(0, 5, "www.youparcel.com", 0, 1, "R")
        self.ln(10)
        self.set_draw_color(243, 112, 33) # Orange
        self.set_line_width(0.8)
        self.line(10, 35, 200, 35)
        self.ln(8)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 5, f"Page {self.page_no()}/{{nb}}", 0, 1, "C")
        self.cell(0, 5, "YouParcel | Freight Quotation & Terms", 0, 0, "C")

def generate_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    
    # --- PAGE 1 ---
    pdf.add_page()
    
    # Metadata
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0, 85, 165) # Blue
    pdf.cell(0, 10, "FREIGHT QUOTATION", 0, 1, "L")
    
    start_y = pdf.get_y()
    pdf.set_fill_color(250, 250, 250)
    pdf.set_draw_color(220, 220, 220)
    pdf.rect(120, start_y - 12, 80, 26, "DF")
    
    pdf.set_xy(125, start_y - 9)
    pdf.set_font("Arial", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(30, 6, "Quote Ref:", 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.cell(40, 6, quote_ref, 0, 1)

    pdf.set_xy(125, start_y - 3)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(30, 6, "Date:", 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.cell(40, 6, quote_date, 0, 1)

    pdf.set_xy(125, start_y + 3)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(30, 6, "Validity:", 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.cell(40, 6, validity, 0, 1)
    pdf.set_y(start_y + 18)
    
    # Shipment Details
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(0, 85, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  SHIPMENT DETAILS", 0, 1, "L", True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.ln(3)
    
    col_width = 95
    pdf.cell(30, 6, "Origin (POL):", 0, 0)
    pdf.cell(col_width, 6, origin, 0, 0)
    pdf.cell(25, 6, "Term:", 0, 0)
    pdf.cell(40, 6, term, 0, 1)
    pdf.cell(30, 6, "Dest (POD):", 0, 0)
    pdf.cell(col_width, 6, dest, 0, 0)
    pdf.cell(25, 6, "Equipment:", 0, 0)
    pdf.cell(40, 6, equipment, 0, 1)
    pdf.ln(5)
    
    # Ocean Table
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(243, 112, 33)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  1. OCEAN FREIGHT OPTIONS", 0, 1, "L", True)
    pdf.ln(2)
    
    pdf.set_font("Arial", "B", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(230, 230, 230)
    widths = [20, 35, 25, 45, 25, 40]
    headers = ["Carrier", "Origin Locals", "Freight", "Surcharges", "Est. Total", "Remarks"]
    for h, w in zip(headers, widths):
        pdf.cell(w, 10, h, 1, 0, "C", True)
    pdf.ln()
    
    pdf.set_font("Arial", "", 9)
    for c_name, c_status, c_freight, c_surch, c_total, c_remark in carriers:
        if not c_name: continue
        pdf.cell(widths[0], 10, c_name, 1, 0, "C")
        if c_status == "INCLUDED":
            pdf.set_text_color(0, 128, 0)
            pdf.set_font("Arial", "B", 9)
        else:
            pdf.set_text_color(200, 0, 0)
            pdf.set_font("Arial", "B", 7)
        pdf.cell(widths[1], 10, c_status, 1, 0, "C")
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 9)
        pdf.cell(widths[2], 10, c_freight, 1, 0, "C")
        pdf.set_font("Arial", "", 8)
        pdf.cell(widths[3], 10, c_surch, 1, 0, "C")
        pdf.set_font("Arial", "B", 9)
        pdf.cell(widths[4], 10, c_total, 1, 0, "C")
        pdf.set_font("Arial", "I", 8)
        pdf.cell(widths[5], 10, c_remark, 1, 1, "C")
    pdf.ln(8)
    
    # Inland
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(0, 85, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  2. INLAND DELIVERY (Door Delivery)", 0, 1, "L", True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.ln(3)
    pdf.cell(40, 6, "Final Destination:", 0, 0, "B")
    pdf.cell(0, 6, del_addr, 0, 1)
    
    pdf.set_fill_color(240, 240, 240)
    y = pdf.get_y()
    pdf.rect(10, y, 190, 24, "F")
    pdf.set_xy(15, y + 2)
    pdf.set_font("Arial", "", 10)
    pdf.cell(120, 6, "Base Trucking Rate (Includes Drayage + Fuel):", 0, 0)
    pdf.cell(60, 6, base_rate, 0, 1, "R")
    pdf.set_x(15)
    pdf.cell(120, 6, "Toll Fee (NYCT/GCT Bayonne):", 0, 0)
    pdf.cell(60, 6, toll, 0, 1, "R")
    pdf.set_x(15)
    pdf.set_font("Arial", "B", 11)
    pdf.set_text_color(243, 112, 33)
    pdf.cell(120, 8, "TOTAL DELIVERY COST:", 0, 0)
    pdf.cell(60, 8, total_del, 0, 1, "R")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)
    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 5, "Trucking Remarks: Rate includes 2 Days Chassis and 2 hours free unload time. Accessorials: Waiting Time $125/hr (after 2 hrs), Chassis $45/day (after 2 days), Storage $50/day (plus port charges), Pre-pull $150.")

    # --- PAGE 2 ---
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 85, 165)
    pdf.cell(0, 10, "ADDITIONAL CHARGES & GENERAL CONDITIONS", 0, 1, "L")
    pdf.ln(2)
    
    # Customs (RESTORED FULL CONTENT)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(243, 112, 33)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  CUSTOMS CLEARANCE & FEES", 0, 1, "L", True)
    pdf.ln(3)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Standard Fees:", 0, 1)
    pdf.set_font("Arial", "", 10)
    
    # 2-Column Fee Structure
    y_start = pdf.get_y()
    
    # Col 1
    pdf.cell(60, 6, "Customs Clearance:", 0, 0); pdf.cell(30, 6, "$125.00 / set", 0, 1, 'R')
    pdf.cell(60, 6, "ISF Filing:", 0, 0); pdf.cell(30, 6, "$35.00 / set", 0, 1, 'R')
    pdf.cell(60, 6, "Messenger & Handling:", 0, 0); pdf.cell(30, 6, "$75.00 / set", 0, 1, 'R')
    pdf.cell(60, 6, "Documentation Fee:", 0, 0); pdf.cell(30, 6, "$95.00", 0, 1, 'R')
    
    # Col 2
    pdf.set_xy(110, y_start)
    pdf.cell(60, 6, "FDA Prior Notice (if app):", 0, 0); pdf.cell(30, 6, "$75.00 / set", 0, 1, 'R')
    pdf.set_xy(110, pdf.get_y())
    pdf.cell(60, 6, "Add. Line Items (after 1st):", 0, 0); pdf.cell(30, 6, "$5.00 / item", 0, 1, 'R')
    pdf.set_xy(110, pdf.get_y())
    pdf.cell(60, 6, "FDA Lines (after 5th):", 0, 0); pdf.cell(30, 6, "$5.00 / item", 0, 1, 'R')
    
    pdf.ln(10)
    
    # Bond Section (RESTORED)
    pdf.set_x(10)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 6, "Customs Bond Charges (Importer must have Bond):", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, "- Annual Bond: $650.00 (Covers up to $50k duty value/year). Recommended.\n"
                         "- Single Transaction Bond: Min $80.00 or $8.00 per $1,000 invoice value.\n"
                         " (For FDA items: Bond calculated on Commercial Value + Duty x 3).\n"
                         "- ISF Single Bond: $75.00 / set (If no annual bond exists).")
    pdf.ln(5)
    
    # Duty Policy (RESTORED)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(200, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  IMPORT DUTY & TAX POLICY", 0, 1, "L", True)
    pdf.ln(3)
    
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Arial", "B", 10)
    pdf.multi_cell(0, 5, "IMPORTANT: We do not provide credit terms for Duty payments. Duties must be settled prior to vessel arrival to avoid delays.")
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, "Duties are billed at Actual Cost. In addition, US Customs collects:\n"
                         "1. MPF (Merchandise Processing Fee): 0.3464% of FOB Value (Min $33.58 / Max $651.50).\n"
                         "2. HMF (Harbor Maintenance Fee): 0.125% of FOB Value (Ocean shipments only).\n"
                         "3. Draft Entry Fee: $35.00 (Due to tariff complexities, a draft is provided 5-7 days pre-arrival).\n"
                         "4. Disbursement Fee: 3% of duty amount (Minimum $35.00).")
    pdf.ln(5)
    
    # General Conditions (RESTORED)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(0, 85, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 8, "  GENERAL CONDITIONS", 0, 1, "L", True)
    pdf.ln(3)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, "1. IMPORTER OF RECORD (IOR): Consignee must sign Power of Attorney (POA) with us for clearance.\n"
                         "2. LATE ISF: We are not responsible for late ISF penalties (up to $5000) if POA/info is not received on time.\n"
                         "3. VALIDITY: Quotation valid for 30 days. Rates do not include exams, demurrage, or detention.\n"
                         "4. ACCESSORIAL PROOF: Costs such as Pre-pull, Chassis Split, Flip Fee, Waiting Time will only be accepted upon presentation of evidence.\n"
                         "5. INSURANCE: All-Risk Insurance is highly recommended for cargoes over USD 75,000.\n"
                         "6. PAYMENT: Custom Clearance Charges (Duty, HMF, Exam Fees) will be billed without credit terms.")
    
    # Prepared By
    pdf.ln(8)
    if pdf.get_y() > 240: pdf.add_page()
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Prepared by:", 0, 1)
    pdf.ln(1)
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 85, 165)
    pdf.cell(0, 6, prep_name, 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 5, prep_title, 0, 1)
    pdf.cell(0, 5, f"P: {prep_phone}", 0, 1)
    pdf.cell(0, 5, f"E: {prep_email}", 0, 1)

    return pdf.output(dest='S').encode('latin-1')

# --- GENERATE BUTTON ---
if st.button("Generate PDF", type="primary"):
    pdf_bytes = generate_pdf()
    st.success("PDF Generated Successfully!")
    st.download_button(
        label="Download Quote PDF",
        data=pdf_bytes,
        file_name=f"YouParcel_Quote_{quote_ref}.pdf",
        mime="application/pdf"
    )
