# ✈️ PennyPath - Smart Flight Route Optimizer

PennyPath is a Flask-based web app that helps you find the best air routes between airports across India — optimizing by fare or duration. It simulates real-world air travel logic with route calculations, stop compensation, and a dynamic, user-friendly interface.

---


## 🌟 Features

- 🔍 Find flight routes between any two Indian airports
- 💸 Optimize results by:
  - Fare (cheapest route)
  - Duration (fastest route)
- 🔁 Choose number of allowed stops (0, 1, or 2)
- 🧠 Smart fare compensation for layovers (indirect routes get discounts)
- ✨ Direct + Indirect route separation
- 🖱️ Frontend validations to improve UX
- 📈 Scalable for ML/NLP features like:
  - Smart suggestions
  - Natural language input
  - Anomaly detection in fare
  - Personalized recommendations

---

## 🛠️ Tech Stack

| Layer     | Tech Used                      |
|-----------|-------------------------------|
| Backend   | Python, Flask, NetworkX        |
| Frontend  | HTML, CSS, JavaScript          |
| Geo       | geopy (for distance calculation) |
| Graph     | Directed Graph for route logic |
| ML Ready  | AI/ML extendable (Reinforcement, NLP, Clustering)
