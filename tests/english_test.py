import requests


def test_api():
    params = {
        "text": "The epistemological underpinnings of quantum mechanics fundamentally challenge classical Newtonian determinism through the Heisenberg uncertainty principle. Wave-particle duality and quantum entanglement phenomena necessitate a profound reconceptualization of physical reality, wherein probabilistic interpretations supersede causal determinism at subatomic scales, thereby revolutionizing our ontological understanding of the universe's fundamental architecture.",
        "language": "english"
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