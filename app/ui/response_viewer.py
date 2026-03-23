import customtkinter as ctk
import json


class ResponseViewer(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self._build()

    def _build(self):
        self.status_label = ctk.CTkLabel(self, text="Status: -")
        self.status_label.pack(anchor="w", padx=5, pady=2)

        self.meta_label = ctk.CTkLabel(self, text="")
        self.meta_label.pack(anchor="w", padx=5, pady=2)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.pack(fill="both", expand=True, padx=5, pady=5)

    def set_response(self, response):
        self.textbox.delete("1.0", "end")

        if 200 <= response.status_code < 300:
            color = "green"
        elif 400 <= response.status_code < 500:
            color = "orange"
        else:
            color = "red"

        self.status_label.configure(
            text=f"Status: {response.status_code}",
            text_color=color
        )

        self.meta_label.configure(
            text=f"Time: {response.response_time} ms | Size: {response.size} bytes"
        )

        try:
            pretty = json.dumps(response.body, indent=2)
        except Exception:
            pretty = str(response.body)

        self.textbox.insert("1.0", pretty)
        self.textbox.see("1.0")
