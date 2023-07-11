from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']


class QA:
    template = """First: Always thank the user for the contacting,
    Second: Only answer questions that:
      1. doesnt need user context or
      2. doesnt need asssitant action or
      3. that have context available if doenst have context,
    if not satisfy those 3 conditions than, simply respond with "I don't know, Would you like to talk to a human agent".
    answer in English and your own words and in a very polite way and as truthfully as possible from the context given to you.
    If you do not know the answer or not have context to the question, simply respond with "I don't know. Would you like to talk to a human agent".
    If questions are asked where there is no relevant context available or needs more user context or agent action?, simply respond with "I don't know. Would you like to talk to a human agent?"
    If the user asks to talk to a human agent or the agent needs to escalate the issue, simply respond with "I will transfer you to a human agent now, could you fill this form https://www.google.com/forms/about/ and we will get back to you via email as soon as we have an update. Thank you for contacting us."
    Context: {context}

    {chat_history}
    Human: {question}
    Assistant:"""

    persist_directory="./chroma_db"

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"], template=template
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    def __init__(self, file_path):

        self.embedding_function = OpenAIEmbeddings()

        if os.path.exists(self.persist_directory):
            self.load_vectorstore_db()
        else:
            self.file_path = file_path

            self.loader = CSVLoader(
                file_path=self.file_path
            )

            self.docs = self.loader.load()

            self.load_memory_from_dict()

            self.db = Chroma.from_documents(
                self.docs,
                self.embedding_function,
                persist_directory=self.persist_directory
            )
            self.db.persist()

        self.llm = OpenAI(temperature=0)

    def import_csv_to_vectorstore(self, csv_path):
        pass

    def load_vectorstore_db(self, ):
        self.db = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding_function
        )

    def load_memory_from_dict(self, history):
        """
        history: [({"input": "hi"}, {"output": "whats up"})]
        history: [["hi", "whats up"]]
        """
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )

        for message in history:
            memory.save_context({"input": message[0]}, {"output": message[1]})

        return memory

    def run_query(self, query, history=None):

        if history:
            memory = self.load_memory_from_dict(history)

            self.qa = ConversationalRetrievalChain.from_llm(
                llm = self.llm,
                retriever = self.db.as_retriever(),
                memory = memory,
                combine_docs_chain_kwargs={'prompt': self.prompt}
            )
        else:
            self.qa = ConversationalRetrievalChain.from_llm(
                llm = self.llm,
                retriever = self.db.as_retriever(),
                memory = self.memory,
                combine_docs_chain_kwargs={'prompt': self.prompt}
            )

        result = self.qa({'question': query})
        return result