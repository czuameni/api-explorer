from app.core.request_engine import RequestEngine
from app.models.request_model import RequestModel
from app.core.environment import EnvironmentManager
from app.core.history_manager import HistoryManager
from app.core.collection_manager import CollectionManager
from app.core.project_manager import ProjectManager
from app.models.project_model import ProjectModel


# =========================
# 1. ENVIRONMENT
# =========================
env = EnvironmentManager()
env.set("base_url", "https://jsonplaceholder.typicode.com")


# =========================
# 2. REQUEST
# =========================
req = RequestModel(
    method="GET",
    url="{{base_url}}/posts/1"
)

req.url = env.resolve(req.url)

print("Resolved URL:", req.url)


# =========================
# 3. SEND
# =========================
res = RequestEngine.send(req)


# =========================
# 4. HISTORY
# =========================
history = HistoryManager()
history.add(req)


# =========================
# 5. COLLECTIONS
# =========================
collections = CollectionManager()

if not collections.get_all():
    collections.create_collection("Test API")

collections.add_request("Test API", req)


# =========================
# 6. BUILD PROJECT
# =========================
project = ProjectModel(
    collections=collections.get_all(),
    history=history.get_all(),
    environments=env.to_dict()
)


# =========================
# 7. SAVE PROJECT
# =========================
ProjectManager.save(project, "data/project.json")


# =========================
# 8. LOAD PROJECT
# =========================
loaded_project = ProjectManager.load("data/project.json")


# =========================
# 9. OUTPUT
# =========================
print("\n--- RESPONSE ---")
print("Status:", res.status_code)
print("Time:", res.response_time, "ms")

print("\n--- PROJECT ---")
print("Collections:", len(loaded_project.collections))
print("History:", len(loaded_project.history))
print("Env vars:", loaded_project.environments)