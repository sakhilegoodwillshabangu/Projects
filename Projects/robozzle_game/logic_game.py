from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, SlideTransition
from kivy.uix.button import Button
from kivy.lang import Builder
from db_manager import *
import _thread as thread
import time
root_ui = Builder.load_string("""
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
                on_press:root.removePopUp()
    BoxLayout:
<InstructionButton>:
    size_hint:None, None
    size:"30dp", "30dp"
    text:""
    font_name:"Candara"
    color:0, 0, 0, 1
    background_normal:"icons/195_195_195.png"
    background_down:"icons/195_195_195.png"
    button_color:[]
<FunctionsAndControlsBox>:
    orientation:"vertical"
    functions_and_controls_object:functions_and_controls
    id:functions_and_controls
    functions_space_object:functions_space
    function_buttons_space_object:function_buttons_space
    controls_space_object:controls_space
    first_function_button_object:first_function_button
    size_hint_y:None
    height:"130dp"
    padding:5
    BoxLayout:
        size_hint_y:None
        height:"18dp"
        Label:
            text:"Functions"
            font_name:"Candara"
            text_size:self.size
            color:0, 0, 0, 1
    BoxLayout:
        id:functions_space
        orientation:"vertical"
        size_hint_y:None
        height:"30dp"
        BoxLayout:
            GridLayout:
                id:function_buttons_space
                rows:1
                spacing:2
                Button:
                    text:"F1"
                    font_name:"Candara"
                    color:0, 0, 0, 1
                    size_hint:None, None
                    size:"30dp", "30dp"
                    background_normal:"icons/230_230_230.png"
                    background_down:"icons/230_230_230.png"
                InstructionButton:
                    id:first_function_button
                    size_hint:None, None
                    size:"30dp", "30dp"
                    text:""
                    font_name:"Candara"
                    color:0, 0, 0, 1
                    background_normal:"icons/_195_195_195.png"
                    background_down:"icons/_195_195_195.png"
                    button_color:[]
                    on_press:root.goToInstruction(self)
                InstructionButton:
                    size_hint:None, None
                    size:"30dp", "30dp"
                    text:""
                    font_name:"Candara"
                    color:0, 0, 0, 1
                    background_normal:"icons/195_195_195.png"
                    background_down:"icons/195_195_195.png"
                    button_color:[]
                    on_press:root.goToInstruction(self)
    BoxLayout:
        size_hint_y:None
        height:"18dp"
        Label:
            text:"Controls"
            font_name:"Candara"
            text_size:self.size
            color:0, 0, 0, 1
    BoxLayout:
        id:controls_space
        orientation:"vertical"
        size_hint_y:None
        height:"30dp"
        GridLayout:
            spacing:2
            rows:1
            ArrowButton:
                size_hint:None, None
                size:"30dp", "30dp"
                font_name:"Candara"
                color:0, 0, 0, 1
                background_normal:"icons/195_195_195_up_arrow.png"
                background_down:"icons/195_195_195_up_arrow.png"
                brush_color:[]
                on_press:root.addArrow(self)
                direction:"up"
            ArrowButton:
                size_hint:None, None
                size:"30dp", "30dp"
                font_name:"Candara"
                color:0, 0, 0, 1
                background_normal:"icons/195_195_195_left_arrow.png"
                background_down:"icons/195_195_195_left_arrow.png"
                brush_color:[]
                on_press:root.addArrow(self)
                direction:"left"
            ArrowButton:
                size_hint:None, None
                size:"30dp", "30dp"
                font_name:"Candara"
                color:0, 0, 0, 1
                background_normal:"icons/195_195_195_right_arrow.png"
                background_down:"icons/195_195_195_right_arrow.png"
                brush_color:[]
                on_press:root.addArrow(self)
                direction:"right"
            ArrowButton:
                size_hint:None, None
                size:"30dp", "30dp"
                text:"F1"
                font_name:"Candara"
                color:0, 0, 0, 1
                background_normal:"icons/195_195_195.png"
                background_down:"icons/195_195_195.png"
                brush_color:[]
                on_press:root.addArrow(self)
                direction:"f1"
    BoxLayout:
        size_hint_y:None
        height:"24dp"
        spacing:2
        ColorButton:
            size_hint:None, None
            size:"20dp", "20dp"
            background_normal:"icons/0_162_232.png"
            background_down:"icons/0_162_232.png"
            button_color:[0, 162, 232]
            on_press:root.addColor(self)
        ColorButton:
            size_hint:None, None
            size:"20dp", "20dp"
            background_normal:"icons/255_157_60.png"
            background_down:"icons/255_157_60.png"
            button_color:[255, 157, 60]
            on_press:root.addColor(self)
        ColorButton:
            size_hint:None, None
            size:"20dp", "20dp"
            background_normal:"icons/0_255_128.png"
            background_down:"icons/0_255_128.png"
            button_color:[0, 255, 128]
            on_press:root.addColor(self)
<MainStageSpaceBox>:
    orientation:"vertical"
    grid_blocks_layout_object:grid_blocks_layout
    transparent_screen_manager_object:transparent_screen_manager
    function_and_control_box_object:function_and_control_box
    pop_up_box_object:pop_up_box
    speed_munipulate_buttons_space_object:speed_munipulate_buttons_space
    canvas:
        Color:
            rgb:230/float(255), 230/float(255), 230/float(255)
        Rectangle:
            size:self.size
            pos:self.pos
    FloatLayout:
        BoxLayout:
            id:body_space
            orientation:"vertical"
            FunctionsAndControlsBox:
                id:function_and_control_box
            BoxLayout:
                GridLayout:
                    spacing:2
                    id:grid_blocks_layout
            BoxLayout:
                size_hint_y:None
                height:"70dp"
                padding:"5dp"
                BoxLayout:
                    orientation:"vertical"
                    spacing:2
                    BoxLayout:
                        size_hint_y:None
                        height:"18dp"
                        Label:
                            text:"Game Speed"
                            font_name:"Candara"
                            color:0, 0, 0, 1
                            text_size:self.size
                    BoxLayout:
                        spacing:2
                        id:speed_munipulate_buttons_space
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            text:"x1"
                            font_name:"Candara"
                            background_normal:"icons/48_48_48.png"
                            background_down:"icons/48_48_48.png"
                            on_press:root.setOneSecondSpeed(self)
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            text:"2x"
                            color:0, 0, 0, 1
                            font_name:"Candara"
                            background_normal:"icons/255_255_255.png"
                            background_down:"icons/255_255_255.png"
                            on_press:root.setOneHalfSecondSpeed(self)
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            text:"3x"
                            color:0, 0, 0, 1
                            font_name:"Candara"
                            background_normal:"icons/255_255_255.png"
                            background_down:"icons/255_255_255.png"
                            on_press:root.setOneTenthSecondSpeed(self)
                BoxLayout:
                    orientation:"vertical"
                    size_hint_x:None
                    width:"210dp"
                    BoxLayout:
                        size_hint_y:None
                        height:"18dp"
                        Label:
                            text:"Execution commands"
                            font_name:"Candara"
                            color:0, 0, 0, 1
                            text_size:self.size
                    BoxLayout:
                        spacing:2
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            background_normal:"icons/white_play.png"
                            background_down:"icons/white_play.png"
                            on_press:root.playGame(self)
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            background_normal:"icons/white_re_play.png"
                            background_down:"icons/white_re_play.png"
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            background_normal:"icons/white_pause.png"
                            background_down:"icons/white_pause.png"
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            background_normal:"icons/white_stop.png"
                            background_down:"icons/white_stop.png"
                        Button:
                            size_hint:None, None
                            size:"40dp", "40dp"
                            background_normal:"icons/white_cancel.png"
                            background_down:"icons/white_cancel.png"
        BoxLayout:
            ScreenManager:
                id:transparent_screen_manager
                Screen:
                    name:"empty_screen"
                    BoxLayout:
                Screen:
                    name:"controls_settings_screen"
                    BoxLayout:
                        orientation:"vertical"
                        BoxLayout:
                            size_hint_y:None
                            height:"40dp"
                        BoxLayout:
                            padding:5
                            orientation:"vertical"
                            canvas:
                                Color:
                                    rgba:50/float(255), 50/float(255), 50/float(255), 128/float(255)
                                Rectangle:
                                    size:self.size
                                    pos:self.pos
				Screen:
                    name:"pop_up_screen"
                    PopUpBox:
                        id:pop_up_box
""")
def getRootBox(starting_box, specified_root_box = None):
    parent_box = starting_box.parent
    box = True
    while box:
        print(parent_box)
        parent_box = parent_box.parent
        core = parent_box.parent
        if specified_root_box != None:
            if specified_root_box in str(parent_box):
                root_box = parent_box
                return root_box
        elif core == parent_box:
            box = False
        else:
            root_box = parent_box
    return root_box
