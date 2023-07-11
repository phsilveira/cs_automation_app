from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
# from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma
# from promptlayer.langchain.llms import OpenAI
from langchain import OpenAI
from langchain.document_loaders import CSVLoader
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import openai
import os

os.environ['OPENAI_API_KEY'] = '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'
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

    Example of chat:
    Human: Can you please help me to remove block?
    Assistant: I will transfer you to a human agent now, could you fill this form https://www.google.com/forms/about/ and we will get back to you via email as soon as we have an update. Thank you for contacting us.
    Human: hi ur filter dont works really i dont see any woman or someone 0 users... why?
    Assistant: I'm sorry to hear that you're having trouble with our gender filter. Usually this problem occurs when filters are selected. Please try removing interest tags and country filters and try again, this usually fixes the issue of not being able to connect to female partners. If it does not resolve I will have to escalate this to find out why you are having this issue.
    Human: Is there something wrong with the website?? I am not pairing with anyone...
    Assistant: I'm sorry to hear that you're having trouble with our gender filter. Usually this problem occurs when filters are selected. Please try removing interest tags and country filters and try again, this usually fixes the issue of not being able to connect to female partners. If it does not resolve I will have to escalate this to find out why you are having this issue.
    Human: how cancel my subscription
    Assitant: Thank you for reaching out to us! For security reasons, only users can cancel their subscription. To cancel your membership please log into your account area. Then under your membership status click the “Details” button and then the “Cancel Membership” button.
    Human: I can't open my camera
    Assistant: Make sure your webcam is properly connected to your device. 2. Check if your webcam is working properly by doing a webcam test on this website: https://www.onlinemictest.com/webcam-test/ If you are still having issues with your webcam, please provide us with your email address so we can assist you further.
    Human: I want a refund, I'm not using the service
    Assistant: Thank you for reaching out to us! but As stated in our terms: Payments are nonrefundable, Would you like to talk to a human agent

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
        self.file_path = file_path

        self.loader = CSVLoader(
            file_path=self.file_path
        )

        # load up ur text into docs
        self.docs = self.loader.load()

        # # turn ur text into embeddings
        self.embedding_function = OpenAIEmbeddings()
        # load it into Chroma
        if os.path.exists(self.persist_directory):
          self.db = Chroma(
              persist_directory=self.persist_directory, 
              embedding_function=self.embedding_function
          )
        else:
          self.db = Chroma.from_documents(
              self.docs, 
              self.embedding_function, 
              persist_directory=self.persist_directory
          )
          self.db.persist()

        # load ur llm
        self.llm = OpenAI(temperature=0)
        # self.llm = OpenAI(temperature=0, pl_tags=["cs_automation"])

        # create a retriever
        self.qa = ConversationalRetrievalChain.from_llm(
            llm = self.llm,
            retriever = self.db.as_retriever(),
            memory = self.memory,
            combine_docs_chain_kwargs={'prompt': self.prompt}
        )

    def reset_retriever(self):
        self.memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True
        )
        # create a retriever
        self.qa = ConversationalRetrievalChain.from_llm(
            llm = self.llm,
            retriever = self.db.as_retriever(),
            memory = self.memory,
            combine_docs_chain_kwargs={'prompt': self.prompt}
        )

    def run_query(self, query):
        # run ur query
        result = self.qa({'question': query})
        return result