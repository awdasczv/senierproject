from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 외부 모듈 import
from function_handler import detect_and_execute_function, get_system_message
from utils import update_chat_history

# 전역 변수로 모델과 토크나이저 선언
model = None
tokenizer = None
chat_history = [] # 대화 기록을 저장하는 리스트

def load_model():
    """모델과 토크나이저를 로딩하는 함수"""
    global model, tokenizer
    
    if model is None or tokenizer is None:
        model_name = "kakaocorp/kanana-1.5-2.1b-instruct-2505"
        
        print("모델 로딩 중...")
        # 모델 로딩
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )

        # 토크나이저 로딩 (문자열을 모델이 이해하는 토큰으로 변환해줌)
        tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side="left")
        tokenizer.pad_token = tokenizer.eos_token
        print("모델 로딩 완료!")

def generate_answer(user_input):
    global model, tokenizer, chat_history
    
    # 모델이 로딩되지 않았다면 로딩
    if model is None or tokenizer is None:
        load_model()

    # 함수 호출 가능성을 알리는 시스템 메시지 추가
    system_message = get_system_message()

    # 사용자 입력
    messages = [system_message] + chat_history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": ""}
    ]

    # 프롬프트를 토큰 ID로 변환하여 모델에 입력
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_special_tokens=False, # chat_template이 자동으로 special token을 추가할 경우 False로 설정    
        add_generation_prompt=True,  # assistant role의 응답 시작을 의미
        return_tensors="pt"
    ).to(model.device)

    # 텍스트 생성
    output = model.generate(
        input_ids,  # [필수] 모델에게 입력할 텍스트를 토큰으로 변환한 것
        max_new_tokens=512,  # [필수] 최대 1024개의 새로운 토큰(단어/문자)을 생성
        do_sample=True,  # [선택] 확률에 따라 다양한 답변 생성 (False면 항상 같은 답변)
    )

    # 출력 텍스트를 디코딩하여 사람이 읽을 수 있게 변환
    response = tokenizer.decode(output[0], skip_special_tokens=True)
 
    #input_ids의 길이만큼 자른 이후만 추출
    generated = output[0][input_ids.shape[-1]:]
    assistant_response = tokenizer.decode(generated, skip_special_tokens=True).strip()

    # print("--------------------------------")
    # print(assistant_response)
    # print("--------------------------------")

    #update_chat_history(user_input, assistant_response)
    # print(response)
    # return assistant_response
    
    # 함수 호출 감지 및 실행
    final_response = detect_and_execute_function(assistant_response)
    
    update_chat_history(chat_history, user_input, final_response)
    
    # print(f"원본 응답: {assistant_response}")
    print(final_response)

    return final_response



if __name__ == "__main__":
    generate_answer()