def unMarkColor(_object):
    print("----UNMark Color-----")
    if _object.button_color == [0, 255, 128]:
        print([0, 255, 128])
        _object.background_normal = "icons/0_255_128.png"
        _object.background_down = "icons/0_255_128.png"
    elif _object.button_color == [0, 162, 232]:
        print([0, 162, 232])
        _object.background_normal = "icons/0_162_232.png"
        _object.background_down = "icons/0_162_232.png"
    elif _object.button_color == [255, 157, 60]:
        print([255, 157, 60])
        _object.background_normal = "icons/255_157_60.png"
        _object.background_down = "icons/255_157_60.png"
    else:
        print("Unmark:"+str([195, 195, 195]))
        _object.background_normal = "icons/195_195_195.png"
        _object.background_down = "icons/195_195_195.png"
def markColor(_object):
    if _object.button_color == [0, 255, 128]:
        _object.background_normal = "icons/_0_255_128.png"
        _object.background_down = "icons/_0_255_128.png"
    elif _object.button_color == [0, 162, 232]:
        _object.background_normal = "icons/_0_162_232.png"
        _object.background_down = "icons/_0_162_232.png"
    elif _object.button_color == [255, 157, 60]:
        _object.background_normal = "icons/_255_157_60.png"
        _object.background_down = "icons/_255_157_60.png"
    else:
        _object.background_normal = "icons/_195_195_195.png"
        _object.background_down = "icons/_195_195_195.png"
def markArrow(_object):
    print("Mark Arrow")
    if _object.direction == "up":
        print("Mark up Arrow")
        _object.background_normal = "icons/_195_195_195_up_arrow.png"
        _object.background_down = "icons/_195_195_195_up_arrow.png"
    elif _object.direction == "left":
        print("Mark left Arrow")
        _object.background_normal = "icons/_195_195_195_left_arrow.png"
        _object.background_down = "icons/_195_195_195_left_arrow.png"
    elif _object.direction == "right":
        print("Mark right Arrow")
        _object.background_normal = "icons/_195_195_195_right_arrow.png"
        _object.background_down = "icons/_195_195_195_right_arrow.png"
    else:
        _object.background_normal = "icons/_195_195_195.png"
        _object.background_down = "icons/_195_195_195.png"
        print("----Mark Arrow-----")
    print("Done Marking Arrow")
def unMarkArrow(_object):
    if _object.direction == "up":
        print("UnMark arrow up")
        _object.background_normal = "icons/195_195_195_up_arrow.png"
        _object.background_down = "icons/195_195_195_up_arrow.png"
    elif _object.direction == "left":
        _object.background_normal = "icons/195_195_195_left_arrow.png"
        _object.background_down = "icons/195_195_195_left_arrow.png"
    elif _object.direction == "right":
        print("unmark right a arrow")
        _object.background_normal = "icons/195_195_195_right_arrow.png"
        _object.background_down = "icons/195_195_195_right_arrow.png"
    else:
        print("-----UnMark Arrow-----")
        _object.background_normal = "icons/195_195_195.png"
        _object.background_down = "icons/195_195_195.png"
