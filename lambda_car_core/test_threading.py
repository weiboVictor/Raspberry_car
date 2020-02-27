import concurrent.futures
import time

start = time.perf_counter()


def do_one():
    print('Sleeping 3 second(s)...')
    time.sleep(3)
    return 'Done Sleeping... 3'

def do_two():
    print('Sleeping 2 second(s)...')
    time.sleep(3)
    return 'Done Sleeping... 2'


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = []
    for _ in range(10):
        result = executor.submit(do_one)
        results.append(result)
    for _ in range(10):
        result = executor.submit(do_two)
        results.append(result)

print(results)
    # for result in results:
    #     print(result)

# threads = []

# for _ in range(10):
#     t = threading.Thread(target=do_something, args=[1.5])
#     t.start()
#     threads.append(t)

# for thread in threads:
#     thread.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')