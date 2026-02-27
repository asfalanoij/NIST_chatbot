.PHONY: setup start-backend start-frontend ingest clean test-backend test-frontend test qa scan maturity auth loadtest rag-eval export-check cicd

setup:
	@echo "Setting up Backend..."
	cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Setting up Frontend..."
	cd frontend && npm install

start-backend:
	@echo "Starting Backend on port 5050..."
	cd backend && . venv/bin/activate && python app.py

start-frontend:
	@echo "Starting Frontend on port 5173..."
	cd frontend && npm run dev

ingest:
	@echo "Ingesting documents from docs/..."
	cd backend && . venv/bin/activate && python ingest.py

# --- Testing ---
test-backend:
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && python -m pytest tests/ -v

test-frontend:
	@echo "Running frontend build check..."
	cd frontend && npm run build

test: test-backend test-frontend
	@echo "All tests passed."

# --- Build Agents ---
qa:
	@./agenticAI_skills/antigravity.sh qa inspect

scan:
	@./agenticAI_skills/antigravity.sh devsecops scan

maturity:
	@./agenticAI_skills/antigravity.sh pm maturity

auth:
	@./agenticAI_skills/antigravity.sh api-auth verify

loadtest:
	@./agenticAI_skills/antigravity.sh api-loadtest stress

rag-eval:
	@./agenticAI_skills/antigravity.sh rag-evaluator evaluate

export-check:
	@./agenticAI_skills/antigravity.sh chat-export check

cicd:
	@./agenticAI_skills/antigravity.sh cicd check

# --- Cleanup ---
clean:
	rm -rf backend/venv
	rm -rf backend/__pycache__
	rm -rf frontend/node_modules
