from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json, os

os.makedirs("data", exist_ok=True)

# ── SOURCE A: Official Laptop Price Manual (PDF) ───────────
c = canvas.Canvas("data/laptop_manual.pdf", pagesize=A4)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 800, "TechStore Official Laptop Price Manual 2024")
c.setFont("Helvetica", 11)

lines = [
    "",
    "SECTION 1: BUDGET LAPTOPS (Under 50000 INR)",
    "Lenovo IdeaPad Slim 3: Rs. 35990",
    "  Specs: Intel i3, 8GB RAM, 512GB SSD, 15.6 inch",
    "  Warranty: 2 years, Battery life: 8 hours",
    "",
    "HP 15s: Rs. 38490",
    "  Specs: AMD Ryzen 5, 8GB RAM, 512GB SSD, 15.6 inch",
    "  Warranty: 2 years, Battery life: 9 hours",
    "",
    "Acer Aspire 5: Rs. 42990",
    "  Specs: Intel i5, 16GB RAM, 512GB SSD, 15.6 inch",
    "  Warranty: 2 years, Battery life: 7 hours",
    "",
    "SECTION 2: MID RANGE LAPTOPS (50000 to 80000 INR)",
    "Dell Inspiron 15: Rs. 58990",
    "  Specs: Intel i5, 16GB RAM, 512GB SSD, 15.6 inch",
    "  Warranty: 3 years, Battery life: 10 hours",
    "",
    "ASUS VivoBook 16X: Rs. 62990",
    "  Specs: AMD Ryzen 7, 16GB RAM, 1TB SSD, 16 inch",
    "  Warranty: 2 years, Battery life: 12 hours",
    "",
    "Lenovo ThinkPad E15: Rs. 72990",
    "  Specs: Intel i7, 16GB RAM, 512GB SSD, 15.6 inch",
    "  Warranty: 3 years, Battery life: 11 hours",
    "",
    "SECTION 3: PREMIUM LAPTOPS (Above 80000 INR)",
    "Apple MacBook Air M2: Rs. 114990",
    "  Specs: Apple M2, 8GB RAM, 256GB SSD, 13.6 inch",
    "  Warranty: 1 year, Battery life: 18 hours",
    "",
    "Dell XPS 15: Rs. 189990",
    "  Specs: Intel i9, 32GB RAM, 1TB SSD, 15.6 inch",
    "  Warranty: 3 years, Battery life: 13 hours",
    "",
    "HP Spectre x360: Rs. 164990",
    "  Specs: Intel i7, 16GB RAM, 1TB SSD, 14 inch",
    "  Warranty: 3 years, Battery life: 17 hours",
    "",
    "SECTION 4: GAMING LAPTOPS",
    "ASUS ROG Strix G15: Rs. 124990",
    "  Specs: AMD Ryzen 9, 16GB RAM, 1TB SSD, RTX 3070",
    "  Warranty: 2 years, Battery life: 5 hours",
    "",
    "Lenovo Legion 5 Pro: Rs. 109990",
    "  Specs: AMD Ryzen 7, 16GB RAM, 512GB SSD, RTX 3060",
    "  Warranty: 2 years, Battery life: 4 hours",
    "",
    "MSI Katana GF66: Rs. 89990",
    "  Specs: Intel i7, 16GB RAM, 512GB SSD, RTX 3060",
    "  Warranty: 2 years, Battery life: 4 hours",
]

y = 760
for line in lines:
    if line.startswith("SECTION"):
        c.setFont("Helvetica-Bold", 11)
    elif line.startswith("  "):
        c.setFont("Helvetica-Oblique", 10)
    else:
        c.setFont("Helvetica", 11)
    c.drawString(50, y, line)
    y -= 16
    if y < 50:
        c.showPage()
        y = 800
c.save()
print("laptop_manual.pdf created!")

