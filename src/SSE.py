from encryption.encryptTools import encrypt, decrypt
import tkinter as tk
import random
import sys
import json

# Helper function used with button
def incrementMoon(planet_var, planets, planet_str):
    value = planet_var.get()    
    planet_var.set((value + 1) % len(planets))
    planet_str.set(planets[planet_var.get()])

# Helper function that is called when the submit button is pressed in GUI
def submit():
    # Get values from GUI Entry fields
    starting_cash = credits_entry.get()
    deadline = deadline_entry.get()
    steps = steps_entry.get()
    days = days_entry.get()
    quota = quota_entry.get()
    seed = seed_var.get()
    planet_id = planet_var.get()
    tele = tele_var.get()
    inv = inv_var.get()

    # Load decrypted data into dict and overwrite with new values
    decrypted_result = decrypt(password, sys.argv[1])
    data = json.loads(decrypted_result)

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

    if inv and 19 not in data['UnlockedShipObjects']['value']:
        data['UnlockedShipObjects']['value'].append(19)
        data['ShipUnlockStored_Inverse Teleporter'] = {'__type':'bool', 'value': True}

    decrypted_result = json.dumps(data)

    # Write edited decrypted file to current directory
    with open('./prev_decrypted_file', 'wb') as decrypted_file:
        decrypted_file.write(decrypted_result.encode('utf-8'))
    
    # Encrypt and overwrite LV save file
    encrypted_result = encrypt(password, './prev_decrypted_file')

    with open(sys.argv[1], 'wb') as encrypted_file:
        encrypted_file.write(encrypted_result)
    
    root.destroy()
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <filepath>",file=sys.stderr)
        sys.exit(1)

    def validate_numeric(value):
        return value.isnumeric()

    # Password 
    password = "lcslime14a5"

    # Initially grab data from file to populate initial Entry fields within GUI; if exception thrown quit
    data = {} 
    try:
        data = json.loads(decrypt(password, sys.argv[1]))
        if 'GroupCredits' not in data or 'DeadlineTime' not in data or 'Stats_StepsTaken' not in data or 'Stats_DaysSpent' not in data or 'ProfitQuota' not in data or 'CurrentPlanetID' not in data:
           raise Exception('File is not a valid Lethal Company save file!') 
    except Exception as e:
        print(f'{e}')
        sys.exit(1)
    
    init_credits = data['GroupCredits']['value']
    init_deadline = data['DeadlineTime']['value']
    init_steps = data['Stats_StepsTaken']['value']
    init_days = data['Stats_DaysSpent']['value']
    init_quota = data['ProfitQuota']['value']
    init_planetid = data['CurrentPlanetID']['value']

    planets = {0:'Experimentation', 1:'Assurance', 2:'Vow', 3:'Company Building',4:'March',5:'Rend',6:'Dine',7:'Offense',8:'Titan'}
    
    # Setting up GUI elements
    root = tk.Tk()
    root.geometry('500x500')
    root.title('LC Simple Save Editor')
    
    frm = tk.Frame(root)
    frm.columnconfigure(0, weight=1)
    frm.columnconfigure(1, weight=1)

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
    
    planet_var = tk.IntVar()
    planet_var.set(int(init_planetid))
    planet_str = tk.StringVar()
    planet_str.set(planets[planet_var.get()])
    planet_text = tk.Label(frm, textvariable=planet_str)
    planet_text.grid(row=5, column=0, sticky=tk.W+tk.E)
    inc_button = tk.Button(frm, text='Change Moon', command=lambda: incrementMoon(planet_var, planets, planet_str))
    inc_button.grid(row=5, column=1, sticky=tk.W+tk.E)

    seed_var = tk.BooleanVar()
    seed_check = tk.Checkbutton(frm, text='Shuffle Seed?', variable=seed_var)
    seed_check.grid(row=6, column=0, sticky=tk.W+tk.E, pady=10)

    tele_var = tk.BooleanVar()
    tele_check = tk.Checkbutton(frm, text='Unlock Teleporter if not purchased?', variable=tele_var)
    tele_check.grid(row=7, column=0, sticky=tk.W+tk.E, pady=10)

    inv_var = tk.BooleanVar()
    inv_check = tk.Checkbutton(frm, text='Unlock Inverse Teleporter if not purchased?', variable=inv_var)
    inv_check.grid(row=8, column=0, sticky=tk.W+tk.E, pady=10)

    submit_btn = tk.Button(frm, text='Submit', font=('Arial', 18), command=submit)
    submit_btn.grid(row=9, column=0, sticky=tk.W+tk.E, pady=10)
    
    frm.pack()

    root.mainloop()
