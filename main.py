from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from kivy.utils import platform


class Wow(App):
    def build(self):

        if platform == 'android':
            from android.permissions import request_permissions, Permission, check_permission
            
            if not check_permission(Permission.CAMERA):
                self.request_camera_permission(None)
                self.permission_button = Button(text="Request Camera Permission")
                self.permission_button.bind(on_press=self.request_camera_permission)
                self.layout.add_widget(self.permission_button)
            else:
                self.start_camera()

        self.layout = BoxLayout(orientation='vertical')
        self.camera_image = Image()
        self.layout.add_widget(self.camera_image)
        self.results_label = Label(text="Scanning QR codes...")
        self.layout.add_widget(self.results_label)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/30.0)  # Update every 30 frames per second
        return self.layout
    
    def request_camera_permission(self, instance):
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.CAMERA])
        
        # Check for permission and start the camera if granted
        if check_permission(Permission.CAMERA):
            self.layout.remove_widget(self.permission_button)
            self.start_camera()
            
    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0/30.0)
    

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
