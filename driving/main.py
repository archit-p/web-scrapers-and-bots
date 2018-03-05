from threading import Lock
from threading import Thread
from DrivingBot import DrivingBot

def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def main():
    zipfile = open("zips.csv", "r")
    content = zipfile.read()
    zips = content.split("\n")
    zipcount = len(zips)
    numzips = zipcount/10;
    zipchunks = chunkIt(zips, 100);
    lock = Lock();
    scrapers = []
    for zipchunk in zipchunks:
        scraper = DrivingBot(zipchunk, lock);
        scraper.start()
        scrapers.append(scraper);
    for scraper in scrapers:
        scraper.join()

if __name__ == "__main__":
    main()
