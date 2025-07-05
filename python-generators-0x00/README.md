# Python Generators and MySQL Integration

This project demonstrates how to use Python generators for efficient data handling with a MySQL database. It covers row streaming, batch processing, lazy pagination, and memory-efficient aggregation using a dataset of user records.

## 📁 Project Structure

```
python-generators-0x00/
├── seed.py                 # Sets up the MySQL DB, creates table, and inserts data
├── 0-stream_users.py       # Streams user data row-by-row using a generator
├── 1-batch_processing.py   # Processes user data in batches
├── 2-lazy_paginate.py      # Implements lazy pagination to simulate page-by-page loading
├── 4-stream_ages.py        # Streams user ages and computes the average using a generator
├── user_data.csv           # Sample data used for seeding
├── 0-main.py               # Driver for seeding the database
├── 1-main.py               # Test script for 0-stream_users
├── 2-main.py               # Test script for 1-batch_processing
├── 3-main.py               # Test script for 2-lazy_paginate
```

---

## 🗃️ Database Schema

**Database Name:** `ALX_prodev`

**Table:** `user_data`

* `user_id` (UUID, Primary Key, Indexed)
* `name` (VARCHAR, NOT NULL)
* `email` (VARCHAR, NOT NULL)
* `age` (DECIMAL, NOT NULL)

---

## ✅ Tasks Overview

### 0. Getting Started with Python Generators

**File:** `seed.py`

* Creates MySQL database and user\_data table.
* Loads data from `user_data.csv`.

### 1. Stream Users One-by-One

**File:** `0-stream_users.py`

* Implements `stream_users()` to yield each user record one at a time.

### 2. Batch Processing Large Data

**File:** `1-batch_processing.py`

* `stream_users_in_batches(batch_size)`: yields users in chunks.
* `batch_processing(batch_size)`: filters users older than 25.

### 3. Lazy Loading Paginated Data

**File:** `2-lazy_paginate.py`

* `lazy_pagination(page_size)`: uses `paginate_users()` to yield pages on-demand.

### 4. Memory-Efficient Aggregation

**File:** `4-stream_ages.py`

* `stream_user_ages()`: yields each user's age.
* `calculate_average_age()`: computes average without loading entire dataset into memory.

---

## ⚙️ Requirements

* Python 3.6+
* MySQL Server
* `mysql-connector-python` package

Install using:

```bash
pip install mysql-connector-python
```

---

## 💡 Tips

* Ensure your MySQL server is running.
* Update `seed.py` with your actual MySQL credentials.
* All scripts close connections/cursors to prevent resource leaks.

---

## 🧪 Testing

Run the seed script to initialize:

```bash
python3 0-main.py
```

Then test the individual modules:

```bash
python3 1-main.py
python3 2-main.py
python3 3-main.py
python3 4-stream_ages.py
```

---

## 📚 Author

**Nebyou Damtew**
**ALX Backend - Python**

---

For more details, refer to individual `.py` files. Contributions and improvements welcome!
