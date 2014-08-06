"""This module functions are to be called from Vim with Python support"""

from hashlib import md5
from logbro.index import Index, IndexBuilder, LB_IndexError
import vim


def make_index():
    
    idx = IndexBuilder(vim.current.line)
    for n, l in enumerate(vim.current.buffer):
        idx.feed_line(l, n)
    
    orig_buffer_no = vim.eval("bufnr('%')")
    
    vim.command("new")
    
    vim.current.buffer[:] = idx.get_human_readable_repr(vim.eval("g:logbro_mask_char"))
    
    vim.command("let b:index = %s" % idx.get_index().python_repr())
    vim.command("let b:orig_buffer_no = %s" % orig_buffer_no)

def slice_into_new_buffer():

    idx = Index(vim.eval("b:index"))
    orig_buffer_no = int(vim.eval("b:orig_buffer_no"))
    
    out_buffer = []
    try:
        idx.slice_for(vim.current.line, vim.buffers[orig_buffer_no], out_buffer);

        vim.command("new")
        vim.current.buffer[:] = out_buffer
    except LB_IndexError as e:
        say(e)

def slice_into_manual_fold():

    idx = Index(vim.eval("b:index"))
    orig_buffer_no = int(vim.eval("b:orig_buffer_no"))
    
    out_buffer = []
    try:
        idx.slice_for(vim.current.line, vim.buffers[orig_buffer_no], out_buffer);

        buf = []
        buf.append('{{{')  # TODO: use Vim foldmarker instead
        buf.extend(out_buffer)
        buf.append('}}}')
        
        cline = vim.current.range.start + 1
        vim.current.buffer[cline:cline] = buf

        # configure foldings
        vim.command("set foldmethod=marker")
        if not int(vim.eval("&foldcolumn")):
            vim.command("set foldcolumn=1")
        
        # return back to the start of new folding
        vim.command(":%s" % (cline + 1))
        
    except LB_IndexError as e:
        say(e)

def dump_var():
    
    nameval = [(n, vim.eval(n)) for n in filter(lambda x: int(vim.eval("exists('%s')" % x)),
                                                vim.eval("s:track_those_vars"))]
    
    vim.command("new")
    vim.current.buffer[0] = "// ---> Dumping logbro variables --->"
    
    for n, v in nameval:
    
        vim.current.buffer.append("// %s:" % n)
        vim.current.buffer.append(repr(v))
    
    vim.command("set filetype=javascript")
    
def say(s):
    
    print 'LogBro says: "%s"' % s
