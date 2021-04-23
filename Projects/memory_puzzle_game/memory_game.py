from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.lang import Builder
import time
import _thread as thread
import random
root_box = Builder.load_string("""
<PopUpBox>:
    orientation:"vertical"
    padding:"10dp", "10dp"
    popup_exit_button_object:popup_exit_button
    pop_up_text_object:pop_up_text
    canvas:
        Color:
            rgba:90/float(255), 90/float(255), 90/float(255), 128/float(255)
        Rectangle:
            size:self.size
            pos:self.pos
    BoxLayout:
        size_hint_y:None
        height:"150dp"
        orientation:"vertical"
        canvas:
            Color:
                rgb:230/float(255), 230/float(255), 230/float(255)
            Rectangle:
                size:self.size
                pos:self.pos
        BoxLayout:
            padding:5
            Label:
                id:pop_up_text
                text:""
                font_name:"Candara"
                text_size:self.size[0], None
                valign:"middle"
                halign:"left"
                color:0, 0, 0, 1
        BoxLayout:
            size_hint_y:None
            height:"2dp"
            canvas:
                Color:
                    rgb:0, 82/float(255), 121/float(255)
                Rectangle:
                    size:self.size
                    pos:self.pos
        BoxLayout:
            size_hint_y:None
            height:"50dp"
            padding:5
            BoxLayout:
            Button:
                id:popup_exit_button
                size_hint:None, None
                size:"100dp", "40dp"
                text:"Ok"
                font_name:"Candara"
                background_normal:"icons/0_162_232.png"
                background_down:"icons/0_162_232.png"
    BoxLayout:
<MainStackSpaceBox>:
    boxes_grid_object:boxes_grid
    pop_up_box_object:pop_up_box
    pop_up_screen_manager_object:pop_up_screen_manager
    canvas:
        Color:
            rgb:230/float(255), 230/float(255), 230/float(255)
        Rectangle:
            size:self.size
            pos:self.pos
    FloatLayout:
        BoxLayout:
            GridLayout:
                padding:5
                spacing:5
                id:boxes_grid
        BoxLayout:
            ScreenManager:
                id:pop_up_screen_manager
                Screen:
                    name:"empty_screen"
                    BoxLayout:
                Screen:
                    name:"pop_up_screen"
                    PopUpBox:
                        id:pop_up_box
""")
class PopUpBox(BoxLayout):
    pass
class MainStackSpaceBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainStackSpaceBox, self).__init__(**kwargs)
        self.level = 1
        self.maximum_errors = self.level + 1
        self.error_counter = 0
        self.button_box_list = []
        self.random_box_list = []
        self.time_counter = 0
        self.error_box_list = []
        self.number_of_correct_box = 0
        self.clicked_box_list = []
        self.seconds = 0
    def generateNumberOfBoxes(self, level):
        return ((level + 1)**2)
    def putBoxesOnGrid(self, number_of_boxes):
        self.button_box_list = []
        counter = 0
        self.boxes_grid_object.cols = int((number_of_boxes)**(1/float(2)))
        self.boxes_grid_object.rows = int((number_of_boxes)**(1/float(2)))
        while counter < number_of_boxes:
            button_box = Button(background_normal = "icons/195_195_195.png",
                                background_down = "icons/195_195_195.png")
            button_box.bind(on_press = self.userRandomButtonBoxPick)
            self.boxes_grid_object.add_widget(button_box)
            self.button_box_list.append(button_box)
            counter = counter + 1
    def generateRandomBoxesList(self, level, boxes_object_list):
        button_boxes_list = []
        counter = 0
        while counter < (level + 1):
            choice_box_object = random.choice(boxes_object_list)
            button_boxes_list.append(choice_box_object)
            boxes_object_list.remove(choice_box_object)
            counter = counter + 1
        self.random_box_list = button_boxes_list
        return button_boxes_list
    def setTimer(self, level):
        self.seconds = (level + 1) * 2
        while self.seconds > 0:
            time.sleep(1)
            self.seconds = self.seconds - 1
        if level == self.level:
            print("Time Failed")
            if self.seconds == -1:
                pass
            elif self.seconds == 0:
                print("Errors:"+str(self.error_counter))
                print("Maximum_Error:"+str(self.maximum_errors))
                self.repeatLevel(self.level, "Bummer, You ran out of time! Click Ok, and Try again.")
        else:
            print("Time Passed")
    def autoRandomButtonBoxPick(self, random_box_list):
        time.sleep(1/float(2))
        self.time_counter = 0.5
        for button_box in random_box_list:
            button_box.background_normal = "icons/0_162_232.png"
            button_box.background_down = "icons/0_162_232.png"
            time.sleep(1)
            button_box.background_normal = "icons/195_195_195.png"
            button_box.background_down = "icons/195_195_195.png"
            self.time_counter = self.time_counter + 1
        thread.start_new_thread(self.setTimer, (self.level, ))
    def respondToErrorPick(self, button_object):
        self.error_box_list.append(button_object)
        button_object.background_normal = "icons/48_48_48.png"
        button_object.background_down = "icons/48_48_48.png"
        time.sleep(0.5)
        button_object.background_normal = "icons/195_195_195.png"
        button_object.background_down = "icons/195_195_195.png"
    def userRandomButtonBoxPick(self, button):
        if self.time_counter == ((self.level + 1) + 0.5):
            if (button in self.random_box_list) and (button not in self.clicked_box_list):
                print("Random button object True:" + str(button))
                button.background_normal = "icons/0_162_232.png"
                button.background_down = "icons/0_162_232.png"
                self.number_of_correct_box = self.number_of_correct_box + 1
                self.clicked_box_list.append(button)
                print(self.clicked_box_list)
                if self.number_of_correct_box == len(self.random_box_list):
                    self.moveToNextLevel(self.level)
            elif (button not in self.clicked_box_list):
                print("Random button object False:" + str(button))
                self.error_counter = self.error_counter + 1
                thread.start_new_thread(self.respondToErrorPick, (button, ))
                if self.error_counter == self.maximum_errors:
                    self.seconds = -1
                    self.repeatLevel(self.level, "Shucks you have made too many mistakes, try again!")
    def resetVariables(self, new_level):
        self.level = new_level
        self.maximum_errors = self.level + 1
        self.error_counter = 0
        self.button_box_list = []
        self.random_box_list = []
        self.time_counter = 0
        self.error_box_list = []
        self.number_of_correct_box = 0
        self.clicked_box_list = []
    def callPopUp(self, message, pop_up_removal_function):
        self.pop_up_box_object.pop_up_text_object.text = message
        self.pop_up_screen_manager_object.transition = NoTransition()
        self.pop_up_screen_manager_object.current = "pop_up_screen"
        self.pop_up_box_object.popup_exit_button_object.bind(on_press = pop_up_removal_function)
    def confirmLevelFormation(self, button):
        self.pop_up_screen_manager_object.transition = NoTransition()
        self.pop_up_screen_manager_object.current = "empty_screen"
        self.boxes_grid_object.clear_widgets()
        number_of_boxes = self.generateNumberOfBoxes(self.level)
        self.putBoxesOnGrid(number_of_boxes)
        random_boxes_list = self.generateRandomBoxesList(self.level, self.button_box_list)
        thread.start_new_thread(self.autoRandomButtonBoxPick, (random_boxes_list, ))
    def moveToNextLevel(self, level):
        self.seconds = 0
        self.resetVariables((level + 1))
        self.callPopUp("Well done! Time for the next level!", self.confirmLevelFormation)
    def repeatLevel(self, level, message):
        self.markBoxes(self.error_box_list, "icons/48_48_48.png")
        self.markBoxes(self.clicked_box_list, "icons/0_255_128.png")
        self.markBoxes(list(set(self.random_box_list) - set(self.clicked_box_list)), "icons/237_28_36.png")
        self.resetVariables(level)
        self.callPopUp(message, self.confirmLevelFormation)
    def markBoxes(self, box_object_list, image_color_path):
        for button_box in box_object_list:
            button_box.background_normal = image_color_path
            button_box.background_down = image_color_path
class TestApp(App):
    def build(self):
        root_box = MainStackSpaceBox()
        number_of_boxes = root_box.generateNumberOfBoxes(root_box.level)
        root_box.putBoxesOnGrid(number_of_boxes)
        random_boxes_list = root_box.generateRandomBoxesList(root_box.level, root_box.button_box_list)
        thread.start_new_thread(root_box.autoRandomButtonBoxPick, (random_boxes_list, ))
        return root_box
if __name__ == "__main__":
    TestApp().run()
