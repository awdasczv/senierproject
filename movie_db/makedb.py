import requests
import os,csv,time
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TMDB_API_KEY")
read_access_token = os.getenv("TMDB_READ_ACCESS_TOKEN")

TOTAL_PAGES = 500
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
OUTPUT_FILE_MOVIES = "korean_movies_10000.csv"
OUTPUT_FILE_DRAMAS = "korean_dramas_10000.csv"

def test():
    movie_id = 1017163
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": api_key,
    }
    response = requests.get(url, params=params)
    print(response.json())

def get_korean_movies(page=1):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": api_key,
        "language": "ko-KR",
        "region": "KR",
        "sort_by": "popularity.desc",
        "with_original_language": "ko",
        "page": page
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error on page {page}: {response.status_code}")
        return None

def get_korean_dramas(page=1):
    url = f"{BASE_URL}/discover/tv"
    params = {
        "api_key": api_key,
        "language": "ko-KR",
        "region": "KR",
        "sort_by": "popularity.desc",
        "with_original_language": "ko",
        "page": page
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error on page {page}: {response.status_code}")
        return None

def save_movies_to_csv(movies, filename):
    file_exists = os.path.isfile(filename)
    with open(filename, mode='a', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "id",               # TMDb 영화 ID
            "title",            # 제목
            "original_title",   # 원제 (비한글 제목이면 중요)
            "overview",         # 줄거리
            "release_date",     # 출시일
            "original_language",# 원어
            "popularity",       # TMDb 인기점수
            "vote_average",     # 평균 평점
            "vote_count",       # 투표 수
            "genre_ids",        # 장르 ID 리스트
            "poster_path",      # 포스터 이미지 경로 (URL로 가공 가능)
            "backdrop_path",    # 배경 이미지 경로 (선택사항)
            "video",            # 동영상 여부 (True/False)
            "adult"             # 성인 콘텐츠 여부 (True/False)
        ])
        if not file_exists:
            writer.writeheader()
        for movie in movies:
            writer.writerow({
                "id": movie.get("id"),
                "title": movie.get("title"),
                "original_title": movie.get("original_title"),
                "overview": movie.get("overview"),
                "release_date": movie.get("release_date"),
                "original_language": movie.get("original_language"),
                "popularity": movie.get("popularity"),
                "vote_average": movie.get("vote_average"),
                "vote_count": movie.get("vote_count"),
                "genre_ids": ",".join(map(str, movie.get("genre_ids", []))),
                "poster_path": movie.get("poster_path"),
                "backdrop_path": movie.get("backdrop_path"),
                "video": movie.get("video"),
                "adult": movie.get("adult"),
            })

def save_dramas_to_csv(dramas, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "name", "original_name", "overview", "first_air_date",
            "original_language", "origin_country", "popularity",
            "vote_average", "vote_count", "genre_ids",
            "poster_path", "backdrop_path", "adult"
        ])

        if not file_exists:
            writer.writeheader()

        for drama in dramas:
            writer.writerow({
                "id": drama.get("id"),
                "name": drama.get("name"),
                "original_name": drama.get("original_name"),
                "overview": drama.get("overview"),
                "first_air_date": drama.get("first_air_date"),
                "original_language": drama.get("original_language"),
                "origin_country": ",".join(drama.get("origin_country", [])),
                "popularity": drama.get("popularity"),
                "vote_average": drama.get("vote_average"),
                "vote_count": drama.get("vote_count"),
                "genre_ids": ",".join(map(str, drama.get("genre_ids", []))),
                "poster_path": drama.get("poster_path"),
                "backdrop_path": drama.get("backdrop_path"),
                "adult": drama.get("adult"),
            })

def save_n_dramas():
    all_dramas = []
    for page in range(1, TOTAL_PAGES + 1):
        print(f"Fetching page {page}...")
        dramas = get_korean_dramas(page)
        all_dramas.extend(dramas)
        time.sleep(0.5)
    save_dramas_to_csv(all_dramas, OUTPUT_FILE_DRAMAS)
    print(f"✅ 저장 완료: {len(all_dramas)}편 -> {OUTPUT_FILE_DRAMAS}")

def save_n_movies():
    all_movies = []
    for page in range(1, TOTAL_PAGES + 1):
        print(f"Fetching page {page}...")
        movies = get_korean_movies(page)
        all_movies.extend(movies)
        time.sleep(0.5)  # TMDb 권장: 과도한 요청 방지 (초당 4회 이하)
    save_movies_to_csv(all_movies, OUTPUT_FILE_MOVIES)
    print(f"✅ 저장 완료: {len(all_movies)}편 -> {OUTPUT_FILE_MOVIES}")

def main():
    test()


if __name__ == "__main__":
    main()
