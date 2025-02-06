# API Documentation

## Authentication

All API endpoints require authentication using JWT (JSON Web Token). To obtain a token:

```http
POST /api/token/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

Response:
```json
{
    "access": "your.access.token",
    "refresh": "your.refresh.token"
}
```

Include the access token in all subsequent requests:
```http
Authorization: Bearer your.access.token
```

## Categories

### List Categories
```http
GET /api/categories/
```

Response:
```json
[
    {
        "id": 1,
        "name": "Category Name",
        "description": "Category Description",
        "created_at": "2024-02-04T10:00:00Z",
        "updated_at": "2024-02-04T10:00:00Z"
    }
]
```

### Create Category
```http
POST /api/categories/
Content-Type: application/json

{
    "name": "New Category",
    "description": "Category Description"
}
```

## Products

### List Products
```http
GET /api/products/
```

Response:
```json
[
    {
        "id": 1,
        "name": "Product Name",
        "category": {
            "id": 1,
            "name": "Category Name"
        },
        "description": "Product Description",
        "specifications": {
            "potencia": 100,
            "peso": 5.5,
            "dimensiones": "30x20x10",
            "voltaje": 220,
            "frecuencia": 50
        },
        "created_at": "2024-02-04T10:00:00Z",
        "updated_at": "2024-02-04T10:00:00Z"
    }
]
```

### Create Product
```http
POST /api/products/
Content-Type: application/json

{
    "name": "New Product",
    "category": 1,
    "description": "Product Description",
    "specifications": {
        "potencia": 100,
        "peso": 5.5,
        "dimensiones": "30x20x10",
        "voltaje": 220,
        "frecuencia": 50
    }
}
```

## Imports

### List Imports
```http
GET /api/imports/
```

Response:
```json
[
    {
        "id": 1,
        "reference_number": "IMP-2024-001",
        "status": "pending",
        "import_date": "2024-02-04",
        "created_by": {
            "id": 1,
            "username": "admin"
        },
        "documents": null,
        "notes": "",
        "items": [
            {
                "id": 1,
                "product": {
                    "id": 1,
                    "name": "Product Name"
                },
                "expected_quantity": 5,
                "received_quantity": 3
            }
        ],
        "created_at": "2024-02-04T10:00:00Z",
        "updated_at": "2024-02-04T10:00:00Z"
    }
]
```

### Create Import
```http
POST /api/imports/
Content-Type: application/json

{
    "reference_number": "IMP-2024-001",
    "import_date": "2024-02-04",
    "notes": "Optional notes"
}
```

### Add Import Item
```http
POST /api/import-items/
Content-Type: application/json

{
    "import_record": 1,
    "product": 1,
    "expected_quantity": 5
}
```

## Product Units

### List Product Units
```http
GET /api/product-units/
```

Response:
```json
[
    {
        "id": 1,
        "product": {
            "id": 1,
            "name": "Product Name"
        },
        "import_item": {
            "id": 1,
            "import_record": "IMP-2024-001"
        },
        "serial_number": "LPX1-2024-001",
        "status": "available",
        "notes": "",
        "created_at": "2024-02-04T10:00:00Z",
        "updated_at": "2024-02-04T10:00:00Z"
    }
]
```

### Create Product Unit
```http
POST /api/product-units/
Content-Type: application/json

{
    "product": 1,
    "import_item": 1,
    "serial_number": "LPX1-2024-001",
    "status": "available",
    "notes": "Optional notes"
}
```

## PDF Generation

### Generate Verification PDF
```http
POST /api/imports/{import_id}/generate-verification-pdf/
```

Response:
```json
{
    "task_id": "task-uuid",
    "status": "processing"
}
```

### Generate Technical Sheet PDF
```http
POST /api/product-units/{unit_id}/generate-technical-sheet-pdf/
```

Response:
```json
{
    "task_id": "task-uuid",
    "status": "processing"
}
```

### Check PDF Generation Status
```http
GET /api/tasks/{task_id}/status/
```

Response:
```json
{
    "task_id": "task-uuid",
    "status": "completed",
    "result": {
        "pdf_url": "/media/pdfs/verification_IMP-2024-001_20240204_123456.pdf"
    }
}
```

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
    "error": "Validation error message"
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```
