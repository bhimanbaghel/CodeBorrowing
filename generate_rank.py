import sys
import operator

reload(sys)
sys.setdefaultencoding('utf8')

with open("Tag_Datasheet.txt",'r') as data_file:
	datasheet = data_file.readlines()

with open("230_words.txt",'r') as word_file:
	wordlist = word_file.readlines()

word_count = {}
words = []
for word in wordlist:
	w = (word.strip('\n')).strip('\r')
	words.append(w) 
	word_count[str(w +'EN:EN')] = 0
	word_count[str(w +'EN:HI')] = 0
	word_count[str(w +'EN:CME')] = 0
	word_count[str(w +'EN:CMH')] = 0
	word_count[str(w +'EN:CMEQ')] = 0
	word_count[str(w +'HI:EN')] = 0
	word_count[str(w +'HI:HI')] = 0
	word_count[str(w +'HI:CME')] = 0
	word_count[str(w +'HI:CMH')] = 0
	word_count[str(w +'HI:CMEQ')] = 0

print words
print word_count

for lineno in range(0,len(datasheet)):
	print lineno
	line = datasheet[lineno].strip('\n')
	data = line.split('\t')
	tag = data[0].split("/")[0]
	data1 = data[1].split(" ")
	for i in range(0, len(data1)):
		try:
			word = data1[i].split('/')
			if word[0] in words:
				if word[1] == 'EN' or word[1] == 'HI':
					print word[0]
					word_count[str(word[0] + word[1] + ':' + tag)] += 1
		except IndexError:
			continue

utr = {}
for w in words:
	try:
		utr[w] = float(0.700*word_count[str(w +'HI:HI')] + 0.200*word_count[str(w +'HI:CMH')] + 0.75*word_count[str(w +'EN:CMH')] + 0.15*word_count[str(w +'HI:CMEQ')]+0.10*word_count[str(w +'EN:CMEQ')])/float(word_count[str(w +'EN:EN')])
	except ZeroDivisionError:
		utr[w] = float(0.700*word_count[str(w +'HI:HI')] + 0.200*word_count[str(w +'HI:CMH')] + 0.75*word_count[str(w +'EN:CMH')] + 0.15*word_count[str(w +'HI:CMEQ')]+0.10*word_count[str(w +'EN:CMEQ')])/0.01

sorted_utr = sorted(utr.items(), key=operator.itemgetter(1), reverse=True)

print sorted_utr

rank_word = {}
i=1
for word in sorted_utr:
	rank_word[word[0]] = i
	i+=1

print rank_word
rank_file = open("Rank_list.txt","w") 
for word in words:
	rank_file.write(word + ", " + str(utr[word]) + ", " +str(rank_word[word])  + "\n")

rank_file.close()
