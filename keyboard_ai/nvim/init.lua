vim.opt.number = true 
-- enables numbered rows

local getthisbuffer = require("buffer_logic") --tries to load the lua script from a bunch of known locations
vim.api.nvim_create_user_command('LLM', function()
	getthisbuffer.run() --lua execution function to run my script that returns a table with run() fuction
end,{})
--embeds new function as argument (just lua things i guess)


