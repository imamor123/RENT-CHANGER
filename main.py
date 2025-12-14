from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

Window.clearcolor = (0.95, 0.95, 0.95, 1)  # light background

class ColoredBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.9, 0.95, 1, 1)  # light blue background
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class RentDepositApp(App):
    def build(self):
        self.title = "Rent & Deposit Converter"
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Inputs with large font size
        self.deposit_initial = TextInput(hint_text="Initial Deposit", multiline=False, halign='center', input_filter='float', font_size=64)
        self.rent_initial = TextInput(hint_text="Initial Rent", multiline=False, halign='center', input_filter='float', font_size=64)
        self.deposit_new = TextInput(hint_text="New Deposit", multiline=False, halign='center', input_filter='float', font_size=64)
        self.rent_new = TextInput(hint_text="New Rent", multiline=False, halign='center', input_filter='float', font_size=64)

        layout.add_widget(self.deposit_initial)
        layout.add_widget(self.rent_initial)
        layout.add_widget(self.deposit_new)
        layout.add_widget(self.rent_new)

        # Buttons
        btn_calc_rent = Button(text="Calculate New Rent", background_color=(0.2, 0.6, 0.9, 1), font_size=64)
        btn_calc_rent.bind(on_press=self.calculate_rent)

        btn_calc_deposit = Button(text="Calculate New Deposit", background_color=(0.3, 0.7, 0.4, 1), font_size=64)
        btn_calc_deposit.bind(on_press=self.calculate_deposit)

        btn_calc_totals = Button(text="Calculate Totals & Commissions", background_color=(0.8, 0.5, 0.2, 1), font_size=64)
        btn_calc_totals.bind(on_press=self.calculate_totals)

        layout.add_widget(btn_calc_rent)
        layout.add_widget(btn_calc_deposit)
        layout.add_widget(btn_calc_totals)

        # Result box with colored background
        result_box = ColoredBox(orientation='vertical', padding=10)
        self.result_label = Label(text="", font_size=48, color=(0, 0, 0, 1))
        result_box.add_widget(self.result_label)
        layout.add_widget(result_box)

        return layout

    def calculate_rent(self, instance):
        try:
            deposit_initial = float(self.deposit_initial.text)
            rent_initial = float(self.rent_initial.text)
            deposit_new = float(self.deposit_new.text)
            rent_new = rent_initial + ((deposit_initial - deposit_new) / 1000 * 30)
            self.result_label.text = f"New Rent: {int(rent_new)}"
        except:
            self.result_label.text = "⚠️ Please enter valid numbers!"

    def calculate_deposit(self, instance):
        try:
            deposit_initial = float(self.deposit_initial.text)
            rent_initial = float(self.rent_initial.text)
            rent_new = float(self.rent_new.text)
            deposit_new = deposit_initial + ((rent_initial - rent_new) * 1000 / 30)
            self.result_label.text = f"New Deposit: {int(deposit_new)}"
        except:
            self.result_label.text = "⚠️ Please enter valid numbers!"

    def calculate_totals(self, instance):
        try:
            deposit_initial = float(self.deposit_initial.text)
            rent_initial = float(self.rent_initial.text)

            total_rent = (deposit_initial / 1000 * 30) + rent_initial
            total_deposit = (rent_initial * 1000 / 30) + deposit_initial
            union_commission = (total_rent / 4) + ((total_rent / 4) * 10 / 100)
            our_commission = total_rent / 3

            self.result_label.text = (
                f"Total Rent: {int(total_rent)}\n"
                f"Total Deposit: {int(total_deposit)}\n"
                f"Union Commission: {int(union_commission)}\n"
                f"Realstate Commission: {int(our_commission)}"
            )
        except:
            self.result_label.text = "⚠️ Please enter valid numbers!"

if __name__ == "__main__":
    RentDepositApp().run()