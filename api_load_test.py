from locust import HttpUser, task, between


class APILoadTest(HttpUser):
    wait_time = between(1, 2)  # Time between tasks
    host = "http://localhost:8000"  # Replace with your API's base host URL

    @task
    def transfer_credits(self):
        self.client.post(f'/transfer_credits/1/', {'phone_number': '987654321', 'amount': 10.00})



#locust -f api_load_test.py --headless -u 2 -r 1 --host=http://localhost:8000
#locust -f api_load_test.py --headless -u 40 -r 5 --host=http://localhost:8000
