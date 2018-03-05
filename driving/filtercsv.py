fp = open("results.csv", "r");
content = fp.read();
lines = content.split("\n");
fp.close();

fp = open("results.csv", "w");
fp.write("Name,Email,Phone Number, Zip Code\n");
for line in lines:
    fp.write(line + "\n");
fp.close();
