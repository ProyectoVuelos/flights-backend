# Flights Backend

This project is the backend service for a flight tracking or booking application. It provides a RESTful API to interact with flight data and user information, powered by [Supabase](https://supabase.com).

## ✨ Features

-   RESTful API for flight management.
-   Integration with Supabase for database and authentication.
-   Type-safe configuration management using Pydantic.
-   Asynchronous from the ground up, likely with FastAPI.

## 🛠️ Tech Stack

-   **Language**: Python 3.8+
-   **Framework**: FastAPI
-   **Server**: Uvicorn
-   **Backend as a Service (BaaS)**: [Supabase](https://supabase.com)
-   **Configuration**: [Pydantic](https://docs.pydantic.dev/)

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.8+
-   `pip` and `venv`
-   A Supabase account and an active project.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd flights-backend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    *(You should have a `requirements.txt` file in your project root)*
    ```bash
    make install
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root. You can copy the example structure below.

    ```sh
    # .env file
    
    # Supabase Credentials (Required)
    SUPABASE_URL="your_supabase_project_url"
    SUPABASE_KEY="your_supabase_anon_key"

    # Uvicorn Server Settings (Optional)
    UVICORN_HOST="0.0.0.0"
    UVICORN_PORT=8000
    ```
    Fill in the `SUPABASE_URL` and `SUPABASE_KEY` with your actual Supabase project credentials.

### Running the Application

To start the development server, run the following command from the project root:

```bash
make run
```

This command assumes your FastAPI application instance is named `app` and is located in `api/main.py`. The server will use the host and port defined in your `.env` file or the defaults (`0.0.0.0:8000`).

The API will be accessible at `http://127.0.0.1:8000`, and interactive documentation (Swagger UI) will be available at `http://127.0.0.1:8000/docs`.

## ⚙️ Configuration

The application's configuration is managed via environment variables, as defined in `api/utils/env_manager.py`.

| Variable       | Description                                          | Required | Default   |
| -------------- | ---------------------------------------------------- | :------: | --------- |
| `SUPABASE_URL` | The URL for your Supabase project.                   | **Yes**  | `N/A`     |
| `SUPABASE_KEY` | The public (anon) API key for your Supabase project. | **Yes**  | `N/A`     |
| `UVICORN_HOST` | The host for the Uvicorn server.                     |    No    | `0.0.0.0` |
| `UVICORN_PORT` | The port for the Uvicorn server.                     |    No    | `8000`    |

## 📄 License

This project is licensed under the MIT License.
