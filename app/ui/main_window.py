import customtkinter as ctk

from app.ui.sidebar import Sidebar
from app.ui.request_builder import RequestBuilder
from app.ui.response_viewer import ResponseViewer
from app.core.environment import EnvironmentManager
from app.core.history_manager import HistoryManager


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.iconbitmap("api.ico")

        self.title("API Explorer")
        self.geometry("1200x700")

        self.env_manager = EnvironmentManager()

        self.history_manager = HistoryManager()

        self._setup_layout()

    def _setup_layout(self):
    
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            history_manager=self.history_manager,
            on_select_request=self.load_request_to_builder
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew")

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.response_viewer = ResponseViewer(self.main_frame)
        self.response_viewer.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.request_builder = RequestBuilder(
            self.main_frame,
            response_viewer=self.response_viewer,
            env_manager=self.env_manager,
            sidebar=self.sidebar,
            history_manager=self.history_manager
        )
        self.request_builder.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    def load_request_to_builder(self, request):
        self.request_builder.load_request(request)