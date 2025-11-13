# Daily Roadmap: Wednesday, 12 November 2025

This roadmap outlines the plan for today's projects, with a primary focus on the Data Science Interview Question Database and the Weather Station.

## 📍 **Primary Objectives**

1.  **Data Science Interview Question Database:** Create a comprehensive database of potential interview questions for data science roles.
2.  **Weather Station:** Build a system to collect weather data, store it in a database, and stream it to a publicly accessible website.

---

## 🗺️ **Detailed Plan**

### 1. Data Science Interview Question Database

This project will be broken down into the following steps:

*   **1.1. Database & Table Creation:**
    *   **Technology:** We will use Python with its built-in `sqlite3` library for this project. It's a lightweight, file-based database that is easy to set up and use.
    *   **Database File:** A file named `interview_questions.db` will be created.
    *   **Table Schema:** A table named `questions` will be created with the following columns:
        *   `id`: (INTEGER, PRIMARY KEY) - Unique identifier for each question.
        *   `category`: (TEXT) - The category of the question (e.g., "Python", "Machine Learning", "Statistics").
        *   `question`: (TEXT) - The interview question itself.
        *   `difficulty`: (TEXT) - The difficulty of the question (e.g., "Easy", "Medium", "Hard").

*   **1.2. Data Population:**
    *   We will start by gathering a list of common data science interview questions from online resources.
    *   These questions will then be inserted into the `questions` table.

*   **1.3. Database Interaction:**
    *   A Python script will be created to interact with the database, allowing you to:
        *   Add new questions.
        *   View all questions.
        *   Filter questions by category or difficulty.

### 2. Weather Station with Database and Web Streaming

This project will be broken down into the following steps:

*   **2.1. Hardware Setup (Conceptual):**
    *   **Sensors:** We will assume the use of standard weather sensors (e.g., temperature, humidity, pressure). For the initial software development, we will simulate this data.
    *   **Microcontroller:** A Raspberry Pi or similar single-board computer will be the central processing unit.

*   **2.2. Database Setup:**
    *   **Technology:** We will use Python and `sqlite3` for this project as well.
    *   **Database File:** A file named `weather_data.db` will be created.
    *   **Table Schema:** A table named `readings` will be created with the following columns:
        *   `id`: (INTEGER, PRIMARY KEY) - Unique identifier for each reading.
        *   `timestamp`: (DATETIME) - The date and time of the reading.
        *   `temperature`: (REAL) - The temperature in Celsius.
        *   `humidity`: (REAL) - The humidity in percentage.
        *   `pressure`: (REAL) - The atmospheric pressure in hPa.

*   **2.3. Data Collection & Storage:**
    *   A Python script will be created to:
        *   Simulate sensor data.
        *   Insert the data into the `readings` table in the `weather_data.db` database.

*   **2.4. Web Streaming:**
    *   **Framework:** We will use a simple web framework like Flask (Python) to create a web server.
    *   **Website:** A simple HTML page will be created to display the latest weather data.
    *   **Data Streaming:** The Flask application will query the `weather_data.db` database and display the data on the webpage. The page will be set to auto-refresh to show the latest readings.

---

##  secondary objectives

*   **3. Transmit Book/Image:**
    *   This is a bit ambiguous. Could you please clarify what you mean by "transmit"? Do you want to upload it to a server, send it to someone, or something else?

*   **4. Watch Docker Videos:**
    *   I recommend watching videos from sources like "NetworkChuck" or other reputable tech educators on YouTube.

*   **5. Prepare Presentation:**
    *   After watching the Docker videos, you can create a short 5-10 minute presentation summarizing what you've learned.

*   **6. Test SpringerLink:**
    *   You can use the SpringerLink website to find a book and then use a PDF-to-text tool to extract the content. From there, you can generate questions.

*   **7. Watch NetworkChuck Docker:**
    *   This is a great resource for learning Docker.

---

I will now await your command to start with the first step of the plan.
