
# 📡 NetSage: Visualize Your Digital Footprints

**NetSage** is an elegant and interactive web app built with **Streamlit** and **Pandas** to help you analyze and visualize your internet usage data. Whether you're monitoring daily consumption, spotting monthly trends, or summarizing yearly activity — NetSage turns raw CSV logs into meaningful insights.



## ✨ Features

- 📁 Automatically loads data from `usage/you_usage.csv` if available
- 🖼️ Upload your own usage CSV if default file is not found
- 📅 Filter data by **month** and **year**
- 📏 Select display units: **MB**, **GB**, or **TB**
- 📊 Daily usage breakdown in **tabular** and **graphical** formats
- 🧮 Summary statistics:
  - Monthly total usage
  - Average daily usage (in month)
  - Yearly total usage
  - Average monthly usage (in year)



## 📂 CSV Format

Your CSV file should have the following columns:

```
Ip-Mac,Start Date,Start Time,End Date,End Time,MB Consumption
```

📝 Example:
```
A1:B2:C3:D4:E5,2025-04-01,09:00,2025-04-01,10:00,150.5
A1:B2:C3:D4:E5,2025-04-01,11:00,2025-04-01,12:00,300.75
```

- Place your file at: `usage/you_usage.csv`  
- Or upload it manually when prompted

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/netsage.git
cd netsage
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 📸 Screenshots

> _Add screenshots here to showcase your dashboard in action_

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) – UI framework
- [Pandas](https://pandas.pydata.org/) – Data processing
- [Matplotlib](https://matplotlib.org/) – Visualizations

---

## 🧊 License

MIT License © 2025 Your Name  
_“Measure what you consume — visualize what you control.”_

---
