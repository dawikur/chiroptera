" Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>

" Preamble {{{

let &background = '{mode}'

hi clear
if exists('syntax_on')
	syntax reset
endif

let g:colors_name = '{name}_{mode}_{contrast}'

if !exists('g:chiroptera_italic_comments')
	let g:chiroptera_italic_comments = 1
endif

" }}} Preamble
" Colors {{{

let s:none           = {'cterm': 'NONE'                , 'gui': 'NONE'                }

let s:bg_dim         = {'cterm': '{bg.dim.256}'        , 'gui': '{bg.dim.hex}'        }
let s:bg             = {'cterm': '{bg.256}'            , 'gui': '{bg.hex}'            }
let s:bg_bright      = {'cterm': '{bg.bright.256}'     , 'gui': '{bg.bright.hex}'     }
let s:fg_dim         = {'cterm': '{fg.dim.256}'        , 'gui': '{fg.dim.hex}'        }
let s:fg             = {'cterm': '{fg.256}'            , 'gui': '{fg.hex}'            }
let s:fg_bright      = {'cterm': '{fg.bright.256}'     , 'gui': '{fg.bright.hex}'     }
let s:red_dim        = {'cterm': '{red.dim.256}'       , 'gui': '{red.dim.hex}'       }
let s:red            = {'cterm': '{red.256}'           , 'gui': '{red.hex}'           }
let s:red_bright     = {'cterm': '{red.bright.256}'    , 'gui': '{red.bright.hex}'    }
let s:green_dim      = {'cterm': '{green.dim.256}'     , 'gui': '{green.dim.hex}'     }
let s:green          = {'cterm': '{green.256}'         , 'gui': '{green.hex}'         }
let s:green_bright   = {'cterm': '{green.bright.256}'  , 'gui': '{green.bright.hex}'  }
let s:blue_dim       = {'cterm': '{blue.dim.256}'      , 'gui': '{blue.dim.hex}'      }
let s:blue           = {'cterm': '{blue.256}'          , 'gui': '{blue.hex}'          }
let s:blue_bright    = {'cterm': '{blue.bright.256}'   , 'gui': '{blue.bright.hex}'   }
let s:yellow_dim     = {'cterm': '{yellow.dim.256}'    , 'gui': '{yellow.dim.hex}'    }
let s:yellow         = {'cterm': '{yellow.256}'        , 'gui': '{yellow.hex}'        }
let s:yellow_bright  = {'cterm': '{yellow.bright.256}' , 'gui': '{yellow.bright.hex}' }
let s:magenta_dim    = {'cterm': '{magenta.dim.256}'   , 'gui': '{magenta.dim.hex}'   }
let s:magenta        = {'cterm': '{magenta.256}'       , 'gui': '{magenta.hex}'       }
let s:magenta_bright = {'cterm': '{magenta.bright.256}', 'gui': '{magenta.bright.hex}'}
let s:cyan_dim       = {'cterm': '{cyan.dim.256}'      , 'gui': '{cyan.dim.hex}'      }
let s:cyan           = {'cterm': '{cyan.256}'          , 'gui': '{cyan.hex}'          }
let s:cyan_bright    = {'cterm': '{cyan.bright.256}'   , 'gui': '{cyan.bright.hex}'   }

