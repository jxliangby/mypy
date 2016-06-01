

class Test():
  id = None
  name = None


test1 = Test()
test1.id=1
test1.name = "name-1"

test2 = Test()
test2.id=2

Test.id=11111111

test3 = Test()
test3.name = "name-3"

print("test1 id:%s,name:%s" %(test1.id,test1.name))
print("test2 id:%s,name:%s" %(test2.id,test2.name))
print("test3 id:%s,name:%s" %(test3.id,test3.name))