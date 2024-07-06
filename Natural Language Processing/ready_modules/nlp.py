""" NLP Module for Interview Evaluation"""
# pylint: disable=line-too-long
import json
from ans_eval import AnswerEvaluator
from s_record import SoundRecorder


class NLP_MODULE:
    """
    This class is used to evaluate the interviewee's answers.
    """

    def __init__(self, path_to_interviewee_answer: str, model_answers_dict: dict):
        """
        This method is used to initialize the class.
        :param path_to_interviewee_answer: str
        :param model_answers_json: str
        """
        self.path_to_interviewee_answer = path_to_interviewee_answer
        self.model_answers_json = model_answers_dict
        self.interviewee_answer = {}
        self.results = {}


    def listen_to_answer(self):
        """
        This method is used to listen to the answer 
        :return: dict, dict
        """
        self.interviewee_answer = SoundRecorder.get_answers(
            self.path_to_interviewee_answer)
        return self.interviewee_answer

    def generate_results(self):
        """
        This method is used to generate results.
        :return: None
        """
        results = {}
        for _, answer in self.model_answers_json.items():
            model_answer = answer['model_answer']
            keywords = answer['hint_keywords']
            a_evaluator = AnswerEvaluator(model_answer, keywords)
            for q_no, ans in self.interviewee_answer.items():
                results[q_no] = a_evaluator.evaluate(ans, keywords)
        del self.model_answers_json
        del self.interviewee_answer
        self.results = results
        return self.results

    def export_results_to_json(self):
        """
        This method is used to export results to json file.
        :return: None
        """
        with open("results.json", "w") as file:
            json.dump(self.results, file, indent=4)
        del self.results


if __name__ == "__main__":
    # take arguments from command line
    questions = {"Q5": {
      "question": "What is regularization in machine learning, and why is it used?",
      "model_answer": "Javascript library designed by facebook thank you",
      "hint_keywords": ["Javascript", "library", "facebook", "thank"]
    }}

    print("Printing Question : ", questions['Q5']['question'])
    nlp_class_module = NLP_MODULE(
        "audio samples/interviewee_answer/test.wav", questions)
    print("Listening to the answer...")
    nlp_class_module.listen_to_answer()
    print("Comparing answer to model answer...")
    print("Model answer is : " , questions['Q5']['model_answer'])
    result = nlp_class_module.generate_results()
    print(result)
    nlp_class_module.export_results_to_json() #Optional