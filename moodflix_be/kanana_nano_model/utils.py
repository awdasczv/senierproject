def update_chat_history(chat_history, user_input, assistant_response=None):
    """chat_history에 user/assistant 대화를 추가"""
    chat_history.append({"role": "user", "content": user_input})
    if assistant_response is not None:
        chat_history.append({"role": "assistant", "content": assistant_response})

def summarize_dialogue(conversation: str, model, tokenizer, max_new_tokens=256) -> str:
    """
    Kanana 모델을 사용하여 User-Assistant 대화를 요약하는 함수
    :param conversation: 전체 대화 문자열 (User:, Assistant:로 구성)
    :param model: 사전 로드된 kanana 모델
    :param tokenizer: 사전 로드된 토크나이저
    :param max_new_tokens: 요약문 최대 생성 길이
    :return: 요약된 문자열
    """

    # 요약 지시가 포함된 프롬프트 구성
    prompt = f"""다음은 사용자와 챗봇 간의 대화입니다. 이 대화를 간단히 요약해 주세요.

    {conversation}

    요약:"""

    input_ids = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=8192).input_ids.to(model.device)

    output = model.generate(
        input_ids=input_ids,
        attention_mask=input_ids.ne(tokenizer.pad_token_id).to(model.device),
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.pad_token_id
    )

    # 출력된 텍스트 디코딩
    summary = tokenizer.decode(output[0], skip_special_tokens=True)

    # "요약:" 이후만 추출
    return summary.split("요약:")[-1].strip() 