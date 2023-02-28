def WriteToken(token) :
    f = open("./token.txt", "w")
    f.write(token)
    f.close()