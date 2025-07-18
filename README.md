# Keyboard_AI
LUA / Python implementation of LLM integration for coding (this is an optimization problem if you try to do this locally on small models)
# Commands

:LLM - this invokes an instance of LLM in Ollama <br/>
i - type in any prompt <br/>
:Go - send prompt to a temporary file, buffer gets sent into different file, concatenates as prompt for LLM <br/>

wait for response depending on the speed of your GPU..

# Explanation
init.lua : standard configuration file for lua, require method to use lua scripts and add command :LLM
buffer_logic.lua : this script is responsible for sending the buffer to the python script and making changes in the buffer
llm_logic.py : this script interacts with the LLM and gets called by init.lua 
temp: this directory stores the temporary buffer to avoid complex inter-process communication

# requires: neovim >= 0.70, Ollama

# Install
create a "nvim" directory in .config/ and insert the folders: "lua", "python", "temp". Also insert "init.lua" to use the custom commands.

This will require the custom model-file "devstralcustom" to create a custom model with parameters and a custom system prompt in ollama.
To do this go to home/.ollama , copy "devstralcustom" into this directory. 
Now run "ollama create yourcustomname -f devstralcustom"

