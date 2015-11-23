import subprocess


class ShellException(Exception):
    pass


def run(cmd, err_msg=None, return_result=False, *args, **kwargs):
    """
    >>> run('echo hi', return_result=True)
    'hi'

    >>> run('echo Pass', return_result=False)

    """
    if __debug__ and kwargs.get('verbose', False):
        print("calling: `{cmd}`".format(cmd=cmd))

    if return_result:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)

        return result.rstrip('\n')

    else:
        err = subprocess.call(cmd, shell=True, stderr=subprocess.STDOUT)

        if err:
            if __debug__ and kwargs.get('verbose', False) and err_msg:
                print(err_msg)

            raise ShellException("Running: `{cmd}` Error: `{err}` Msg: `{msg}`".format(cmd=cmd, err=err, msg=err_msg))


## ---------------------
if __name__ == "__main__":
    import doctest
    print("[shell.py] Testing...")
    doctest.testmod()
    print("Done.")
