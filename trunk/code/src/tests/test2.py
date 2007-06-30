class Test2:
	def GetValue( self ):
		return "Woo hoo - 2 "

def Info():
	return "This is information about the test2"

def Main():
  	print "[INFO] : Processing starts now for test2"
	objTest = Test2()
	print "[INFO] : Object returned", objTest.GetValue()
	return True
