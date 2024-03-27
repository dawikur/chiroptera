" Template: token values are generated

let g:chiroptera_mode = '{mode}'
let g:chiroptera_contrast = '{contrast}'
let s:chiroptera_bg_rgb = '#{bg.rgb}'
let s:normal_ansi = {fg.normal.256}
let s:comment_ansi = {fg.note.16}

hi Normal   guifg={fg.normal.hex} guibg={bg.normal.hex}
hi Comment  guifg={fg.note.hex}
hi Function guifg={fg.blue.hex}
hi String   guifg={fg.green.hex}
