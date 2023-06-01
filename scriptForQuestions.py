import re

'''
Из текстового файла достаю вопросы и ответы, деля их на а) и б)
'''

with open('./QandA/data.txt', 'r') as f:
    text = f.read()


questions = re.findall(r"\d+\.\s(.+?)\n", text)
answers = re.findall(r"\n\s*(\w\))\s*(.+?)(?=\n\s*\w|\Z)", text, flags=re.DOTALL)


a_answers = []
b_answers = []
answer_a = []
answer_b = []

for answer in answers:
    if answer[0].startswith("а"):
        a_answers.append(answer[1])
    elif answer[0].startswith("б"):
        b_answers.append(answer[1])


for i in range(len(a_answers)):
    answer_a.append(a_answers[i].replace(';', '').replace('.', '').rstrip())
    answer_b.append(b_answers[i].replace('.', '').replace(':', '').rstrip())

# print(questions)
# print(answer_a)
# print(answer_b)

