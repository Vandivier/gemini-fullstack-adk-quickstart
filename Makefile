.PHONY: help dev-frontend dev-backend dev debug-server debug-dev

help:
	@echo "Available commands:"
	@echo "  make dev-frontend    - Starts the frontend development server (Vite)"
	@echo "  make dev-backend     - Starts the backend development server (Uvicorn with reload)"
	@echo "  make dev             - Starts both frontend and backend development servers"
	@echo "  make debug-server    - Starts the custom backend server with full CORS control"
	@echo "  make debug-dev       - Starts both frontend and custom backend server together"

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server..."
	@cd backend && adk web

debug-server:
	@echo "Starting custom backend server with CORS debugging..."
	@cd backend/src && source ../.venv/bin/activate && python -m agent.server

debug-dev:
	@echo "Starting both frontend and custom backend development servers..."
	@make dev-frontend & make debug-server

# Run frontend and backend concurrently
dev:
	@echo "Starting both frontend and backend development servers..."
	@make dev-frontend & make dev-backend 