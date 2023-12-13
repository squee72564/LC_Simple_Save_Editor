from encryption.encryptTools import encrypt, decrypt
import tkinter as tk
from tkinter import filedialog
import random
import sys
import json

# Used with button to increment moon
def incrementMoon(planet_var, planets, planet_str):
    value = planet_var.get()    
    planet_var.set((value + 1) % len(planets))
    planet_str.set(planets[planet_var.get()])

# Used to validate numeric input for tkinter
def validate_numeric(value):
    return value.isnumeric() or value == ''

# Used with entry to change scrap value for selected item
def on_entry_change(*args):
    selected_index = items_listbox.curselection()
    if selected_index and selected_index[0] < len(item_info):
        selected_index = selected_index[0]
        item_name, scrap_val = item_info[selected_index]
        value = scrap_price_var.get()
        if value != '' and value != '0' and item_ids[selected_index] in scrap:
            scrap_idx = sum(1 for item in item_ids[:selected_index] if item in scrap)
            item_values[scrap_idx] = int(value)
            item_info[selected_index] = (item_name, int(value))

# Used with button to add new item
def on_add_item(*args):
    val = selected_dropdown_value.get()
    if val in items.values():
        key = items_rev_mapping[val]
        item_ids.append(key)
        item_pos.append({'x':0, 'y':0, 'z':0})
        if key in scrap:
            num = 30
            item_values.append(num)
            item_info.append((val, num))
        elif key in save_items:
            num =20 
            item_info.append((val, None))

            if key == 'shotgun':
                save_data.append(1)
            if key == 'shotgun shell':
                save_data.append(0)
        else:
            item_info.append((val, None))
        items_listbox.insert(tk.END, val)

def on_remove_item(*args):
    selected_index = items_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        items_listbox.delete(selected_index)

        if item_ids[selected_index] in scrap:
            scrap_idx = sum(1 for item in item_ids[:selected_index] if item in scrap)
            item_values.pop(scrap_idx)

        if item_ids[selected_index] in save_items:
            idx = sum(1 for item in item_ids[:selected_index] if item in save_items)
            save_data.pop(idx)

        selected_item_text.set(f'none:\nx: n/a\ny: n/a\nz: n/a\n')            

        item_ids.pop(selected_index)
        item_pos.pop(selected_index)
        item_info.pop(selected_index)

        if items_listbox.size() > 0:
            next_idx = min(selected_index, items_listbox.size()-1)
            items_listbox.select_set(next_idx)
            items_listbox.event_generate('<<ListboxSelect>>')
        else:
            items_listbox.selection_clear(0, tk.END)

# Used to select a item in the listbox
def on_select(event):
    selected_index = items_listbox.curselection()
    if selected_index:
        selected_index = selected_index[0]
        item_name, scrap_value = item_info[selected_index]
        x,y,z = item_pos[selected_index]['x'], item_pos[selected_index]['y'], item_pos[selected_index]['z']
        value = ''

        if item_ids[selected_index] in scrap:
            value = str(scrap_value)

        scrap_price_entry.delete(0, tk.END)
        scrap_price_entry.insert(0, value)
        selected_item_text.set(f'{item_name}:\nx: {x:^}\ny: {y:^}\nz: {z:^}\n')

# Helper function that is called when the submit button is pressed in GUI
def submit(data):
    data['shipScrapValues']['value'] = item_values
    data['shipGrabbableItemIDs']['value'] = item_ids
    data['shipGrabbableItemPos']['value'] = item_pos
    data['shipItemSaveData']['value'] = save_data

    # Get values from GUI Entry fields
    starting_cash = credits_entry.get()
    if starting_cash == '': starting_cash = '60'
    deadline = deadline_entry.get()
    if deadline == '': deadline = '3240'
    steps = steps_entry.get()
    if steps == '': steps = '0'
    days = days_entry.get()
    if days == '': days = '0'
    quota = quota_entry.get()
    if quota == '': quota = '160'
    quota_passed = quota_passed_entry.get()
    if quota_passed == '': quota_passed = '0'
    quota_fulfilled = quota_fulfilled_entry.get()
    if quota_fulfilled == '': quota_fulfilled = '0'
    seed = seed_var.get()
    planet_id = planet_var.get()
    tele = tele_var.get()
    inv = inv_var.get()

    data['GroupCredits']['value'] = int(starting_cash)
    data['DeadlineTime']['value'] = int(deadline)
    data['Stats_StepsTaken']['value'] = int(steps)
    data['Stats_DaysSpent']['value'] = int(days)
    data['ProfitQuota']['value'] = int(quota)
    data['CurrentPlanetID']['value'] = int(planet_id)

    if seed:
        data['RandomSeed']['value'] = random.randint(0, 2147483647)

    if 'UnlockedShipObjects' not in data:
        data['UnlockedShipObjects'] = {'__type':'System.Int32[],mscorlib', 'value' : []}

    if tele and 5 not in data['UnlockedShipObjects']['value']:
        data['UnlockedShipObjects']['value'].append(5)
        data['ShipUnlockStored_Teleporter'] = {'__type':'bool', 'value': True}
    elif not tele and 5 in data['UnlockedShipObjects']['value']:
        data['UnlockedShipObjects']['value'].remove(5)
        data['ShipUnlockStored_Teleporter'] = {'__type':'bool', 'value': False}

    if inv and 19 not in data['UnlockedShipObjects']['value']:
        data['UnlockedShipObjects']['value'].append(19)
        data['ShipUnlockStored_Inverse Teleporter'] = {'__type':'bool', 'value': True}
    elif not inv and 19 in data['UnlockedShipObjects']['value']:
        data['UnlockedShipObjects']['value'].remove(19)
        data['ShipUnlockStored_Inverse Teleporter'] = {'__type':'bool', 'value': False}

    decrypted_result = json.dumps(data)

    # Write edited decrypted file to current directory
    with open('./prev_decrypted_file', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_result.encode('utf-8'))
    
    # Encrypt and overwrite LV save file
    encrypted_result = encrypt(password, './prev_decrypted_file')

    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_result)
    
    root.destroy()
    sys.exit()

