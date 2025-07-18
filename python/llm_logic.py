import ollama
import requests 
import os
import json
 
def load_file(filepath):
    with open(filepath,'r') as f:
        content = f.read()
    return content

def write_to_file(filepath, contents):
    with open(filepath, 'w') as f:
        for line in contents:
            f.write(line + "\n")

def write_to_file_edits(filepath, contents):
    with open(filepath, 'w') as f:
        f.write("{" + ",".join(str(i) for i in contents) + "}")

def parse_to_json(text_response): 
        try:
            return json.loads(text_response) #returns dictionary with keys as value paris
        except:
            print("Failed to decode JSON",text_response)

# this function parses the user-prompt and the code file from temp to the llm for processing
def llm_processing(prompt):#prompt is actually concatenation of 'prompt' and codefile 
    url = "http://localhost:11434/api/generate" 
    payload = {
        "prompt": prompt,
        "stream": False,
        "raw": False, #to receive JSON set to raw (we dont want that)
        "model": "devstralsystemp" #old:devstralsystemp,this is devstral:24b 8bit quantization with system prompt
             }
    response = requests.post(url, json=payload, stream=False)
    data = response.json()
    text_response = data.get("response") 
    #print(text_response)#debug
    return text_response  #returns response from LLM 

#this function iterates through the llm response and performs the actions del, insert 
def iterating_objects(text_response): 
    home_dir = os.path.expanduser("~")
    filepath = home_dir + "/.config/nvim/temp/tempfile"
    with open(filepath,'r') as file:
        file_content = file.readlines() #list of strings each line
        for i in range(len(file_content)):
            file_content[i] = file_content[i].rstrip('\n') #remove all trailing escapes 
        json_response = parse_to_json(text_response) #turn to json(if valid)
        #print(json_response)#debug

     #need to add length of the code too that gets inserted between lines
        edits = []
        for i in range(len(json_response)):#iterates through n json {} objects/actions llm takes
            try: #in case we are not getting insert_code key from LLM
                insert_code(file_content, json_response[i]["start_line"],json_response[i]["insert_code"]) 
                start = json_response[i]["start_line"]
                end = json_response[i]["end_line"]
                
                if end != start:
                    edits.append(start)
                for i in range(len(json_response[i]["insert_code"])):
                    edits.append(start+i)
            except: 
                pass
            
            try:
                delete_code(file_content, json_response[i]["start_delete"], json_response[i]["end_delete"])
            except:
                pass
       
        print(edits)
        return file_content, edits #now returns tuple     

# this function inserts code(changes) into the buffer thats in our tempfile, at specified line
def insert_code(tempfile, start_line, insert_code): #wir sollten nicht jedes mal file oeffnen sondern nur 1x am anfang, vorher in var speichern einfach
    try: 
        code = insert_code
        start = start_line     #ende spielt bei insertion keine rolle
        for i in range(len(code)): #code ist array of strings
            index = start+i  # wenn i 0-indexiert ist
            if index < len(tempfile):
                tempfile[index] = code[i]
            else:
                tempfile.append(code[i])
        return tempfile
    except:
        return#just exit the stack no need to return an error this is intentional: case no insertion 

# this is the delete function the llm calls in its response, deletes in ranges start to finish
def delete_code(tempfile, start_delete, end_delete):
    try:
        start = start_delete
        end = end_delete
        number_of_deletes = end - start 
       #sadly not possible to delete starting from end bc llm parses wrong index sometimes longer
        for i in range(number_of_deletes):
            index = start-1
            i = i-1
            del tempfile[index] 
        if start == end:
            for i in range(1):
                index = start -1
                del tempfile[index]
        return tempfile 
    
    except Exception as e:
        return f"Error: {e}" 

def main(): 
    home_dir = os.path.expanduser("~")
    
    filepath_temp = home_dir + "/.config/nvim/temp/tempfile"
    filepath_userprompt = home_dir + "/.config/nvim/temp/userprompt"
    filepath_lineedits = home_dir + "/.config/nvim/temp/lineedits"
    
    tempfile = load_file(filepath_temp)
    userprompt = load_file(filepath_userprompt) 
    line_edits = load_file(filepath_lineedits) 
    
    #we join the prompt and file now
    final_prompt = "prompt: " + userprompt + "  File: " + tempfile #this concatenates the prompt and the file 
                                                              #for the llm tor process together
    llm_response = iterating_objects(llm_processing(final_prompt)) # return type is tuple with contents[0] and lines of edits[1]
    
    new_tempfile = llm_response[0]
    write_to_file(filepath_temp, new_tempfile) #hier schreiben wir in tempfile die aenderung 
    edits_list = llm_response[1]    
    write_to_file_edits(filepath_lineedits, edits_list) #write edits temp file  
    
    print(llm_response[0], llm_response[1]) #debug
    



if __name__ == "__main__":
    main()
