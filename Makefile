
# Target to run your script
gpt3:
	@echo "Running script..."
	@sleep 1
	@echo "Loading Environment Variables..."
	@sleep 1
	@(export $$(grep -v '^#' .env | xargs) && python3 src/gpt3-5.py)

# Target to run your script for llama2 model
llama2:
	@echo "Running script..."
	@sleep 1
	@echo "Loading Environment Variables..."
	@sleep 1
	@(export $$(grep -v '^#' .os.env | xargs) && python3 src/llama2.py)

.PHONY: run
