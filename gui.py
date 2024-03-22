from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, PhotoImage, Text, Scrollbar, Frame
from pathlib import Path
import cv2
from tkinter import Canvas
from PIL import Image, ImageTk
import os
import glob
import requests
import time
from datetime import timedelta, datetime
import sys
import io
import base64


class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1920x1080")
        self.configure(bg="#110E24")
        self.is_fullscreen = True
        self.image_references = []
        self.vehicle_type_text = []
        self.dimension_texts = []
        self.weight_texts = []
        self.status_rectangle = []
        self.status_text_item = []

        self.canvas = Canvas(
            self,
            bg="#110E24",
            height=1080,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.entry_images = []
        self.entry_bgs = []
        self.entries = []

        # Create a new frame with a vertical scrollbar
        self.frame = Frame(self, bg="#1D1A33")

        # Place the frame on the window
        self.frame.place(x=655, y=180.5)

        # Ambil data dari backend
        self.data = self.fetch_data()

        self.start_time = time.time()
        self.create_widgets()
        self.bind_events()
        self.resizable(True, True)
        self.update_data()
    
    def relative_to_assets(self, file_path):
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent
        return str((base_path / "assets" / "frame0"/ file_path).resolve())

    def fetch_data(self):
        try:
            response = requests.get("http://192.168.1.125:8081/hs_data")
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print("Error fetching latest data:", e)
            return None

    def update_data(self):
        # Fetch new data from API
        new_data = self.fetch_data()

        # If there's new data, update the GUI
        if new_data and new_data != self.data:
            self.data = new_data
            self.show_texts()

        self.after(1000, self.update_data)

    def create_entry(self, x_pos, y_pos, i):
        if i > 6:
            return None, None, None
        
        entry_image = PhotoImage(file=self.relative_to_assets(f"entry_{i}.png"))
        entry_bg = self.canvas.create_image(x_pos, y_pos, image=entry_image)
        entry = Entry(
            bd=0,
            bg="#110E24",
            fg="#000716",
            highlightthickness=0
        )
        entry.place(
            x=x_pos - 116,
            y=y_pos - 108 if i in [1, 4, 7, 10] else y_pos - 109,
            width=232.0,
            height=215.0 if i in [1, 2, 3, 7, 8, 9] else 218.0
        )
        if i == 1:  # If it's the first entry
            self.video_source = "rtsp://admin:dcttotal2024@192.168.1.21:554/cam/realmonitor?channel=1&subtype=0"
            self.vid = cv2.VideoCapture(self.video_source)
            self.canvas1 = Canvas(self, width=228, height=212)
            self.canvas1.place(x=x_pos - 116, y=y_pos - 108)
            self.update_image()

            # Bind the refresh function to the Ctrl+Space key combination
            self.bind("<Control-space>", self.refresh_camera)

        # elif i == 2:  
        #     self.canvas2 = Canvas(self, width=228, height=212)
        #     self.canvas2.place(x=x_pos - 116, y=y_pos - 108)
        #     self.update_image2(self.data['imageData'])  # Panggil update_image2 dengan data imageData dari backend

        elif i == 2:  
            self.canvas2 = Canvas(self, width=228, height=212)
            self.canvas2.place(x=x_pos - 116, y=y_pos - 108)
            self.update_image2() 

        elif i == 3: 
            self.frame = Frame(self, bg="#1D1A33")
            self.scrollbar = Scrollbar(self.frame)
            self.scrollbar.pack(side="right", fill="y")
            self.text_widget = Text(self.frame, width=27, height=13, bg="#1D1A33", fg="white", yscrollcommand=self.scrollbar.set)
            self.text_widget.pack(side="left")
            self.scrollbar.config(command=self.text_widget.yview)
            self.frame.place(x=x_pos - 116, y=y_pos - 108, width=228, height=212)
            self.update_text()

        elif i == 4:
            self.frame4 = Frame(self, bg="#1D1A33")
            self.scrollbar4 = Scrollbar(self.frame4)
            self.scrollbar4.pack(side="right", fill="y")
            self.text_widget4 = Text(self.frame4, width=27, height=13, bg="#1D1A33", fg="white",
                                     yscrollcommand=self.scrollbar4.set)
            self.text_widget4.pack(side="left")
            self.scrollbar4.config(command=self.text_widget4.yview)
            self.frame4.place(x=x_pos - 116, y=y_pos - 108, width=228, height=212)
            self.update_run_time()

        elif i == 5:
            self.frame5 = Frame(self, bg="#1D1A33")
            self.scrollbar5 = Scrollbar(self.frame5)
            self.scrollbar5.pack(side="right", fill="y")
            self.text_widget5 = Text(self.frame5, width=27, height=13, bg="#1D1A33", fg="white",
                                     yscrollcommand=self.scrollbar5.set)
            self.text_widget5.pack(side="left")
            self.scrollbar5.config(command=self.text_widget5.yview)
            self.frame5.place(x=x_pos - 116, y=y_pos - 108, width=228, height=212)
            self.update_date()
        
        elif i == 6:
            self.frame6 = Frame(self, bg="#1D1A33")
            self.scrollbar6 = Scrollbar(self.frame6)
            self.scrollbar6.pack(side="right", fill="y")
            self.text_widget6 = Text(self.frame6, width=27, height=13, bg="#1D1A33", fg="white",
                                     yscrollcommand=self.scrollbar6.set)
            self.text_widget6.pack(side="left")
            self.scrollbar6.config(command=self.text_widget6.yview)
            self.frame6.place(x=x_pos - 116, y=y_pos - 108, width=228, height=212)

        return entry_image, entry_bg, entry

    def update_image(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.resize(frame, (232, 217))  # Resize the frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            self.imgtk = ImageTk.PhotoImage(image=img)  # Store as instance variable
            self.canvas1.create_image(0, 0, image=self.imgtk, anchor='nw')  # Use instance variable
        self.after(10, self.update_image)

    def refresh_camera(self, event=None):
        # Release the current video capture
        self.vid.release()

        # Reinitialize the video capture with the same video source
        self.vid = cv2.VideoCapture(self.video_source)

        # Call the update_image function to refresh the camera feed
        self.update_image()
    
    # def update_image2(self, base64_str):
    #     # Convert base64 string to bytes
    #     image_bytes = base64.b64decode(base64_str)

    #     # Convert bytes to image
    #     image = Image.open(io.BytesIO(image_bytes))

    #     # Resize the image
    #     image = image.resize((232, 217))

    #     # Convert the image to a PhotoImage
    #     self.photo_image2 = ImageTk.PhotoImage(image)

    #     # Display the image on canvas2
    #     self.canvas2.create_image(0, 0, image=self.photo_image2, anchor="nw")

    def update_image2(self):
        image_dir = "gambar"
        image_files = glob.glob(os.path.join(image_dir, "*"))
        image_files = [
            img for img in image_files if img.endswith((".png", ".jpg", ".jpeg"))
        ]
        image_files.sort(key=os.path.getmtime, reverse=True)
        if image_files:
            image_path = image_files[0]
            image = Image.open(image_path)
            image = image.resize((232, 217))
            self.photo_image2 = ImageTk.PhotoImage(image)
            self.canvas2.create_image(0, 0, image=self.photo_image2, anchor="nw")
        self.after(1000, self.update_image2)
    


    def update_text(self):
        try:
            response = self.fetch_data()  # Use the fetch_data method to get the response
            if response is not None:
                text = "HTTP request successful"
            else:
                text = "HTTP request failed"
        except Exception as e:
            text = f"HTTP request error: {e}"
        self.text_widget.insert('end', text + '\n')  # Add new text
        self.text_widget.see('end')  # Scroll to the end
        self.after(1000, self.update_text)  # Update every 1 second

    def update_run_time(self):
        run_time = time.time() - self.start_time  # Calculate the run time in seconds
        run_time = timedelta(seconds=int(run_time))  # Convert to timedelta
        self.text_widget4.insert('end', f"Run time: {run_time}\n")  # Add new text
        self.text_widget4.see('end')  # Scroll to the end
        self.after(1000, self.update_run_time)  # Update every 1 second

    def update_date(self):
        current_date = datetime.now().strftime("%Y-%m-%d")  # Get the current date
        self.text_widget5.insert('end', f"Current date: {current_date}\n")  # Add new text
        self.text_widget5.see('end')  # Scroll to the end
        self.after(1000, self.update_date)  # Update every 1 second


    def create_text(self, x, y, text, font, fill):
        self.canvas.create_text(x, y, anchor="nw", text=text, fill=fill, font=font)

    def show_texts(self):
        self.status_text()
        self.createtextsumbu()
        self.createtextberat()
        self.createtextdimensi()
        self.jenis_kendaraan()

    def create_widgets(self):
        for i in range(1, 13):
            x_pos = 655.0 if i in [1, 4, 7, 10] else (907.0 if i in [2, 5, 8, 11] else 1159.0)
            y_pos = 180.5 if i in [1, 2, 3] else (432.5 if i in [4, 5, 6] else 683.5)
            entry_image, entry_bg, entry = self.create_entry(x_pos, y_pos, i)
            self.entry_images.append(entry_image)
            self.entry_bgs.append(entry_bg)
            self.entries.append(entry)

        # Mulai pembaruan data
        self.update_data()

        self.canvas.create_text(
            761.0,
            13.0,
            anchor="nw",
            text="Received MSG Monitoring",
            fill="#FFFFFF",
            font=("Poppins", 18, 'bold')
        )

        self.canvas.create_rectangle(
            1.0,
            1.0,
            488.0,
            1026.0,
            fill="#110E24",
            outline=""
        )

        self.canvas.create_rectangle(
            1.0,
            0.0,
            481.0,
            240.0,
            fill="#110E24",
            outline=""
        )

        self.canvas.create_text(
            60.0,
            4.0,
            anchor="nw",
            text="DATA KENDARAAN",
            fill="#FFFFFF",
            font=("Poppins", 22, 'bold')
        )

        self.canvas.create_text(
            105.0,
            35.0,
            anchor="nw",
            text="WEIGH IN MOTION",
            fill="#FFFFFF",
            font=("Poppins", 16, "bold"),
        )

        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(
            26.0,
            28.0,
            image=image_image_1
        )
        self.image_references.append(image_image_1)

        image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(
            355.0,
            28.0,
            image=image_image_2
        )
        self.image_references.append(image_image_2)

        self.canvas.create_rectangle(
            62.9990234375,
            33.5,
            322.00093042839035,
            33.5,
            fill="#FFFFFF",
            outline=""
        )

        image_image_3 = PhotoImage(file=self.relative_to_assets("image_3.png"))
        self.canvas.create_image(
            191.0,
            111.0,
            image=image_image_3
        )
        self.image_references.append(image_image_3)

        self.canvas.create_text(
            130.0,
            66.0,
            anchor="nw",
            text="Berat",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )

        self.canvas.create_text(
            294.0,
            66.0,
            anchor="nw",
            text="Dimensi",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )

        self.canvas.create_text(
            226.0,
            66.0,
            anchor="nw",
            text="KET",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )

        self.canvas.create_text(
            30.0,
            66.0,
            anchor="nw",
            text="Sumbu",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )

        self.canvas.create_text(
            237.0,
            104.0,
            anchor="nw",
            text="T",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            237.0,
            91.0,
            anchor="nw",
            text="L",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            237.0,
            79.0,
            anchor="nw",
            text="P",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_rectangle(
            82.0,
            237.0,
            389.0,
            240.0,
            fill="#1D1A33",
            outline=""
        )

        self.show_texts()

    # def classify_vehicle(self):
    #     veh_type = self.data[-1]['Veh_Type']
    #     golongan = vehicle_types[int(veh_type)].golongan
    #     return golongan
    
    # vehicle_types menggunakan field veh_type dari data yang diambil dari backend
    # def jenis_kendaraan(self):
    #     # Remove old vehicle type text
    #     if self.vehicle_type_text:
    #         self.canvas.delete(self.vehicle_type_text)

    #     self.canvas.create_text(
    #         12.0,
    #         54.0,
    #         anchor="nw",
    #         text="Jenis Kendaraan :  ",
    #         fill="#FFFFFF",
    #         font=("Poppins", 10, 'bold')
    #     )
    #     # Create new vehicle type text
    #     self.vehicle_type_text = self.canvas.create_text(
    #         150.0,
    #         54.0,
    #         anchor="nw",
    #         text=self.classify_vehicle(),
    #         fill="#FFFFFF",
    #         font=("Poppins", 10, 'bold')
    #     )

    def jenis_kendaraan(self):
        # Remove old vehicle type text
        if self.vehicle_type_text:
            self.canvas.delete(self.vehicle_type_text)

        self.canvas.create_text(
            12.0,
            54.0,
            anchor="nw",
            text="No Kendaraan :  ",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )
        # Create new vehicle type text
        self.vehicle_type_text = self.canvas.create_text(
            150.0,
            54.0,
            anchor="nw",
            text=f"{self.data[-1]['License_Plate']}",
            fill="#FFFFFF",
            font=("Poppins", 10, 'bold')
        )

    def createtextdimensi(self):
        # Remove old dimension texts
        for item in self.dimension_texts:
            self.canvas.delete(item)
        self.dimension_texts = []

        # Panjang kendaraan
        item1 = self.canvas.create_text(
            310.0,
            80.0,
            anchor="nw",
            text=f"{self.data[-1]['Veh_Length']} ft",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.dimension_texts.append(item1)

        # Lebar kendaraan
        item2 = self.canvas.create_text(
            310.0,
            92.0,
            anchor="nw",
            text=f"{self.data[-1]['Veh_Width']} ft",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.dimension_texts.append(item2)

        # Tinggi kendaraan
        item3 = self.canvas.create_text(
            310.0,
            104.0,
            anchor="nw",
            text=f"{self.data[-1]['Veh_Heigth']} ft",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.dimension_texts.append(item3)

    def createtextberat(self):
        # Remove old weight texts
        for item in self.weight_texts:
            self.canvas.delete(item)
        self.weight_texts = []

        # Berat sumbu 1
        item1 = self.canvas.create_text(
            129.0,
            80.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt1']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item1)

        # Berat sumbu 2
        item2 = self.canvas.create_text(
            129.0,
            92.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt2']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item2)

        # Berat sumbu 3
        item3 = self.canvas.create_text(
            129.0,
            104.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt3']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item3)

        # Berat sumbu 4
        item4 = self.canvas.create_text(
            129.0,
            116.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt4']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item4)

        # Berat sumbu 5
        item5 = self.canvas.create_text(
            129.0,
            128.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt5']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item5)

        # Berat sumbu 6
        item6 = self.canvas.create_text(
            129.0,
            140.0,
            anchor="nw",
            text=f"{self.data[-1]['AxleWt6']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item6)

        # Berat total
        item7 = self.canvas.create_text(
            130.0,
            152.0,
            anchor="nw",
            text=f"{self.data[-1]['Gross_Load']} kg",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )
        self.weight_texts.append(item7)

    def createtextsumbu(self):
        self.canvas.create_text(
            53.0,
            80.0,
            anchor="nw",
            text="1",
            fill="#FFFFFF",
            font=("Poppins",9, 'bold')
        )

        self.canvas.create_text(
            53.0,
            92.0,
            anchor="nw",
            text="2",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            53.0,
            104.0,
            anchor="nw",
            text="3",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            53.0,
            116.0,
            anchor="nw",
            text="4",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            53.0,
            128.0,
            anchor="nw",
            text="5",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

        self.canvas.create_text(
            53.0,
            140.0,
            anchor="nw",
            text="6",
            fill="#FFFFFF",
            font=("Poppins", 9, 'bold')
        )

    def classify_status(self):
        # Batas maksimum untuk panjang, lebar, dan tinggi kendaraan
        L = 500000  # Ganti dengan nilai sebenarnya
        W = 500000  # Ganti dengan nilai sebenarnya
        H = 500000  # Ganti dengan nilai sebenarnya

        # Cek apakah kendaraan overload
        is_overload = self.data[-1]['OverLoad_Sign'] == 1

        # Cek apakah kendaraan overdimension
        is_overdimension = self.data[-1]['Veh_Length'] > L or self.data[-1]['Veh_Width'] > W or self.data[-1]['Veh_Heigth'] > H

        if is_overload and is_overdimension:
            return 3  # 'OVERLOAD DAN OVERDIMENSION'
        elif is_overdimension:
            return 2  # 'OVERDIMENSION'
        elif is_overload:
            return 1  # 'OVERLOAD'
        else:
            return 0  # 'OK'

    def status_text(self):
        # status = int(self.classify_status())
        status = self.classify_status()
        color = status_types[status].color
        text_pos = status_types[status].text_pos
        canvas_posx = status_types[status].canvas_posx
        canvas_posy = status_types[status].canvas_posy
        canvas_posk = status_types[status].canvas_posk

        # Remove old status rectangle and text
        if self.status_rectangle:
            self.canvas.delete(self.status_rectangle)
        if self.status_text_item:
            self.canvas.delete(self.status_text_item)

        self.status_rectangle = self.canvas.create_rectangle(
            canvas_posx,
            canvas_posy,
            canvas_posk,
            167.0,
            fill=color,
            outline=""
        )

        self.status_text_item = self.canvas.create_text(
            text_pos,
            164.0,
            anchor="nw",
            text=status_types[status].status,  # Use the status text instead of the status number
            fill="#FFFFFF",
            font=("Poppins", 17, 'bold')
        )
    
    


    def bind_events(self):
        self.bind("<F12>", self.toggle_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)


# class VehicleType:
#     def __init__(self, tipe, golongan):
#         self.tipe = tipe
#         self.golongan = golongan


# vehicle_types = {
#     0: VehicleType(0, 'Kendaraan belum diketahui'),
#     1: VehicleType(1, 'Golongan I'),
#     2: VehicleType(2, 'Golongan II'),
#     3: VehicleType(3, 'Golongan IV'),
#     4: VehicleType(4, 'Golongan III'),
#     5: VehicleType(5, 'Golongan IV'),
#     6: VehicleType(6, 'Golongan IV'),
#     7: VehicleType(7, 'Golongan V'),
#     8: VehicleType(8, 'Golongan V'),
#     9: VehicleType(9, 'Golongan V'),
#     10: VehicleType(10, 'Golongan V'),
#     11: VehicleType(11, 'Golongan V'),
#     12: VehicleType(12, 'Golongan V'),
#     13: VehicleType(13, 'Golongan V'),
#     14: VehicleType(14, 'Golongan V'),
#     15: VehicleType(15, 'Golongan V'),
#     16: VehicleType(16, 'Golongan IV'),
#     17: VehicleType(17, 'Golongan IV'),
#     18: VehicleType(18, 'Golongan V'),
#     19: VehicleType(19, 'Golongan V'),
#     20: VehicleType(20, 'Golongan V'),
#     21: VehicleType(21, 'Golongan V'),
#     22: VehicleType(22, 'Golongan V')
# }


class StatusType:
    def __init__(self, tipe, status, color, text_pos, canvas_posx, canvas_posy, canvas_posk):
        self.tipe = tipe
        self.status = status
        self.color = color
        self.text_pos = text_pos
        self.canvas_posx = canvas_posx
        self.canvas_posy = canvas_posy
        self.canvas_posk = canvas_posk


status_types = {
    0: StatusType(0, 'OK', '#008000', 167.0, 163.0, 188.0, 205.0), # text_pos canvas_posx, canvas_posy, canvas_posk
    1: StatusType(1, 'OVERLOAD', '#FF0000', 117.0, 117.0, 188.0, 250.0), # text_pos, canvas_posx, canvas_posy, canvas_posk
    2: StatusType(2, 'OVERDIMENSION', '#FF0000', 100.0, 100.0, 188.0, 300.0), # text_pos, canvas_posx, canvas_posy, canvas_posk
    3: StatusType(3, 'OVERLOAD & OVERDIMENSION', '#FF0000', 15.0, 15.0, 188.0, 370.0), # text_pos, canvas_posx, canvas_posy, canvas_posk
}



gui = GUI()
gui.mainloop()
