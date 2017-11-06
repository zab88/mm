from os.path import splitext, split
import subprocess
import os


class OSUtils:
    """Utilities to work with shell and filesystem"""

    @classmethod
    def run_subprocess(cls, args_list, shellind=False):
        """Create subprocess and get stdout and stderr"""
        # print(' '.join(args_list))
        proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shellind)
        proc_out, proc_err = proc.communicate()
        out, err = [], []
        if proc_out is not None and len(proc_out) > 0:
            out = proc_out.decode(errors='ignore')
        if proc_err is not None and len(proc_err) > 0:
            err = proc_err.decode(errors='ignore')
        return out, err

    @classmethod
    def checkout_path(cls, path_to_file):
        """Returns ('/home/', 'file.ext', 'file') for input '/home/file.ext'"""
        dir_file = split(path_to_file)[0] + os.sep
        name_file = split(path_to_file)[1]
        basename_file = splitext(name_file)[0]
        return dir_file, name_file, basename_file
