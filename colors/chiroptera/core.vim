" Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>
" Core Chiroptera highlight groups shared by every variant.

"" Vim {{{

" black/white red yellow/green blue brown/orange magenta/violet/orange/gray
" red              = deleted   " energy, passion, action
" yellow           = modified  " mind, intellect
" green            = added     " balance, harmony, growth
" blue             = selected  " trust, responsibility
" magenta          = input     " harmony, emotional balance
" cyan             = output    " clarity of thought

let s:comment_attr = g:chiroptera_italic_comments ? 'italic' : 'NONE'

"        ( group-name       , fg                     , bg                       , attr  )
call ChiropteraHL('ColorColumn'     , g:chiroptera.none      , g:chiroptera.ui          )
call ChiropteraHL('Conceal'         , g:chiroptera.fg.ignore , g:chiroptera.none        )
call ChiropteraHL('Cursor'          , g:chiroptera.none      , g:chiroptera.none        , 'inverse')
call ChiropteraHL('CursorColumn'    , g:chiroptera.none      , g:chiroptera.bg.highlight)
call ChiropteraLN('CursorIM'        , 'Cursor')
call ChiropteraHL('CursorLine'      , g:chiroptera.none      , g:chiroptera.bg.highlight)
call ChiropteraHL('CursorLineNr'    , g:chiroptera.fg.note   , g:chiroptera.bg.highlight)
call ChiropteraHL('CursorLineFold'  , g:chiroptera.fg.note   , g:chiroptera.bg.highlight)
call ChiropteraHL('CursorLineSign'  , g:chiroptera.none      , g:chiroptera.bg.highlight)
call ChiropteraHL('DiffAdd'         , g:chiroptera.none      , g:chiroptera.bg.green    )
call ChiropteraHL('DiffChange'      , g:chiroptera.none      , g:chiroptera.none )
call ChiropteraHL('DiffDelete'      , g:chiroptera.none      , g:chiroptera.bg.red      )
call ChiropteraHL('DiffText'        , g:chiroptera.none      , g:chiroptera.bg.yellow   )
call ChiropteraHL('Directory'       , g:chiroptera.fg.mark   , g:chiroptera.none        , 'bold')
call ChiropteraHL('EndOfBuffer'     , g:chiroptera.none      , g:chiroptera.none        )
call ChiropteraHL('ErrorMsg'        , g:chiroptera.ui.red    , g:chiroptera.none        )
call ChiropteraHL('FoldColumn'      , g:chiroptera.fg.ignore , g:chiroptera.none        )
call ChiropteraHL('Folded'          , g:chiroptera.fg.note   , g:chiroptera.ui          , 'italic')
call ChiropteraHL('IncSearch'       , g:chiroptera.none      , g:chiroptera.none        , 'inverse,underline')
call ChiropteraHL('LineNr'          , g:chiroptera.fg.note   , g:chiroptera.none        )
call ChiropteraLN('LineNrAbove'     , 'LineNr')
call ChiropteraLN('LineNrBelow'     , 'LineNr')
call ChiropteraHL('MatchParen'      , g:chiroptera.none      , g:chiroptera.bg.blue     , 'bold')
call ChiropteraHL('ModeMsg'         , g:chiroptera.fg.cyan   , g:chiroptera.none        , 'italic')
call ChiropteraLN('MoreMsg'         , 'ModeMsg')
call ChiropteraHL('MsgArea'         , g:chiroptera.fg.note   , g:chiroptera.none        )
call ChiropteraHL('MsgSeparator'    , g:chiroptera.none      , g:chiroptera.none        )
call ChiropteraHL('NonText'         , g:chiroptera.fg.note   , g:chiroptera.none        , 'italic')
call ChiropteraHL('Normal'          , g:chiroptera.fg        , g:chiroptera.bg          )
call ChiropteraHL('NormalFloat'     , g:chiroptera.fg        , g:chiroptera.ui          )
call ChiropteraHL('NormalNC'        , g:chiroptera.fg.note   , g:chiroptera.bg          )
call ChiropteraHL('FloatBorder'     , g:chiroptera.fg.note   , g:chiroptera.ui          )
call ChiropteraLN('FloatFooter'     , 'FloatBorder')
call ChiropteraHL('FloatTitle'      , g:chiroptera.fg.mark   , g:chiroptera.ui          , 'bold')
call ChiropteraHL('Pmenu'           , g:chiroptera.fg        , g:chiroptera.ui          )
call ChiropteraHL('PmenuExtra'      , g:chiroptera.fg.note   , g:chiroptera.ui          )
call ChiropteraHL('PmenuExtraSel'   , g:chiroptera.fg.note   , g:chiroptera.ui.highlight)
call ChiropteraHL('PmenuKind'       , g:chiroptera.fg.cyan   , g:chiroptera.ui          )
call ChiropteraHL('PmenuKindSel'    , g:chiroptera.fg.cyan   , g:chiroptera.ui.highlight)
call ChiropteraHL('PmenuMatch'      , g:chiroptera.fg.mark   , g:chiroptera.ui          , 'bold')
call ChiropteraHL('PmenuMatchSel'   , g:chiroptera.fg.mark   , g:chiroptera.ui.highlight, 'bold')
call ChiropteraHL('PmenuSbar'       , g:chiroptera.none      , g:chiroptera.ui          )
call ChiropteraHL('PmenuSel'        , g:chiroptera.fg        , g:chiroptera.ui.highlight)
call ChiropteraHL('PmenuThumb'      , g:chiroptera.fg.note   , g:chiroptera.none        , 'inverse')
call ChiropteraHL('Question'        , g:chiroptera.fg.magenta, g:chiroptera.none        , 'italic')
call ChiropteraHL('QuickFixLine'    , g:chiroptera.fg.blue   , g:chiroptera.none        )
call ChiropteraHL('Search'          , g:chiroptera.none      , g:chiroptera.none        , 'inverse')
call ChiropteraHL('SignColumn'      , g:chiroptera.none      , g:chiroptera.none        )
call ChiropteraHL('SpecialKey'      , g:chiroptera.fg.ignore , g:chiroptera.none        )
call ChiropteraHL('SpellBad'        , g:chiroptera.fg.red    , g:chiroptera.none        , 'undercurl', g:chiroptera.fg.red)
call ChiropteraHL('SpellCap'        , g:chiroptera.fg.yellow , g:chiroptera.none        , 'undercurl', g:chiroptera.fg.yellow)
call ChiropteraHL('SpellLocal'      , g:chiroptera.fg.blue   , g:chiroptera.none        , 'undercurl', g:chiroptera.fg.blue)
call ChiropteraHL('SpellRare'       , g:chiroptera.fg.magenta, g:chiroptera.none        , 'undercurl', g:chiroptera.fg.magenta)
call ChiropteraHL('StatusLine'      , g:chiroptera.none      , g:chiroptera.bg          )
call ChiropteraHL('StatusLineNC'    , g:chiroptera.fg.note   , g:chiroptera.bg          )
call ChiropteraLN('StatusLineTerm'  , 'StatusLine')
call ChiropteraLN('StatusLineTermNC', 'StatusLineNC')
call ChiropteraHL('Substitute'      , g:chiroptera.none      , g:chiroptera.bg.yellow   )
call ChiropteraHL('TabLine'         , g:chiroptera.fg.note   , g:chiroptera.none        )
call ChiropteraHL('TabLineFill'     , g:chiroptera.fg.note   , g:chiroptera.none        )
call ChiropteraHL('TabLineSel'      , g:chiroptera.fg        , g:chiroptera.none        )
call ChiropteraLN('TermCursor'      , 'Cursor')
call ChiropteraHL('TermCursorNC'    , g:chiroptera.fg.note   , g:chiroptera.none        , 'inverse')
call ChiropteraHL('Title'           , g:chiroptera.fg.cyan   , g:chiroptera.none        )
call ChiropteraHL('VertSplit'       , g:chiroptera.ui        , g:chiroptera.none        , 'bold')
call ChiropteraHL('WinBar'          , g:chiroptera.fg        , g:chiroptera.none        , 'bold')
call ChiropteraHL('WinBarNC'        , g:chiroptera.fg.note   , g:chiroptera.none        )
call ChiropteraHL('WinSeparator'    , g:chiroptera.ui        , g:chiroptera.none        , 'bold')
call ChiropteraHL('Visual'          , g:chiroptera.none      , g:chiroptera.bg.blue     )
call ChiropteraLN('VisualNOS'       , 'Visual')
call ChiropteraHL('WarningMsg'      , g:chiroptera.fg.yellow , g:chiroptera.none        )
call ChiropteraHL('Whitespace'      , g:chiroptera.fg.ignore , g:chiroptera.none        )
call ChiropteraHL('WildMenu'        , g:chiroptera.none      , g:chiroptera.ui          , 'inverse')
call ChiropteraLN('lCursor'         , 'Cursor')
"" }}} Vim
"" Syntax {{{
" see |group-name|

call ChiropteraHL('Comment'           , g:chiroptera.raw.fg_dim        , g:chiroptera.raw.none      , s:comment_attr)
call ChiropteraHL('Constant'          , g:chiroptera.raw.cyan          , g:chiroptera.raw.none      )
	call ChiropteraHL('Boolean'       , g:chiroptera.raw.magenta_bright, g:chiroptera.raw.none      )
	call ChiropteraHL('Character'     , g:chiroptera.raw.yellow        , g:chiroptera.raw.none      )
	call ChiropteraHL('Number'        , g:chiroptera.raw.blue          , g:chiroptera.raw.none      )
	call ChiropteraLN('Float'         , 'Number')
	call ChiropteraHL('String'        , g:chiroptera.raw.green         , g:chiroptera.raw.none      )
call ChiropteraHL('Error'             , g:chiroptera.raw.none          , g:chiroptera.raw.red_dim   )
call ChiropteraHL('Identifier'        , g:chiroptera.raw.fg_bright     , g:chiroptera.raw.none      )
	call ChiropteraHL('Function'      , g:chiroptera.raw.magenta_bright, g:chiroptera.raw.none      )
call ChiropteraHL('Ignore'            , g:chiroptera.raw.none          , g:chiroptera.raw.none      )
call ChiropteraHL('PreProc'           , g:chiroptera.raw.magenta       , g:chiroptera.raw.none      )
	call ChiropteraLN('Define'        , 'PreProc')
	call ChiropteraLN('Include'       , 'PreProc')
	call ChiropteraHL('Macro'         , g:chiroptera.raw.cyan_bright   , g:chiroptera.raw.none      )
	call ChiropteraLN('PreCondit'     , 'PreProc')
call ChiropteraHL('Special'           , g:chiroptera.raw.magenta_bright, g:chiroptera.raw.none      )
	call ChiropteraHL('SpecialChar'   , g:chiroptera.raw.yellow_bright , g:chiroptera.raw.none      )
	call ChiropteraHL('Tag'           , g:chiroptera.raw.fg_bright     , g:chiroptera.raw.none      , 'bold')
	call ChiropteraHL('Delimiter'     , g:chiroptera.raw.none          , g:chiroptera.raw.none      )
	call ChiropteraHL('SpecialComment', g:chiroptera.raw.magenta       , g:chiroptera.raw.none      )
	call ChiropteraHL('Debug'         , g:chiroptera.raw.none          , g:chiroptera.raw.blue_dim  )
call ChiropteraHL('Statement'         , g:chiroptera.raw.yellow        , g:chiroptera.raw.none      )
	call ChiropteraHL('Conditional'   , g:chiroptera.raw.red           , g:chiroptera.raw.none      )
	call ChiropteraHL('Exception'     , g:chiroptera.raw.red_bright    , g:chiroptera.raw.none      )
	call ChiropteraLN('Keyword'       , 'Statement')
	call ChiropteraHL('Label'         , g:chiroptera.raw.cyan          , g:chiroptera.raw.none      )
	call ChiropteraHL('Operator'      , g:chiroptera.raw.magenta       , g:chiroptera.raw.none      )
	call ChiropteraHL('Repeat'        , g:chiroptera.raw.red           , g:chiroptera.raw.none      )
call ChiropteraHL('Todo'              , g:chiroptera.raw.yellow_bright , g:chiroptera.raw.none      , 'bold')
call ChiropteraHL('Type'              , g:chiroptera.raw.blue          , g:chiroptera.raw.none      )
	call ChiropteraHL('StorageClass'  , g:chiroptera.raw.red           , g:chiroptera.raw.none      )
	call ChiropteraLN('Structure'     , 'Type')
	call ChiropteraHL('Typedef'       , g:chiroptera.raw.cyan_bright   , g:chiroptera.raw.none      )
call ChiropteraHL('Underlined'        , g:chiroptera.raw.none          , g:chiroptera.raw.none      , 'underline')

call ChiropteraLN('Added'             , 'DiffAdd')
call ChiropteraLN('Changed'           , 'DiffChange')
call ChiropteraLN('Removed'           , 'DiffDelete')

"" }}} Syntax
"" Diagnostics and LSP {{{

call ChiropteraHL('DiagnosticError'              , g:chiroptera.fg.red    , g:chiroptera.none)
call ChiropteraHL('DiagnosticWarn'               , g:chiroptera.fg.yellow , g:chiroptera.none)
call ChiropteraHL('DiagnosticInfo'               , g:chiroptera.fg.blue   , g:chiroptera.none)
call ChiropteraHL('DiagnosticHint'               , g:chiroptera.fg.cyan   , g:chiroptera.none)
call ChiropteraHL('DiagnosticOk'                 , g:chiroptera.fg.green  , g:chiroptera.none)
call ChiropteraLN('DiagnosticSignError'          , 'DiagnosticError')
call ChiropteraLN('DiagnosticSignWarn'           , 'DiagnosticWarn')
call ChiropteraLN('DiagnosticSignInfo'           , 'DiagnosticInfo')
call ChiropteraLN('DiagnosticSignHint'           , 'DiagnosticHint')
call ChiropteraLN('DiagnosticSignOk'             , 'DiagnosticOk')
call ChiropteraHL('DiagnosticVirtualTextError'   , g:chiroptera.fg.red    , g:chiroptera.bg.red)
call ChiropteraHL('DiagnosticVirtualTextWarn'    , g:chiroptera.fg.yellow , g:chiroptera.bg.yellow)
call ChiropteraHL('DiagnosticVirtualTextInfo'    , g:chiroptera.fg.blue   , g:chiroptera.bg.blue)
call ChiropteraHL('DiagnosticVirtualTextHint'    , g:chiroptera.fg.cyan   , g:chiroptera.bg.cyan)
call ChiropteraHL('DiagnosticVirtualTextOk'      , g:chiroptera.fg.green  , g:chiroptera.bg.green)
" Keep a chromatic foreground as a terminal fallback, like Spell*. GUI uses guisp.
call ChiropteraHL('DiagnosticUnderlineError'     , g:chiroptera.fg.red    , g:chiroptera.none, 'undercurl', g:chiroptera.fg.red)
call ChiropteraHL('DiagnosticUnderlineWarn'      , g:chiroptera.fg.yellow , g:chiroptera.none, 'undercurl', g:chiroptera.fg.yellow)
call ChiropteraHL('DiagnosticUnderlineInfo'      , g:chiroptera.fg.blue   , g:chiroptera.none, 'undercurl', g:chiroptera.fg.blue)
call ChiropteraHL('DiagnosticUnderlineHint'      , g:chiroptera.fg.cyan   , g:chiroptera.none, 'undercurl', g:chiroptera.fg.cyan)
call ChiropteraHL('DiagnosticUnderlineOk'        , g:chiroptera.fg.green  , g:chiroptera.none, 'undercurl', g:chiroptera.fg.green)
call ChiropteraHL('DiagnosticDeprecated'         , g:chiroptera.fg.note   , g:chiroptera.none, 'strikethrough')
call ChiropteraHL('DiagnosticUnnecessary'        , g:chiroptera.fg.ignore , g:chiroptera.none)
call ChiropteraHL('DiagnosticFloatingError'      , g:chiroptera.fg.red    , g:chiroptera.ui)
call ChiropteraHL('DiagnosticFloatingWarn'       , g:chiroptera.fg.yellow , g:chiroptera.ui)
call ChiropteraHL('DiagnosticFloatingInfo'       , g:chiroptera.fg.blue   , g:chiroptera.ui)
call ChiropteraHL('DiagnosticFloatingHint'       , g:chiroptera.fg.cyan   , g:chiroptera.ui)
call ChiropteraHL('DiagnosticFloatingOk'         , g:chiroptera.fg.green  , g:chiroptera.ui)
call ChiropteraLN('DiagnosticVirtualLinesError'  , 'DiagnosticVirtualTextError')
call ChiropteraLN('DiagnosticVirtualLinesWarn'   , 'DiagnosticVirtualTextWarn')
call ChiropteraLN('DiagnosticVirtualLinesInfo'   , 'DiagnosticVirtualTextInfo')
call ChiropteraLN('DiagnosticVirtualLinesHint'   , 'DiagnosticVirtualTextHint')
call ChiropteraLN('DiagnosticVirtualLinesOk'     , 'DiagnosticVirtualTextOk')
call ChiropteraLN('LspReferenceText'             , 'CursorLine')
call ChiropteraLN('LspReferenceRead'             , 'CursorLine')
call ChiropteraLN('LspReferenceWrite'            , 'CursorLine')

"" }}} Diagnostics and LSP
"" Terminal {{{

if has('nvim')
	let g:terminal_color_0  = g:chiroptera.raw.bg_dim.gui
	let g:terminal_color_1  = g:chiroptera.raw.red.gui
	let g:terminal_color_2  = g:chiroptera.raw.green.gui
	let g:terminal_color_3  = g:chiroptera.raw.yellow.gui
	let g:terminal_color_4  = g:chiroptera.raw.blue.gui
	let g:terminal_color_5  = g:chiroptera.raw.magenta.gui
	let g:terminal_color_6  = g:chiroptera.raw.cyan.gui
	let g:terminal_color_7  = g:chiroptera.raw.fg.gui
	let g:terminal_color_8  = g:chiroptera.raw.bg_bright.gui
	let g:terminal_color_9  = g:chiroptera.raw.red_bright.gui
	let g:terminal_color_10 = g:chiroptera.raw.green_bright.gui
	let g:terminal_color_11 = g:chiroptera.raw.yellow_bright.gui
	let g:terminal_color_12 = g:chiroptera.raw.blue_bright.gui
	let g:terminal_color_13 = g:chiroptera.raw.magenta_bright.gui
	let g:terminal_color_14 = g:chiroptera.raw.cyan_bright.gui
	let g:terminal_color_15 = g:chiroptera.raw.fg_bright.gui
else
	let g:terminal_ansi_colors = [
		\ g:chiroptera.raw.bg_dim.gui,
		\ g:chiroptera.raw.red.gui,
		\ g:chiroptera.raw.green.gui,
		\ g:chiroptera.raw.yellow.gui,
		\ g:chiroptera.raw.blue.gui,
		\ g:chiroptera.raw.magenta.gui,
		\ g:chiroptera.raw.cyan.gui,
		\ g:chiroptera.raw.fg.gui,
		\ g:chiroptera.raw.bg_bright.gui,
		\ g:chiroptera.raw.red_bright.gui,
		\ g:chiroptera.raw.green_bright.gui,
		\ g:chiroptera.raw.yellow_bright.gui,
		\ g:chiroptera.raw.blue_bright.gui,
		\ g:chiroptera.raw.magenta_bright.gui,
		\ g:chiroptera.raw.cyan_bright.gui,
		\ g:chiroptera.raw.fg_bright.gui
		\ ]
endif

"" }}} Terminal
"" Colors {{{

call ChiropteraHL('NvimDarkBlue'    , g:chiroptera.raw.blue_dim       , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkCyan'    , g:chiroptera.raw.cyan_dim       , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkGreen'   , g:chiroptera.raw.green_dim      , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkGrey1'   , g:chiroptera.raw.bg_dim         , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkGrey2'   , g:chiroptera.raw.bg             , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkGrey3'   , g:chiroptera.raw.bg_bright      , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkGrey4'   , g:chiroptera.raw.fg_dim         , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkMagenta' , g:chiroptera.raw.magenta_dim    , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkRed'     , g:chiroptera.raw.red_dim        , g:chiroptera.raw.none)
call ChiropteraHL('NvimDarkYellow'  , g:chiroptera.raw.yellow_dim     , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightBlue'   , g:chiroptera.raw.blue_bright    , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightCyan'   , g:chiroptera.raw.cyan_bright    , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightGreen'  , g:chiroptera.raw.green_bright   , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightGrey1'  , g:chiroptera.raw.fg_bright      , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightGrey2'  , g:chiroptera.raw.fg             , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightGrey3'  , g:chiroptera.raw.fg_dim         , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightGrey4'  , g:chiroptera.raw.bg_bright      , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightMagenta', g:chiroptera.raw.magenta_bright , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightRed'    , g:chiroptera.raw.red_bright     , g:chiroptera.raw.none)
call ChiropteraHL('NvimLightYellow' , g:chiroptera.raw.yellow_bright  , g:chiroptera.raw.none)

"" }}} Colors
