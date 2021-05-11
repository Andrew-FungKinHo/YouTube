import wolframalpha
import base64
import tkinter as tk
from urllib.request import urlopen

API_KEY = 'INSERT YOUR API KEY HERE'
client = wolframalpha.Client(API_KEY)

def math():
  eq = entry1.get()
  res = client.query(eq.strip(), params=(("format", "image,plaintext"),))
  data = {}
  for p in res.pods:
      for s in p.subpods:
          if s.img.alt.lower() == "root plot":
              data['rootPlot'] = s.img.src
          elif s.img.alt.lower() == "number line":
              data['numberLine'] = s.img.src
  data['results'] = [i.texts for i in list(res.results)][0]
  
  print(data)

  image1_url = data['rootPlot']
  image2_url = data['numberLine']

  image1_byt = urlopen(image1_url).read()
  image1_b64 = base64.encodebytes(image1_byt)
  photo1 = tk.PhotoImage(data=image1_b64)

  image2_byt = urlopen(image2_url).read()
  image2_b64 = base64.encodebytes(image2_byt)
  photo2 = tk.PhotoImage(data=image2_b64)

  canvas.photo1 = photo1
  canvas.photo2 = photo2

  canvas.create_image(10, 30, image=canvas.photo1, anchor='nw')
  canvas.create_text(175,40,fill="darkblue",font="Arial 10",text="Root Plot")
  # canvas.pack()
  canvas.create_image(10, 240, image=canvas.photo2, anchor='nw')
  canvas.create_text(175,230,fill="darkblue",font="Arial 10",text="Number Line")

  canvas.create_text(175,320,fill="darkblue",font="Arial 15",text=data['results'])

root = tk.Tk()
root.title("Math Visualizion")

# a little more than width and height of image
w = 500
h = 500
x = 50
y = 100

root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# create a white canvas
canvas = tk.Canvas(bg='white')
canvas.config(height=350)
canvas.pack()

# entry box
entry1 = tk.Entry(root) 
canvas.create_window(150, 15, window=entry1)

# submit button
submit = tk.Button(text='Solve',command=math,height=1, width = 3)
canvas.create_window(280, 15, window=submit)

root.mainloop()