# ── SOURCE B: Sales Support Logs (JSON) ───────────────────
sales_logs = [
    {"ticket_id": "SL-001", "query": "Lenovo IdeaPad Slim 3 price", "agent_response": "Lenovo IdeaPad Slim 3 is Rs. 35990. Intel i3, 8GB RAM, 512GB SSD. Warranty 2 years. Battery 8 hours.", "verified": True},
    {"ticket_id": "SL-002", "query": "Dell Inspiron 15 price and specs", "agent_response": "Dell Inspiron 15 costs Rs. 58990. i5, 16GB RAM, 512GB SSD. Warranty 3 years. Battery 10 hours.", "verified": True},
    {"ticket_id": "SL-003", "query": "MacBook Air M2 price", "agent_response": "Apple MacBook Air M2 is Rs. 114990. M2 chip, 8GB RAM, 256GB SSD. Battery 18 hours. Warranty 1 year.", "verified": True},
    {"ticket_id": "SL-004", "query": "ASUS ROG Strix G15 specs", "agent_response": "ASUS ROG Strix G15 at Rs. 124990. Ryzen 9, RTX 3070, 16GB RAM, 1TB SSD. Warranty 2 years. Battery 5 hours.", "verified": True},
    {"ticket_id": "SL-005", "query": "MSI Katana GF66 price", "agent_response": "MSI Katana GF66 at Rs. 89990. RTX 3060, i7, 16GB RAM, 512GB SSD. Warranty 2 years.", "verified": True},
    {"ticket_id": "SL-006", "query": "HP Spectre x360 battery", "agent_response": "HP Spectre x360 has 17 hour battery. Price Rs. 164990. i7, 16GB RAM, 1TB SSD. Warranty 3 years.", "verified": True},
    {"ticket_id": "SL-007", "query": "Lenovo Legion 5 Pro price", "agent_response": "Lenovo Legion 5 Pro Rs. 109990. Ryzen 7, RTX 3060, 16GB RAM. Warranty 2 years. Battery 4 hours.", "verified": True},
]
with open("data/laptop_sales_logs.json", "w") as f:
    json.dump(sales_logs, f, indent=2)
print("laptop_sales_logs.json created!")

# ── SOURCE C: Outdated Wiki (Markdown) ────────────────────
wiki = """# TechStore Laptop Wiki (Last Updated 2022 - OUTDATED)

## Budget Laptops

### Lenovo IdeaPad Slim 3
Price: Rs. 29990
Specs: Intel i3, 4GB RAM, 256GB SSD, 15.6 inch
Warranty: 1 year
Battery life: 5 hours

### HP 15s
Price: Rs. 31990
Specs: AMD Ryzen 3, 4GB RAM, 256GB SSD, 15.6 inch
Warranty: 1 year
Battery life: 6 hours

### Acer Aspire 5
Price: Rs. 36990
Specs: Intel i5, 8GB RAM, 256GB SSD, 15.6 inch
Warranty: 1 year
Battery life: 5 hours

## Mid Range Laptops

### Dell Inspiron 15
Price: Rs. 52990
Specs: Intel i5, 8GB RAM, 256GB SSD, 15.6 inch
Warranty: 1 year
Battery life: 7 hours

### ASUS VivoBook 16X
Price: Rs. 54990
Specs: AMD Ryzen 5, 8GB RAM, 512GB SSD, 16 inch
Warranty: 1 year
Battery life: 8 hours

### Lenovo ThinkPad E15
Price: Rs. 65990
Specs: Intel i5, 8GB RAM, 256GB SSD, 15.6 inch
Warranty: 2 years
Battery life: 8 hours

## Premium Laptops

### Apple MacBook Air M2
Price: Rs. 99990
Specs: Apple M1, 8GB RAM, 256GB SSD, 13.3 inch
Warranty: 1 year
Battery life: 12 hours

### Dell XPS 15
Price: Rs. 159990
Specs: Intel i7, 16GB RAM, 512GB SSD, 15.6 inch
Warranty: 2 years
Battery life: 10 hours

### HP Spectre x360
Price: Rs. 139990
Specs: Intel i5, 8GB RAM, 512GB SSD, 14 inch
Warranty: 1 year
Battery life: 12 hours

## Gaming Laptops

### ASUS ROG Strix G15
Price: Rs. 104990
Specs: AMD Ryzen 7, 8GB RAM, 512GB SSD, RTX 3060
Warranty: 1 year
Battery life: 3 hours

### Lenovo Legion 5 Pro
Price: Rs. 94990
Specs: AMD Ryzen 5, 8GB RAM, 256GB SSD, RTX 3050
Warranty: 1 year
Battery life: 3 hours

### MSI Katana GF66
Price: Rs. 79990
Specs: Intel i5, 8GB RAM, 256GB SSD, RTX 3050
Warranty: 1 year
Battery life: 3 hours
"""
with open("data/laptop_wiki.md", "w") as f:
    f.write(wiki)
print("laptop_wiki.md created!")
print("\nAll 3 files ready in data/ folder!")