# Keyboard_AI
It's Keyboard AI. LUA / Python implementation of LOCAL AGENTIC code ASSISTANT LIKE YOU WOULDN'T BELIEVE ALL IN NEOVIM

# Commands

:LLM - this invokes an instance of LLM in Ollama
i - type in any prompt
:Go - send prompt to a temporary file, buffer gets sent into different file, concatenates as prompt for LLM

wait for response depending on the speed of your GPU..

# Explanation
init.lua : standard configuration file for lua, require method to use lua scripts and add command :LLM
buffer_logic.lua : this script is responsible for sending the buffer to the python script and making changes in the buffer
llm_logic.py : this script interacts with the LLM and gets called by init.lua 
temp: this directory stores the temporary buffer to avoid complex inter-process communication

# requires: neovim >= 0.70, Ollama

# Install
Just copy the nvim folder into .config/ 
This will require a custom model-file with a specific system prompt in the future.
