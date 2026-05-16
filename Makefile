.PHONY: backend-dev frontend-dev landing-dev test-backend docker-up docker-down diagrams

diagrams:
	node scripts/render-diagrams.mjs

backend-dev:
	cd backend && PYTHONPATH=src uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload

frontend-dev:
	cd frontend && npm run dev

landing-dev:
	cd landing && npm run dev

test-backend:
	cd backend && PYTHONPATH=src python -m pytest

docker-up:
	docker compose up --build

docker-down:
	docker compose down
