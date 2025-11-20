import streamlit as st

st.title("🎈 Demo Update Title")
st.write(
    "Hello. Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
from tkinter import *
from clipspy import Environment

# -------------------------------
# Initialize CLIPS Environment
# -------------------------------
env = Environment()

# Define facts and rules
env.build("""
(deftemplate symptom
    (slot fever)
    (slot cough))

(defrule covid-high-risk
    (symptom (fever yes) (cough yes))
    =>
    (assert (diagnosis "High possibility of COVID-19. Please get tested.")))

(defrule covid-low-risk
    (symptom (fever no))
    =>
    (assert (diagnosis "Low risk of COVID-19.")))
""")

# -------------------------------
# UI Functions
# -------------------------------
def diagnose():
    # Clear previous facts
    env.reset()

    fever_value = "yes" if fever_var.get() == 1 else "no"
    cough_value = "yes" if cough_var.get() == 1 else "no"

    # Assert user input into CLIPS
    env.assert_string(f'(symptom (fever {fever_value}) (cough {cough_value}))')

    # Run the rules
    env.run()

    # Retrieve diagnosis
    results = env.facts()
    diagnosis_text = "No diagnosis found."

    for fact in results:
        if fact.template.name == "diagnosis":
            diagnosis_text = fact.slot_value(0)

    result_label.config(text=diagnosis_text)


# -------------------------------
# Tkinter GUI
# -------------------------------
window = Tk()
window.title("COVID-19 Diagnosis Expert System")
window.geometry("380x260")

Label(window, text="COVID-19 Self-Diagnosis System", font=("Arial", 14, "bold")).pack(pady=10)

# Fever question
fever_var = IntVar()
Label(window, text="Do you have fever?").pack()
Radiobutton(window, text="Yes", variable=fever_var, value=1).pack()
Radiobutton(window, text="No", variable=fever_var, value=0).pack()

# Cough question
cough_var = IntVar()
Label(window, text="Do you have cough?").pack()
Radiobutton(window, text="Yes", variable=cough_var, value=1).pack()
Radiobutton(window, text="No", variable=cough_var, value=0).pack()

# Diagnose button
Button(window, text="Diagnose", command=diagnose, width=20, bg="lightblue").pack(pady=10)

# Result label
result_label = Label(window, text="", font=("Arial", 12), fg="blue")
result_label.pack()

window.mainloop()
