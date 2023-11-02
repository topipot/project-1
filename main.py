from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.utils import platform
import android

from kivy import __version__ as kivy_version
from opencv import __version__ as opencv_version


def check_library_versions():
    # Check Kivy version
    if platform == 'android':
        required_kivy_version = '2.2.1'  # Update this to your required Kivy version
        if kivy_version < required_kivy_version:
            print(f"Kivy version {kivy_version} is not compatible. Required: {required_kivy_version}")
            return False
    
    # Check OpenCV version
    if platform == 'android':
        required_opencv_version = '4.8.0'  # Update this to your required OpenCV version
        if opencv_version < required_opencv_version:
            print(f"OpenCV version {opencv_version} is not compatible. Required: {required_opencv_version}")
            return False

    return True

class Wow(MDApp):
    def build(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission

            # Check if CAMERA permission is granted
            if not check_permission(Permission.CAMERA):
                request_permissions([Permission.CAMERA])
                print('camera permission requested')

            # Check library versions
            if not check_library_versions():
                print('Library versions are not compatible with the target SDK version.')
                return

        self.layout = BoxLayout(orientation='vertical')
        self.camera_image = Image()
        self.layout.add_widget(self.camera_image)
        return self.layout

    def on_start(self):
        try:
            self.capture = cv2.VideoCapture(0)
            if not self.capture.isOpened():
                raise Exception("Camera not opened")

            Clock.schedule_interval(self.update, 1.0 / 30.0)
        except Exception as e:
            print(f"Error starting camera: {e}")
            print(type(e))
            print(e.args)

    def update(self, dt):
        try:
            ret, frame = self.capture.read()
            if ret:
                self.show_frame(frame)
        except Exception as e:
            print(f"Error updating frame: {e}")
            print(type(e))
            print(e.args)

    def show_frame(self, frame):
        try:
            buf = cv2.flip(frame, 0).tostring()
            #buf = buf1.tobytes()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.camera_image.texture = image_texture

        except Exception as e:
            print(f"Error displaying frame: {e}")

if __name__ == '__main__':
    Wow().run()
