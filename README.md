# Course-IA

Course profesional Apps with LLMs, IAG and Agents with LangChain, LangGraph and Python.

We only need python installed.

## Topic 1 - Langchain

Create a folder for the aplication "course_langchain".

Create a virtual environent for the course "python -m venv venv".

Execute the virtual environment "venv/Scripts/activate".

Install langchain "pip install langchain==1.*"

Install other packages related "pip install langchain-openai langchain-google-genai streamlit"

See a package info "pip show langchain"

Create windows env in cmd "setx NAME(OPENAI_API_KEY/GOOGLE_API_KEY) "KEY""

See Windows env in cmd "set"

Run streamlit "streamlit run .\streamlit_chatbot.py"

## Topic 2 - Project

Install pypdf "pip install pypdf"

## Topic 3 - RAG

install langchain-community "pip install langchain-community"

install for webloader: "pip install beautifulsoup4"

install for google drive loader "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"

Go to google cloud console > use the project

	> Menu "APIs and services" > Enable APIs and services > Google Drive API > Enable

	> Credentials > Create OAuth client ID > Configure Screen > Create Oauth Client ID > Download credentials.json

	> Google Drive API > Admin > Audience > Add Users > our email

install PyPDF2 "pip install PyPDF2"

install real langchain google community "pip install langchain_google_community"

install for directory loader "pip install tqdm"

install for youtube loader "pip install youtube-transcript-api"

install for UnstructuredHTML "pip install unstructured"

install for Selenium "pip install selenium"

## Topic 3 - vector db

Install python estable "winget install Python.Python.3.12"

Create venv python estable "py -3.12 -m venv venv_312" | "py --list"

Activate venv ".\venv_312\Scripts\Activate.ps1"

install vector database chormadb "pip install chromadb langchain_chroma"

install langchain-classic "pip install -U langchain-classic"

"streamlit run app.py"

## Topic 4 - langGraph

Install langGraph "pip install langgraph"

Fix project, use google AI

## Topic 5 - Memory and context manage

installa langgraph sqlite "pip install langgraph-checkpoint-sqlite"

## Topic 6 - Agents

install PythonREPL "pip install langchain_experimental"

install integration wikipedia "pip install wikipedia"

Go to google cloud console > use the project

	> Menu "APIs and services" > Credentials > Create OAuth client ID > Configure Screen > Create Oauth Client ID > Download credentialsOauth2.json

	> Library > Gmail API > Enable

	> Gmail API > Admin > Audience > Add Users > our email

install for agente_ia_langchain.py: "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"

install langgraph-supervisor for multiagents "pip install langgraph-supervisor"

Project:

Google "tavily API key" > register and get API key

Google "virustotal API key" > register and get API key

Install virustotal, dotenv for python and tavily "pip install python-dotenv vt-py langchain-tavily fastapi uvicorn"


git push origin main
