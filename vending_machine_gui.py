import kivy
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image


class CustomButton(Button):
    snack_name = ""


class CustomTextInput(TextInput):
    pass


class VendingMachine:
    total_revenue = 0  

    snack_prices = {"candy": 2.00, "soda": 1.50, "chips": 3.00, "cookies": 3.50}
    snack_images = {"candy":"candy.jpg", "soda":"soda.jpg", "chips":"chips.jpg", "cookies":"cookies.jpg"}
   
    def __init__(self, inventory, serial, days_until_maintenance):
        self.inventory = inventory  
        self.revenue = 0  
        self.days_until_maintenance = days_until_maintenance
        self.purchase_made=False

    
    def sales_menu(self, instance):
        content = BoxLayout(orientation='vertical')
        greetings = Label(text="Welcome! I have:")
        content.add_widget(greetings)
        for snack, quantity in self.inventory.items():
            inventory_label = Label(text=f"{snack.capitalize()} :  Available Quantity {quantity}")
            content.add_widget(inventory_label)

             # Create an Image widget for the snack
            snack_image = Image(source=self.snack_images[snack])
            content.add_widget(snack_image)
            
            button = CustomButton(text="Buy")
            button.snack_name = snack
            button.bind(on_press=self.process_sale)
            content.add_widget(button)

        if self.purchase_made:
            back_button = Button(text='Back to Main Menu')
            back_button.bind(on_press=self.back_to_menu)
            content.add_widget(back_button)


        popup = Popup(title='Select a snack', content=content, size_hint=(0.5, 0.5))
        popup.open()

    def back_to_menu(self, instance):
        self.purchase_made = False  # reset the flag when going back to the main menu
        self.sales_menu(instance)

    
    def process_sale(self, button):
        option = button.snack_name
        print(f"Button {option.capitalize()} was pressed.")
        content = BoxLayout(orientation='vertical')
        prompt = Label(text=f"How many {option.capitalize()} would you like to buy?")
        input_box = TextInput(multiline=False)
        content.add_widget(prompt)
        content.add_widget(input_box)
    
    
        def update_inventory(self, snack_name, quantity):
            if snack_name in self.inventory:
                self.inventory[snack_name] += quantity
            else:                
                self.inventory[snack_name] = quantity


        def buy_snacks(button):
            num_items_str = input_box.text
            try:
                num_items = int(num_items_str)
            except ValueError:
                error_msg = Label(text="Please enter a positive integer")
                content.add_widget(error_msg)
                return

            if num_items <= 0:
                error_msg = Label(text="Please enter a positive integer")
                content.add_widget(error_msg)
                return
                
                
            if num_items > self.inventory[option]:
                error_msg = Label(text="I'm sorry, I don't have enough {} in stock. Please choose a smaller quantity".format(option))
                content.add_widget(error_msg)
                return

    
            total_price = num_items * self.snack_prices[option]
            self.revenue += total_price
            VendingMachine.total_revenue += total_price


            self.inventory[option] -= num_items
            confirmation_msg = Label(text="Great! That will be ${:.2f}. Enjoy your {}!".format(total_price, option))
            content.add_widget(confirmation_msg)
            time.sleep(0)

            # Show a popup asking if the user wants to make another purchase
            another_purchase_popup_content = BoxLayout(orientation='vertical')
            another_purchase_prompt = Label(text="Would you like to buy the  another item?")
            yes_button = Button(text='Yes')
            no_button = Button(text='No')


            def show_sales_menu(button):
                self.sales_menu(None)


            def dismiss_popup(button):
                popup.dismiss()


            yes_button.bind(on_press=show_sales_menu)
            no_button.bind(on_press=dismiss_popup)


            another_purchase_popup_content.add_widget(another_purchase_prompt)
            another_purchase_popup_content.add_widget(yes_button)
            another_purchase_popup_content.add_widget(no_button)


            popup = Popup(title='Purchase Complete', content=another_purchase_popup_content, size_hint=(0.5, 0.5))
            popup.open()
            

        buy_button = Button(text='Buy')
        buy_button.bind(on_press=buy_snacks)
        content.add_widget(buy_button)
        

        popup= Popup(title=option.capitalize(), content=content, size_hint=(0.5, 0.5))
        popup.open()


    def check_maintenance(self):
        if self.days_until_maintenance == 0:
            msg = "Maintenance is required for vending machine {}.".format(self.serial)
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text=msg))
            popup = Popup(title="Maintenance Required", content=content, size_hint=(0.5, 0.5))
            popup.open()
            
        else:
            msg = "Vending machine {} is in good condition.".format(self.serial)
            content = BoxLayout(orientation='vertical')
            content.add_widget(Label(text=msg))
            popup = Popup(title="Maintenance Check", content=content, size_hint=(0.5, 0.5))
            popup.open()


class VendingMachineWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #size: root.width;root.height
        self.vm = VendingMachine(inventory={"candy": 100, "soda": 100, "chips": 100, "cookies": 100}, serial="VM001", days_until_maintenance=5)
        layout = BoxLayout(orientation='vertical')
        sales_button = Button(text='Sales Menu',font_size=15,size_hint=(None,None), size=(200,100),pos=(Window.width, Window.height))
        sales_button.bind(on_press=self.vm.sales_menu)
        layout.add_widget(sales_button)
        self.add_widget(layout)
        

class VendingMachineApp(App):
    def build(self):
        root_widget = BoxLayout(orientation='vertical')
        vm_widget = VendingMachineWidget()
        root_widget.add_widget(vm_widget)
        return root_widget


    def on_start(self):
        pass


if __name__ == '__main__':
    VendingMachineApp().run()



