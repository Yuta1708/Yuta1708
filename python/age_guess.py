age_min=0
age_max=150
med=75

while age_max-age_min>1:
    med=(float(age_min)+float(age_max))/2
    med=int(med)
    word=str(med)+"歳以上であれば T \n  そうでなければ F を入力して！>>>"
    answer=input(str(word))
    if answer=="T":
        age_min=med
    elif answer=="F":
        age_max=med
    else:
        input(str(word))
    print(med,age_min,age_max)

print("あなたは"+str(age_min)+"歳です")
