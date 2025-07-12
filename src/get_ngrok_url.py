# get_ngrok_url.py
import requests
import logging as logs

# Setup logging to show INFO level logs
logs.basicConfig(level=logs.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def get_ngrok_url():
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        response.raise_for_status()
        tunnels = response.json().get("tunnels", [])

        for t in tunnels:
            if t.get("proto") == "https":
                public_url = t.get("public_url")
                logs.info(f"{public_url}")
                return public_url

        logs.warning("⚠️ No HTTPS tunnel found.")
        return None

    except Exception as e:
        logs.error(f"❌ Error while fetching ngrok URL: {e}")
        return None

# Example usage
if __name__ == "__main__":
    url = get_ngrok_url()
    if url:
        print(f"{url}")
