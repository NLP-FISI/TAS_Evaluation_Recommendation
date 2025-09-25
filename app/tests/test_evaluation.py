# Tests for the evaluation input service and automatic level assignment algorithm
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.evaluation_input_service import EvaluationInputService
from app.schemas.evaluation_schemas import EvaluationInputRequest, EvaluationInputResponse

client = TestClient(app)


class TestEvaluationInputService:
    """Test cases for the EvaluationInputService class."""
    
    def test_basic_level_assignment_grade_2(self):
        """Test that grade 2 students get basic level with complexity 1."""
        request = EvaluationInputRequest(
            student_id="student_001",
            grade_level=2,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.student_id == "student_001"
        assert response.initial_level == "básico"
        assert len(response.recommended_texts) > 0
        assert "2° grado" in response.message
    
    def test_basic_level_assignment_grade_3(self):
        """Test that grade 3 students get basic level with complexity 2."""
        request = EvaluationInputRequest(
            student_id="student_002",
            grade_level=3,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.student_id == "student_002"
        assert response.initial_level == "básico"
        assert len(response.recommended_texts) > 0
        assert "3° grado" in response.message
    
    def test_intermediate_level_assignment_grade_4(self):
        """Test that grade 4 students get intermediate level."""
        request = EvaluationInputRequest(
            student_id="student_003",
            grade_level=4,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.student_id == "student_003"
        assert response.initial_level == "intermedio"
        assert len(response.recommended_texts) > 0
        assert "4° grado" in response.message
    
    def test_intermediate_level_assignment_grade_5(self):
        """Test that grade 5 students get intermediate level with complexity 2."""
        request = EvaluationInputRequest(
            student_id="student_004",
            grade_level=5,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.student_id == "student_004"
        assert response.initial_level == "intermedio"
        assert len(response.recommended_texts) > 0
        assert "5° grado" in response.message
    
    def test_advanced_level_assignment_grade_6(self):
        """Test that grade 6 students get advanced level."""
        request = EvaluationInputRequest(
            student_id="student_005",
            grade_level=6,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.student_id == "student_005"
        assert response.initial_level == "avanzado"
        assert len(response.recommended_texts) > 0
        assert "6° grado" in response.message
    
    def test_preferences_animals_basic_level(self):
        """Test that animal preferences are reflected in text recommendations."""
        request = EvaluationInputRequest(
            student_id="student_006",
            grade_level=2,
            preferences=["animales"]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "básico"
        assert any("gato" in text.lower() or "animal" in text.lower() or "ratón" in text.lower() 
                  for text in response.recommended_texts)
        assert "animales" in response.message
    
    def test_preferences_adventures_intermediate_level(self):
        """Test that adventure preferences are reflected in text recommendations."""
        request = EvaluationInputRequest(
            student_id="student_007",
            grade_level=4,
            preferences=["aventuras"]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "intermedio"
        assert any("aventura" in text.lower() or "viaje" in text.lower() or "explorador" in text.lower()
                  for text in response.recommended_texts)
        assert "aventuras" in response.message
    
    def test_preferences_science_advanced_level(self):
        """Test that science preferences work with advanced level."""
        request = EvaluationInputRequest(
            student_id="student_008",
            grade_level=6,
            preferences=["ciencia"]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "avanzado"
        assert any("ciencia" in text.lower() or "tecnológico" in text.lower() or "científico" in text.lower()
                  for text in response.recommended_texts)
        assert "ciencia" in response.message
    
    def test_multiple_preferences(self):
        """Test handling of multiple preferences."""
        request = EvaluationInputRequest(
            student_id="student_009",
            grade_level=5,
            preferences=["animales", "aventuras", "ciencia"]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "intermedio"
        assert len(response.recommended_texts) <= 4  # Maximum 4 texts
        # Should mention at least some preferences in message
        message_lower = response.message.lower()
        assert any(pref in message_lower for pref in ["animales", "aventuras", "ciencia"])
    
    def test_invalid_grade_below_range(self):
        """Test handling of grade level below valid range."""
        request = EvaluationInputRequest(
            student_id="student_010",
            grade_level=1,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "básico"
        assert "fuera del rango válido" in response.message
        assert len(response.recommended_texts) > 0
    
    def test_invalid_grade_above_range(self):
        """Test handling of grade level above valid range."""
        request = EvaluationInputRequest(
            student_id="student_011",
            grade_level=8,
            preferences=[]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "básico"
        assert "fuera del rango válido" in response.message
        assert len(response.recommended_texts) > 0
    
    def test_unknown_preference(self):
        """Test handling of unknown preferences."""
        request = EvaluationInputRequest(
            student_id="student_012",
            grade_level=4,
            preferences=["deportes", "música"]  # Unknown preferences
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert response.initial_level == "intermedio"
        assert len(response.recommended_texts) > 0
        # Should fall back to default texts for the level
    
    def test_recommended_texts_no_duplicates(self):
        """Test that recommended texts don't contain duplicates."""
        request = EvaluationInputRequest(
            student_id="student_013",
            grade_level=3,
            preferences=["animales", "animales"]  # Duplicate preference
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        # Check for duplicates
        assert len(response.recommended_texts) == len(set(response.recommended_texts))
    
    def test_maximum_recommended_texts_limit(self):
        """Test that maximum 4 texts are recommended."""
        request = EvaluationInputRequest(
            student_id="student_014",
            grade_level=5,
            preferences=["animales", "aventuras", "ciencia"]
        )
        
        response = EvaluationInputService.evaluate_student(request)
        
        assert len(response.recommended_texts) <= 4


class TestEvaluationInputAPI:
    """Test cases for the evaluation input API endpoint."""
    
    def test_evaluation_input_endpoint_success(self):
        """Test successful API call to evaluation input endpoint."""
        response = client.post("/api/v1/evaluation-input/", json={
            "student_id": "api_test_001",
            "grade_level": 4,
            "preferences": ["aventuras", "ciencia"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["student_id"] == "api_test_001"
        assert data["initial_level"] == "intermedio"
        assert len(data["recommended_texts"]) > 0
        assert "message" in data
    
    def test_evaluation_input_endpoint_basic_level(self):
        """Test API endpoint returns basic level for grade 2."""
        response = client.post("/api/v1/evaluation-input/", json={
            "student_id": "api_test_002",
            "grade_level": 2,
            "preferences": ["animales"]
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["initial_level"] == "básico"
        assert "animales" in data["message"]
    
    def test_evaluation_input_endpoint_advanced_level(self):
        """Test API endpoint returns advanced level for grade 6."""
        response = client.post("/api/v1/evaluation-input/", json={
            "student_id": "api_test_003",
            "grade_level": 6,
            "preferences": []
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["initial_level"] == "avanzado"
    
    def test_evaluation_input_endpoint_validation_error(self):
        """Test API endpoint handles validation errors."""
        response = client.post("/api/v1/evaluation-input/", json={
            "student_id": "api_test_004",
            # Missing required grade_level
            "preferences": []
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_evaluation_input_endpoint_invalid_grade(self):
        """Test API endpoint handles invalid grade levels."""
        response = client.post("/api/v1/evaluation-input/", json={
            "student_id": "api_test_005",
            "grade_level": 10,  # Invalid grade
            "preferences": []
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["initial_level"] == "básico"  # Fallback level
        assert "fuera del rango válido" in data["message"]
