
import google.generativeai as genai
import sys

def verify_key(api_key):
    print(f"Testing API Key: {api_key[:10]}...{api_key[-5:]}")
    
    try:
        genai.configure(api_key=api_key)
        
        # List models to verify access
        print("Listing available models...")
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not models:
            print("No models found. Key might be valid but has no access to models.")
            return False
            
        print(f"Success! Found {len(models)} models.")
        
        # Try generation with the first available model
        model_name = 'gemini-2.0-flash' if 'models/gemini-2.0-flash' in models else models[0]
        print(f"Testing generation with {model_name}...")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello, can you hear me?")
        
        print(f"Generation successful: {response.text}")
        return True
        
    except Exception as e:
        print(f"Error validating key: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        key = sys.argv[1]
    else:
        key = input("Enter your Gemini API Key: ").strip()
        
    verify_key(key)
