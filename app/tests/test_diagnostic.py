# Tests for the diagnostic test functionality
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.diagnostic_schemas import DifficultLevel, QuestionType

client = TestClient(app)


def test_generate_diagnostic_test():
    """Test generating a diagnostic test for basic level"""
    response = client.post("/api/v1/diagnostic-test/generate", json={
        "student_id": "test_student_001",
        "grade_level": 3,
        "test_level": "básico",
        "preferences": ["animales", "cuentos"]
    })
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "student_id" in data
    assert "test_id" in data
    assert "questions" in data
    assert "instructions" in data
    assert "time_limit" in data
    
    # Verify student data
    assert data["student_id"] == "test_student_001"
    
    # Verify questions
    questions = data["questions"]
    assert len(questions) > 0
    assert isinstance(questions, list)
    
    # Verify first question structure
    first_question = questions[0]
    assert "question_id" in first_question
    assert "question_text" in first_question
    assert "question_type" in first_question
    assert "correct_answer" in first_question
    assert "skill_area" in first_question
    assert "difficulty_level" in first_question
    
    # Verify instructions are provided
    assert len(data["instructions"]) > 0
    assert "tiempo" in data["instructions"].lower() or "instrucciones" in data["instructions"].lower()
    
    # Verify time limit is reasonable
    assert data["time_limit"] > 0


def test_evaluate_diagnostic_test():
    """Test evaluating a diagnostic test submission"""
    # First generate a test to get questions
    generate_response = client.post("/api/v1/diagnostic-test/generate", json={
        "student_id": "test_student_002",
        "grade_level": 2,
        "test_level": "básico"
    })
    
    assert generate_response.status_code == 200
    test_data = generate_response.json()
    test_id = test_data["test_id"]
    questions = test_data["questions"]
    
    # Create sample answers (mix of correct and incorrect)
    answers = []
    for i, question in enumerate(questions[:4]):  # Answer first 4 questions
        if i < 2:
            # First 2 answers correct
            answers.append({
                "question_id": question["question_id"],
                "answer": question["correct_answer"],
                "time_spent": 30
            })
        else:
            # Next 2 answers incorrect (use first option if available)
            wrong_answer = "Wrong answer"
            if question.get("options"):
                # Find an option that's not the correct answer
                for option in question["options"]:
                    if option != question["correct_answer"]:
                        wrong_answer = option
                        break
            
            answers.append({
                "question_id": question["question_id"],
                "answer": wrong_answer,
                "time_spent": 45
            })
    
    # Submit evaluation
    evaluation_response = client.post("/api/v1/diagnostic-test/evaluate", json={
        "student_id": "test_student_002",
        "test_id": test_id,
        "answers": answers
    })
    
    assert evaluation_response.status_code == 200
    eval_data = evaluation_response.json()
    
    # Verify evaluation response structure
    assert "student_id" in eval_data
    assert "test_id" in eval_data
    assert "overall_score" in eval_data
    assert "overall_level" in eval_data
    assert "skill_assessments" in eval_data
    assert "recommendations" in eval_data
    assert "next_steps" in eval_data
    assert "message" in eval_data
    
    # Verify evaluation data
    assert eval_data["student_id"] == "test_student_002"
    assert eval_data["test_id"] == test_id
    assert 0 <= eval_data["overall_score"] <= 1
    assert eval_data["overall_level"] in ["básico", "intermedio", "avanzado"]
    
    # Verify skill assessments
    skill_assessments = eval_data["skill_assessments"]
    assert isinstance(skill_assessments, list)
    
    if skill_assessments:
        first_skill = skill_assessments[0]
        assert "skill_area" in first_skill
        assert "score" in first_skill
        assert "level" in first_skill
        assert "strengths" in first_skill
        assert "weaknesses" in first_skill
        assert 0 <= first_skill["score"] <= 1
    
    # Verify recommendations and next steps
    assert isinstance(eval_data["recommendations"], list)
    assert isinstance(eval_data["next_steps"], list)
    assert len(eval_data["message"]) > 0


def test_get_basic_level_questions():
    """Test getting basic level questions"""
    response = client.get("/api/v1/diagnostic-test/questions/basic")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response structure
    assert "questions" in data
    assert "total" in data
    
    # Verify questions data
    questions = data["questions"]
    assert isinstance(questions, list)
    assert len(questions) > 0
    assert data["total"] == len(questions)
    
    # Verify each question has required fields
    for question in questions:
        assert "question_id" in question
        assert "question_text" in question
        assert "question_type" in question
        assert "correct_answer" in question
        assert "skill_area" in question
        assert "difficulty_level" in question
        assert question["difficulty_level"] == "básico"


def test_diagnostic_test_with_minimal_data():
    """Test diagnostic test generation with minimal required data"""
    response = client.post("/api/v1/diagnostic-test/generate", json={
        "student_id": "minimal_test",
        "grade_level": 1
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["student_id"] == "minimal_test"
    assert len(data["questions"]) > 0
    assert data["time_limit"] > 0


def test_evaluate_diagnostic_with_all_correct_answers():
    """Test evaluation with all correct answers"""
    # Generate test
    generate_response = client.post("/api/v1/diagnostic-test/generate", json={
        "student_id": "perfect_student",
        "grade_level": 3
    })
    
    test_data = generate_response.json()
    questions = test_data["questions"]
    
    # Create all correct answers
    answers = []
    for question in questions:
        answers.append({
            "question_id": question["question_id"],
            "answer": question["correct_answer"],
            "time_spent": 25
        })
    
    # Evaluate
    evaluation_response = client.post("/api/v1/diagnostic-test/evaluate", json={
        "student_id": "perfect_student",
        "test_id": test_data["test_id"],
        "answers": answers
    })
    
    assert evaluation_response.status_code == 200
    eval_data = evaluation_response.json()
    
    # Should have high score
    assert eval_data["overall_score"] >= 0.8
    assert "Excelente" in eval_data["message"] or eval_data["overall_score"] == 1.0


def test_evaluate_diagnostic_with_all_wrong_answers():
    """Test evaluation with all wrong answers"""
    # Generate test
    generate_response = client.post("/api/v1/diagnostic-test/generate", json={
        "student_id": "struggling_student",
        "grade_level": 2
    })
    
    test_data = generate_response.json()
    questions = test_data["questions"]
    
    # Create all wrong answers
    answers = []
    for question in questions:
        wrong_answer = "Definitely wrong answer"
        if question.get("options"):
            # Find first option that's not correct
            for option in question["options"]:
                if option != question["correct_answer"]:
                    wrong_answer = option
                    break
        
        answers.append({
            "question_id": question["question_id"],
            "answer": wrong_answer,
            "time_spent": 60
        })
    
    # Evaluate
    evaluation_response = client.post("/api/v1/diagnostic-test/evaluate", json={
        "student_id": "struggling_student",
        "test_id": test_data["test_id"],
        "answers": answers
    })
    
    assert evaluation_response.status_code == 200
    eval_data = evaluation_response.json()
    
    # Should have low score and basic level
    assert eval_data["overall_score"] < 0.6
    assert eval_data["overall_level"] == "básico"
    assert len(eval_data["recommendations"]) > 0