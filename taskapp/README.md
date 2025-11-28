# Task App

A modern, responsive task management application built with Flask (Python backend), HTML, CSS, and JavaScript.

## Features

- Create, view, update, and delete tasks
- Mark tasks as complete/incomplete
- Add task descriptions
- Persistent storage using JSON
- Beautiful, modern UI with gradient design
- Fully responsive design

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open your browser and navigate to:
```
http://localhost:5000
```

## Project Structure

```
TASKAPP/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── tasks.json            # Task storage (created automatically)
├── README.md             # This file
│
├── templates/
│   └── index.html        # Main HTML template
│
└── static/
    ├── style.css         # Application styles
    └── script.js         # Client-side JavaScript
```

## Usage

1. **Add a Task**: Enter a task title and optional description, then click "Add Task"
2. **Complete a Task**: Click the "Complete" button next to any pending task
3. **Mark Incomplete**: Click "Mark Incomplete" on completed tasks
4. **Delete a Task**: Click the "Delete" button to remove a task

## API Endpoints

- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: JSON file-based storage
- **Design**: Modern gradient UI with responsive design

## License

This project is open source and available for personal and commercial use.


