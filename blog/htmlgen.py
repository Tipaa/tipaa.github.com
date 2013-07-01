#Copyright Edmund Smith 2012
#Pyml HTML Generator
import io
import os
import re
import string
import numbers
import sys
import readline
import datetime	
import hashlib

def __hash(hash,a):
	return hash.hexdigest()
	
def md5(a):
	return __hash(hashlib.md5(),a)
	
def sha1(a):
	return __hash(hashlib.sha1(),a)
	
def sha512(a):
	return __hash(hashlib.sha512(),a)

DEBUG = False

def w(a,b,c):
	return False;
	
def p(a,b,c):
	print a
	return a
	
def f(a,b,c):
	print b
	return a

def h(a,b,c):
	if len(b[0])==len(b[1]):
		print htmlify(b)
	else:
		print 'Error: The number of titles and paragraphs is unbalanced.'
	return a
	
def e(a,b,c):
	exec c in globals()
	return a
	
class Guard:
	def ok(self,str):
		return True
	def ext(self):
		return ""
	def replacement(self,str):
		return str
	def hash(self):
		return -12341451

class BlogGuard(Guard):
	def ok(self, str):
		return str.endswith(".blog")
	def replacement(self, str):
		return ".html"	

global guard
guard = BlogGuard()

def register(g):
	guard = g
	
commands = {
	':w':w,
	':q':p,
	':f':f,
	#':h':h,
	':e':e
	}

def input(t=""):
	return str(raw_input(t))

def parse(script):
	script = re.split('(<!)|(!>)',script)
	out = ""
	i = 0
	for s in script:
		outs = s
		if s == None or s == '<!' or s == '!>': 
			i += 1
			continue
		if i > 2 and script[i-1] == None and script[i-2] == '<!':
			if DEBUG: print s
			outs = [""]
			def echo(t=""):
				outs[0] += t
			def echon(t=""):
				outs[0] += t + '\n'
			def register(g):
				guard = g
				
			exec s in globals(), {'echo':echo,'echon':echon,'register':register}
			
			outs = outs[0]
		out = out + outs
		i += 1
	return out
	
def preprocess(text):
	text = re.split('(<code>)|(</code>)',text)
	iscode = False
	out = ''
	for t in text:
		if t == None or t == "<code>" or t == "</code>":
			continue
		elif iscode:
			out += codetohtml(t)	
		else:
			out += t
		iscode = not iscode		

	return out.replace('</<','&lt;/<').replace('\n','<br>').replace('\r','').replace('\t','&nbsp;&nbsp;&nbsp;&nbsp;')
	
def codetohtml(text):
	out = ''
	text = text.replace('{','&#123;').replace('}','&#125;').replace('<!','&gt;!')
	words = re.findall('([a-zA-Z][a-zA-Z0-9]*)',text)	
	wordlist = [w for w in words]
	index = 0
	text = "<code>" + text + "</code>"
	for w in wordlist:				
		if w == None:
			continue
		text = text[:index] + text[index:].replace(w, "<a class=\""+w+"\">"+w+"</a>",1)
		index += text[index:].index("<a class=\""+w+"\">"+w+"</a>")+len("<a class=\""+w+"\">"+w+"</a>")
	return text
	
	
def generate():
	lastinput = ""
	inputs = [[],[]]
	inputnames = ["Paragraph Title", "Paragraph Text"]
	lastin = 0;
	#while not lastinput in commands or not commands[lastinput](lastinput):	
	while True:
		lastinput = input('Next '+inputnames[lastin]+':\n').replace(r'\n','\n')		
		if not lastinput[:2] in commands:
			inputs[lastin].append(lastinput)
		if not lastinput[:2] in commands:
			lastin = 1 - lastin
		if lastinput[:2] in commands and not commands[lastinput[:2]](inputs[1-lastin][len(inputs[1-lastin])-1],inputs,lastinput[3:]):
			break
	
	return inputs
	
