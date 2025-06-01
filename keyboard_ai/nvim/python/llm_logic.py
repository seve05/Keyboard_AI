import ollama
import requests 
import os

def load_file(filepath):
    with open(filepath,'r') as f:
        content = f.read()
    return content



def llm_processing(prompt):
    url = "http://localhost:11434/api/generate" #local ollama addresse
    payload = {
        "prompt": prompt,
        "stream": False,
        "raw": False,
        "model": "devstral:24b"
             }

    response = requests.post(url, json=payload, stream=False)
    data = response.json()
    text_response = data.get("response") #json response von ollama
    return text_response


def main(): 
    home_dir = os.path.expanduser("~")
    
    filepath_temp = home_dir + "/.config/nvim/temp/tempfile"
    filepath_userprompt = home_dir + "/.config/nvim/temp/userprompt"
    
    tmp = load_file(filepath_temp)
    userprompt = load_file(filepath_userprompt) 
    
#we want to join the prompt and file now
    final_prompt = "prompt: " + userprompt + "  File: " + tmp #this concatenates the prompt and the file 
                                                              #for the llm tor process together
    print(" ")
    print(llm_processing(final_prompt))
    




if __name__ == "__main__":
    main()
