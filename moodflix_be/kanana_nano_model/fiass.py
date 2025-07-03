from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def main():
    # 1. 임베딩 모델 불러오기
    model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

    # 2. 문서들을 벡터로 변환
    docs  = [row_to_english_sentence(r) for r in rows]
    doc_embeddings = model.encode(docs, convert_to_numpy=True)

    # 3. 벡터 DB 생성 (FAISS)
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])  # L2 거리
    index.add(doc_embeddings)

    # 4. 사용자의 질문 벡터화
    query = "Recommend me a horror movie"
    query_vector = model.encode([query])

    # 5. 유사 문서 검색 (Top 1개)
    distances, indices = index.search(np.array(query_vector), k=1)
    print("가장 유사한 문서:", docs[indices[0][0]])


# 예시 영화 정보 리스트 
rows = [
    {"title": "Dune: Part Two", "year": 2024, "genre": "SF", "director": "Denis Villeneuve"},
    {"title": "Inside Out 2", "year": 2024, "genre": "animation", "director": "Kelsey Mann"},
    {"title": "The Substance", "year": 2024, "genre": "psychological thriller", "director": "Hannah Fidell"},
    {"title": "Anora", "year": 2024, "genre": "drama", "director": "Sean Baker"},
    {"title": "Wicked", "year": 2024, "genre": "musical", "director": "Jon M. Chu"},
    {"title": "Furiosa: A Mad Max Saga", "year": 2024, "genre": "action", "director": "George Miller"},
    {"title": "Gladiator II", "year": 2024, "genre": "historical action", "director": "Ridley Scott"},
    {"title": "Joker: Folie à Deux", "year": 2024, "genre": "crime drama", "director": "Todd Phillips"},
    {"title": "The Wild Robot", "year": 2024, "genre": "family animation", "director": "?",},  # 감독 정보 없음
    {"title": "A Real Pain", "year": 2024, "genre": "drama", "director": "Chiwetel Ejiofor"},
]

# 문장으로 변환하는 함수
def row_to_sentence(row: dict) -> str:
    # 감독 정보가 없으면 감독 부분 제외
    director_part = f"{row['director']} 감독이 연출했습니다." if row.get("director") and row["director"] != "?" else ""
    return f"{row['title']}은 {row['year']}년에 개봉한 {row['genre']} 영화로, {director_part}".strip()

def row_to_english_sentence(row: dict) -> str:
    # 감독 정보가 없을 경우 생략
    if row.get("director") and row["director"] != "?":
        director_part = f"It was directed by {row['director']}."
    else:
        director_part = ""
    
    return f"{row['title']} is a {row['genre']} film released in {row['year']}. {director_part}".strip()


if __name__ == "__main__":
    main()