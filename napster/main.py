from multiprocessing import Lock, Process
from NapsterBot import NapsterBot

def main():
    login_sem = Lock();
    proxy_sem = Lock();

    procs = []
    count = 0
    while(count < 1):
        scraper = NapsterBot(login_sem, proxy_sem, 0, 0, "https://npstr.cm/tnlivr");
        proc = Process(target=scraper.main)
        procs.append(proc)
        proc.start()
        count += 1

    for proc in procs:
        proc.join()

if __name__ == "__main__":
    main()
