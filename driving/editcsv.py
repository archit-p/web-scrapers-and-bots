fp = open('final.csv', 'r');
content = fp.read()
fp.close()
lines = content.split("\n");
print(len(lines))
saved = []
count = 0
for line in lines:
    line = line.split(",")
    pop = line[-1];
    if(pop == "Population\r"):
        continue
    if(pop == '\r' or pop == ''):
        continue;
    elif(int(pop) > 180):
        saved.append(line[0])
        print(line[0])
        count += 1

fp = open('zips.csv', "w")
for save in saved:
    fp.write(save + "\n")
fp.close()
print(count)