let s:fg_normal      = {'cterm': '{fg.normal.256}'     , 'gui': '{fg.normal.hex}'     }
let s:fg_note        = {'cterm': '{fg.note.256}'       , 'gui': '{fg.note.hex}'       }
let s:fg_mark        = {'cterm': '{fg.mark.256}'       , 'gui': '{fg.mark.hex}'       }
let s:fg_ignore      = {'cterm': '{fg.ignore.256}'     , 'gui': '{fg.ignore.hex}'     }
let s:fg_red         = {'cterm': '{fg.red.256}'        , 'gui': '{fg.red.hex}'        }
let s:fg_green       = {'cterm': '{fg.green.256}'      , 'gui': '{fg.green.hex}'      }
let s:fg_blue        = {'cterm': '{fg.blue.256}'       , 'gui': '{fg.blue.hex}'       }
let s:fg_yellow      = {'cterm': '{fg.yellow.256}'     , 'gui': '{fg.yellow.hex}'     }
let s:fg_magenta     = {'cterm': '{fg.magenta.256}'    , 'gui': '{fg.magenta.hex}'    }
let s:fg_cyan        = {'cterm': '{fg.cyan.256}'       , 'gui': '{fg.cyan.hex}'       }
let s:bg_normal      = {'cterm': '{bg.normal.256}'     , 'gui': '{bg.normal.hex}'     }
let s:bg_highlight   = {'cterm': '{bg.highlight.256}'  , 'gui': '{bg.highlight.hex}'  }
let s:bg_mark        = {'cterm': '{bg.mark.256}'       , 'gui': '{bg.mark.hex}'       }
let s:bg_red         = {'cterm': '{bg.red.256}'        , 'gui': '{bg.red.hex}'        }
let s:bg_green       = {'cterm': '{bg.green.256}'      , 'gui': '{bg.green.hex}'      }
let s:bg_blue        = {'cterm': '{bg.blue.256}'       , 'gui': '{bg.blue.hex}'       }
let s:bg_yellow      = {'cterm': '{bg.yellow.256}'     , 'gui': '{bg.yellow.hex}'     }
let s:bg_magenta     = {'cterm': '{bg.magenta.256}'    , 'gui': '{bg.magenta.hex}'    }
let s:bg_cyan        = {'cterm': '{bg.cyan.256}'       , 'gui': '{bg.cyan.hex}'       }
let s:ui_normal      = {'cterm': '{ui.normal.256}'     , 'gui': '{ui.normal.hex}'     }
let s:ui_highlight   = {'cterm': '{ui.highlight.256}'  , 'gui': '{ui.highlight.hex}'  }
let s:ui_red         = {'cterm': '{ui.red.256}'        , 'gui': '{ui.red.hex}'        }
let s:ui_green       = {'cterm': '{ui.green.256}'      , 'gui': '{ui.green.hex}'      }
let s:ui_blue        = {'cterm': '{ui.blue.256}'       , 'gui': '{ui.blue.hex}'       }
let s:ui_yellow      = {'cterm': '{ui.yellow.256}'     , 'gui': '{ui.yellow.hex}'     }
let s:ui_magenta     = {'cterm': '{ui.magenta.256}'    , 'gui': '{ui.magenta.hex}'    }
let s:ui_cyan        = {'cterm': '{ui.cyan.256}'       , 'gui': '{ui.cyan.hex}'       }

" }}} Colors
" Palette {{{

let g:chiroptera = {
	\     'none': s:none,
	\     'fg' : {
	\         'normal'   : s:fg_normal,
	\         'note'     : s:fg_note,
	\         'mark'     : s:fg_mark,
	\         'ignore'   : s:fg_ignore,
	\
	\         'red'      : s:fg_red,
	\         'green'    : s:fg_green,
	\         'blue'     : s:fg_blue,
	\         'yellow'   : s:fg_yellow,
	\         'magenta'  : s:fg_magenta,
	\         'cyan'     : s:fg_cyan,
	\     },
	\     'bg' : {
	\         'normal'   : s:bg_normal,
	\         'highlight': s:bg_highlight,
	\         'mark'     : s:bg_mark,
	\
	\         'red'      : s:bg_red,
	\         'green'    : s:bg_green,
	\         'blue'     : s:bg_blue,
	\         'yellow'   : s:bg_yellow,
	\         'magenta'  : s:bg_magenta,
	\         'cyan'     : s:bg_cyan,
	\     },
	\     'ui' : {
	\         'normal'   : s:ui_normal,
	\         'highlight': s:ui_highlight,
	\
	\         'red'      : s:ui_red,
	\         'green'    : s:ui_green,
	\         'blue'     : s:ui_blue,
	\         'yellow'   : s:ui_yellow,
	\         'magenta'  : s:ui_magenta,
	\         'cyan'     : s:ui_cyan,
	\     },
	\ }

let g:chiroptera.raw = {
	\ 'none'             : s:none,
	\ 'bg_dim'           : s:bg_dim,
	\ 'bg'               : s:bg,
	\ 'bg_bright'        : s:bg_bright,
	\ 'fg_dim'           : s:fg_dim,
	\ 'fg'               : s:fg,
	\ 'fg_bright'        : s:fg_bright,
	\ 'red_dim'          : s:red_dim,
	\ 'red'              : s:red,
	\ 'red_bright'       : s:red_bright,
	\ 'green_dim'        : s:green_dim,
	\ 'green'            : s:green,
	\ 'green_bright'     : s:green_bright,
	\ 'blue_dim'         : s:blue_dim,
	\ 'blue'             : s:blue,
	\ 'blue_bright'      : s:blue_bright,
	\ 'yellow_dim'       : s:yellow_dim,
	\ 'yellow'           : s:yellow,
	\ 'yellow_bright'    : s:yellow_bright,
	\ 'magenta_dim'      : s:magenta_dim,
	\ 'magenta'          : s:magenta,
	\ 'magenta_bright'   : s:magenta_bright,
	\ 'cyan_dim'         : s:cyan_dim,
	\ 'cyan'             : s:cyan,
	\ 'cyan_bright'      : s:cyan_bright,
	\ }

" }}} Palette

runtime  colors/chiroptera/utils.vim
runtime  colors/chiroptera/core.vim
runtime! colors/chiroptera/plugins/*.vim