def updateArrow(_object, color_button, arrow_button, arrow_direction):
    print("CCOLOR:"+str(color_button.background_normal))
    if color_button.button_color != []:
        slash_index = color_button.background_normal.index("/")
        print("CLC:"+str(color_button.background_normal[slash_index:]))
        print("+++:"+str(color_button.background_normal[slash_index + 1])+":+++++")
        if color_button.background_normal[slash_index + 1] != "_":
            _object.background_normal = "icons/_" + color_button.background_normal[slash_index + 1:-4] + arrow_direction
            _object.background_down = "icons/_" + color_button.background_down[slash_index + 1:-4] + arrow_direction
        else:
            _object.background_normal = color_button.background_normal[:-4] + arrow_direction
            _object.background_down = color_button.background_down[:-4] + arrow_direction
    else:
        print("Arrow image:"+str(arrow_button.background_normal))
        _object.background_normal = arrow_button.background_normal
        _object.background_down = arrow_button.background_normal
def unmarkButtonWithArrow(_object, color_button, arrow_button, arrow_direction):
    print("Line 1:unmarkButtonWithArrow")
    if color_button.button_color != []:
        print("Line 2:unmarkButtonWithArrow")
        print("Put color on non current box")
        print("color is:"+str(color_button.background_normal))
        slash_index = color_button.background_normal.index("/")
        print("Line 3:unmarkButtonWithArrow")
        print("COLOR will be:"+str(color_button.background_normal[slash_index + 2:]))
        print("Button color:" +str(color_button.button_color))
        slash_index = color_button.background_normal.index("/")
        print("+++:"+str(color_button.background_normal[:-4])+":+++++")
        print("Line 4:unmarkButtonWithArrow")
        _object.background_normal = "icons/" + color_button.background_normal[slash_index + 2:-4] + arrow_direction
        print("Line 5:unmarkButtonWithArrow")
        _object.background_down = "icons/" + color_button.background_down[slash_index + 2:-4] + arrow_direction
        print("Line 6:unmarkButtonWithArrow")
        if color_button.background_normal[slash_index + 1] != "_":
            print("Line 7:unmarkButtonWithArrow")
            _object.background_normal = color_button.background_normal[:-4] + arrow_direction
            print("Line 8:unmarkButtonWithArrow")
            _object.background_down = color_button.background_down[:-4] + arrow_direction
            print("Line 9:unmarkButtonWithArrow")
        else:
            print("Line 10:unmarkButtonWithArrow")
            _object.background_normal = color_button.background_normal[:-4] + arrow_direction
            print("Line 11:unmarkButtonWithArrow")
            _object.background_down = color_button.background_down[:-4] + arrow_direction
            print("Line 12:unmarkButtonWithArrow")
    else:
        print("Line 13:unmarkButtonWithArrow")
        print("background_normal:"+ str(color_button.background_normal[:-4] + arrow_direction))
        _object.background_normal = arrow_button.background_normal
        print("Line 14:unmarkButtonWithArrow")
        _object.background_down = arrow_button.background_normal
        print("Line 15:unmarkButtonWithArrow")
def markAndInstructionBox(_object, table):
    print("TABLE:"+str(table))
    arrow_button = table[_object]["arrow_button"]
    color_button = table[_object]["color_button"]
    direction = arrow_button.direction
    print("DIRECTION:" + direction)
    print(color_button.button_color)
    print("Arrow button image:"+str(arrow_button))
    if direction == "up":
        _object.text =  ""
        print("DD:UP")
        updateArrow(_object, color_button, arrow_button, "_up_arrow.png")
    elif direction == "left":
        _object.text =  ""
        print("DD:LL")
        updateArrow(_object, color_button, arrow_button, "_left_arrow.png")
        print("Function test ran well")
    elif direction == "right":
        _object.text =  ""
        print("DD:RIGHT")
        updateArrow(_object, color_button, arrow_button, "_right_arrow.png")
    elif direction != "":
        if direction[0] == "f":
            print("DD:" + direction)
            _object.text = direction.upper()
            if color_button.button_color != []:
                _object.text = direction.upper()
                slash_index = color_button.background_normal.index("/")
                print(direction + " type 1 Button Color:"+str(color_button.background_normal[slash_index + 1:]))
                if color_button.background_normal[slash_index + 1] != "_":
                    _object.background_normal = "icons/_" + color_button.background_normal[slash_index + 1:]
                    _object.background_down = "icons/_" + color_button.background_down[slash_index + 1:]
                else:
                    _object.background_normal = color_button.background_normal
                    _object.background_down = color_button.background_down
            else:
                print(direction + " type 2 Button Color:"+str(color_button.background_normal))
                _object.background_normal = "icons/_195_195_195.png"
                _object.background_down = "icons/_195_195_195.png"
    else:
        _object.text = ""
        print("Mark Button")
        if color_button.button_color == []:
            
            if (_object.background_normal != "icons/_195_195_195.png"):
                print("gray instruction box _195_195_195")
                _object.background_normal = "icons/_195_195_195.png"
                _object.background_down = "icons/_195_195_195.png"
                print("_Object.backround_normal:"+_object.background_down)
                
        else:
            slash_index = color_button.background_normal.index("/")
            if color_button.background_normal[slash_index + 1] != "_":
                _object.background_normal = "icons/_" + color_button.background_normal[slash_index + 1:]
                _object.background_down = "icons/_" + color_button.background_down[slash_index + 1:]
            else:
                _object.background_normal = color_button.background_normal
                _object.background_down = color_button.background_down
        print("Done Marking Button")
