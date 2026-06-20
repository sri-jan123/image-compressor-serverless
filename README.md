# Image Compressor - Serverless

A **serverless image compression web application** built on Microsoft Azure. Users can upload images, which are automatically compressed using an Azure Blob Trigger function. Compression history is stored in Cosmos DB, and compressed images can be downloaded through secure SAS URLs.

## Architecture

<img width="1536" height="1024" alt="ChatGPT Image Jun 20, 2026, 11_47_35 PM" src="https://github.com/user-attachments/assets/c7eb8147-5ab4-4c58-9e55-6351da8f449a" />


---

## Features

- Upload images from the browser
- Automatic image compression using Pillow
- Blob Trigger for event-driven image processing
- Store compression history in Cosmos DB
- Download compressed images using SAS URLs
- Real-time status polling from the frontend
- Fully serverless architecture
- Frontend hosted on Azure Static Web Apps
- Backend hosted on Azure Functions

---

## Tech Stack

### Frontend

- React
- Vite
- Axios
- React Icons

### Backend

- Azure Functions (Python v2 Programming Model)
- Azure Blob Storage
- Azure Cosmos DB
- Pillow
- Azure Storage SDK
- Azure Cosmos SDK

---

## Azure Services Used

| Service | Purpose |
|---------|---------|
| Azure Static Web Apps | Host React frontend |
| Azure Functions | Serverless backend |
| Azure Blob Storage | Store original and compressed images |
| Azure Cosmos DB | Store compression history |

---

# Project Structure

```text
image_compressor/
│
├── frontend/
│   ├── src/
│   ├── .env.production
│   └── package.json
│
└── backend/
    ├── function_app.py
    ├── app_instance.py
    ├── host.json
    ├── requirements.txt
    │
    └── triggers/
        ├── upload_image.py
        ├── process_image.py
        ├── get_history.py
        ├── get_image_status.py
        └── download_image.py
```

---

# How It Works

### 1. Upload Image

- User uploads an image from the React frontend.
- `uploadImage` HTTP Trigger stores the image in the **raw-images** container.

---

### 2. Blob Trigger Executes

The `processImage` Blob Trigger automatically runs whenever a new image is uploaded.

It:

- Downloads the image
- Compresses it using Pillow
- Uploads the compressed image to `compressed-images`
- Stores metadata in Cosmos DB

---

### 3. Poll Image Status

The frontend periodically calls:

```text
GET /api/getImageStatus
```

to check whether compression has completed.

---

### 4. Download Compressed Image

The frontend calls:

```text
GET /api/downloadImage
```

The backend generates a SAS URL and returns it.

The user downloads the image securely without exposing storage keys.

---

# Backend Setup

## 1. Clone Repository

```bash
git clone <repository-url>

cd image_compressor/backend
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure `local.settings.json`

Create:

```json
{
  "IsEncrypted": false,
  "Values": {

    "AzureWebJobsStorage":
    "<storage_connection_string>",

    "FUNCTIONS_WORKER_RUNTIME":
    "python",

    "CosmosDBConnectionString":
    "<cosmos_connection_string>",

    "StorageAccountKey":
    "<storage_account_key>"
  }
}
```

---

## 5. Run Azure Functions Locally

```bash
func start
```

The APIs become available at:

```text
http://localhost:7071/api
```

---

# Frontend Setup

## 1. Navigate to Frontend

```bash
cd frontend
```

---

## 2. Install Dependencies

```bash
npm install
```

---

## 3. Create `.env`

For local development:

```env
VITE_API_URL=http://localhost:7071/api
```

For production:

Create:

```text
frontend/.env.production
```

Add:

```env
VITE_API_URL=https://<your-function-app>.azurewebsites.net/api
```

Example:

```env
VITE_API_URL=https://imgcompressorfunctions123.azurewebsites.net/api
```

---

## 4. Run Frontend

```bash
npm run dev
```

---

## 5. Build Frontend

```bash
npm run build
```

---

# Deploy Backend to Azure Functions

Login:

```bash
az login
```

Publish:

```bash
func azure functionapp publish <function-app-name>
```

Example:

```bash
func azure functionapp publish imgcompressorfunctions123
```

This command:

- Packages the code
- Performs a remote Oryx build
- Installs dependencies
- Uploads the application
- Syncs triggers automatically

---

# Deploy Frontend to Azure Static Web Apps

1. Push the project to GitHub.

2. Create an Azure Static Web App.

3. Configure:

```text
App location: ./frontend

API location:

Output location: dist
```

4. Azure automatically creates a GitHub Actions workflow.

5. Every push to the `main` branch automatically:

- Builds the React app
- Deploys to Azure Static Web Apps

No manual deployment is required afterwards.

---

# Environment Variables

## Azure Functions

Add the following Application Settings:

```text
AzureWebJobsStorage

FUNCTIONS_WORKER_RUNTIME

CosmosDBConnectionString

StorageAccountKey

APPLICATIONINSIGHTS_CONNECTION_STRING
```

---

## Azure Static Web Apps

Add:

```text
VITE_API_URL
```

Example:

```text
https://imgcompressorfunctions123.azurewebsites.net/api
```

---

# Event-Driven Architecture

This project follows an **event-driven architecture**.

When a user uploads an image:

1. Image is stored in Blob Storage.
2. Blob Storage emits an event.
3. Blob Trigger Function executes automatically.
4. The image is compressed.
5. Metadata is stored in Cosmos DB.
6. Frontend polls the status and displays the result.

No servers need to be managed manually.

---

# Live Demo
🌐 https://ambitious-desert-00c731c00.7.azurestaticapps.net/

# Author

**Srijan Mani Tripathi**
