from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.utils import platform
from kivymd.uix.button import MDRaisedButton

class Wow(MDApp):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission

            # Check if CAMERA permission is granted
            if not check_permission(Permission.CAMERA):
                request_permissions([Permission.CAMERA])

        self.layout = BoxLayout(orientation='vertical')

        # Add Start Camera Button
        self.start_button = MDRaisedButton(text="Start Camera")
        self.start_button.size_hint = (1, 0.2)
        self.start_button.bind(on_press=self.start_camera)
        self.layout.add_widget(self.start_button)

        self.camera_image = Image()
        self.layout.add_widget(self.camera_image)

        return self.layout

    def start_camera(self, *args):
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise Exception("Camera not opened")

            Clock.schedule_interval(self.update, 1.0 / 30.0)
            self.start_button.disabled = True  # Disable the button
        except Exception as e:
            print(f"Error starting camera: {e}")

    def update(self, dt):
        try:
            ret, frame = self.capture.read()
            if ret:
                self.show_frame(frame)
        except Exception as e:
            print(f"Error updating frame: {e}")

    def show_frame(self, frame):
        try:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_image.texture = image_texture
        except Exception as e:
            print(f"Error displaying frame: {e}")

if __name__ == '__main__':
    Wow().run()
