from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import OpenAI
from langchain.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

class QA:
    template = """First: Always thank the user for the contacting,
    Second: Only answer questions that doesnt need user context or doesnt need agent action or that have context available if doenst have context, simply respond with "I don't know".
    answer in your own words and in a very polite way and as truthfully as possible from the context given to you.
    If you do not know the answer or not have context to the question, simply respond with "I don't know. Can you ask another question".
    If questions are asked where there is no relevant context available or needs more user context or agent action?, simply respond with "I don't know. Would you like to talk to a human agent?"
    If the user asks to talk to a human agent or escalate to tech team, simply respond with "I will transfer you to a human agent now, could you fill this form https://www.google.com/forms/about/. Thank you for contacting us."
    Context: {context}


    {chat_history}
    Human: {question}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["context", "chat_history", "question"], template=template
    )

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )

    def __init__(self, file_path): 
        self.file_path = file_path

        # loader = DirectoryLoader('/content/langchain-tutorials/data/PaulGrahamEssaySmall', glob='**/*.txt')
        self.loader = CSVLoader(
            file_path=self.file_path
        )

        # load up ur text into docs
        self.docs = self.loader.load()

        # turn ur text into embeddings
        self.embeddings = OpenAIEmbeddings()

        # get ur docsearch ready
        self.docsearch = FAISS.from_documents(self.docs, self.embeddings)

        # load ur llm
        self.llm = OpenAI(temperature=0)

        # create a retriever
        self.qa = ConversationalRetrievalChain.from_llm(
            llm = self.llm, 
            retriever = self.docsearch.as_retriever(), 
            memory = self.memory,
            combine_docs_chain_kwargs={'prompt': self.prompt}
        )
    
    def run_query(self, query):
        # run ur query
        result = self.qa({'question': query})
        return result


if __name__ == '__main__':
    query_runner = QA(file_path='macros.csv') 
    query = "Je n'arrive plus à allumer ma cam" 
    result = query_runner.run_query(query) 
    print(result)

