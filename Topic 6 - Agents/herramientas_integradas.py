from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

# Ver todas las integraciones: https://docs.langchain.com/oss/python/integrations/tools
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

response = wikipedia.run("Spain")

print(response)