" Copyright (c) 2024-2026 Dawid Kurek <hello@dawikur.dev>

" Preamble {{{

let &background = 'light'

hi clear
if exists('syntax_on')
	syntax reset
endif

let g:colors_name = 'chiroptera_light_soft'

if !exists('g:chiroptera_italic_comments')
	let g:chiroptera_italic_comments = 1
endif

" }}} Preamble
" Colors {{{

let s:none           = {'cterm': 'NONE'                , 'gui': 'NONE'                }

let s:bg_dim         = {'cterm': '188'        , 'gui': '#dcd9ce'        }
let s:bg             = {'cterm': '251'            , 'gui': '#cfccc1'            }
let s:bg_bright      = {'cterm': '145'     , 'gui': '#b4b2a9'     }
let s:fg_dim         = {'cterm': '241'        , 'gui': '#6f6e68'        }
let s:fg             = {'cterm': '239'            , 'gui': '#585652'            }
let s:fg_bright      = {'cterm': '237'     , 'gui': '#42403d'     }
let s:red_dim        = {'cterm': '217'       , 'gui': '#febcaf'       }
let s:red            = {'cterm': '124'           , 'gui': '#ac1716'           }
let s:red_bright     = {'cterm': '88'    , 'gui': '#880009'    }
let s:green_dim      = {'cterm': '185'     , 'gui': '#d5d157'     }
let s:green          = {'cterm': '58'         , 'gui': '#5a5a00'         }
let s:green_bright   = {'cterm': '58'  , 'gui': '#434300'  }
let s:blue_dim       = {'cterm': '116'      , 'gui': '#97d7da'      }
let s:blue           = {'cterm': '23'          , 'gui': '#1b6063'          }
let s:blue_bright    = {'cterm': '23'   , 'gui': '#00484b'   }
let s:yellow_dim     = {'cterm': '216'    , 'gui': '#febf89'    }
let s:yellow         = {'cterm': '94'        , 'gui': '#834800'        }
let s:yellow_bright  = {'cterm': '58' , 'gui': '#633500' }
let s:magenta_dim    = {'cterm': '218'   , 'gui': '#feb8d6'   }
let s:magenta        = {'cterm': '95'       , 'gui': '#883d61'       }
let s:magenta_bright = {'cterm': '53', 'gui': '#6f254a'}
let s:cyan_dim       = {'cterm': '115'      , 'gui': '#8bdcc1'      }
let s:cyan           = {'cterm': '23'          , 'gui': '#02634d'          }
let s:cyan_bright    = {'cterm': '23'   , 'gui': '#004a39'   }

let s:fg_normal      = {'cterm': '239'     , 'gui': '#585652'     }
let s:fg_note        = {'cterm': '241'       , 'gui': '#6f6e68'       }
let s:fg_mark        = {'cterm': '237'       , 'gui': '#42403d'       }
let s:fg_ignore      = {'cterm': '145'     , 'gui': '#b4b2a9'     }
let s:fg_red         = {'cterm': '88'        , 'gui': '#880009'        }
let s:fg_green       = {'cterm': '58'      , 'gui': '#434300'      }
let s:fg_blue        = {'cterm': '23'       , 'gui': '#00484b'       }
let s:fg_yellow      = {'cterm': '58'     , 'gui': '#633500'     }
let s:fg_magenta     = {'cterm': '53'    , 'gui': '#6f254a'    }
let s:fg_cyan        = {'cterm': '23'       , 'gui': '#004a39'       }
let s:bg_normal      = {'cterm': '251'     , 'gui': '#cfccc1'     }
let s:bg_highlight   = {'cterm': '188'  , 'gui': '#dcd9ce'  }
let s:bg_mark        = {'cterm': '145'       , 'gui': '#b4b2a9'       }
let s:bg_red         = {'cterm': '217'        , 'gui': '#febcaf'        }
let s:bg_green       = {'cterm': '185'      , 'gui': '#d5d157'      }
let s:bg_blue        = {'cterm': '116'       , 'gui': '#97d7da'       }
let s:bg_yellow      = {'cterm': '216'     , 'gui': '#febf89'     }
let s:bg_magenta     = {'cterm': '218'    , 'gui': '#feb8d6'    }
let s:bg_cyan        = {'cterm': '115'       , 'gui': '#8bdcc1'       }
let s:ui_normal      = {'cterm': '145'     , 'gui': '#b4b2a9'     }
let s:ui_highlight   = {'cterm': '188'  , 'gui': '#dcd9ce'  }
let s:ui_red         = {'cterm': '124'        , 'gui': '#ac1716'        }
let s:ui_green       = {'cterm': '58'      , 'gui': '#5a5a00'      }
let s:ui_blue        = {'cterm': '23'       , 'gui': '#1b6063'       }
let s:ui_yellow      = {'cterm': '94'     , 'gui': '#834800'     }
let s:ui_magenta     = {'cterm': '95'    , 'gui': '#883d61'    }
let s:ui_cyan        = {'cterm': '23'       , 'gui': '#02634d'       }

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