def uNMarkInstructionBox(_object, table):
    print("UNMark Object from table:"+str(table))
    print("_Object:"+str(_object))
    arrow_button = table[_object]["arrow_button"]
    color_button = table[_object]["color_button"]
    direction = arrow_button.direction
    arrow_button = table[_object]["arrow_button"]
    color_button = table[_object]["color_button"]
    direction = arrow_button.direction
    if direction == "up":
        print("Going Up")
        unmarkButtonWithArrow(_object, color_button, arrow_button, "_up_arrow.png")
    elif direction == "left":
        unmarkButtonWithArrow(_object, color_button, arrow_button, "_left_arrow.png")
    elif direction == "right":
        unmarkButtonWithArrow(_object, color_button, arrow_button, "_right_arrow.png")
    elif direction == "f1":
        print("F1F1")
        print("--------------------------------------------------------------------------")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        if color_button.button_color != []:
            _object.background_normal = color_button.background_normal
            _object.background_down = color_button.background_down
        else:
            _object.background_normal = "icons/195_195_195.png"
            _object.background_down = "icons/195_195_195.png"
    else:
        print("Put color on non current box")
        print("color is:"+str(color_button.background_normal))
        slash_index = color_button.background_normal.index("/")
        print("COLOR will be:"+str(color_button.background_normal[slash_index + 2:]))
        print("Button color:" +str(color_button.button_color))
        if color_button.button_color != []:
            _object.background_normal = color_button.background_normal
            _object.background_down = color_button.background_down
        else:
            _object.background_normal = "icons/195_195_195.png"
            _object.background_down = "icons/195_195_195.png"
class PopUpBox(BoxLayout):
    def removePopUp(self):
    	root = getRootBox(self)
    	if root.result == 0:
    		root.putColorBlocks()
    		root.accomplishment_points = list()
    		root.playing = 0
    	else:
    		root.deleteFunctions()
    		root.deleteColorBlocks()
    		root.stage_level += 1
    		root.putColorBlocks()
    		root.accomplishment_points = list()
    		root.playing = 0
    	root.transparent_screen_manager_object.transition =NoTransition()
    	root.transparent_screen_manager_object.current = "empty_screen"
class InstructionButton(Button):
    def __init__(self, **kwargs):
        super(InstructionButton, self).__init__(**kwargs)
    def mark(self, instruction_table):
        arrow_button = instruction_table[self]["arrow_button"]
        print("Arrow Button:"+str(arrow_button))
        markAndInstructionBox(self, instruction_table)
    def unmark(self, instruction_table):
        print("Self:"+str(self))
        uNMarkInstructionBox(self, instruction_table)
class ArrowButton(Button):
    def __init__(self, **kwargs):
        super(ArrowButton, self).__init__(**kwargs)
    def mark(self, instruction_table):
        markArrow(self)
    def unmark(self):
        unMarkArrow(self)
class ColorButton(Button):
    def __init__(self, **kwargs):
        super(ColorButton, self).__init__(**kwargs)
    def mark(self, instruction_table):
        print(self.button_color)
        markColor(self)
    def unmark(self):
        unMarkColor(self)
class NullObject(Button):
    def __init__(self, **kwargs):
        super(NullObject, self).__init__(**kwargs)
        self.direction = ""
        self.button_color = []
    def mark(self, instruction_table):
        pass
    def unmark(self):
        pass
class FunctionsAndControlsBox(BoxLayout):
    def __init__(self, **kwargs):
        super(FunctionsAndControlsBox, self).__init__(**kwargs)
        self.instruction_table = dict()
        self.current_instruction = None
    def goToInstruction(self, button):

        print("Am on goToInstruction--")
        if self.current_instruction:
            print("The is Current")
            print("Self.current..:"+str(self.current_instruction))
            
            arrow_button = self.instruction_table[self.current_instruction]["arrow_button"]
            color_button = self.instruction_table[self.current_instruction]["color_button"]
            arrow_button.unmark()
            color_button.unmark()
            self.current_instruction.unmark(self.instruction_table)
            self.current_instruction = button
            if button in self.instruction_table:
                print("Instruction table")
                arrow_button = self.instruction_table[button]["arrow_button"]
                color_button = self.instruction_table[button]["color_button"]
                arrow_button.mark(self.instruction_table)
                button.mark(self.instruction_table)
                color_button.mark(self.instruction_table)
                self.current_instruction = button
            else:
                print("New Sub table")
                sub_table = dict()
                sub_table["arrow_button"] = NullObject()
                sub_table["color_button"] = NullObject()
                self.instruction_table[button] = sub_table
                button.mark(self.instruction_table)
        else:
            print("Else assign current button")
            sub_table = dict()
            sub_table["arrow_button"] = NullObject()
            sub_table["color_button"] = NullObject()
            self.current_instruction = button
            self.instruction_table[button] = sub_table
            if self.first_function_button_object != button:
                print("First Object not equal to button")
                sub_table = dict()
                sub_table["arrow_button"] = NullObject()
                sub_table["color_button"] = NullObject()
                self.instruction_table[self.first_function_button_object] = sub_table
                self.first_function_button_object.unmark(self.instruction_table)
            else:
                print("First button equal to button")
                print("Instruction table:"+str(self.instruction_table))
            arrow_button = self.instruction_table[button]["arrow_button"]
            color_button = self.instruction_table[button]["color_button"]
            arrow_button.mark(self.instruction_table)
            color_button.mark(self.instruction_table)
        self.current_instruction.mark(self.instruction_table)
    def addArrow(self, button):
        if self.current_instruction:
            arrow_button = self.instruction_table[self.current_instruction]["arrow_button"]
            arrow_button.unmark()
            if arrow_button != button:
                print("arrows not equal")
                self.instruction_table[self.current_instruction]["arrow_button"] = button
                button.mark(self.instruction_table)
            else:
                print("arrows equal")
                self.instruction_table[self.current_instruction]["arrow_button"] = NullObject()
        else:
            self.current_instruction = self.first_function_button_object
            sub_table = {"color_button":None, "arrow_button":None}
            self.instruction_table[self.current_instruction] = sub_table
            self.instruction_table[self.current_instruction]["color_button"] = NullObject()
            self.instruction_table[self.current_instruction]["arrow_button"] = button
            button.mark(self.instruction_table)
        self.current_instruction.mark(self.instruction_table)
    def addColor(self, button):
        if self.current_instruction:
            color_button = self.instruction_table[self.current_instruction]["color_button"]
            color_button.unmark()
            if color_button != button:
                self.instruction_table[self.current_instruction]["color_button"] = button
                button.mark(self.instruction_table)
            else:
                self.instruction_table[self.current_instruction]["color_button"] = NullObject()
        else:
            self.current_instruction = self.first_function_button_object
            sub_table = {"color_button":None, "arrow_button":None}
            self.instruction_table[self.current_instruction] = sub_table
            self.instruction_table[self.current_instruction]["arrow_button"] = NullObject()
            self.instruction_table[self.current_instruction]["color_button"] = button
            button.mark(self.instruction_table)
        self.current_instruction.mark(self.instruction_table)
class MainStageSpaceBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MainStageSpaceBox, self).__init__(**kwargs)
        self.stage_level = 1
        self.current_arrow_direction = ""
        self.arrow_speed = 1
        self.playing = 0
        self.end_point_list = list()
        self.start_position = int()
        self.accomplishment_points = list()
        self.places = dict()
        self.start_end = dict() 
        self.functions_list = list()
        self.brushes_list = list()
        self.result = 1
        self.stage_game_blocks = list()
        self.right_switch = {"n":["e", "_arrow_e.png"], "s":["w", "_arrow_w.png"], "e":["s", "_arrow_s.png"], "w":["n", "_arrow_n.png"]}
        self.left_switch = {"n":["w", "_arrow_w.png"], "s":["e", "_arrow_e.png"], "e":["n", "_arrow_n.png"], "w":["s" ,"_arrow_s.png"]}
        self.locks = []
    def walkOnIndexPlacesList(self, place_list, index):
        button_block = Button(background_normal = "icons/48_48_48.png",
                            background_down = "icons/230_230_230.png")
        button_block.bind(on_press = self.pressButton)
        return button_block
    def deleteFunctions(self):
    	self.function_and_control_box_object.function_buttons_space_object.children.reverse()
    	for i in range(len(self.function_and_control_box_object.function_buttons_space_object.children)):
    		if i > 2:
    			print("index:", i)
    			try:
    				_object = self.function_and_control_box_object.function_buttons_space_object.children[i]
    				self.function_and_control_box_object.function_buttons_space_object.remove_widget(_object)
    			except:
    				print("##index:", i)
    				print("children range:", len(self.function_and_control_box_object.function_buttons_space_object.children))
    				_object = self.function_and_control_box_object.function_buttons_space_object.children[i-1]
    				self.function_and_control_box_object.function_buttons_space_object.remove_widget(_object)
    	self.function_and_control_box_object.function_buttons_space_object.children.reverse()
    def putMoreFunctions(self, function_list):
        for index in range(len(function_list)):
            number_of_blocks = function_list[index]["blocks"]
            for i in range(number_of_blocks - 2):
                button = InstructionButton()
                button.bind(on_press = self.function_and_control_box_object.goToInstruction)
                self.function_and_control_box_object.function_buttons_space_object.add_widget(button)
    def putSartArrow(self, button, direction):
        if "0_162_232" in button.background_normal:
            print("Change directory:--")
            button.background_normal = "icons/0_162_232_arrow_" + direction +".png"
            button.background_down = "icons/0_162_232_arrow_" + direction + ".png"
        elif "255_157_60" in button.background_normal:
            button.background_normal = "icons/255_157_60_arrow_" + direction + ".png"
            button.background_down = "icons/255_157_60_arrow_" + direction + ".png"
        elif "0_255_128" in button.background_normal:
            button.background_normal = "icons/0_255_128_arrow_" + direction + ".png"
            button.background_down = "icons/0_255_128_arrow_" + direction + ".png"
    def putButtonColor(self, button, button_image):
        if "0_162_232" in button_image:
            button.button_color = [0, 162, 232]
        elif "255_157_60" in button_image:
            button.button_color = [255, 157, 60]
        elif "0_255_128" in button_image:
            button.button_color = [0, 255, 128]
    def addGameBlockToList(self, button):
        self.stage_game_blocks.append(button)
    def deleteColorBlocks(self):
    	index_place_table = self.places["index_place"]
    	button_list = self.grid_blocks_layout_object.children
    	for sub_place in index_place_table:
    	    button_block = button_list[sub_place["place"]]
    	    button_block.background_normal = "icons/230_230_230.png"
    	    button_block.background_down = "icons/230_230_230.png"
    	    self.stage_game_blocks.remove(button_block)
    def putColorBlocks(self):
        button_list = self.grid_blocks_layout_object.children
        x = "places, start_end, functions_list, brushes_list = self.readGdbFile()"
        self.places = self.readGdbFile()[0]
        self.start_end = self.readGdbFile()[1]
        self.functions_list = self.readGdbFile()[2]
        self.brushes_list = self.readGdbFile()[3]
        if self.result:
        	self.putMoreFunctions(self.functions_list)
        try:
            index_place_table = self.places["index_place"]
            start_point_table = self.start_end["start_point"]
            self.current_arrow_direction = start_point_table["direction"]
            self.end_point_list = self.start_end["end_points"]
            self.start_position = start_point_table["position"]
            start_point_index = self.start_end["start_point"]["position"]
            start_point_direction = self.start_end["start_point"]["direction"]
            print("Index length:"+str(len(index_place_table)))
        except:
            return 0
        for sub_place in index_place_table:
            if sub_place["color"] != "":
                button_block = button_list[sub_place["place"]]
                button_block.background_normal = sub_place["color"]
                button_block.background_down = sub_place["color"]
                self.putButtonColor(button_block, sub_place["color"])
                self.addGameBlockToList(button_block)
            else:
                button_block = button_list[sub_place["place"]]
                button_block.background_normal = sub_place["treaty"]
                button_block.background_down = sub_place["treaty"]
                self.putButtonColor(button_block, sub_place["treaty"])
                self.addGameBlockToList(button_block)
            lock = thread.allocate_lock()
            lock.acquire()
            _lock = thread.allocate_lock()
            _lock.acquire()
            self.locks.append(lock)
            self.locks.append(_lock)
            button_block.bind(on_press = self.buttonBlockResponse)
        button = button_list[start_point_index]
        self.putSartArrow(button, start_point_direction) 
    def buttonBlockResponse(self, button):
        print(button.button_color)
        button_block_index = self.grid_blocks_layout_object.children.index(button)
        print("Button_Block_index:"+str(button_block_index))
    def deleteBlocksGrid(self):
        for button in self.grid_blocks_layout_object.children:
            self.grid_blocks_layout_object.remove_widget(button)
    def formBlocksGrid(self):
        self.grid_blocks_layout_object.cols = 16
        self.grid_blocks_layout_object.rows = 16
        indexes_places = list(range(256))
        indexes_places.reverse()
        for i in indexes_places:
            button_block = Button(background_normal = "icons/230_230_230.png",
                        background_down = "icons/230_230_230.png", 
                        size_hint = (None, None), size=("20dp", "20dp"))
            self.grid_blocks_layout_object.add_widget(button_block)
    def readGdbFile(self):
        db_object = DatabaseManager()
        table = db_object.loadData("gdb.dat")
        try:
            places = table["stage_"+str(self.stage_level)]["places_table"]
            start_end_table = table["stage_"+str(self.stage_level)]["start_end"]
            functions_list = table["stage_"+str(self.stage_level)]["functions"]
            brushes_list = table["stage_"+str(self.stage_level)]["brushes"]
            return places, start_end_table, functions_list, brushes_list
        except:
            return dict(), dict(), list(), list()
    def goToControls(self, button):
        if button.background_normal == "icons/0_162_232.png":
            button.background_normal = "icons/48_48_48.png"
            self.transparent_screen_manager_object.transition = NoTransition()
            self.transparent_screen_manager_object.current = "empty_screen"
        else:
            button.background_normal = "icons/0_162_232.png"
            button.background_down = "icons/0_162_232.png"
            self.transparent_screen_manager_object.transition = NoTransition()
            self.transparent_screen_manager_object.current = "controls_settings_screen"
    def updateArrow(self, button_block, arrow_image):
        if button_block.button_color == [0, 162, 232]:
            button_block.background_normal = "icons/0_162_232" + arrow_image[-12:]
            button_block.background_down = "icons/0_162_232" + arrow_image[-12:]
        elif button_block.button_color == [255, 157, 60]:
            button_block.background_normal = "icons/255_157_60" + arrow_image[-12:]
            button_block.background_down = "icons/255_157_60" + arrow_image[-12:]
        elif button_block.button_color == [0, 255, 128]:
            button_block.background_normal = "icons/0_255_128" + arrow_image[-12:]
            button_block.background_down = "icons/0_255_128" + arrow_image[-12:]
    def changeColor(self, button_block, color_two = None):
        if color_two == [0, 162, 232]:
            time.sleep(self.arrow_speed)
            arrow_image = button_block.background_normal
            button_block.button_color = color_two
            button_block.background_normal = "icons/0_162_232.png"
            button_block.background_down = "icons/0_162_232.png"
            self.updateArrow(button_block, arrow_image)
            
        elif color_two == [0, 255, 128]:
            time.sleep(self.arrow_speed)
            arrow_image = button_block.background_normal
            button_block.button_color = color_two
            button_block.background_normal = "icons/0_255_128.png"
            button_block.background_down = "icons/0_255_128.png"
            self.updateArrow(button_block, arrow_image)
            
        elif color_two == [255, 157, 60]:
            time.sleep(self.arrow_speed)
            arrow_image = button_block.background_normal
            button_block.button_color = color_two
            button_block.background_normal = "icons/255_157_60.png"
            button_block.background_down = "icons/255_157_60.png"
            self.updateArrow(button_block, arrow_image)
    def moveToNextBlockAndKeepColor(self, button_block, new_block):
        self.moveToNextBlock(button_block, new_block)
    def moveToNextBlock(self, button_block, next_block):
        if button_block.button_color == [0, 162, 232]:
            arrow_image = button_block.background_normal
            time.sleep(self.arrow_speed)
            button_block.background_normal = "icons/0_162_232.png"
            button_block.background_down = "icons/0_162_232.png"
            self.updateArrow(next_block, arrow_image)
        elif button_block.button_color == [0, 255, 128]:
            arrow_image = button_block.background_normal
            time.sleep(self.arrow_speed)
            button_block.background_normal = "icons/0_255_128.png"
            button_block.background_down = "icons/0_255_128.png"
            self.updateArrow(next_block, arrow_image)
        elif button_block.button_color == [255, 157, 60]:
            arrow_image = button_block.background_normal
            time.sleep(self.arrow_speed)
            button_block.background_normal = "icons/255_157_60.png"
            button_block.background_down = "icons/255_157_60.png"
            self.updateArrow(next_block, arrow_image)
    def switchArrowLeft(self, button_block):
        time.sleep(self.arrow_speed)
        button_block.background_normal = button_block.background_normal[:-12] + self.left_switch[self.current_arrow_direction][1]
        button_block.background_down = button_block.background_down[:-12] + self.left_switch[self.current_arrow_direction][1]
        self.current_arrow_direction = self.left_switch[self.current_arrow_direction][0]
    def switchArrowRight(self, button_block):
        time.sleep(self.arrow_speed)
        button_block.background_normal = button_block.background_normal[:-12] + self.right_switch[self.current_arrow_direction][1]
        button_block.background_down = button_block.background_down[:-12] + self.right_switch[self.current_arrow_direction][1]
        self.current_arrow_direction = self.right_switch[self.current_arrow_direction][0]
    def turnArrow(self, direction, button_block):
        if direction == "right":
            self.switchArrowRight(button_block)
            return 0
        elif direction == "left":
            self.switchArrowLeft(button_block)
            return 0
        elif direction == "up":
            self.current_arrow_direction = self.current_arrow_direction
            return 1
        else:
            return 0
    def getNextWestBlock(self, button_block):
        button_block_index = self.grid_blocks_layout_object.children.index(button_block)
        next_button_block = self.grid_blocks_layout_object.children[button_block_index + 1]
        return next_button_block
    def getNextEastBlock(self, button_block):
        button_block_index = self.grid_blocks_layout_object.children.index(button_block)
        next_button_block = self.grid_blocks_layout_object.children[button_block_index - 1]
        return next_button_block
    def getNextNorthBlock(self, button_block):
        button_block_index = self.grid_blocks_layout_object.children.index(button_block)
        next_button_block = self.grid_blocks_layout_object.children[button_block_index + 16]
        
        return next_button_block
    def getNextSouthBlock(self, button_block):
        button_block_index = self.grid_blocks_layout_object.children.index(button_block)
        next_button_block = self.grid_blocks_layout_object.children[button_block_index - 16]
        
        return next_button_block
    def checkBlockValidity(self, button_block):
        if button_block in self.stage_game_blocks:
            return True
        else:
            return False
    def checkColorQualification(self, button_block, block_color = None):
        if (button_block.button_color == block_color) or (block_color == None):
            return True
        else:
            return False
    def determineNextBox(self, current_button_block):
        if self.current_arrow_direction == "n":
            return self.getNextNorthBlock(current_button_block)
        elif self.current_arrow_direction == "s":
            return self.getNextSouthBlock(current_button_block)
        elif self.current_arrow_direction == "e":
            return self.getNextEastBlock(current_button_block)
        elif self.current_arrow_direction == "w":
            return self.getNextWestBlock(current_button_block)
    def moveArrow(self, counter, instruction_list, button_block):
        self.changeColor(button_block, instruction_list[counter][2])
        direction_output = self.turnArrow(instruction_list[counter][0], button_block)
        print(self.function_and_control_box_object.functions_space_object.children)
        if direction_output:
            pass
        else:
            return button_block, 0
        next_button_block = self.determineNextBox(button_block)
        next_button_block_index = self.grid_blocks_layout_object.children.index(next_button_block)
        block_valid = self.checkBlockValidity(next_button_block)
        if block_valid:
            self.moveToNextBlockAndKeepColor(button_block, next_button_block)
            if next_button_block_index in self.end_point_list:
                if next_button_block_index not in self.accomplishment_points:
                    self.accomplishment_points.append(next_button_block_index)
                    print("acc len:" + str(len(self.accomplishment_points)) + " end_points:" + str(len(self.end_point_list)))
            return next_button_block, 1
        else:
            print("Block not valid")
            self.accomplishment_points = range(len(self.end_point_list))
            return button_block, 0
    def _moveArrow(self, item, button_block):
        self.changeColor(button_block, item[2])
        direction_output = self.turnArrow(item[0], button_block)
        if direction_output:
            pass
        else:
            return button_block, 0
        try:
        	next_button_block = self.determineNextBox(button_block)
        except:
        	self.goToPopup("Bummer you made a wrong move", 0)
        	self.accomplishment_points = range(len(self.end_point_list))
        next_button_block_index = self.grid_blocks_layout_object.children.index(next_button_block)
        block_valid = self.checkBlockValidity(next_button_block)
        if block_valid:
            self.moveToNextBlockAndKeepColor(button_block, next_button_block)
            if next_button_block_index in self.end_point_list:
                if next_button_block_index not in self.accomplishment_points:
                    self.accomplishment_points.append(next_button_block_index)
                    print("acc len:" + str(len(self.accomplishment_points)) + " end_points:" + str(len(self.end_point_list)))
                    if len(self.accomplishment_points) == len(self.end_point_list):
                    	self.goToPopup("Congrats you've made to the next level!", 1)
            return next_button_block, 1
        else:
            print("Block not valid")
            print("go to popup")
            self.goToPopup("Bummer you made a wrong move", 0)
            self.accomplishment_points = range(len(self.end_point_list))
            return button_block, 0
    def goToPopup(self, message, result):
        self.pop_up_box_object.pop_up_text_object.text = message
        self.transparent_screen_manager_object.transition =NoTransition()
        self.transparent_screen_manager_object.current = "pop_up_screen"
        self.result = result
    def colordBlockValidity(self, button_block, item):
        color = button_block.button_color
        command_color = item[1]
        if (command_color == color) or (command_color == []):
            return True
        else:
            return False
    def _walkArrow(self, commands):
        commands_table = commands
        try:
            instruction_list = commands_table["f1"]
            print("instruction_list:"+str(instruction_list))
        except:
            instruction_list = []
        direction = self.current_arrow_direction
        print("initial direction:"+str(direction))
        button_block = self.grid_blocks_layout_object.children[self.start_position]
        for item in instruction_list:
            print("Item:"+str(item))
            color_qual = self.checkColorQualification(button_block, item[1])
            if color_qual:
                button_block, put_lock = self._moveArrow(item, button_block)
                if item[0] in commands_table:    
                    self.start_position = self.grid_blocks_layout_object.children.index(button_block)
                    self._walkArrow(commands_table)
            if len(self.accomplishment_points) == len(self.end_point_list):
                break
        print("LOOP DONE")
    def wa(self, commands):
        commands_table = commands
        try:
            instruction_list = commands["f1"]
            print("instruction_list:"+str(instruction_list))
        except:
            instruction_list = []
            self.goToPopup("Bummer you made a wrong move", 0)
        lock_count = 0
        direction = self.current_arrow_direction
        tt= commands_table
        print("Commands table before loop:"+str(commands_table))
        print("initial direction:"+str(direction))
        button_block = self.grid_blocks_layout_object.children[self.start_position]
        while len(self.accomplishment_points) != len(self.end_point_list):
            if len(instruction_list) > 0:
                color_qual = self.checkColorQualification(button_block, instruction_list[0][1])
                if color_qual:
                    button_block, put_lock = self._moveArrow(instruction_list[0], button_block)
                    if put_lock:
                        print("Putting lock")
                        lock = self.locks[lock_count]
                        try:
                        	lock.release()
                        except:
                        	pass
                        lock_count = lock_count + 1
                        print(len(self.locks))
                    if instruction_list[0][0] in commands_table:
                        print("command_key:"+str(instruction_list[0][0]))
                        print("command_table:"+str(commands))
                        new_commands = commands_table[instruction_list[0][0]]
                        print("new_commands:"+str(new_commands))
                        instruction_list = instruction_list[1:]
                        instruction_list = new_commands + instruction_list
                    else:
                        print("Current Action:"+str(instruction_list[0]))
                        instruction_list = instruction_list[1:]	
                else:
                    print("Color does not fit")
                    instruction_list = instruction_list[1:]
            else:
                print("Instruction List now equal to zero")
                if len(self.accomplishment_points) == len(self.end_point_list):
                	self.goToPopup("Congrats you've made to the next level!", 1)
                else:
                	self.accomplishment_points = range(len(self.end_point_list))
                	self.goToPopup("Bummer you made a wrong move", 0)
                break
    def walkArrow(self):
        direction = self.current_arrow_direction
        print("initial direction:"+str(direction))
        instruction_list = [("up", None, [255, 157, 60]), ("left", [0, 255, 128], None),
                            ("left", [0, 162, 232], [255, 157, 60]), ("left", [0, 255, 128], None)]
        button_block = self.grid_blocks_layout_object.children[self.start_position]
        counter = 0
        lock_count = 0
        print("nLocks:"+str(len(self.locks)))
        print("End points:" + str(self.end_point_list))
        while len(self.accomplishment_points) != len(self.end_point_list):
            color_qual = self.checkColorQualification(button_block, instruction_list[counter][1])
            if color_qual: 
                counter = self.findInstructionForColordBlock(button_block, instruction_list, counter)
                button_block, put_lock = self.moveArrow(counter, instruction_list, button_block)
                if put_lock:
                    print("Putting lock")
                    lock = self.locks[lock_count]
                    lock.release()
                    lock_count = lock_count + 1
                    print(len(self.locks))
                counter = counter + 1
            else:
                try:
                    print("On try")
                    counter = counter + 1
                except:
                    counter = 0
            
            if counter == len(instruction_list):
                counter = 0
    def findInstructionForColordBlock(self, button_block, instr_list, counter):
        color = button_block.button_color
        print(color)
        command_color = instr_list[counter][1]
        if command_color == None:
            return counter
        else:
            if command_color != color:
                if (counter + 1) == len(instr_list):
                    return 0
                else:
                    return counter + 1
        return counter
    def speedChange(self, button, buttons_list):
        button.background_normal = "icons/48_48_48.png"
        button.background_down = "icons/48_48_48.png"
        button.color = [1, 1, 1, 1]
        for _button in buttons_list:
            if _button != button:
                _button.background_normal = "icons/255_255_255.png"
                _button.background_down = "icons/255_255_255.png"
                _button.color = [0, 0, 0, 1]
    def setOneSecondSpeed(self, button):
        buttons_list = self.speed_munipulate_buttons_space_object.children
        self.arrow_speed = 1
        self.speedChange(button, buttons_list)
    def setOneHalfSecondSpeed(self, button):
        buttons_list = self.speed_munipulate_buttons_space_object.children
        self.arrow_speed = 0.5
        self.speedChange(button, buttons_list)
    def setOneTenthSecondSpeed(self, button):
        buttons_list = self.speed_munipulate_buttons_space_object.children
        self.arrow_speed = 0.1
        self.speedChange(button, buttons_list)
    def getReverseList(self, _list):
        new_list = []
        for i in range(len(_list)):
            new_list.append(0)
        index = -1
        for item in _list:
            new_list[index] = item
            index = index -1
        return new_list
    def getFunctionInstruction(self, function_space_parent):
        instructions_table = dict()
        function_counter = 1
        user_inputs = self.function_and_control_box_object.instruction_table
        for function_space in function_space_parent:
            print("Function space:"+str(function_space))
            grid_layout = function_space.children[0]
            print("Instruction Buttons Space:"+str(grid_layout))
            buttons_list = grid_layout.children
            buttons_list = self.getReverseList(buttons_list)
            print("Buttons List:"+str(buttons_list))
            if user_inputs:
                instructions_table["f"+str(function_counter)] = []
                buttons_counter = 1
                print("Buttons List Length:"+str(len(buttons_list)))
                while buttons_counter < len(buttons_list):
                    print("user_inputs--:"+str(user_inputs))
                    print("input_buttons--:"+str(buttons_list))
                    print("Button-Counter--:"+str(buttons_counter))
                    print("input_button_one--:"+str(buttons_list[buttons_counter]))
                    try:
                        print("-------INstruction:---"+str(user_inputs[buttons_list[buttons_counter]]))
                        sub_commands = []
                        arrow_object = user_inputs[buttons_list[buttons_counter]]["arrow_button"]
                        print("Arrow:-----"+str(arrow_object.direction))
                        sub_commands.append(arrow_object.direction)
                        color_object = user_inputs[buttons_list[buttons_counter]]["color_button"]
                        print("Color:-----"+str(color_object.button_color))
                        if color_object.button_color == []:
                            sub_commands.append(None)
                        else:
                            sub_commands.append(color_object.button_color)
                        if arrow_object.brush_color == []:
                            sub_commands.append(None)
                        else:
                            sub_commands.append(arrow_object.brush_color)
                        print("Arrow:-----"+str(arrow_object.brush_color))
                        print("button_list index:"+str(buttons_counter))
                        buttons_counter = buttons_counter + 1
                        instructions_table["f"+str(function_counter)].append(sub_commands)
                        print("button list length:"+str(len(buttons_list)))
                        print("button_list index:"+str(buttons_counter))
                    except:
                        buttons_counter = buttons_counter + 1
            function_counter = function_counter + 1
        print("INSTRUCTIONS____TABLE:"+str(instructions_table))
        return instructions_table
    def playGame(self, button):
        if self.playing == 0:
            self.playing = 1
            functions_space_list = self.function_and_control_box_object.functions_space_object.children
            functions_space_list.reverse()
            commands = self.getFunctionInstruction(functions_space_list)
            button.background_normal = "icons/black_play.png"
            button.background_down = "icons/black_play.png"
            thread.start_new_thread(self.wa, (commands, ))
class TestApp(App):
    def build(self):
        root = MainStageSpaceBox()
        print("Start form blocks")
        root.formBlocksGrid()
        root.putColorBlocks()
        print("End form blocks")
        return root
if __name__ == "__main__":
    TestApp().run()
