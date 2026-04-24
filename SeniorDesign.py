import tkinter as tk
from tkinter import filedialog, messagebox
import os
import pandas as pd

# Template files
TEMPLATE_FILES = {
    "Script 1": "protocol_template.py", #All of 1
    "Script 2": "protocol_template_2.py", #Front half
    "Script 3": "protocol_template_3.py" #Back half
}

# Output files for each script
OUTPUT_FILES = {
    "Script 1": "FillBot_Output_File_1.py",
    "Script 2": "FillBot_Output_File_2.py",
    "Script 3": "FillBot_Output_File_3.py"
}

#Default to opentrons if user does not input anything
LABWARE_DEFAULTS = {

    "source_plate": "opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap",

}


# Store selected scripts
selected_scripts = set()



#Input a CSV file
def select_csv():
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        file_label.config(text=os.path.basename(file_path))
        root.selected_file = file_path

#Read the CV file and setup the variables
def read_csv():
    if not hasattr(root, "selected_file"):
        print("No file selected!")
        return

    try:
        df = pd.read_csv(root.selected_file, header=None)
        
        # Parse columns by position: A=well, B=sample_id, C=location in 384,
        # D=vol of 384, E=location protein, F=vol protein, G=vol aqueous,
        # H=vol to move into tube
        wells = []
        sample_ids = []
        location_384 = []
        vol_384 = []
        location_protein = []
        vol_protein = []
        vol_aqueous = []
        vol_to_tube = []
        combined_data = []
        
        #Parse the vairables based on columns
        # Skip first row (header)
        for index, row in df.iterrows():
            if index == 0:
                continue
                
            if pd.notna(row.iloc[0]):
                well = str(row.iloc[0]).strip()
                sample_id = str(row.iloc[1]).strip() if len(row) > 1 and pd.notna(row.iloc[1]) else ''
                loc_384 = str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else ''
                v_384 = str(row.iloc[3]).strip() if len(row) > 3 and pd.notna(row.iloc[3]) else ''
                loc_prot = str(row.iloc[4]).strip() if len(row) > 4 and pd.notna(row.iloc[4]) else ''
                v_prot = str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else ''
                v_aq = str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ''
                v_to_tube = str(row.iloc[7]).strip() if len(row) > 7 and pd.notna(row.iloc[7]) else ''
                
                # Skip rows where only one column has data and all others are empty
                if not sample_id and not loc_384 and not v_384 and not loc_prot and not v_prot and not v_aq and not v_to_tube:
                    continue
                
                #Assign the parsed variables to the orginial variable names and store in combined data
                wells.append(well)
                sample_ids.append(sample_id)
                location_384.append(loc_384)
                vol_384.append(v_384)
                location_protein.append(loc_prot)
                vol_protein.append(v_prot)
                vol_aqueous.append(v_aq)
                vol_to_tube.append(v_to_tube)
                combined_data.append({
                    'well': well,
                    'sample_id': sample_id,
                    'location_384': loc_384,
                    'vol_384': v_384,
                    'location_protein': loc_prot,
                    'vol_protein': v_prot,
                    'vol_aqueous': v_aq,
                    'vol_to_tube': v_to_tube
                })
        
        # Store all variables in root to make it accessible 
        root.wells = wells
        root.sample_ids = sample_ids
        root.location_384 = location_384
        root.vol_384 = vol_384
        root.location_protein = location_protein
        root.vol_protein = vol_protein
        root.vol_aqueous = vol_aqueous
        root.vol_to_tube = vol_to_tube
        root.combined_data = combined_data
        
        # Display plate visualization based on wells from spreadsheet
        rows = "ABCDEFGH"
        columns = range(1, 13)

        # clear plate display
        for widget in plate_frame.winfo_children():
            widget.destroy()

        # row labels
        for i, r in enumerate(rows):
            tk.Label(
                plate_frame, text=r,
                width=4, height=2, bg="lightgray"
            ).grid(row=i+1, column=0)

        # column labels
        for j, c in enumerate(columns):
            tk.Label(
                plate_frame, text=c,
                width=6, height=2, bg="lightgray"
            ).grid(row=0, column=j+1)

        # plate cells - mark wells from spreadsheet as filled
        for i, r in enumerate(rows):
            for j, c in enumerate(columns):
                well_id = f"{r}{c}"
                
                if well_id in wells:
                    # Find the index of this well
                    idx = wells.index(well_id)
                    text = sample_ids[idx]
                    color = "lightgreen"
                else:
                    text = ""
                    color = "white"

                tk.Label(
                    plate_frame,
                    text=text,
                    bg=color,
                    width=6,
                    height=3,
                    relief="ridge"
                ).grid(row=i+1, column=j+1)
        #Input variables in the control panel
        print("Wells:", wells)
        print("Sample IDs:", sample_ids)
        print("Location 384:", location_384)
        print("Vol 384:", vol_384)
        print("Location Protein:", location_protein)
        print("Vol Protein:", vol_protein)
        print("Vol Aqueous:", vol_aqueous)
        print("Vol To Tube:", vol_to_tube)
        print("Combined Data:", combined_data)

        next_button.pack(pady=10)

    except Exception as e:
        print("CSV error:", e)

