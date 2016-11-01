### Copyright (C) 2005-2016 Peter Williams <pwil3058@gmail.com>
###
### This program is free software; you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation; version 2 of the License only.
###
### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.
###
### You should have received a copy of the GNU General Public License
### along with this program; if not, write to the Free Software
### Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

def create_flag_generator():
    """
    Create a new flag generator
    """
    next_flag_num = 0
    while True:
        yield 2 ** next_flag_num
        next_flag_num += 1

def path_rel_home(path):
    """Return the given path as a path relative to user's home directory."""
    import os
    import urllib.parse
    pr = urllib.parse.urlparse(path)
    if pr.scheme and pr.scheme != "file":
        return path
    if pr.path.startswith("~" + os.sep):
        return pr.path
    return os.path.join("~", os.path.relpath(os.path.abspath(pr.path), os.getenv("HOME")))

def cwd_rel_home():
    """Return path of current working directory relative to user's home
    directory.
    """
    import os
    return path_rel_home(os.getcwd())

quote_if_needed = lambda string: string if string.count(" ") == 0 else "\"" + string + "\""

quoted_join = lambda strings, joint=" ": joint.join((quote_if_needed(file_path) for file_path in strings))

def strings_to_quoted_list_string(strings):
    if len(strings) == 1:
        return quote_if_needed(strings[0])
    return quoted_join(strings[:-1], ", ") + _(" and ") + quote_if_needed(strings[-1])

def get_file_contents(srcfile, decompress=True):
    """
    Get the contents of filename to text after (optionally) applying
    decompression as indicated by filename's suffix.
    """
    if decompress:
        import bz2
        import gzip
        import os
        import sys
        from . import runext
        _root, ext = os.path.splitext(srcfile)
        res = 0
        if ext == ".gz":
            return gzip.open(srcfile).read()
        elif ext == ".bz2":
            bz2f = bz2.BZ2File(srcfile, "r")
            text = bz2f.read()
            bz2f.close()
            return text
        elif ext == ".xz":
            res, text, serr = runext.run_cmd(["xz", "-cd", srcfile])
        elif ext == ".lzma":
            res, text, serr = runext.run_cmd(["lzma", "-cd", srcfile])
        else:
            return open(srcfile).read()
        if res != 0:
            sys.stderr.write(serr)
        return text
    else:
        return open(srcfile).read()

def set_file_contents(filename, text, compress=True):
    """
    Set the contents of filename to text after (optionally) applying
    compression as indicated by filename's suffix.
    """
    from . import CmdResult
    if compress:
        import bz2
        import gzip
        import os
        import sys
        from . import runext
        _root, ext = os.path.splitext(filename)
        res = 0
        if ext == ".gz":
            try:
                gzip.open(filename, "wb").write(text)
                return True
            except (IOError, zlib.error):
                return False
        elif ext == ".bz2":
            try:
                bz2f = bz2.BZ2File(filename, "w")
                text = bz2f.write(text)
                bz2f.close()
                return True
            except IOError:
                return False
        elif ext == ".xz":
            res, text, serr = run_cmd("xz -c", text)
        elif ext == ".lzma":
            res, text, serr = run_cmd("lzma -c", text)
        if res != 0:
            sys.stderr.write(serr)
            return False
    try:
        open(filename, "w").write(text)
    except IOError as edata:
        return CmdResult.error(stderr=str(edata))
    return CmdResult.ok()

def get_first_in_envar(envar_list, default=""):
    import os
    for envar in envar_list:
        try:
            value = os.environ[envar]
            if value != "":
                return value
        except KeyError:
            continue
    return default

def turn_off_write(mode):
    """Return the given mode with the write bits turned off"""
    import stat
    return mode & ~(stat.S_IWUSR|stat.S_IWGRP|stat.S_IWOTH)

def get_mode_for_file(filepath):
    import os
    try:
        return os.stat(filepath).st_mode
    except OSError:
        return None

def do_turn_off_write_for_file(filepath):
    """Turn off write bits for name file and return original mode"""
    import os
    mode = get_mode_for_file(filepath)
    os.chmod(filepath, turn_off_write(mode))
    return mode

def is_utf8_compliant(text):
    try:
        text.encode("utf-8")
    except UnicodeError:
        return False
    return True

ISO_8859_CODECS = ["iso-8859-{0}".format(x) for x in range(1, 17)]
ISO_2022_CODECS = ["iso-2022-jp", "iso-2022-kr"] + \
    ["iso-2022-jp-{0}".format(x) for x in list(range(1, 3)) + ["2004", "ext"]]

def make_utf8_compliant(text):
    """Return a UTF-8 compliant version of text"""
    if text is None:
        return ""
    if isinstance(text, bytes):
        return text.decode("utf-8")
    elif is_utf8_compliant(text):
        return text
    for codec in ISO_8859_CODECS + ISO_2022_CODECS:
        try:
            text = unicode(text, codec).encode("utf-8")
            return text
        except UnicodeError:
            continue
    raise UnicodeError

def ensure_file_dir_exists(filepath):
    import os
    file_dir = os.path.dirname(filepath)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

def convert_patchname_to_filename(patchname):
    import re
    repl = options.get("export", "replace_spc_in_name_with")
    if isinstance(repl, str):
        return re.sub("(\s+)", repl, patchname.strip())
    else:
        return patchname

def get_sha1_for_file(filepath):
    import hashlib
    import os
    if os.path.isfile(filepath):
        return hashlib.sha1(open(filepath).read()).hexdigest()
    return None

def get_git_hash_for_content(content):
    import hashlib
    h = hashlib.sha1("blob {0}\000".format(len(content)).encode())
    h.update(content)
    return h.hexdigest()

def get_git_hash_for_file(filepath):
    import hashlib
    import os
    if os.path.isfile(filepath):
        h = hashlib.sha1("blob {0}\000".format(os.path.getsize(filepath)).encode())
        h.update(open(filepath, "rb").read())
        return h.hexdigest()
    return None

def iter_chunks(iterable, chunk_size):
    """iterate over "iterable" in chunks of size "chunk_size" at a time
    leaving client to worry about an incomplete chunk at the end if
    that occasion arises
    """
    import itertools
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, chunk_size))
       if not chunk:
           return
       yield chunk
