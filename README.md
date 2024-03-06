# Scheduling

Brief description of your project.

## Prerequisites

- Python (version 3.8)
- Virtualenv (optional but recommended)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ahsanfurqan/scheduler.git
cd scheduler

## Optional for the virtual env
python -m venv venv

##On Windows 
venv\Scripts\activate

##ON Linux
source venv/bin/activate

## Install Dependencies
pip install -r requirements.txt

## Migrate Database
python manage.py migrate

## Create Super User
python manage.py createsuperuser

## Run Server
python manage.py runserver


