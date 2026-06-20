from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/")

    @task(3)
    def upload_file(self):
        with open("test_data.csv", "rb") as file:
            self.client.post("/", files={"file": file})

    @task(2)
    def activity_percentage(self):
        self.client.post("/activity_percentage", data={"user": "username", "activity": "typing"})

    @task(4)
    def get_heatmap(self):
        self.client.get("/get_heatmap")

    @task(1)
    def download_image(self):
        self.client.get("/download_image/activity_heatmap.png")
