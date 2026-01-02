import requests
import json

# Test data
test_data = {
    "age": 22,
    "gpa": 3.5,
    "study_hours": 25,
    "social_media": 3,
    "sleep": 7,
    "exercise": 5,
    "family_support": 4,
    "financial_stress": 2,
    "peer_pressure": 3,
    "relationship_stress": 2,
    "counseling": "No",
    "diet_quality": 4,
    "cognitive_distortions": 2,
    "family_mental_history": "No",
    "medical_condition": "No",
    "substance_use": 1,
    "gender": "Female",
    "current_mechanisms": ["Exercise", "Reading"]
}

def test_local():
    """Test the application running on localhost"""
    url = "http://localhost:5000/predict"
    
    try:
        response = requests.post(url, json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            print("SUCCESS: Prediction received")
            print(f"Predicted Stress Level: {result['prediction']}")
            print(f"Probabilities: {result['probabilities']}")
            print(f"Number of Recommendations: {len(result['recommendations'])}")
            
            if result['recommendations']:
                print("\nTop Recommendations:")
                for i, rec in enumerate(result['recommendations'][:3], 1):
                    print(f"{i}. {rec['mechanism']} (Success rate: {rec['success_rate']:.2%})")
            
            return True
        else:
            print(f"ERROR: Status code {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to server. Make sure Flask app is running.")
        print("Start the app with: python app.py")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def test_health():
    """Test the health endpoint"""
    url = "http://localhost:5000/health"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Health check: OK")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except:
        print("Health check: Could not connect")
        return False

if __name__ == "__main__":
    print("Testing Mental Stress Assessment Application")
    print("=" * 50)
    
    print("\n1. Testing health endpoint...")
    health_ok = test_health()
    
    print("\n2. Testing prediction endpoint...")
    predict_ok = test_local()
    
    print("\n" + "=" * 50)
    if health_ok and predict_ok:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the output above.")
