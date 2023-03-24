import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget


class CustomButton(Button):
    snack_name = ""


class CustomTextInput(TextInput):
    pass


class VendingMachine:
    total_revenue = 0  

    snack_prices = {"candy": 2.00, "soda": 1.50, "chips": 3.00, "cookies": 3.50}

   
    def __init__(self, inventory, serial, days_until_maintenance):
        self.inventory = inventory  
        self.revenue = 0  
        self.days_until_maintenance = days_until_maintenance

    
    def sales_menu(self, instance):
        
        content = BoxLayout(orientation='vertical')
        greetings = Label(text="Welcome! I have:")
        content.add_widget(greetings)
        for i, snack in enumerate(self.inventory):
            button = CustomButton(text=snack.capitalize())
            button.snack_name = snack
            button.bind(on_press=self.process_sale)
            content.add_widget(button)

        popup = Popup(title='Select a snack', content=content, size_hint=(0.5, 0.5))
        popup.open()

    
    def process_sale(self, button):
        option = button.snack_name
        print(f"Button {option.capitalize()} was pressed.")
        content = BoxLayout(orientation='vertical')
        prompt = Label(text=f"How many {option.capitalize()} would you like to buy?")
        input_box = TextInput(multiline=False)
        content.add_widget(prompt)
        content.add_widget(input_box)

        def update_inventory(instance):
            try:
                quantity = int(input_box.text)
                if quantity > 0:
                    self.update_inventory(option, quantity)
                    popup.dismiss()
                    confirm_popup = Popup(title='Sale confirmed',
                                        content=Label(text=f"You bought {quantity} {option.capitalize()}!"),
                                        size_hint=(0.5, 0.5))
                    confirm_popup.open()
            except ValueError:
                pass

        
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
                
                
            # Check if there are enough snacks in the inventory to fulfill the order
            if num_items > self.inventory[option]:
                error_msg = Label(text="I'm sorry, I don't have enough {} in stock. Please choose a smaller quantity".format(option))
                content.add_widget(error_msg)
                return

            # Calculate the total price of the purchase
            total_price = num_items * self.snack_prices[option]
            self.revenue += total_price
            VendingMachine.total_revenue += total_price

            # Update the inventory
            self.inventory[option] -= num_items

            # Display a confirmation message
            confirmation_msg = Label(text="Great! That will be ${:.2f}. Enjoy your {}!".format(total_price, option))
            content.add_widget(confirmation_msg)
            popup.dismiss()

        confirm_button = Button(text='Confirm')
        confirm_button.bind(on_press=update_inventory)
        content.add_widget(confirm_button)

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



class VendingMachineApp(App):
    def build(self):
        vm= VendingMachine(inventory={"candy": 10, "soda": 10, "chips": 10, "cookies": 10}, serial="VM001", days_until_maintenance=5)
        vm.sales_menu(None)
        return Widget()

if __name__== '__main__':
    VendingMachineApp().run()
