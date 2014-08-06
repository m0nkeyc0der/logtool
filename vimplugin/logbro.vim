" LogBro config vars
let g:logbro_mask_char = "."
let s:track_those_vars = [ "b:index", "b:orig_buffer_no", "g:logbro_mask_char", "s:track_those_vars" ]


" LogBro command mapping
command LBIndex  call LogBro_MakeIndex()
command LBSlice  call LogBro_SliceIntoNewBuf()
command LBSlicef call LogBro_SliceIntoManualFold()
command LBVars   call LogBro_DumpVar()


" LogBro function that calls their Python counter parties

function! LogBro_MakeIndex()

    py from logbro.vimplugin import make_index
    py make_index()

endfunction


function! LogBro_SliceIntoNewBuf()

    py from logbro.vimplugin import say, slice_into_new_buffer

    if !exists("b:index")
        py say("No index for this buffer")
        return
    endif

    py slice_into_new_buffer()

endfunction


function! LogBro_SliceIntoManualFold()

    py from logbro.vimplugin import say, slice_into_manual_fold

    if !exists("b:index")
        py say("No index for this buffer")
        return
    endif

    py slice_into_manual_fold()

endfunction


" Dump LogBro internal variables list to new buffer
function! LogBro_DumpVar()

    py from logbro.vimplugin import dump_var
    py dump_var()

endfunction
