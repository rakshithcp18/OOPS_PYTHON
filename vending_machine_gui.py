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
from kivy.uix.gridlayout import GridLayout

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
        self.menu_displayed = False
        self.total_quantity_purchased = 0
        self.snack_quantities = {"candy": 0, "soda": 0, "chips": 0, "cookies": 0}
        self.snack_costs = {"candy": 0.0, "soda": 0.0, "chips": 0.0, "cookies": 0.0}

    
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
            
            button = CustomButton(text="Buy",size_hint=(0.1, 0.5), pos_hint={'center_x':0.5,'center_y':0.5})
            button.background_normal=''
            button.background_color=(81/255,52/255,186/255,1)
            button.padding:50
            button.spacing:20
            button.snack_name = snack
            button.bind(on_press=self.process_sale)
            content.add_widget(button)

        exit_button = Button(text='Exit', size_hint=(0.1, 0.5), pos_hint={'x':0,'top':1})
        exit_button.background_normal=''
        exit_button.background_color=(52/255,171/255,235/255,1)
        exit_button.bind(on_press=App.get_running_app().stop)
        content.add_widget(exit_button)


        popup = Popup(title='Select a snack', content=content, size_hint=(0.5, 0.5))
        popup.open()

        self.menu_displayed = False

    def show_purchase_summary(self):
        if self.menu_displayed:
            self.sales_menu(None)
        else:
            content = BoxLayout(orientation='vertical')
            total_quantity = (self.total_quantity_purchased)
            total_amount = self.revenue

            summary_label = Label(text=" Thanks for purchasing the items.\n You have purchased a total of {0} items for ${1}.\n  Have a good day".format(total_quantity,total_amount))
            content.add_widget(summary_label)

            ok_button = Button(text='Click here to exit the page', size_hint=(0.3, 0.1), pos_hint={'center_x':0.5,'center_y':0.5})
            ok_button.background_normal=''
            ok_button.background_color=(52/255,171/255,235/255,1)
            ok_button.bind(on_press=App.get_running_app().stop)
            content.add_widget(ok_button)

            popup = Popup(title='Purchase Summary', content=content, size_hint=(0.5, 0.5))
            popup.open()
        
        
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

        self.purchase_made = True

        def show_error_popup(error_msg):
            invalid_input_entered_content = BoxLayout(orientation="vertical")
            invalid_input_entered_prompt = Label(text=error_msg)
            
            # Create an input box for the quantity of snacks
            input_box = TextInput(multiline=False, input_type='number')
            invalid_input_entered_content.add_widget(invalid_input_entered_prompt)
            invalid_input_entered_content.add_widget(input_box)

            # Create a button to buy snacks with the corrected quantity
            buy_button = Button(text='Buy')
            buy_button.bind(on_press=lambda button: self.buy_snacks(num_items_str=input_box.text, snack_name=option))

            
            # Create a button to show the sales menu
            sales_menu_button = Button(text="Show Sales Menu")
            sales_menu_button.bind(on_press=self.sales_menu)

            def buy_snacks(button,num_items_str):
                popup.dismiss()
                # Call the buy_snacks function with the corrected parameter
                buy_snacks_func()

            buy_button.bind(on_press=buy_snacks)

            # invalid_input_entered_content.add_widget(invalid_input_entered_prompt)
            invalid_input_entered_content.add_widget(buy_button)
            invalid_input_entered_content.add_widget(sales_menu_button)

            popup = Popup(title='Invalid Input', content=invalid_input_entered_content, size_hint=(0.5, 0.5))
            popup.open()


        def buy_snacks_func(num_items_str):
            num_items_str = input_box.text
            try:
                num_items = int(num_items_str)
            except ValueError:
                show_error_popup("Please enter a positive integer")
                return

            if num_items <= 0:
                show_error_popup("Please enter a positive integer")
                return
                
            if num_items > self.inventory.get(option, 0):   
                show_error_popup("I'm sorry, I don't have enough {} in stock. Please choose a smaller quantity".format(option))
                return
            
    
            total_price = num_items * self.snack_prices[option]
            self.revenue += total_price
            VendingMachine.total_revenue += total_price


            self.inventory[option] -= num_items
            self.total_quantity_purchased += num_items
            confirmation_msg = Label(text="Great! That will be ${:.2f}. Enjoy your {}!".format(total_price, option))
            content.add_widget(confirmation_msg)
 
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
            no_button.bind(on_press=lambda instance: [dismiss_popup(instance), self.show_purchase_summary()])

            another_purchase_popup_content.add_widget(another_purchase_prompt)
            another_purchase_popup_content.add_widget(yes_button)
            another_purchase_popup_content.add_widget(no_button)


            popup = Popup(title='Purchase Complete', content=another_purchase_popup_content, size_hint=(0.5, 0.5))
            popup.open()

        buy_button = Button(text='Buy')
        buy_button.bind(on_press=buy_snacks_func)
        content.add_widget(buy_button)

        # Create a button to cancel the purchase
        cancel_button = Button(text='Cancel')
        cancel_button.bind(on_press=self.sales_menu)
        content.add_widget(cancel_button)

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
        self.vm = VendingMachine(inventory={"candy": 100, "soda": 100, "chips": 100, "cookies": 100}, serial="VM001", days_until_maintenance=0)
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
