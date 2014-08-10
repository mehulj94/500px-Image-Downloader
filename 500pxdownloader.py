from Tkinter import *
import re
import urllib,urllib2
import requests
from bs4 import BeautifulSoup
import tkMessageBox as box

fields = 'URL','Filename'

class download(Frame):
  
	def __init__(self, parent):
		Frame.__init__(self, parent, background="white")   
         
		self.parent = parent
		self.parent.title("500px Downloader")
		self.pack(fill=BOTH, expand=1)
		self.centerWindow()
		self.ipop()

	def centerWindow(self):
      
		w = 350
		h = 150

		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
        
		x = (sw - w)/2
		y = (sh - h)/2
		self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))
	
	def ipop(self):
		ents = self.makeform(fields)
		self.parent.bind('<Return>', (lambda event, e=ents: self.fetch(e)))   
		b1 = Button(self, text='Download',relief=RIDGE ,
				command=(lambda e=ents: self.fetch(e)))
		b1.pack(side=LEFT, padx=5, pady=5)
		b2 = Button(self, text='Quit', relief=RIDGE , command=self.quit)
		b2.pack(side=LEFT, padx=5, pady=5)
	
	def makeform(self, fields):
		entries = []
		for field in fields:
			row = Frame(self)
			lab = Label(row, width=15, text=field, anchor='w')
			ent = Entry(row)
			row.pack(side=TOP, fill=X, padx=5, pady=5)
			lab.pack(side=LEFT)
			ent.pack(side=RIGHT, expand=YES, fill=X)
			entries.append((field, ent))
		return entries
		
	def fetch(self,entries):
		for entry in entries:
			field = entry[0]
			text  = entry[1].get()
			#print('%s: "%s"' % (field, text)) 
		self.downloader(entries)

	def downloader(self,x):
		try:
			url = x[0][1].get()
			req = urllib2.Request(url)
			req.add_header("http://500px.com", {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'})
			html = urllib2.urlopen(req)
			htmlcode = html.read()
			title = x[1][1].get()
			links = [] 
			soup = BeautifulSoup(htmlcode)
			tags = soup('img')
			for tag in tags:
				try:
					links.append(tag['src'])
				except:
					None 

			for i in links:
				try:
					match = re.search(r'\S+5.jpg',i)
					match1 = re.search(r'\S+2048.jpg',i)
					if match:
						print 'Downloading...'
						src = match.group()
						urllib.urlretrieve(src,title+'.jpg')
						x[0][1].delete(0,END)
						x[1][1].delete(0,END)
						self.onDownLoad()
					elif match1:
						print 'Downloading...'
						src = match1.group()
						urllib.urlretrieve(src,title+'.jpg')
						x[0][1].delete(0,END)
						x[1][1].delete(0,END)
						self.onDownLoad()
				except Exception,e:
					self.onError()

		except Exception,e:
			self.onError()
	
	def onDownLoad(self):
		box.showinfo("Info", "Image Downloaded!!!!\nCoded by--> Mehul Jain\nFor queries contact: mehulj94@gmail.com")
	
	def onError(self):
		box.showerror("Error", "Please try again.\nCoded by--> Mehul Jain\nFor queries contact: mehulj94@gmail.com")
			
def main():
  
	root = Tk()
	handle = download(root)
	root.mainloop()  

if __name__ == '__main__':
    main()  

