import os.path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    get_response_synthesizer
)

class Chatbot:
    def __init__(self, persist_dir):
        self.persist_dir = persist_dir
        self.index = None
        self._initialize_index()

    def _initialize_index(self):
        if not os.path.exists(self.persist_dir):
            documents = SimpleDirectoryReader("data").load_data()
            # index data
            self.index = VectorStoreIndex.from_documents(documents)
            # persist storage
            self.index.storage_context.persist(persist_dir=self.persist_dir)
        else:
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
            self.index = load_index_from_storage(storage_context)

    def query_index(self, query):
        if self.index:
            query_engine = self.index.as_query_engine(streaming=True)
            streaming_response = query_engine.query(query)
            print("\033[91mAI: ", end="")
            print("\033[0m", end="") 
            streaming_response.print_response_stream()
        else:
            return "Index not initialized properly."

    def handle_user_input(self, user_input):
        self.query_index(user_input)

# Usage
persist_dir = "./storage"
chatbot = Chatbot(persist_dir)

while True:
    print("\n\033[91mAI:\033[0m [suggestion] Enter your question (type 'exit' to stop)")
    user_query = input("\033[92mUser: \033[0m")
    if user_query.lower() == "exit":
        print("\n\033[91mAI: Exiting chatbot.\033[0m")  # Red color for AI
        break
    chatbot.handle_user_input(user_query)
