-- LUA communicates with the NEOVIM API and you can also call python scripts

-- vim.opt = settings and getting options
-- vim.cmd = executing vim commands (nice and useful for doing replacement of lines i guess)
-- vim.api.nvim_get_current_buf() = getting current buffer, return value is int (unique identifiers) 
-- 	buffers are in-memory representation of files or text content, 
-- 	if you know buffer you can access content of buffer, r/w/modify/delete
-- 	Get: 'buftype', 'filetype', 'modifiable'
-- 	Operations(buffer specific): save, reload, close
-- vim.api.nvim_get_current_win() = getting the current window id, return value is an integer
-- 	can do visual highlighting, executin gcommands within the windows context and checking properties

-- ways to call python script: we could just always pass the buffer into the script ? 

local M = {}

function M.read_tempfile() -- read tempfile to then display in neovim
	local home = os.getenv("HOME")
        local filename = "tempfile"
        local filepath = string.format("%s/.config/nvim/temp/%s", home, filename)
        local file = io.open(filepath, "r")
	
	local function split(str, sep) --splits at separator
		local result = {}
		for part in string.gmatch(str, "([^" .. sep .. "]+)") do
			table.insert(result, part)
		end
		return result
	end

	local new_lines = {}
	
	for line in file:lines() do
	table.insert(new_lines, line)
	end
	file:close()
	local buf = vim.api.nvim_get_current_buf()
	vim.api.nvim_buf_set_lines(buf, 0, -1, false, new_lines)
end


function M.get_buffer()
	--local input_value = vim.fn.input("What would you like to happen:   ")
	local start_buffer = vim.api.nvim_get_current_buf() --returns identifier
	local buffer_lines = vim.api.nvim_buf_get_lines(start_buffer, 0, -1, false) 
	local buffer_content = table.concat(buffer_lines,"\n")
	return buffer_content
	
end


function M.read_lineedits()
	local home = os.getenv("HOME")
        local filename = "lineedits"
        local filepath = string.format("%s/.config/nvim/temp/%s", home, filename)
        local file = io.open(filepath, "r")
	local content = file:read("*a")
	file:close()
	local ok, lines = pcall(load("return " .. content))
	if not ok then
		vim.notify("Failed to parse edited lines", vim.log.levels.ERROR)
		return {}
	end
	return lines
end

function M.highlight(lines)
	local buf = vim.api.nvim_get_current_buf()
	local maxlines = vim.api.nvim_buf_get_lines(buf, 0, -1, false)
	local last_line = #maxlines
	print(last_line)
	local highlight_group = "Changes"
	for i, entry in ipairs(lines) do
		if entry <= last_line then
			vim.api.nvim_buf_add_highlight(buf, -1, highlight_group, entry , 0, -1)
		end
	end
end


function M.write_temp(content)
	local home = os.getenv("HOME")
	local filename = "tempfile"
	local filepath = string.format("%s/.config/nvim/temp/%s", home, filename)
	local file = io.open(filepath, "w")
	file:write(content)
	file:close()
end


-- asynchronous but we need to halt the script here
function M.call_python()
local python_script = vim.fn.stdpath("config") .."/python/llm_logic.py" --relative file path to config
	local result = vim.fn.system({"python3", python_script})--executes shell command script
	print(result) --results contains the ollama llms answer (json data parsed by requests library in python) 
	return result
end


function M.prompt()
	local original_buf = vim.api.nvim_get_current_buf() --to go back to original win and buffer
	local original_win = vim.api.nvim_get_current_win()

	local buf = vim.api.nvim_create_buf(false, true)
	vim.api.nvim_buf_set_option(buf, "filetype", "text")
	vim.api.nvim_buf_set_option(buf, "buftype", "nofile")
	vim.cmd("highlight NormalFloat term=none ctermfg=white ctermbg=23 guibg=#CCCCFF")
	local win = vim.api.nvim_open_win(buf, true, {
		relative = "cursor",
		width = 60,
		height = 3,
		row = 30,
		col = 25,
		border = "none",
	})

		vim.notify("Write prompt and quit with :Go ")
		vim.api.nvim_buf_create_user_command(buf, "Go", function()
		local lines = vim.api.nvim_buf_get_lines(buf, 0, -1, false)
		local home = os.getenv("HOME")
		local filename = "userprompt"
		local filepath = string.format("%s/.config/nvim/temp/%s", home, filename)

		vim.fn.writefile(lines, filepath)--writes our prompt to tempfile
		vim.notify("Loading LLM...this might take longer the first time the instance is being loaded into memory")
		M.call_python() -- needs to halt until python is done
	
		vim.api.nvim_win_close(win, true) -- closes this window
		--to restore the original window and buf then work in this with our new tempfiles
		vim.api.nvim_set_current_win(original_win)
        	vim.api.nvim_set_current_buf(original_buf)

		local lines = M.read_lineedits()  -- Reads lineedits
	        M.read_tempfile()        -- Loads tempfile into buffer
        	M.highlight(lines)

	end, {})
end
			
	
--------- this is basically the main funciton for require imports in LUA------------------
function M.run()
	
	buf = M.get_buffer() --reads bufffer data 
	M.write_temp(buf)  --writes buffer to temp file
	
	M.prompt()
    
	
end

return M
