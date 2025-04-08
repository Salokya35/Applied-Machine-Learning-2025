import os
import time
import subprocess
import requests
import pytest

def test_docker():
    """Test if the Docker container builds and runs correctly."""
    # Build the Docker image
    print("Building Docker image...")
    build_process = subprocess.run(
        ['docker', 'build', '-t', 'flask-app', '.'],
        check=True,
        capture_output=True
    )
    
    # Run the Docker container
    print("Running Docker container...")
    container_process = subprocess.Popen(
        ['docker', 'run', '-d', '-p', '5000:5000', '--name', 'flask-app-test', 'flask-app'],
        stdout=subprocess.PIPE
    )
    container_id = container_process.stdout.read().decode('utf-8').strip()
    
    try:
        # Wait for the container to start up
        print("Waiting for container to start...")
        time.sleep(5)
        
        # Check if the container is running
        ps_process = subprocess.run(
            ['docker', 'ps', '--filter', f'id={container_id}', '--format', '{{.Status}}'],
            capture_output=True, text=True
        )
        
        if not ps_process.stdout.strip():
            # If container isn't running, check logs
            logs_process = subprocess.run(
                ['docker', 'logs', container_id],
                capture_output=True, text=True
            )
            print(f"Container failed to start. Logs:\n{logs_process.stdout}")
            pytest.fail("Docker container failed to start")
        
        # Test the API endpoint
        print("Testing API endpoint...")
        try:
            # Test the home page
            home_response = requests.get('http://localhost:5000/')
            assert home_response.status_code == 200, "Home page is not accessible"
            
            # Test the predict endpoint
            predict_response = requests.post(
                'http://localhost:5000/predict',
                json={"text": "This is a sample text for testing"},
                timeout=5
            )
            
            # Check if the response is as expected
            assert predict_response.status_code == 200, "Predict endpoint returned non-200 status"
            result = predict_response.json()
            assert "prediction" in result, "Response doesn't contain prediction"
            assert "propensity" in result, "Response doesn't contain propensity"
            assert isinstance(result["propensity"], (int, float)), "Propensity is not a number"
            
            print("All tests passed successfully!")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the Flask app: {e}")
            
    finally:
        # Stop and remove the container
        print("Cleaning up container...")
        subprocess.run(['docker', 'stop', container_id], check=False)
        subprocess.run(['docker', 'rm', container_id], check=False)

if __name__ == "__main__":
    test_docker()
