# 🗺️ Shortest Path Finder using A\* Algorithm

This is a Flask-based web application that calculates and displays the **shortest path** between two selected locations on a map (Bejaia). The app is built using **Flask, Folium, OSMnx, and NetworkX**, and implements the **A\* algorithm manually**.

## 🚀 Features

✅ Find the shortest path between two points using **A\*** (A-star)  
✅ Interactive **clickable map** to select start and destination  
✅ Uses **real-world road networks** from OpenStreetMap (OSM)

---

## 🛠️ Installation

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/cynhlfn/Shortest_path_AI_assignment01.git
cd Shortest_path_AI_assignment01
```

### **2️⃣ Create and Activate a Virtual Environment**

✅ For Linux/macOS:

```sh
python3 -m venv venv
source venv/bin/activate
```

✅ For Windows (Command Prompt):

```sh
python -m venv venv
venv\Scripts\activate
```

### **3️⃣ Install Dependencies**

```sh
pip install -r requirements.txt
```

### 📌 If requirements.txt is missing, create it using:

```sh
pip freeze > requirements.txt
```

### 4️⃣ Run the Application

```sh
python app.py
```

### OR (if using Flask's built-in CLI):

```sh
flask run
```

### Then, open your browser and go to:

🔗 http://127.0.0.1:5000

### 📂 Project Structure

```
Shortest_path_AI_assignment01/
│── templates/
│ ├── selection_map.html
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
└── venv/

```
