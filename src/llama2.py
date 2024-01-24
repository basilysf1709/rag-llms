import os.path
from llama_index import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext
)
from llama_index.llms import Replicate
from llama_index.llms.llama_utils import (
    messages_to_prompt,
    completion_to_prompt,
)

class Chatbot:
    def __init__(self, persist_dir):
        self.persist_dir = persist_dir
        self.index = None
        self.ctx = None
        self._initialize_index()

    # initialize index, load data, select llm using replicate
    def _initialize_index(self):
        # load the 13B llama2 from replicate, uses replicate's compute to run an open source model
        LLAMA_13B_V2_CHAT = "a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5"
        llm = Replicate(
            model=LLAMA_13B_V2_CHAT,
            temperature=0.01,
            context_window=4096,
            completion_to_prompt=self.custom_completion_to_prompt,
            messages_to_prompt=messages_to_prompt,
        )
        # declare the context for llm used and embed_model (here the embed model is local)
        self.ctx = ServiceContext.from_defaults(llm=llm, embed_model="local")
        if not os.path.exists(self.persist_dir):
            # load data from the data folder
            documents = SimpleDirectoryReader("data").load_data()
            # create vector embeddings of the data loaded
            self.index = VectorStoreIndex.from_documents(documents, service_context=self.ctx)
            # persist that data in vectordb or just locally, since use case is small
            self.index.storage_context.persist(persist_dir=self.persist_dir)
        else:
            # load the vector embeddings from persisted storage
            storage_context = StorageContext.from_defaults(persist_dir=self.persist_dir)
            self.index = load_index_from_storage(storage_context, service_context=self.ctx)

    # run the query engine to get a streamed response
    def query_index(self, prompt):
        if self.index:
            # query response
            query_engine = self.index.as_query_engine(service_context=self.ctx, streaming=True)
            streaming_response = query_engine.query(prompt)
            print("\033[91mAI: ", end="")
            print("\033[0m", end="") 
            # print the streamed response
            streaming_response.print_response_stream()
        else:
            return "Index not initialized properly."

    # handle incoming user input
    def handle_user_input(self, user_input):
        self.query_index(user_input)
    
    # custom completion to prompt with system_prompt
    def custom_completion_to_prompt(self, completion: str) -> str:
        return completion_to_prompt(
            completion,
            system_prompt=(
                "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature."
                "If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information, just say you don't know."
            ),
        )
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
