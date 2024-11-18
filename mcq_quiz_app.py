import streamlit as st
import random
import re

# Paste the content of the MCQs document here
mcqs_text = """
QUESTION 1
A 53-year-old woman is seen in the general surgical outpatient clinic. She attended her GP with a 1-month history of upper abdominal pain and was found to have a palpable, firm mass in the epigastrium. An upper gastrointestinal (GI) endoscopy is normal and the surgical team requests a contrast-enhanced CT of the abdomen. This demonstrates a multicystic mass in the pancreas. Which findings would make a mucinous cystic tumour more likely than a serous cystadenoma?
Central stellate calcification is present within the lesion.
The mass contains 12 separate cysts.
The smallest cystic component measures 28 mm in diameter.
The patient has a known diagnosis of von Hippel-Lindau disease.
The tumour is located in the head of the pancreas.
ANSWER: C
Mucinous cystic pancreatic tumours (cystadenomas and cystadenocarcinomas) typically contain a few large cysts, each measuring more than 20 mm in diameter.
Reference: Grainger & Allison’s 5e, pp 804-806.

QUESTION 2
A 54-year-old man with hepatitis B cirrhosis attends the hepatology outpatient clinic. The patient’s serum alpha fetoprotein level is found to be significantly elevated, having been normal 6 months ago. An abdominal ultrasound demonstrates a new 3-cm lesion in the right lobe of the liver, and a diagnosis of hepatocellular carcinoma (HCC) is suspected. Which one of the following statements is correct regarding HCC?
Brain metastases are hypovascular and calcified.
HCC derives its blood supply primarily from the hepatic artery.
Portal vein invasion is more suggestive of a liver metastasis than HCC.
Small HCC (< 1 cm) are typically heterogeneous and hyperechoic on US.
The bony skeleton is the most common site for distant metastases.
ANSWER: B
HCC derives its blood supply from the hepatic artery (hence the rapid arterial phase enhancement). A large HCC will usually demonstrate heterogeneous reflectivity due to areas of necrosis, but smaller lesions are typically of homogeneous low reflectivity on ultrasound. HCC often invades the branches of the portal vein and the most frequent site of metastases is the lungs. Metastases to the brain are typically hypervascular and do not usually contain calcification.
Reference: Yu SCH, Yeung DTK, So NMC. Imaging features of hepatocellular carcinoma Clin Radiol 2004;59:145-156.
"""

def parse_mcqs(mcqs_text):
    """Parses the MCQs from a plain text string."""
    questions = []
    current_question = {}
    lines = mcqs_text.strip().split("\n")
    pattern_question = re.compile(r"QUESTION \d+", re.IGNORECASE)
    pattern_answer = re.compile(r"ANSWER: (\w)", re.IGNORECASE)

    for i, line in enumerate(lines):
        line = line.strip()
        if pattern_question.match(line):
            if current_question:
                questions.append(current_question)
            current_question = {"question": "", "options": [], "answer": "", "explanation": "", "reference": ""}
        elif line.startswith("ANSWER:"):
            match = pattern_answer.match(line)
            if match:
                current_question["answer"] = match.group(1)
            # The explanation is assumed to be in the next line
            if i + 1 < len(lines):
                current_question["explanation"] = lines[i + 1].strip()
        elif line.startswith("Reference:"):
            current_question["reference"] = line.replace("Reference:", "").strip()
        elif current_question and not current_question["answer"]:
            if not current_question["question"]:
                current_question["question"] = line
            else:
                current_question["options"].append(line)

    if current_question:
        questions.append(current_question)
    
    return questions

def quiz_app(questions):
    """Runs the quiz app."""
    st.title("MCQ Quiz Game")
    st.markdown("Test your knowledge with the MCQs!")

    # Initialize session state
    if "current_question_index" not in st.session_state:
        st.session_state.current_question_index = 0
        st.session_state.score = 0
        st.session_state.questions_order = random.sample(range(len(questions)), len(questions))  # Random order
        st.session_state.completed = False

    if st.session_state.current_question_index < len(questions):
        question_index = st.session_state.questions_order[st.session_state.current_question_index]
        question = questions[question_index]

        # Display score
        st.sidebar.subheader(f"Current Score: {st.session_state.score}/{st.session_state.current_question_index}")
        
        st.subheader(f"Question {st.session_state.current_question_index + 1}")
        st.write(question["question"])
        
        selected_option = st.radio("Select your answer:", question["options"], key=st.session_state.current_question_index)
        
        if st.button("Submit Answer"):
            correct_option = question["options"][ord(question["answer"]) - ord("A")]
            if selected_option == correct_option:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(f"Incorrect. Correct answer: {correct_option}")
            
            # Show the explanation
            st.markdown(f"**Explanation:** {question.get('explanation', 'No explanation provided.')}")
            st.markdown(f"**Reference:** {question.get('reference', 'No reference provided.')}")
            
            # Enable "Next Question" button after submitting
            st.session_state.allow_next = True
        
        if st.session_state.get("allow_next", False):
            if st.button("Next Question"):
                st.session_state.current_question_index += 1
                st.session_state.allow_next = False

    if st.session_state.current_question_index == len(questions):
        st.session_state.completed = True

    if st.session_state.completed:
        st.balloons()
        st.subheader("Quiz Completed!")
        st.write(f"Your final score: {st.session_state.score} / {len(questions)}")
        st.button("Restart Quiz", on_click=reset_quiz)

def reset_quiz():
    """Resets the quiz."""
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.questions_order = random.sample(range(len(st.session_state.questions)), len(st.session_state.questions))
    st.session_state.completed = False
    st.session_state.allow_next = False

def main():
    # Parse the MCQs from the embedded text
    questions = parse_mcqs(mcqs_text)

    if questions:
        quiz_app(questions)
    else:
        st.error("No valid questions found in the embedded text.")

if __name__ == "__main__":
    main()
