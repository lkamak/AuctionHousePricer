from BlizzardAPI import BlizzardAPI

newObj = BlizzardAPI()
newObj.get_all_realms()
newObj.write_realms_to_file()
newObj.get_realm_id("Illidan")
newObj.get_all_auctions()
skygolem_id = newObj.get_item_id("Shadowghast Ingot")
print(skygolem_id)
print(newObj.is_stackable(skygolem_id))
print(newObj.get_item_price(skygolem_id))

def simple_interface():
    user_in = input("What item are you looking for?: ")
    loop_check = True

    while loop_check == True:
        curr_item = user_in1
        curr_item_id = newObj.get_item_id(curr_item)
        curr_item_cost = newObj.get_item_price(curr_item_id)
        print(curr_item_cost)

        user_in2 = input("Would you like to search for something else? ")

        if user_in2 != "yes":
            loop_check = False
            break

        user_in = input("What item are you looking for?: ")

#class Search_Interface():


