# Reliability Analysis Dashboard

A **web-based reliability monitoring and maintenance management system** built using **Flask, JavaScript, and TailwindCSS**.
The system helps monitor equipment reliability metrics, analyze failures, manage alerts, and schedule preventive maintenance.

---

## Project Overview

The ** Reliability Analysis Dashboard** is designed to simulate an industrial reliability dashboard used in manufacturing or operations environments.

It allows users to:

* Monitor key reliability metrics such as **MTBF, MTTR, and Availability**
* Track equipment operational status
* View failure alerts and system issues
* Schedule maintenance activities
* Visualize maintenance schedules through a calendar
* Manage equipment maintenance records stored in **CSV-based data storage**

This project demonstrates **full-stack development concepts** and basic **DevOps-style system design**.

---

## Features

### Dashboard

* Displays system reliability metrics:

  * MTBF (Mean Time Between Failures)
  * MTTR (Mean Time To Repair)
  * Availability percentage
* Shows active alerts
* Displays equipment operational status

### Equipment Monitoring

* Tracks equipment health and operational status
* Displays last failure time and last update time

### Failure Analysis

* Provides failure-related insights
* Helps identify potential reliability issues

### Maintenance Management

* Schedule maintenance activities
* View upcoming and recent maintenance
* Calendar overview of scheduled maintenance
* Maintenance records saved to CSV file

### Alerts System

* Displays active system alerts
* Helps detect critical equipment failures

---

## Technology Stack

### Backend

* Python
* Flask

### Frontend

* HTML5
* TailwindCSS
* JavaScript

### Data Storage

* CSV files

### UI Libraries

* Lucide Icons
* TailwindCSS

---

## Project Structure

```
 Reliability Analysis Dashboard/
│
├── app.py
│
├── templates/
│   ├── dashboard.html
│   ├── equipment.html
│   ├── analysis.html
│   └── maintenance.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── dashboard.js
│       └── components.js
│
├── data/
│   ├── equipment.csv
│   ├── maintenance.csv
│   └── failures.csv
│
└── README.md
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/cleonamonteiro1604/Reliability-Analysis-Dashboard.git
cd smart-reliability-system
```

### 2. Install dependencies

```
pip install flask
```

### 3. Run the application

```
python app.py
```

### 4. Open in browser

```
http://127.0.0.1:5000
```

---

## API Endpoints

| Endpoint           | Method | Description                      |
| ------------------ | ------ | -------------------------------- |
| `/api/metrics`     | GET    | Returns MTBF, MTTR, Availability |
| `/api/equipment`   | GET    | Returns equipment status         |
| `/api/alerts`      | GET    | Returns active alerts            |
| `/api/maintenance` | GET    | Returns maintenance schedule     |
| `/api/schedule`    | POST   | Add new maintenance schedule     |

---

## Screens Included

* Dashboard Overview
* Equipment Monitoring
* Failure Analysis
* Maintenance Scheduling

---

## Future Improvements

* Database integration (PostgreSQL / MySQL)
* Authentication system
* Real-time alerts
* Advanced reliability analytics
* Predictive maintenance using machine learning
* Docker containerization
* CI/CD pipeline integration

---

## Learning Objectives

This project demonstrates:

* Full stack web development
* REST API design
* Frontend and backend integration
* Reliability engineering concepts
* Maintenance scheduling workflows

---

## Author

Cleona Jyothsna Monteiro

---

## License

This project is for **educational and portfolio purposes**.
