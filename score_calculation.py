import json
from datetime import datetime


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_quiz(user_response, answer_key):
    correct_marks = 4.0
    negative_marks = -1.0

    response_map = user_response["response_map"]

    correct_answers = 0
    incorrect_answers = 0

    for question in answer_key["quiz"]["questions"]:
        qid = question["id"]
        correct_option = next((opt["id"] for opt in question["options"] if opt["is_correct"]), None)

        if qid in response_map:
            if response_map[qid] == correct_option:
                correct_answers += 1
            else:
                incorrect_answers += 1

    score = (correct_answers * correct_marks) + (incorrect_answers * negative_marks)
    accuracy = round((correct_answers / (correct_answers + incorrect_answers)) * 100,
                     2) if correct_answers + incorrect_answers > 0 else 0

    return {
        "id": user_response["id"],
        "quiz_id": user_response["quiz_id"],
        "user_id": user_response["user_id"],
        "submitted_at": datetime.now().isoformat(),
        "score": int(score),
        "trophy_level": 2,
        "accuracy": f"{accuracy} %",
        "speed": "100",
        "final_score": str(score),
        "negative_score": str(incorrect_answers * negative_marks),
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "source": "live",
        "type": "topic",
        "response_map": response_map,
        "total_questions": len(response_map),
        "rank_text": "Topic Rank - #N/A",
        "mistakes_corrected": 0,
        "initial_mistake_count": incorrect_answers,
        "next_steps": [{"pageType": "resultPage"}]
    }



llqt_data = load_json("LLQT.json")  #load the data

user_response_data = load_json("XgAgFJ.json")[4]  #take one entry from 14 entries as an example


result_data = evaluate_quiz(user_response_data, llqt_data)  #quiz paper anlaysis


output_path = "generated_result.json" #saving the result for comparision with with the previous data
with open(output_path, "w", encoding="utf-8") as outfile:
    json.dump(result_data, outfile, indent=4)
