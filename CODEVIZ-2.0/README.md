# CodeViz 2.0

AI-powered interactive learning platform for Computer Science and Programming.

## Project Structure

This project follows a clean, modular architecture separated into frontend, backend, and documentation.

### 📂 /backend
*Python (FastAPI) application handling API requests, LLM integration, and database operations.*

- **app/core**: Configuration, settings, and core application logic.
- **app/api**: REST API endpoints and route handlers.
- **app/services**: Business logic layer (e.g., LLM interaction, RAG processing).
- **app/schemas**: Pydantic models for data validation and serialization.
- **app/models**: Database models.
- **tests**: Unit and integration tests.

### 📂 /frontend
*React + TypeScript application for the user interface.*

- **src/components/ui**: Reusable, generic UI components (buttons, input fields).
- **src/components/features**: Complex, business-logic-aware components (Editor, Visualizer).
- **src/pages**: Full page layouts used by the router.
- **src/hooks**: Custom React hooks for reusable logic.
- **src/services**: API interaction layer.
- **src/types**: TypeScript type definitions.

### 📂 /docs
*Project documentation and guides.*

- **architecture**: High-level design documents and diagrams.
- **api**: API specifications and usage guides.
- **setup**: Instructions for setting up the development environment.

## Getting Started

*(Instructions to be added)*
