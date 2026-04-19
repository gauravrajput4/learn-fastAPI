# What is an API?

APIs (Application Programming Interfaces) are mechanisms that enable two software components—such as the frontend and backend of an application—to communicate with each other using a defined set of rules, protocols, and data formats.

---

## Why do we need APIs?

APIs address several critical needs in modern software development and integration:

- **Interoperability**:  
  They allow different software systems, often built with diverse technologies and programming languages, to communicate and work together seamlessly.

- **Modularity and Reusability**:  
  APIs enable developers to build modular applications. Instead of reinventing the wheel, developers can use existing API functionalities (e.g., payment processing, mapping services, social media integration) as building blocks.

- **Abstraction**:  
  APIs hide the complexity of underlying systems. Developers don’t need to understand internal workings—just the API interface.

- **Innovation**:  
  APIs allow third-party developers to build new applications using existing services.

- **Efficiency**:  
  Faster development and integration reduce time to market.

- **Scalability**:  
  APIs help break systems into smaller, manageable services (microservices architecture).

- **Data Exchange**:  
  APIs enable secure and efficient data sharing between applications.

---

# FastAPI

FastAPI is a modern, high-performance web framework for building APIs with Python.

It is built with:

- **Starlette** → Handles request and response (ASGI framework)
- **Pydantic** → Handles data validation and type checking

---

## Philosophy of FastAPI

- High performance
- Fast to run
- Fast to code

---

### Old Mechanism
Client → Web Server → SGI (Server Gateway Interface) → API Code


---

### In Flask
Client → Web Server (Uvicorn) → ASGI (Starlette) → API Code


- **WSGI Limitation**:  
  Synchronous and blocking → slower performance and scalability issues.

---

### In FastAPI
Client → Web Server (Uvicorn) → ASGI (Starlette) → API Code

- Uses **async/await**
- Supports asynchronous programming
- Much faster and scalable

---

## Why FastAPI is fast to code?

- Automatic input validation (via Pydantic)
- Auto-generated interactive documentation (Swagger UI & ReDoc)
- Easy integration with modern tools:
  - Machine Learning / Deep Learning libraries
  - OAuth, JWT authentication
  - SQLAlchemy (database)
  - Docker, Kubernetes

# HTTP Methods in FastAPI

FastAPI uses standard HTTP methods to perform operations on resources. These methods define the type of action you want to perform.

---

## Common HTTP Methods

### 1. GET

- **Purpose**: Retrieve data from the server  
- **Usage**: Fetch resources (no data modification)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### 2. POST

- **Purpose**: Send data to the server
- **Usage**: Create a new resource

```python
from fastapi import FastAPI

app = FastAPI()

@app.post("/items/")
def create_item(item: dict):
    return {"item": item}
```

### 3. PUT

- **Purpose**: Update an existing resource (complete update)
- **Usage**: Replace entire data

```python
from fastapi import FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    return {"item_id": item_id, "updated_item": item}
```
### 4. PATCH

- **Purpose**: Partial update of a resource
- **Usage**: Modify specific fields only

```python
from fastapi import FastAPI

app = FastAPI()

@app.patch("/items/{item_id}")
def partial_update(item_id: int, item: dict):
    return {"item_id": item_id, "updated_fields": item}
```

### 5. DELETE

- **Purpose**: Remove a resource
- **Usage**: Delete data

```python
from fastapi import FastAPI

app = FastAPI()

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

# 🔗 Path Parameters in FastAPI

Path parameters allow you to pass dynamic values in the URL. These values are used to identify specific resources.

---

## 📌 What are Path Parameters?

Path parameters are parts of the URL that are variable.

👉 Example:
/items/1
/items/100


Here, `1` and `100` are path parameters.

---

## 💻 Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

# 🔗 Path function in FastAPI
The Path() function in FastAPI is used to provide metadata, validation rules and documentation hints for path parameters in your API endpoints.
* Title
* Description
* Example
* ge, gt, le, lt
* Min_length
* Max_length
* regex
```Python
from  fastapi import FastAPI,Path
app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int=Path(...,description='ID of the item in the DB',example='1234')):
    return {"item_id": item_id}
```

# HTTP status code
HTTP status code are 3- digit numbers returned by a web server (like FastAPI) to indicate the result of a client's request (like from a browser or API consumer).

They help the client(browser, frontend, mobile app, etc) understand.
* whether the request was successful.
* whether something went wrong.
* and what kind of issues occurred (if any).
## 📌 Categories of Status Codes

| Range | Category        | Meaning                                               |
|-------|----------------|-------------------------------------------------------|
| 1xx   | Informational  | Request received, processing                          |
| 2xx   | Success        | The request was successfully received and processed   |
| 3xx   | Redirection    | Further action needs to be taken (e.g. redirect)      |
| 4xx   | Client Error   | Something went wrong with the request from the client |
| 5xx   | Server Error   | Something went wrong on the server side.              |

## 📊 Common HTTP Status Codes

| Code | Status Name              | Description                              |
|------|--------------------------|------------------------------------------|
| 200  | OK                       | Request successful                       |
| 201  | Created                  | Resource created successfully            |
| 204  | No Content               | Success, but no response body            |
| 400  | Bad Request              | Invalid request from client              |
| 401  | Unauthorized             | Authentication required                  |
| 403  | Forbidden                | Access denied                            |
| 404  | Not Found                | Resource not found                       |
| 422  | Unprocessable Entity     | Validation error (FastAPI specific)      |
| 500  | Internal Server Error    | Server-side error                        |
| 503  | Service Unavailable      | Server temporarily unavailable           |

## HTTPException
HTTPException is a special built-in exception in FastAPI used to return custom HTTP error responses when something goes wrong in your API.

Instead of returning a normal json or crashing the server . You can gracefully raise an error with:
* a proper HTTP code (like 404, 400, 403, etc.)
* a custom error message.
* (optional) extra headers.

# Query Parameter
Query Parameters are optional key-value pairs appended to the end of a URL used to pass additional data to the server in an HTTP request.They are typically employed for operations like filtering sorting, searching and pagination without altering the endpoint path itself.

e.g. :- /patient?city=Kanpur&sort_by=age

* The ? marks the start of query parameters.
* Each parameter is a key value pair key=value
* Multiple parameters are separated by &

In this case:
* city=Kanpur is a query parameter for filtering
* sort_by=age is a query parameter for sorting.

