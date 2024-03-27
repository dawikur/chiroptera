" Copyright (c) 2026 Dawid Kurek <hello@dawikur.dev>

" Recolour nvim-web-devicons from the active Chiroptera palette.  Devicons
" exposes the source icon colour, so this also covers icons added by later
" versions without making the colourscheme depend on a fixed icon list.
if !has('nvim')
	finish
endif

lua << EOF
local function apply()
    local ok, devicons = pcall(require, 'nvim-web-devicons')
    if not ok then
        return
    end

    local function role(color)
        local red = tonumber(color:sub(2, 3), 16) / 255
        local green = tonumber(color:sub(4, 5), 16) / 255
        local blue = tonumber(color:sub(6, 7), 16) / 255
        local maximum = math.max(red, green, blue)
        local minimum = math.min(red, green, blue)
        local delta = maximum - minimum

        if maximum < 0.22 or delta / maximum < 0.18 then
            return 'fg_bright'
        end

        local hue
        if maximum == red then
            hue = 60 * ((green - blue) / delta % 6)
        elseif maximum == green then
            hue = 60 * ((blue - red) / delta + 2)
        else
            hue = 60 * ((red - green) / delta + 4)
        end

        if hue < 20 or hue >= 340 then
            return 'red_bright'
        elseif hue < 75 then
            return 'yellow_bright'
        elseif hue < 165 then
            return 'green_bright'
        elseif hue < 205 then
            return 'cyan_bright'
        elseif hue < 265 then
            return 'blue_bright'
        end
        return 'magenta_bright'
    end

    for _, icon in pairs(devicons.get_icons()) do
        if icon.name and icon.color and icon.cterm_color then
            local color = vim.g.chiroptera.raw[role(icon.color)]
            vim.api.nvim_set_hl(0, 'DevIcon' .. icon.name, {
                fg = color.gui,
                ctermfg = tonumber(color.cterm),
            })
        end
    end
end

apply()
vim.api.nvim_create_autocmd('ColorScheme', {
    group = vim.api.nvim_create_augroup('ChiropteraDevicons', { clear = true }),
    callback = apply,
})
EOF
