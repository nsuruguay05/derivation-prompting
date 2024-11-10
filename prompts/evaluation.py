evaluation_prompt = '''###Task Description:
An instruction (might include an Input inside it), a response to evaluate, a reference answer that gets a score of 5, and a score rubric representing a evaluation criteria are given.
1. Write a detailed feedback that assess the quality of the response strictly based on the given score rubric, not evaluating in general.
2. After writing a feedback, write a score that is an integer between 1 and 5. You should refer to the score rubric.
3. The output format should look as follows: "Feedback: (write a feedback for criteria) [RESULT] (an integer number between 1 and 5)"
4. Please do not generate any other opening, closing, and explanations.

###The instruction to evaluate:
Responder la siguiente pregunta en español: {question}

###Response to evaluate:
{prediction}

###Reference Answer (Score 5):
{reference}

###Score Rubrics:
[Is the model response correct and truthful?]
Score 1: The response to evaluate contradicts the reference answer in a way that the information is untruthful in comparison to the reference answer.
Score 2: The response to evaluate has conflicts with the reference answer in a way that the information is partially untruthful  in comparison to the reference answer.
Score 3: The response to evaluate has nothing to do with the reference answer, but it does not have conflicts with it. It may or may not be untruthful, but it does not contradict the reference answer.
Score 4: The response to evaluate partially matches semantically to the reference answer in a way that the information is truthful but not complete.
Score 5: The response to evaluate matches completely with the reference answer in a way thaat is truthful and has all the information that is expressed in the reference answer.'''