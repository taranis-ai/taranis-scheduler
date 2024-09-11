# Scheduler Service

This service provides a scheduling system that interacts with a PostgreSQL backend to manage tasks. It supports adding, deleting, and viewing scheduled jobs via a Flask web interface, utilizing **HTMX** for dynamic updates. The service also includes special handling for **debug mode**, which displays a warning and disables job modification capabilities in production.

## Features

- **Task Scheduling**: View scheduled tasks with options to add and delete jobs in debug mode.
- **HTMX Integration**: Dynamic updates to the job list without full page reloads.
- **Flask Web Interface**: Clean and responsive user interface with job management.
- **Debug Mode Handling**: Debug mode displays a warning and disables modification actions (add/delete).
- **Tailwind CSS**: Modern and responsive UI styling.

---

## Installation

It's recommended to use a uv to setup an virtual environment.

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
```

Source venv and install dependencies

```bash
source .venv/bin/activate
uv pip install -Ue .[dev]
```

## Development Setup

### 1. Download and Setup Tailwind CSS

We use Tailwind CSS for styling the frontend. First, download the Tailwind CSS CLI tool:

```bash
curl -sLo tailwindcss https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64
chmod +x tailwindcss
```

### 2. Start Tailwind CSS in Watch Mode

Run **Tailwind CSS** in watch mode to automatically build the CSS files as you modify the styles:

```bash
./tailwindcss -i scheduler/static/css/input.css -o scheduler/static/css/tailwind.css --watch
```

This will generate the `tailwind.css` file based on the input CSS and keep it updated as you develop.

### 3. Start Flask

Run the Flask development server:

```bash
flask run
```

This will start the Flask server and run the scheduler service at `http://localhost:5000`.

---

## Usage

The job list shows all scheduled jobs, including their arguments, next run times, and triggers.


### Debug Mode


### Adding & Deleting Jobs

In debug mode, the interface allows you to add jobs by specifying the job name and interval (in seconds). These jobs are then stored in the PostgreSQL job store and managed by the APScheduler.
Similarly, in debug mode, you can delete jobs from the interface using the delete buttons next to each job in the list.

When the service is running in **debug mode**, a warning banner will be displayed at the top of the page, and you will have access to the job add/delete functionality.

In production (when debug mode is off), job modification functionality will be hidden, and users cannot modify the schedule.

---

## Configuration

Configuration is handled via environment variables.

### Required Environment Variables

- **`SQLALCHEMY_DATABASE_URI`**: The connection string to your PostgreSQL database.
  - Example: `postgresql://username:password@localhost:5432/your_database`
  
- **`FLASK_ENV`**: Set to `development` or `production`.
  - Example: `export FLASK_ENV=development`

- **`FLASK_APP`**: Set this to the name of your app (e.g., `scheduler`).
  - Example: `export FLASK_APP=scheduler`

- **`JWT_SECRET_KEY`**: The secret key for signing JWT tokens.
  - Example: `export JWT_SECRET_KEY=your-secret-key`