if __name__ == '__main__':

    data = {}
    file_path = ''
    
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = filedialog.askopenfilename(title="Select a file")
        if not file_path:
            sys.exit(1)

    # Password 
    password = "lcslime14a5"
            
    # Initially grab data from file to populate initial Entry fields within GUI; if exception thrown quit
    try:
        data = json.loads(decrypt(password, file_path))
        if 'GroupCredits' not in data or 'DeadlineTime' not in data \
                or 'Stats_StepsTaken' not in data or 'Stats_DaysSpent' not in data \
                or 'ProfitQuota' not in data or 'CurrentPlanetID' not in data:
            raise Exception('File is not a valid Lethal Company save file!') 
    except Exception as e:
        print(f'Exception when loading file: {e}', file=sys.stderr)
        sys.exit(1)
        
    init_credits = data['GroupCredits']['value']
    init_deadline = data['DeadlineTime']['value']
    init_steps = data['Stats_StepsTaken']['value']
    init_days = data['Stats_DaysSpent']['value']
    init_quota = data['ProfitQuota']['value']
    init_quota_passed = data['QuotasPassed']['value']
    init_quota_fulfilled = data['QuotaFulfilled']['value']
    init_planetid = data['CurrentPlanetID']['value']
    init_tele = False
    init_inv = False
    if 'UnlockedShipObjects' in data and 5 in data['UnlockedShipObjects']['value']:
        init_tele = True 
    if 'UnlockedShipObjects' in data and 19 in data['UnlockedShipObjects']['value']:
        init_inv = True

    item_values = []
    item_ids = []
    item_pos = []
    save_data = []

    # Data related to items; this data may not be present in file
    items_v40 = {
            0:'binoculars',
            1:'boom box',
            3:'flashlight',
            4:'jetpack',
            5:'key',
            6:'lockpick',
            7:'apparatus',
            8:'handheld monitor',
            9:'pro flashlight',
            10:'shovel',
            11:'flashbang',
            12:'extension ladder',
            13:'tzp inhalant',
            14:'walkie talkie',
            15:'stun gun',
            16:'magic 7 ball',
            17:'airhorn',
            18:'bell',
            19:'big bolt',
            20:'bottles',
            21:'hairbrush',
            22:'candy',
            23:'cash register',
            24:'chemical jug',
            25:'clown horn',
            26:'large axel',
            27:'teeth',
            28:'dustpan',
            29:'egg beater',
            30:'v type engine',
            31:'golden cup',
            32:'lamp',
            33:'painting',
            34:'plastic fish',
            35:'laser pointer',
            36:'gold bar',
            37:'hairdryer',
            38:'magnifying glass',
            39:'tattered metal sheet',
            40:'cookie mold pan',
            41:'coffee mug',
            42:'perfume bottle',
            43:'old phone',
            44:'jar of pickles',
            45:'pill bottle',
            47:'ring',
            48:'robot toy',
            49:'rubber ducky',
            50:'red soda',
            51:'steering wheel',
            52:'stop sign',
            53:'tea kettle',
            54:'toothpaste',
            55:'toy cube',
            56:'bee hive',
            57:'radar booster',
            58:'yield sign',
    }

    items_v45 = {
        59:'shotgun',
        60:'shotgun shell',
        61:'spray paint',
        62:'homemade flashbang',
        63:'gift box',
        64:'flask',
        65:'tragedy',
        66:'comedy',
        67:'whoopie cushion',
    }
    
    # Use the intersection for whatever versions you want
    items = items_v40 | items_v45

    items_rev_mapping = {v:k for k,v in items.items()}

    not_in_game = {
        0:'binoculars',
        8:'handheld monitor',
    }

    scrap_v40 = {
            7:'apparatus',
            16:'magic 7 ball',
            17:'airhorn',
            18:'bell',
            19:'big bolt',
            20:'bottles',
            21:'hairbrush',
            22:'candy',
            23:'cash register',
            24:'chemical jug',
            25:'clown horn',
            26:'large axel',
            27:'teeth',
            28:'dustpan',
            29:'egg beater',
            30:'v type engine',
            31:'golden cup',
            32:'lamp',
            33:'painting',
            34:'plastic fish',
            35:'laser pointer',
            36:'gold bar',
            37:'hairdryer',
            38:'magnifying glass',
            39:'tattered metal sheet',
            40:'cookie mold pan',
            41:'coffee mug',
            42:'perfume bottle',
            43:'old phone',
            44:'jar of pickles',
            45:'pill bottle',
            47:'ring',
            48:'robot',
            49:'rubber ducky',
            50:'red soda',
            51:'steering wheel',
            52:'stop sign',
            53:'tea kettle',
            54:'toothpaste',
            55:'toy cube',
            56:'bee hive',
            58:'yield sign',
    }

    scrap_v45 = {
        59:'shotgun',
        #60:'shotgun shell',
        62:'homemade flashbang',
        63:'gift box',        
        64:'flask',
        65:'tragedy',
        66:'comedy',
        67:'whoopie cushion',
    }

    scrap = scrap_v40 | scrap_v45

    save_itemsv45 = {
        59:'shotgun',
        60:'shotgun shell',
    }

    save_items = save_itemsv45


    if 'shipScrapValues' in data:
        item_values = data['shipScrapValues']['value']
    else:
        data['shipScrapValues'] = {'__type':'System.Int32[],mscorlib', 'value':[]}

    if 'shipGrabbableItemIDs' in data:
        item_ids = data['shipGrabbableItemIDs']['value']
    else:
        data['shipGrabbableItemIDs'] = {'__type':'System.Int32[],mscorlib', 'value':[]}

    if 'shipGrabbableItemPos' in data:
        item_pos = data['shipGrabbableItemPos']['value']
    else:
        data['shipGrabbableItemPos'] = {'__type':'UnityEngine.Vector3[],UnityEngine.CoreModule', 'value':[]}

    if 'shipItemSaveData' in data:
        save_data = data['shipItemSaveData']['value']
    else:
        data['shipItemSaveData'] = {'__type':'System.Int32[],mscorlib', 'value':[]}

    
    # Setting up GUI elements
    root = tk.Tk()
    root.geometry('600x700')
    root.title('LC Simple Save Editor')
    
    frm = tk.Frame(root)
    frm.columnconfigure(0, weight=1)
    frm.columnconfigure(1, weight=1)
    frm.columnconfigure(2, weight=1)

    vcmd = (frm.register(validate_numeric), '%P')
    
    credits_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    credits_entry.insert(0, init_credits)
    credits_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=10)
    credits_text = tk.Label(frm, text='Group Credits: ')
    credits_text.grid(row=0, column=0, sticky=tk.W+tk.E, pady=10)

    deadline_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    deadline_entry.insert(0, init_deadline)
    deadline_entry.grid(row=1, column=1, sticky=tk.W+tk.E, pady=10)
    deadline_text = tk.Label(frm, text='Quota Deadline (One day is 1080): ')
    deadline_text.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)

    steps_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    steps_entry.insert(0, init_steps)
    steps_entry.grid(row=2, column=1, sticky=tk.W+tk.E,pady=10)
    steps_text = tk.Label(frm, text='Steps Taken: ')
    steps_text.grid(row=2,column=0, sticky=tk.W+tk.E,pady=10)

    days_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    days_entry.insert(0, init_days)
    days_entry.grid(row=3, column=1, sticky=tk.W+tk.E, pady=10)
    days_text = tk.Label(frm, text='Days Survived: ')
    days_text.grid(row=3, column=0, sticky=tk.W+tk.E, pady=10)

    quota_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    quota_entry.insert(0, init_quota)
    quota_entry.grid(row=4, column=1, sticky=tk.W+tk.E, pady=10)
    quota_text = tk.Label(frm, text='Current Quota: ')
    quota_text.grid(row=4, column=0, sticky=tk.W+tk.E, pady=10)

    quota_fulfilled_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    quota_fulfilled_entry.insert(0, init_quota_fulfilled)
    quota_fulfilled_entry.grid(row=5, column=1, sticky=tk.W+tk.E, pady=10)
    quota_fulfilled_text = tk.Label(frm, text='Quota Amount Fulfilled: ')
    quota_fulfilled_text.grid(row=5, column=0, sticky=tk.W+tk.E, pady=10)

    quota_passed_entry = tk.Entry(frm, validate='key', validatecommand=vcmd)
    quota_passed_entry.insert(0, init_quota_passed)
    quota_passed_entry.grid(row=6, column=1, sticky=tk.W+tk.E, pady=10)
    quota_passed_text = tk.Label(frm, text='Quotas Completed: ')
    quota_passed_text.grid(row=6, column=0, sticky=tk.W+tk.E, pady=10)
    
    planets = {0:'Experimentation', 1:'Assurance', 2:'Vow', 3:'Company Building',4:'March',5:'Rend',6:'Dine',7:'Offense',8:'Titan'}

    planet_var = tk.IntVar()
    planet_var.set(int(init_planetid))
    planet_str = tk.StringVar()
    planet_str.set(planets[planet_var.get()])
    planet_text = tk.Label(frm, textvariable=planet_str)
    planet_text.grid(row=7, column=0, sticky=tk.W+tk.E)
    inc_button = tk.Button(frm, text='Change Moon', command=lambda: incrementMoon(planet_var, planets, planet_str))
    inc_button.grid(row=7, column=1, sticky=tk.W+tk.E)

    seed_var = tk.BooleanVar()
    seed_check = tk.Checkbutton(frm, text='Shuffle Seed', variable=seed_var)
    seed_check.grid(row=8, column=0, sticky=tk.W+tk.E, pady=10)

    tele_var = tk.BooleanVar(frm, init_tele)
    tele_check = tk.Checkbutton(frm, text='Unlock Teleporter', variable=tele_var)
    tele_check.grid(row=9, column=0, sticky=tk.W+tk.E, pady=10)

    inv_var = tk.BooleanVar(frm, init_inv)
    inv_check = tk.Checkbutton(frm, text='Unlock Inverse Teleporter', variable=inv_var)
    inv_check.grid(row=10, column=0, sticky=tk.W+tk.E, pady=10)

    scrollbar = tk.Scrollbar(frm, orient=tk.VERTICAL)
    items_listbox = tk.Listbox(frm, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    items_listbox.grid(row=0, rowspan=8, column=2, sticky=tk.N+tk.S, padx = 10, pady=10)
    
    item_info = []
    ini_scrap_idx = 0
    for _id in item_ids:
        if _id in scrap:
            item_info.append((items[_id], item_values[ini_scrap_idx]))
            ini_scrap_idx += 1
        elif _id in items:
            item_info.append((items[_id], None))
        else: 
            print(f'There is an unknown item of id {_id}', file=sys.stderr)
            item_info.append((f'Unknown Item id {_id}', None))

        if _id in save_items:
            if items[_id] == 'shotgun':
                save_data.append(1)
            if items[_id] == 'shotgun shell':
                save_data.append(0)

    [items_listbox.insert(tk.END, items[_id]) if _id in items
            else items_listbox.insert(tk.END, f'unknown id {_id}') for _id in item_ids]

    selected_item_text = tk.StringVar(frm, f'none:\nx: n/a\ny: n/a\nz: n/a\n')
    selected_item_label = tk.Label(frm, textvariable=selected_item_text)
    selected_item_label.grid(row=9, column=2, pady=10,padx=10)

    items_listbox.bind('<<ListboxSelect>>', on_select)

    scrap_price_var = tk.StringVar()
    scrap_price_var.trace_add('write', on_entry_change)
    scrap_price_entry = tk.Entry(frm, textvariable=scrap_price_var, validate='key', validatecommand=vcmd)
    scrap_price_entry.insert(0, 0)
    scrap_price_entry.grid(row=10, column=2, sticky=tk.W+tk.E, pady=10)
    scrap_price_text = tk.Label(frm, text='Scrap Price: ')
    scrap_price_text.grid(row=10, column=1, sticky=tk.W+tk.E, pady=10)
    
    selected_dropdown_value = tk.StringVar(frm, '')
    item_dropdown = tk.OptionMenu(frm, selected_dropdown_value, *sorted(items.values()))
    item_dropdown.grid(row=11, column=2, sticky=tk.W+tk.E, padx=10, pady=10)

    item_add_button = tk.Button(frm, text='Add Item', command=on_add_item)
    item_add_button.grid(row=12,column=2, sticky=tk.W+tk.E, pady=10, padx=10)

    item_remove_button = tk.Button(frm, text='Remove Item', command=on_remove_item)
    item_remove_button.grid(row=13,column=2, sticky=tk.W+tk.E, pady=10, padx=10)

    submit_btn = tk.Button(frm, text='Overwite Save', font=('Arial', 18), command=lambda: submit(data))
    submit_btn.grid(row=11, column=0, sticky=tk.W+tk.E, pady=10)
    
    frm.pack()

    root.mainloop()
