" Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>

function! ChiropteraHL(group, fg, bg, ...) abort
	let l:fg = has_key(a:fg, 'normal') ? a:fg.normal : a:fg
	let l:bg = has_key(a:bg, 'normal') ? a:bg.normal : a:bg
	let l:attr = a:0 == 0 ? 'NONE' : a:1

	execute 'highlight! ' . a:group .
		\ ' ctermfg=' . l:fg.cterm . ' guifg=' . l:fg.gui .
		\ ' ctermbg=' . l:bg.cterm . ' guibg=' . l:bg.gui .
		\ ' cterm=' . l:attr . ' gui=' . l:attr

	if a:0 >= 2
		execute 'highlight! ' . a:group . ' guisp=' . a:2.gui
	endif
endfunction

function! ChiropteraLN(group, target) abort
	execute 'highlight! link ' . a:group . ' ' . a:target
endfunction
