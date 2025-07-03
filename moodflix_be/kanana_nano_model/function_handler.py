import json
import re

def hello_world():
    """테스트용 hello world 함수"""
    return "Hello, world!"

def detect_and_execute_function(response: str):
    """응답에서 함수 호출을 감지하고 실행하는 함수"""
    # 함수 태그 패턴 감지 (공백 허용)
    function_call_pattern = r"<function=(\w+)>\s*(\{.*?\})\s*</function>"
    
    match = re.search(function_call_pattern, response)
    if not match:
        print("일반 응답")
        return response  # 일반 응답이면 그대로 반환
    
    func_name, raw_args = match.groups()
    print(f"함수 호출 감지됨: {func_name}, 인자: '{raw_args}'")
    
    # 인자가 있는 경우와 없는 경우 처리
    if raw_args.strip():
        try:
            args = json.loads(raw_args)
        except json.JSONDecodeError:
            return f"잘못된 JSON 형식의 인자입니다: {raw_args}"
    else:
        args = {}

    # 함수 실행
    if func_name == "hello_world":
        result = hello_world()
        return f"함수 '{func_name}' 실행 결과: {result}"
    else:
        return f"알 수 없는 함수입니다: {func_name}"

def get_system_message():

    #함수 호출을 위한 시스템 메시지를 반환
    system_message_function_call = {
        "role": "system",
        "content": """당신은 사용자와 대화를 나누는 AI 어시스턴트 입니다.

        당신은 사용자의 요청에 따라 외부 함수를 호출할 수 있습니다.

        호출 형식은 다음과 같습니다:
        <function=함수명>{"파라미터명": "값"}</function>

        다음은 사용 가능한 함수 목록입니다:
        - hello_world(): 파라미터 없음

        예시:
        사용자: hello_world 함수를 실행해줘
        어시스턴트: <function=hello_world>{}</function>
        """
    } 

    return system_message_function_call