def htmlify(text):
	if DEBUG: print text
	out = ""
	for i in range(len(text[0])):
		out = out + "<h2>"+text[0][i]+"</h2><p>"+text[1][i]+"</p>\n"
	return out

class Generator (object):
	def htmlify(self, text):
		if DEBUG: print text
		out = ""
		for i in range(len(text[0])):
			out = out + "<h2>"+text[0][i]+"</h2><p>"+text[1][i]+"</p>\n"
		return out
		
	def generate(self):
		lastinput = ""
		inputs = [[],[]]
		inputnames = ["Paragraph Title", "Paragraph Text"]
		lastin = 0;
		#while not lastinput in commands or not commands[lastinput](lastinput):	
		while True:
			lastinput = input('Next '+inputnames[lastin]+':\n').replace(r'\n','\n')		
			if not lastinput[:2] in commands:
				inputs[lastin].append(lastinput)
			if not lastinput[:2] in commands:
				lastin = 1 - lastin
			if lastinput[:2] in commands and not commands[lastinput[:2]](inputs[1-lastin][len(inputs[1-lastin])-1],inputs,lastinput[3:]):
				break
		
		return inputs
		
class MultiPurposeGenerator(object):
	def htmlify(self, text):
		if DEBUG: print text
		out = ""
		lastTag="a"
		tags = {
			':a':'a',
			':p':'p',
			':code':'code',
			':h1':'h1',
			':h2':'h2',
			':h3':'h3'
			}
		for t in text:
			cut = t.index(' ')-1
			lastTag = (t[1:])[:cut]
			out = out + "<"+lastTag+">"+t[cut+2:]+"</"+lastTag+">\n"
		return out
		
	def generate(self):
		lastinput = ""
		inputs = []
		while True:
			lastinput = input('Next Text Block:\n').replace(r'\n','\n')		
			if not lastinput[:2] in commands:
				inputs.append(lastinput)
			elif not commands[lastinput[:2]](inputs[len(inputs)-1],inputs,lastinput[3:]):
				break
		
		return inputs

def main():
	html = io.open("template.pyml",'rb').read()	

	argm = {':m':'once'}
	last = None
	for a in sys.argv[1:]:
		if(last == None):
			last = a
		else:
			argm[last] = a
			last = None
			
	
	file = argm[':f'] if ':c' in argm else "_._"#(sys.argv[1] if len(sys.argv)>1 else raw_input("File name:"))+".html"
	mode = argm[':m']#(sys.argv[2] if len(sys.argv)>2 else "once")
	fcontents = argm[':c'] if ':c' in argm else "none"
		
	htmlgen = MultiPurposeGenerator()
	parse(html.format(title='',style='',text=''))
	if mode == "once":
		print "\n"+'-'*30+"\n"
		title = raw_input("Page title:\n")
		style = ""
		
		text = htmlgen.htmlify(htmlgen.generate())
		
		html1 = html.format(title=title, style=style, text=text)
		output(file,html,title,text,style)
	
	elif mode == "all":
		files = os.listdir(os.getcwd())
		mfiles = {}
		for f in files:
			if guard.ok(f):
				mfiles[f] = f[:f.rfind('.')]+".html"
				parts = re.split("\\\\\\\\\n",io.open(f,'rb').read())
				title = parts[0]
				text = preprocess(parts[1][1:])
				style = (parts[2] if (len(parts)>2) else "")
				html1 = html.format(title=title, style=style, text=text)
				print parts[0][:10]
				output(f[:f.rfind('.')]+".html",html1,not parts[1][0]== '-')
				
		if not fcontents == "none":
			html = io.open("contents.pyml",'rb').read()
			title = "Contents"
			hash = str(mfiles)
			style = ""
			html1 = html.format(title=title, style=style, contents=hash)
			output(fcontents+".html",html1)
	
def output(file,html,doparse = True):	
	if doparse:
		html = parse(html)
	print '<!' in html
	#print html
	
	with io.open(file, 'wb') as ffile:
		ffile.write(html)
	return html
		
if __name__ == "__main__":
	main()
