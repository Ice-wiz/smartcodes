from utils.weaviate_client import weaviate_client

if __name__ == "__main__":
    connected, info = weaviate_client.is_connected()
    if connected:
        print("✅ Connected to Weaviate.")
        print("Available collections:", info)
    else:
        print("❌ Failed to connect to Weaviate.")
        print("Error:", info)