#Allow the user to input labware 
def get_labware_config():
    """Return labware config, with one user-controlled field for protein solution labware."""
    return {
        "source_plate": protein_solution_labware_entry.get().strip() or LABWARE_DEFAULTS["source_plate"],
    }

#Command to create the protocol
def generate_protocol():
    if not hasattr(root, "combined_data"):
        print("No data available!")
        return

    if not selected_scripts:
        messagebox.showwarning("No Selection", "Please select at least one script!")
        return

    try:
        combined_data = root.combined_data
        wells = root.wells
        sample_ids = root.sample_ids
        location_384 = root.location_384
        vol_384 = root.vol_384
        location_protein = root.location_protein
        vol_protein = root.vol_protein
        vol_aqueous = root.vol_aqueous
        vol_to_tube = root.vol_to_tube
        labware_config = get_labware_config()

        # Generate protocol for each selected script
        for script_name in selected_scripts:
            template_file = TEMPLATE_FILES[script_name]
            output_file = OUTPUT_FILES[script_name]
            
            # Check if template file exists
            if not os.path.exists(template_file):
                messagebox.showerror("Error", f"Template file not found: {template_file}")
                print(f"Template file not found: {template_file}")
                continue

            with open(template_file, "r", encoding="utf-8") as f:
                template = f.read()

            new_protocol = (
                template
                .replace("{{COMBINED_DATA}}", str(combined_data))
                .replace("{{WELLS}}", str(wells))
                .replace("{{SAMPLE_IDS}}", str(sample_ids))
                .replace("{{LOCATION_384}}", str(location_384))
                .replace("{{VOL_384}}", str(vol_384))
                .replace("{{LOCATION_PROTEIN}}", str(location_protein))
                .replace("{{VOL_PROTEIN}}", str(vol_protein))
                .replace("{{VOL_AQUEOUS}}", str(vol_aqueous))
                .replace("{{VOL_TO_TUBE}}", str(vol_to_tube))
                .replace("{{LABWARE_PROTEIN_SOLUTION}}", labware_config["source_plate"]))
               

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(new_protocol)

            print(f"Protocol generated for {script_name}!")
            print(f"Saved as: {output_file}")

        messagebox.showinfo("Success", f"Protocols generated for {len(selected_scripts)} script(s)!")

    except Exception as e:
        messagebox.showerror("Error", f"Generation error: {e}")
        print("Generation error:", e)


def toggle_script_1():
    """Generate for Script 1 only"""
    selected_scripts.clear()
    selected_scripts.add("Script 1")
    button_script_1.config(relief="sunken", bg="lightgreen")
    button_scripts_23.config(relief="raised", bg="SystemButtonFace")
    generate_protocol()


def toggle_scripts_2_3():
    """Generate for Scripts 2 and 3"""
    selected_scripts.clear()
    selected_scripts.add("Script 2")
    selected_scripts.add("Script 3")
    button_script_1.config(relief="raised", bg="SystemButtonFace")
    button_scripts_23.config(relief="sunken", bg="lightblue")
    generate_protocol()



#UI Functions
root = tk.Tk()
root.title("FillBot")
root.geometry("950x600")

# Scrollable canvas setup
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

scrollable_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def _on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def _on_canvas_configure(event):
    canvas.itemconfig(canvas_window, width=event.width)

def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

scrollable_frame.bind("<Configure>", _on_frame_configure)
canvas.bind("<Configure>", _on_canvas_configure)
canvas.bind_all("<MouseWheel>", _on_mousewheel)

file_label = tk.Label(scrollable_frame, text="No file selected")
file_label.pack(pady=5)

tk.Button(scrollable_frame, text="Select CSV", command=select_csv).pack()
tk.Button(scrollable_frame, text="Read CSV", command=read_csv).pack()

plate_frame = tk.Frame(scrollable_frame)
plate_frame.pack(pady=10)

# Labware selection input
labware_frame = tk.LabelFrame(scrollable_frame, text="Protein Solution Labware (Input labware API if different from default)", padx=10, pady=8)
labware_frame.pack(pady=8)


protein_solution_labware_entry = tk.Entry(labware_frame, width=45)
protein_solution_labware_entry.grid(row=0, column=1, padx=5, pady=3)
protein_solution_labware_entry.insert(0, LABWARE_DEFAULTS["source_plate"])

# Script selection buttons
tk.Label(scrollable_frame, text="Select Script(s) to Generate:", font=("Arial", 10, "bold")).pack(pady=10)

button_frame = tk.Frame(scrollable_frame)
button_frame.pack()

button_script_1 = tk.Button(
    button_frame,
    text="Generate One Script",
    command=toggle_script_1,
    width=25,
    bg="SystemButtonFace"
)
button_script_1.pack(side="left", padx=10)

button_scripts_23 = tk.Button(
    button_frame,
    text="Generate Scripts in Two Parts",
    command=toggle_scripts_2_3,
    width=25,
    bg="SystemButtonFace"
)
button_scripts_23.pack(side="left", padx=10)

next_button = tk.Button(
    scrollable_frame,
    text="Close",
    command=root.quit
)
next_button.pack(pady=10)

root.mainloop()
