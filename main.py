from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.utils import platform


class Wow(MDApp):  # Inherit from MDApp instead of App
    def build(self):

        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA])

        self.layout = MDBoxLayout(orientation='vertical')  # Use MDBoxLayout instead of BoxLayout
        self.camera_image = Image()
        self.layout.add_widget(self.camera_image)

        self.results_label = MDLabel(text="Scanning QR codes...", halign="center", valign="middle")  # Use MDLabel instead of Label
        self.results_label.size_hint = (1, None)
        self.layout.add_widget(self.results_label)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update every 30 frames per second

        return self.layout

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.show_frame(frame)

    def show_frame(self, frame):
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_image.texture = image_texture


if __name__ == '__main__':
    Wow().run()
