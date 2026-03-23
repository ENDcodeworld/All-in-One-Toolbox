from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.metrics import dp
import random
import string
import qrcode
from io import BytesIO
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image


class ToolboxApp(App):
    """全能工具箱APP"""
    
    def build(self):
        self.title = '全能工具箱'
        Window.clearcolor = get_color_from_hex('#263238')
        
        self.root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title = Label(
            text='🧰 全能工具箱',
            font_size=dp(28),
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=None,
            height=dp(60),
            bold=True
        )
        self.root.add_widget(title)
        
        # 工具按钮网格
        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, padding=dp(10))
        grid.bind(minimum_height=grid.setter('height'))
        
        tools = [
            ('📏 单位换算', self.show_converter, '#FF5722'),
            ('🔢 科学计算器', self.show_calculator, '#2196F3'),
            ('🔐 密码生成', self.show_password, '#9C27B0'),
            ('🎲 随机数', self.show_random, '#4CAF50'),
            ('📊 单位换算', self.show_unit, '#FF9800'),
            ('⏱️ 计时器', self.show_timer, '#00BCD4'),
            ('📝 计数器', self.show_counter, '#E91E63'),
            ('📐 BMI计算', self.show_bmi, '#8BC34A'),
        ]
        
        for text, callback, color in tools:
            btn = Button(
                text=text,
                font_size=dp(16),
                background_color=get_color_from_hex(color),
                color=get_color_from_hex('#FFFFFF'),
                size_hint_y=None,
                height=dp(100)
            )
            btn.bind(on_press=callback)
            grid.add_widget(btn)
        
        scroll.add_widget(grid)
        self.root.add_widget(scroll)
        
        # 内容区
        self.content_box = BoxLayout(orientation='vertical', size_hint_y=0.6)
        self.root.add_widget(self.content_box)
        
        # 默认显示密码生成器
        self.show_password(None)
        
        return self.root
    
    def clear_content(self):
        self.content_box.clear_widgets()
    
    def show_converter(self, instance):
        """单位换算"""
        self.clear_content()
        
        title = Label(text='📏 单位换算', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 输入
        input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        self.conv_input = TextInput(hint_text='输入数值', input_filter='float', multiline=False, font_size=dp(16))
        input_box.add_widget(self.conv_input)
        self.content_box.add_widget(input_box)
        
        # 换算按钮
        btn_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(5))
        
        conversions = [
            ('米→英尺', lambda x: float(x) * 3.28084),
            ('℃→℉', lambda x: float(x) * 9/5 + 32),
            ('kg→磅', lambda x: float(x) * 2.20462),
            ('km→英里', lambda x: float(x) * 0.621371),
        ]
        
        for text, func in conversions:
            btn = Button(text=text, font_size=dp(12))
            btn.bind(on_press=lambda x, f=func: self.do_convert(f))
            btn_box.add_widget(btn)
        
        self.content_box.add_widget(btn_box)
        
        # 结果
        self.conv_result = Label(text='结果将显示在这里', font_size=dp(18), color=get_color_from_hex('#4CAF50'))
        self.content_box.add_widget(self.conv_result)
    
    def do_convert(self, func):
        try:
            val = float(self.conv_input.text)
            result = func(val)
            self.conv_result.text = f'结果: {result:.2f}'
        except:
            self.conv_result.text = '请输入有效数字'
    
    def show_calculator(self, instance):
        """科学计算器"""
        self.clear_content()
        
        title = Label(text='🔢 科学计算器', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 显示屏
        self.calc_display = TextInput(text='0', multiline=False, font_size=dp(24), halign='right', readonly=True)
        self.content_box.add_widget(self.calc_display)
        
        # 按钮
        buttons = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '⌫']
        ]
        
        for row in buttons:
            box = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(60))
            for btn_text in row:
                btn = Button(text=btn_text, font_size=dp(20))
                btn.bind(on_press=self.calc_pressed)
                box.add_widget(btn)
            self.content_box.add_widget(box)
    
    def calc_pressed(self, instance):
        text = instance.text
        current = self.calc_display.text
        
        if text == 'C':
            self.calc_display.text = '0'
        elif text == '⌫':
            self.calc_display.text = current[:-1] if len(current) > 1 else '0'
        elif text == '=':
            try:
                result = eval(current)
                self.calc_display.text = str(result)[:12]
            except:
                self.calc_display.text = 'Error'
        else:
            if current == '0' and text not in '+-*/.()':
                self.calc_display.text = text
            else:
                self.calc_display.text = current + text
    
    def show_password(self, instance):
        """密码生成器"""
        self.clear_content()
        
        title = Label(text='🔐 密码生成器', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 长度选择
        len_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        len_box.add_widget(Label(text='长度:', color=get_color_from_hex('#FFFFFF'), size_hint_x=0.3))
        self.pwd_length = TextInput(text='12', input_filter='int', multiline=False, font_size=dp(16))
        len_box.add_widget(self.pwd_length)
        self.content_box.add_widget(len_box)
        
        # 生成按钮
        gen_btn = Button(text='🔑 生成强密码', font_size=dp(18), background_color=get_color_from_hex('#9C27B0'), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(60))
        gen_btn.bind(on_press=self.generate_password)
        self.content_box.add_widget(gen_btn)
        
        # 结果显示
        self.pwd_result = TextInput(text='', multiline=False, font_size=dp(20), readonly=True, halign='center')
        self.content_box.add_widget(self.pwd_result)
        
        # 复制按钮
        copy_btn = Button(text='📋 复制密码', font_size=dp(14), background_color=get_color_from_hex('#4CAF50'), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(50))
        copy_btn.bind(on_press=self.copy_password)
        self.content_box.add_widget(copy_btn)
        
        # 生成一个默认密码
        self.generate_password(None)
    
    def generate_password(self, instance):
        try:
            length = int(self.pwd_length.text)
            length = max(4, min(32, length))
        except:
            length = 12
        
        chars = string.ascii_letters + string.digits + '!@#$%^&*'
        password = ''.join(random.choice(chars) for _ in range(length))
        self.pwd_result.text = password
    
    def copy_password(self, instance):
        from kivy.core.clipboard import Clipboard
        Clipboard.copy(self.pwd_result.text)
        self.pwd_result.text += ' (已复制)'
    
    def show_random(self, instance):
        """随机数生成"""
        self.clear_content()
        
        title = Label(text='🎲 随机数生成', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 范围输入
        range_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        self.rand_min = TextInput(hint_text='最小值', text='1', input_filter='int', multiline=False)
        self.rand_max = TextInput(hint_text='最大值', text='100', input_filter='int', multiline=False)
        range_box.add_widget(self.rand_min)
        range_box.add_widget(self.rand_max)
        self.content_box.add_widget(range_box)
        
        # 生成按钮
        gen_btn = Button(text='🎲 生成随机数', font_size=dp(18), background_color=get_color_from_hex('#4CAF50'), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(60))
        gen_btn.bind(on_press=self.generate_random)
        self.content_box.add_widget(gen_btn)
        
        # 结果
        self.rand_result = Label(text='?', font_size=dp(48), color=get_color_from_hex('#FFEB3B'), bold=True)
        self.content_box.add_widget(self.rand_result)
    
    def generate_random(self, instance):
        try:
            min_val = int(self.rand_min.text)
            max_val = int(self.rand_max.text)
            result = random.randint(min_val, max_val)
            self.rand_result.text = str(result)
        except:
            self.rand_result.text = '错误'
    
    def show_unit(self, instance):
        """单位换算（简化版）"""
        self.show_converter(instance)
    
    def show_timer(self, instance):
        """计时器"""
        self.clear_content()
        
        title = Label(text='⏱️ 计时器', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 时间显示
        self.timer_label = Label(text='00:00:00', font_size=dp(48), color=get_color_from_hex('#00BCD4'), bold=True)
        self.content_box.add_widget(self.timer_label)
        
        # 控制按钮
        btn_box = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(60))
        
        start_btn = Button(text='▶️ 开始', background_color=get_color_from_hex('#4CAF50'))
        start_btn.bind(on_press=self.start_timer)
        btn_box.add_widget(start_btn)
        
        stop_btn = Button(text='⏸️ 暂停', background_color=get_color_from_hex('#FF9800'))
        stop_btn.bind(on_press=self.stop_timer)
        btn_box.add_widget(stop_btn)
        
        reset_btn = Button(text='🔄 重置', background_color=get_color_from_hex('#F44336'))
        reset_btn.bind(on_press=self.reset_timer)
        btn_box.add_widget(reset_btn)
        
        self.content_box.add_widget(btn_box)
        
        self.timer_seconds = 0
        self.timer_event = None
    
    def start_timer(self, instance):
        if not self.timer_event:
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
    
    def stop_timer(self, instance):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
    
    def reset_timer(self, instance):
        self.stop_timer(None)
        self.timer_seconds = 0
        self.timer_label.text = '00:00:00'
    
    def update_timer(self, dt):
        self.timer_seconds += 1
        hours = self.timer_seconds // 3600
        minutes = (self.timer_seconds % 3600) // 60
        seconds = self.timer_seconds % 60
        self.timer_label.text = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    
    def show_counter(self, instance):
        """计数器"""
        self.clear_content()
        
        title = Label(text='📝 计数器', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 计数显示
        self.count_label = Label(text='0', font_size=dp(72), color=get_color_from_hex('#E91E63'), bold=True)
        self.content_box.add_widget(self.count_label)
        
        # 控制按钮
        btn_box = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(80))
        
        minus_btn = Button(text='➖', font_size=dp(30), background_color=get_color_from_hex('#F44336'))
        minus_btn.bind(on_press=self.decrement)
        btn_box.add_widget(minus_btn)
        
        reset_btn = Button(text='🔄', font_size=dp(24), background_color=get_color_from_hex('#FF9800'))
        reset_btn.bind(on_press=self.reset_count)
        btn_box.add_widget(reset_btn)
        
        plus_btn = Button(text='➕', font_size=dp(30), background_color=get_color_from_hex('#4CAF50'))
        plus_btn.bind(on_press=self.increment)
        btn_box.add_widget(plus_btn)
        
        self.content_box.add_widget(btn_box)
        
        self.counter = 0
    
    def increment(self, instance):
        self.counter += 1
        self.count_label.text = str(self.counter)
    
    def decrement(self, instance):
        self.counter -= 1
        self.count_label.text = str(self.counter)
    
    def reset_count(self, instance):
        self.counter = 0
        self.count_label.text = '0'
    
    def show_bmi(self, instance):
        """BMI计算器"""
        self.clear_content()
        
        title = Label(text='📐 BMI计算器', font_size=dp(20), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(40))
        self.content_box.add_widget(title)
        
        # 身高输入
        height_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        height_box.add_widget(Label(text='身高(cm):', color=get_color_from_hex('#FFFFFF'), size_hint_x=0.4))
        self.bmi_height = TextInput(hint_text='170', input_filter='float', multiline=False)
        height_box.add_widget(self.bmi_height)
        self.content_box.add_widget(height_box)
        
        # 体重输入
        weight_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50), spacing=dp(10))
        weight_box.add_widget(Label(text='体重(kg):', color=get_color_from_hex('#FFFFFF'), size_hint_x=0.4))
        self.bmi_weight = TextInput(hint_text='65', input_filter='float', multiline=False)
        weight_box.add_widget(self.bmi_weight)
        self.content_box.add_widget(weight_box)
        
        # 计算按钮
        calc_btn = Button(text='📊 计算BMI', font_size=dp(18), background_color=get_color_from_hex('#8BC34A'), color=get_color_from_hex('#FFFFFF'), size_hint_y=None, height=dp(60))
        calc_btn.bind(on_press=self.calculate_bmi)
        self.content_box.add_widget(calc_btn)
        
        # 结果显示
        self.bmi_result = Label(text='输入身高体重后点击计算', font_size=dp(16), color=get_color_from_hex('#FFFFFF'), markup=True)
        self.content_box.add_widget(self.bmi_result)
    
    def calculate_bmi(self, instance):
        try:
            height = float(self.bmi_height.text) / 100  # 转换为米
            weight = float(self.bmi_weight.text)
            bmi = weight / (height ** 2)
            
            if bmi < 18.5:
                status = '[color=#2196F3]偏瘦[/color]'
            elif bmi < 24:
                status = '[color=#4CAF50]正常[/color]'
            elif bmi < 28:
                status = '[color=#FF9800]偏胖[/color]'
            else:
                status = '[color=#F44336]肥胖[/color]'
            
            self.bmi_result.text = f'您的BMI: [b]{bmi:.1f}[/b]\n体型: {status}'
            self.bmi_result.markup = True
        except:
            self.bmi_result.text = '请输入有效的数字'


if __name__ == '__main__':
    ToolboxApp().run()
