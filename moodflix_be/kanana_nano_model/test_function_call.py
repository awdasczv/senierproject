from kanana import generate_answer, load_model
from function_handler import detect_and_execute_function

def test_function_call():
    """함수 호출 기능을 테스트하는 함수"""
    print("=== Kanana 함수 호출 테스트 ===")
    
    # 모델 로딩
    load_model()
    
    # 테스트 케이스들
    test_cases = [
        "안녕하세요!",
        "hello_world 함수를 실행해주세요",
        "함수 호출 테스트를 해보고 싶어요",
        "hello_world를 실행시켜줘"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n--- 테스트 {i} ---")
        print(f"입력: {test_input}")
        response = generate_answer(test_input)
        print(f"응답: {response}")
        print("-" * 50)

if __name__ == "__main__":
    test_function_call() 