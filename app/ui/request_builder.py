import customtkinter as ctk
import json

from app.models.request_model import RequestModel
from app.core.request_engine import RequestEngine


class RequestBuilder(ctk.CTkFrame):

    def __init__(self, parent, response_viewer, env_manager, sidebar, history_manager):
        super().__init__(parent)

        self.response_viewer = response_viewer
        self.env_manager = env_manager
        self.sidebar = sidebar
        self.history_manager = history_manager
        self.headers = []

        self._build()

    def _build(self):
        # =========================
        # TOP BAR
        # =========================
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=5, pady=5)

        self.method = ctk.CTkOptionMenu(
            top_frame,
            values=["GET", "POST", "PUT", "DELETE"]
        )
        self.method.pack(side="left", padx=5)

        self.method.set("GET")

        self.url_entry = ctk.CTkEntry(
            top_frame,
            placeholder_text="Enter API URL..."
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.send_button = ctk.CTkButton(
            top_frame,
            text="Send",
            command=self.send_request
        )
        self.send_button.pack(side="left", padx=5)

        # =========================
        # ENV SECTION
        # =========================
        env_frame = ctk.CTkFrame(self)
        env_frame.pack(fill="x", padx=5, pady=5)

        self.env_key = ctk.CTkEntry(env_frame, placeholder_text="env key (np. base_url)")
        self.env_key.pack(side="left", padx=5)

        self.env_value = ctk.CTkEntry(env_frame, placeholder_text="value")
        self.env_value.pack(side="left", padx=5)

        env_add_btn = ctk.CTkButton(
            env_frame,
            text="Add Env",
            command=self.add_env
        )
        env_add_btn.pack(side="left", padx=5)

        # =========================
        # TABS
        # =========================
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=5, pady=5)

        self.body_tab = self.tabs.add("Body")
        self.headers_tab = self.tabs.add("Headers")

        # BODY
        self.body_text = ctk.CTkTextbox(self.body_tab)
        self.body_text.pack(fill="both", expand=True, padx=5, pady=5)

        # HEADERS
        input_frame = ctk.CTkFrame(self.headers_tab)
        input_frame.pack(fill="x", padx=5, pady=5)

        self.header_key = ctk.CTkEntry(input_frame, placeholder_text="Key")
        self.header_key.pack(side="left", padx=5)

        self.header_value = ctk.CTkEntry(input_frame, placeholder_text="Value")
        self.header_value.pack(side="left", padx=5)

        add_button = ctk.CTkButton(
            input_frame,
            text="Add",
            command=self.add_header
        )
        add_button.pack(side="left", padx=5)

        self.headers_display = ctk.CTkTextbox(self.headers_tab)
        self.headers_display.pack(fill="both", expand=True, padx=5, pady=5)

    # =========================
    # ENV
    # =========================
    def add_env(self):
        key = self.env_key.get()
        value = self.env_value.get()

        if key and value:
            self.env_manager.set(key, value)
            print("ENV SET:", key, "=", value)

            self.env_key.delete(0, "end")
            self.env_value.delete(0, "end")

    # =========================
    # HEADERS
    # =========================
    def add_header(self):
        key = self.header_key.get()
        value = self.header_value.get()

        if key and value:
            self.headers.append((key, value))
            self.update_headers_display()

            self.header_key.delete(0, "end")
            self.header_value.delete(0, "end")

    def update_headers_display(self):
        self.headers_display.delete("1.0", "end")

        for k, v in self.headers:
            self.headers_display.insert("end", f"{k}: {v}\n")

    # =========================
    # SEND
    # =========================
    def send_request(self):
        raw_url = self.url_entry.get()
        method = self.method.get()

        if not raw_url:
            print("URL is empty!")
            return

        # ENV RESOLVE
        url = self.env_manager.resolve(raw_url)

        # BODY
        raw_body = self.body_text.get("1.0", "end").strip()

        parsed_body = None
        if raw_body:
            try:
                parsed_body = json.loads(raw_body)
            except json.JSONDecodeError:
                parsed_body = raw_body
       
        if method == "GET":
            parsed_body = None

        # HEADERS
        headers_dict = {k: v for k, v in self.headers}

        request = RequestModel(
            method=method,
            url=url,
            headers=headers_dict,
            body=parsed_body
        )

        response = RequestEngine.send(request)

        self.history_manager.add(request)
        self.sidebar.refresh()

        self.sidebar.refresh()

        self.response_viewer.set_response(response)

    def load_request(self, request):
        # METHOD
        if request.method in ["GET", "POST", "PUT", "DELETE"]:
            self.method.set(request.method)
        else:
            self.method.set("GET")

        # URL
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, request.url)

        # BODY
        self.body_text.delete("1.0", "end")

        if request.body is not None:
            try:
                pretty = json.dumps(request.body, indent=2)
                self.body_text.insert("1.0", pretty)
            except Exception:
                self.body_text.insert("1.0", str(request.body))

        # HEADERS
        self.headers = list(request.headers.items()) if request.headers else []
        self.update_headers_display()