import time

import fmt


def run_fn(fn, s, n=1000000, t=3):
    print(str(fn))

    for x in range(0, t):
        i = 0
        started = time.time()

        while i < n:
            fn(s)
            i += 1

        finished = time.time()

        print("Ran {n} times in {t}".format(n=n, t=finished-started))


## ---------------------
if __name__ == "__main__":
    # run_fn(fmt.compress_whitespace, s=' oh hai This is     nice  ')
    #run_fn(fmt.strip_tags, s='<p>oh hai.</p><p>goodbye</p>')
    run_fn(fmt.number_as_words, s='42')

