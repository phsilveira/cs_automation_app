from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains.question_answering import load_qa_chain
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]


class QA:
    template = """You are an AI assistant chatbot. You will provide for the user answers based \
    on the Context FAQ, you will follow these instructions:

    1) Always thank the user for the contacting,
    2) Only answer questions that you have context, inside ```, If you don't have context, simply \
    respond with "Can you rephrase the question?".
    3) answer in English and your own words and in a very polite way and as truthfully as possible \
    from the context given to you.
    4) Only If the user asks to talk to a human agent or the agent needs to escalate the issue, \
    respond with "I will transfer you to a human agent now, could you fill this \
    form https://www.google.com/forms/about/ and we will get back to you via email as soon \
    as we have an update. Thank you for contacting us."

    common user expressions to help:
    - been banned == been flagged

    Context:
    ```
    {context}
    ```

    {chat_history}
    Human: {question}
    AI:"""

    persist_directory = "./chroma_db"

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"], template=template
    )

    def __init__(self, csv_path:str = None) -> None:
        self.embedding_function = OpenAIEmbeddings()
        self.llm = OpenAI(temperature=0)

        if os.path.exists(self.persist_directory):
            self.load_vectorstore_db()
        elif csv_path is not None:
            self.import_csv_to_vectorstore(csv_path)
        else:
            raise ValueError("Missing 'csv_path'")
        
        self.chain = self.create_chain()

    def load_vectorstore_db(self) -> None:
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )

    def import_csv_to_vectorstore(self, csv_path: str) -> None:
        loader = CSVLoader(file_path=csv_path)
        docs = loader.load()

        self.db = Chroma.from_documents(
            docs,
            self.embedding_function,
            persist_directory=self.persist_directory,
        )
        self.db.persist()

    def load_history_messages(self, history: list = None) -> ConversationBufferMemory:
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            input_key='question'
        )        
        
        if history is not None:
            for message in history:
                memory.save_context({"question": message[0]}, {"output": message[1]})

        return memory

    def run_chain(self, question: str, history: list = None) -> str:
        memory = self.load_history_messages(history)
        chain = load_qa_chain(
            self.llm, chain_type='stuff', prompt=self.prompt, memory=memory, verbose=False
        )
        docs = self.db.similarity_search(question, k=3)
        return chain.run({"input_documents": docs, "question": question})

    def create_chain(self):
        self.memory = self.load_history_messages()
        return load_qa_chain(
            self.llm, chain_type='stuff', prompt=self.prompt, memory=self.memory, verbose=False
        )

    def ask(self, question: str) -> str:
        docs = self.db.similarity_search(question, k=3)
        return self.chain.run({"input_documents": docs, "question": question})
