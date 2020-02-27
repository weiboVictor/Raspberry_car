import concurrent.futures
import time

start = time.time()


def do_something(seconds):
    print('Sleeping %d second(s)...'%seconds)
    time.sleep(seconds)
    return 'Done Sleeping...%d'%seconds


with concurrent.futures.ProcessPoolExecutor() as executor:
    secs = [5, 4, 3, 2, 1]
    results = executor.map(do_something, secs)

    # for result in results:
    #     print(result)

finish = time.time()

print('Finished in %d second(s)'%(round(finish-start, 2)))