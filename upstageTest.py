from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

# 환경 변수에서 API 키 가져오기
api_key = os.getenv("UPSTAGE_API_KEY")
# if api_key:
#     api_key = api_key.encode('ascii', 'ignore').decode('ascii').strip('"')  # Added strip('"') to remove quotes

# API 키가 없으면 오류 발생
if not api_key:
    raise ValueError("UPSTAGE_API_KEY가 환경 변수에 설정되지 않았습니다.")

chat = ChatUpstage(api_key=api_key)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hi, how are you?")
]
response = chat.invoke(messages)
print(response)