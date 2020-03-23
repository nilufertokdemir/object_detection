import os

number = []

for num in os.listdir("demo_image"):
    num = num.split("_")[1]
    number.append(num.split(".")[0])

for i in range(0, len(number)):
    number[i] = int(number[i])

number = sorted(number)
size = len(number)

print(number[size-1])