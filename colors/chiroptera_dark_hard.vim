" Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>

" Preamble {{{

let &background = 'dark'

hi clear
if exists('syntax_on')
	syntax reset
endif

let g:colors_name = 'chiroptera_dark_hard'

if !exists('g:chiroptera_italic_comments')
	let g:chiroptera_italic_comments = 1
endif

" }}} Preamble
" Colors {{{

let s:none           = {'cterm': 'NONE'                , 'gui': 'NONE'                }

let s:bg_dim         = {'cterm': '233'        , 'gui': '#1d1d1b'        }
let s:bg             = {'cterm': '234'            , 'gui': '#272625'            }
let s:bg_bright      = {'cterm': '236'     , 'gui': '#3c3b38'     }
let s:fg_dim         = {'cterm': '102'        , 'gui': '#88867f'        }
let s:fg             = {'cterm': '246'            , 'gui': '#a19f97'            }
let s:fg_bright      = {'cterm': '249'     , 'gui': '#bbb8af'     }
let s:red_dim        = {'cterm': '52'       , 'gui': '#530700'       }
let s:red            = {'cterm': '209'           , 'gui': '#fe745f'           }
let s:red_bright     = {'cterm': '216'    , 'gui': '#fe9f8d'    }
let s:green_dim      = {'cterm': '234'     , 'gui': '#292800'     }
let s:green          = {'cterm': '142'         , 'gui': '#a5a329'         }
let s:green_bright   = {'cterm': '143'  , 'gui': '#c0bd44'  }
let s:blue_dim       = {'cterm': '234'      , 'gui': '#002c2e'      }
let s:blue           = {'cterm': '73'          , 'gui': '#69a9ac'          }
let s:blue_bright    = {'cterm': '116'   , 'gui': '#83c3c6'   }
let s:yellow_dim     = {'cterm': '235'    , 'gui': '#3c2000'    }
let s:yellow         = {'cterm': '172'        , 'gui': '#e28a2f'        }
let s:yellow_bright  = {'cterm': '215' , 'gui': '#fea44b' }
let s:magenta_dim    = {'cterm': '53'   , 'gui': '#500430'   }
let s:magenta        = {'cterm': '175'       , 'gui': '#d886aa'       }
let s:magenta_bright = {'cterm': '218', 'gui': '#f49fc4'}
let s:cyan_dim       = {'cterm': '234'      , 'gui': '#002d21'      }
let s:cyan           = {'cterm': '72'          , 'gui': '#5dad94'          }
let s:cyan_bright    = {'cterm': '115'   , 'gui': '#77c8ad'   }

let s:fg_normal      = {'cterm': '246'     , 'gui': '#a19f97'     }
let s:fg_note        = {'cterm': '102'       , 'gui': '#88867f'       }
let s:fg_mark        = {'cterm': '249'       , 'gui': '#bbb8af'       }
let s:fg_ignore      = {'cterm': '236'     , 'gui': '#3c3b38'     }
let s:fg_red         = {'cterm': '216'        , 'gui': '#fe9f8d'        }
let s:fg_green       = {'cterm': '143'      , 'gui': '#c0bd44'      }
let s:fg_blue        = {'cterm': '116'       , 'gui': '#83c3c6'       }
let s:fg_yellow      = {'cterm': '215'     , 'gui': '#fea44b'     }
let s:fg_magenta     = {'cterm': '218'    , 'gui': '#f49fc4'    }
let s:fg_cyan        = {'cterm': '115'       , 'gui': '#77c8ad'       }
let s:bg_normal      = {'cterm': '234'     , 'gui': '#272625'     }
let s:bg_highlight   = {'cterm': '233'  , 'gui': '#1d1d1b'  }
let s:bg_mark        = {'cterm': '236'       , 'gui': '#3c3b38'       }
let s:bg_red         = {'cterm': '52'        , 'gui': '#530700'        }
let s:bg_green       = {'cterm': '234'      , 'gui': '#292800'      }
let s:bg_blue        = {'cterm': '234'       , 'gui': '#002c2e'       }
let s:bg_yellow      = {'cterm': '235'     , 'gui': '#3c2000'     }
let s:bg_magenta     = {'cterm': '53'    , 'gui': '#500430'    }
let s:bg_cyan        = {'cterm': '234'       , 'gui': '#002d21'       }
let s:ui_normal      = {'cterm': '236'     , 'gui': '#3c3b38'     }
let s:ui_highlight   = {'cterm': '233'  , 'gui': '#1d1d1b'  }
let s:ui_red         = {'cterm': '209'        , 'gui': '#fe745f'        }
let s:ui_green       = {'cterm': '142'      , 'gui': '#a5a329'      }
let s:ui_blue        = {'cterm': '73'       , 'gui': '#69a9ac'       }
let s:ui_yellow      = {'cterm': '172'     , 'gui': '#e28a2f'     }
let s:ui_magenta     = {'cterm': '175'    , 'gui': '#d886aa'    }
let s:ui_cyan        = {'cterm': '72'       , 'gui': '#5dad94'       }

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
