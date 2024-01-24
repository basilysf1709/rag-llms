
# Target to run your script
text:
	@echo "Running script..."
	@sleep 1
	@echo "Loading Environment Variables..."
	@sleep 1
	@(export $$(grep -v '^#' .env | xargs) && python3 src/talkToTextFile.py)

# Target to run your script for llama2 model
llama2:
	@echo "Running script..."
	@sleep 1
	@echo "Loading Environment Variables..."
	@sleep 1
	@(export $$(grep -v '^#' .os.env | xargs) && python3 src/openSourceModel.py)

.PHONY: run
