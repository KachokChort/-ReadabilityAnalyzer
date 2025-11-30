import requests


def test_api():
    params = {
        "text": "Эпистемологическая парадигма постмодернистского дискурса, имплицитно деконструируя метафизические основания классического рационализма, актуализирует проблему легитимации нарративных практик условиях тотального семиотического плюрализма, очередь, детерминирует необходимость переосмысления традиционных герменевтических процедур интерпретации культурных нелинейных синергетических моделей, трансцендирующих бинарные оппозиции субъект-объектной диалектики.",
        "language": "russian"
    }

    try:
        response = requests.post("http://127.0.0.1:8000/text/", json=params)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Score: {data['score']}")
            print(f"Level: {data['level']}")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    test_api()