import ast

def savelist(dictionary):
    file = open("src\shortcuts.txt","w")
    file.write(str(dictionary))
    file.close()

def openlist():
    with open("src\shortcuts.txt","r") as file:
        dictionary = ast.literal_eval(file.read())
    return dictionary

'''
##Testing
save = {"1":"Hello","2":"Hi"}
print(save)
savelist(save)
temp = openlist()
print(temp)
print(temp["1"])
'''
