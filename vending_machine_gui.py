from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class CustomButton(Button):
    snack_name = ""


class CustomTextInput(TextInput):
    pass


class VendingMachine:
    total_revenue = 0  # Total revenue of all vending machines in the system

    snack_prices = {"candy": 2.00, "soda": 1.50, "chips": 3.00, "cookies": 3.50}

    # Instance attributes
    def __init__(self, inventory, serial, days_until_maintenance):
        self.inventory = inventory  # dictionary with {<snack>: <amount>} as key-value pairs. Possible snacks: candy, soda, chips, cookies. Keys written in lowercase.
        self.revenue = 0  # Initially, when an instance of the vending machine is created, the revenue is 0 and it's updated with each sale.
        self.serial = serial
        self.days_until_maintenance = days_until_maintenance

    # Method that displays an interactive menu to process a sale.
    # Displays the options, gets user input to select the snack, and calls
    # another method to process the sale.
    def sales_menu(self, instance):
        # The user has the option to buy several types of snacks
        # so the program is repeated if the user indicates that he/she
        # would like to buy another snack
        content = BoxLayout(orientation='vertical')
        greetings = Label(text="Welcome! I have:")
        content.add_widget(greetings)
        for i, snack in enumerate(self.inventory):
            button = CustomButton(text=snack.capitalize())
            button.snack_name = snack
            button.bind(on_press=instance.process_sale)
            content.add_widget(button)

        popup = Popup(title='Select a snack', content=content, size_hint=(0.5, 0.5))
        popup.open()

    # Method that processes the sale by asking the user how many snacks of that type
    # he/she would like to buy and calls another method to opdate the inventory
    def process_sale(self, button):
        option = button.snack_name
        popup = Popup(title=option.capitalize(), size_hint=(0.5, 0.5))

        if self.inventory[option] > 0:
            # Display current snack inventory and product
            msg1 = Label(text="Great! I currently have {} {} in my inventory".format(self.inventory[option], option))
            content = BoxLayout(orientation='vertical')
            content.add_widget(msg1)

            # Ask for the number of snacks
            num_items_input = CustomTextInput(hint_text="How many {} would you like to buy?".format(option))

            def buy_snacks(button):
                num_items_str = num_items_input.text
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

            buy_button = Button(text="Buy")
            buy_button.bind(on_press=buy_snacks)
            content.add_widget(num_items_input)
            content.add_widget(buy_button)

        else:
            # Display an error message if there are no snacks in the inventory
            msg2 = Label(text="I'm sorry, I'm all out of {} for now".format(option))
            content = BoxLayout(orientation='vertical')
            content.add_widget(msg2)

                
            popup.content = content
            popup.open()

                

# Method that checks if the vending machine needs maintenance based on the number of days until maintenance
# and displays a message to the user if necessary.
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




#Method that creates the instance of the VendingMachine class
# and sets the initial inventory and maintenance days
class MyApp(App):
    def build(self):
        self.vending_machine = VendingMachine(inventory={"candy": 10, "soda": 10, "chips": 10, "cookies": 10}, serial="VM001", days_until_maintenance=5)
        return BoxLayout()

    # Method that gets called when the "Sales menu" button is pressed
    def sales_menu(self, instance):
        self.vending_machine.sales_menu(instance)


if name == 'main':
    MyApp().run()