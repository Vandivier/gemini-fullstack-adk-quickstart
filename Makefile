.PHONY: help dev-frontend dev-backend dev debug-server debug-dev cleanup

help:
	@echo "Available commands:"
	@echo "  make dev-frontend    - Starts the frontend development server (Vite)"
	@echo "  make dev-backend     - Starts the backend development server (Uvicorn with reload)"
	@echo "  make dev             - Starts both frontend and backend development servers"
	@echo "  make debug-server    - Starts the custom backend server with full CORS control"
	@echo "  make debug-dev       - Starts both frontend and custom backend server together"
	@echo "  make cleanup         - Kills any lingering dev servers on common ports"

dev-frontend:
	@echo "Starting frontend development server..."
	@cd frontend && npm run dev

dev-backend:
	@echo "Starting backend development server..."
	@cd backend && adk web

dev:
	@echo "Starting both frontend and backend development servers..."
	@make dev-frontend & make dev-backend

debug-server:
	@echo "Starting custom backend server with CORS debugging..."
	@cd backend/src && source ../.venv/bin/activate && python -m agent.server

debug-dev:
	@echo "Starting both frontend and custom backend server..."
	@make dev-frontend & make debug-server

cleanup:
	@echo "Cleaning up lingering dev servers..."
	@echo "Killing uvicorn processes..."
	@pkill -f "uvicorn" || true
	@echo "Killing processes on ports 5173-5177 and 8000..."
	@lsof -ti:5173,5174,5175,5176,5177,8000 2>/dev/null | xargs kill -9 2>/dev/null || echo "No processes found on these ports"
	@echo "Cleanup complete!" 

instructions:
	@echo "Creating copilot instructions..."
	@cd backend/scripts && uv run create-copilot-instructions.py && cd ../../..