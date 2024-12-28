from openai import OpenAI
import os
import time

def respond_message_to_openai(item, client):
    start_time = time.time()  # 시작 시간 기록
    
    
        # 최근 5개의 대화 기록을 가져옴
    # OpenAI API에 보낼 메시지 형식
    messages = [
        {
            "role": "system",
            "content": f"""
            사용자 입력을 바탕으로 제목과 내용을 생성하고 마크다운을 활용한 임베드 데이터를 반환합니다.
            리턴 형식 : 제목`split`내용
            """
        },
        {
            "role": "user", 
            "content": item

        }
    ]
    
            # - 인사말이나 불필요한 설명은 하지 마. 질문에 바로 답변을 시작해.
    # OpenAI API를 통해 응답 생성
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=1,
            max_completion_tokens=1200,
            top_p=0.85,
            frequency_penalty=0.1,
            presence_penalty=0.1,

        )
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return "응답을 생성하는데 문제가 발생했습니다."

    end_time = time.time()  # 종료 시간 기록
    elapsed_time = end_time - start_time  # 소요 시간 계산
    print(f"응답 시간: {elapsed_time:.2f}초")
    
    # response.choices[0].message['content']로 변경
    return response.choices[0].message.content