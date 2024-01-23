all: run

# Target to run your script
run:
	@echo "Running script..."
	@sleep 1
	@echo "Loading Environment Variables..."
	@sleep 1
	@(export $$(grep -v '^#' .env | xargs) && python3 src/starter.py)

.PHONY: run
