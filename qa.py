from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
import os


class QA:
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
        self.llm = OpenAI()

        # create a retriever
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type='stuff',
            retriever=self.docsearch.as_retriever(),
            return_source_documents=True
        )
    
    def run_query(self, query):
        # run ur query
        result = self.qa({'query': query})
        return result


if __name__ == '__main__':
    query_runner = QA(file_path='macros.csv') 
    query = "Je n'arrive plus à allumer ma cam" 
    result = query_runner.run_query(query) 
    print(result['result'])

