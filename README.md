# PyCash-Flow

A straightforward, locally-hosted desktop application for personal finance management (v1.0).

This project was developed with the primary goal of building a desktop application with a solid architectural foundation. It strictly separates business logic from the graphical interface, avoiding the tight coupling often found in standard desktop app development.

## 🛠️ Technologies & Patterns
* **Language:** Python
* **GUI Framework:** PySide6 (Qt)
* **Icons:** QtAwesome
* **Database:** SQLite (with parameterized queries to prevent SQL Injection)
* **Environment Management:** `python-dotenv`
* **Architecture:** MVC (Model-View-Controller)
* **Design Patterns:** Observer Pattern. The UI "listens" to the database; when data is inserted or removed, the backend emits a signal, and the view automatically repaints itself using a unidirectional data flow (Lifting State Up).

## 📌 Features
* Add, list, and remove detailed expenses.
* Automatic remaining balance calculation based on a fixed monthly income.
* Month/Year pagination system.
* Custom-built pie chart rendered from scratch using Qt's native `paintEvent`.

## 🚀 How to Run Locally

1. Clone the repository:
```bash
git clone [https://github.com/pemcauwilla/PyCash-Flow.git](https://github.com/pemcauwilla/PyCash-Flow.git)
cd PyCash-Flow
```

2. Install the required dependencies:
```bash
pip install PySide6 qtawesome python-dotenv
```

3. Create a `.env` file in the root directory. This will feed the database with your initial configuration (values are in cents, e.g., 500000 = $ 5,000.00):
```env
MONTHLY_INCOME=500000
TOTAL_BALANCE=1000000
```

4. Run the main file:
```bash
python main.py
```

## 🚧 Project Status
The main development of this MVP is complete. The core focus of this repository was to consolidate advanced software architecture studies (SOLID principles) applied to desktop development using the Qt framework.
