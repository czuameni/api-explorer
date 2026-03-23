import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, history_manager, on_select_request):
        super().__init__(parent, width=250)

        self.history_manager = history_manager
        self.on_select_request = on_select_request

        self.pack_propagate(False)

        self._build()
        self.refresh()

    def _build(self):
        title = ctk.CTkLabel(self, text="History", font=("Arial", 16))
        title.pack(pady=10)

        self.container = ctk.CTkScrollableFrame(self)
        self.container.pack(fill="both", expand=True)

    def refresh(self):
        # wyczyść
        for widget in self.container.winfo_children():
            widget.destroy()

        # dodaj elementy
        for req in self.history_manager.get_all():
            text = f"{req.method} {req.url}"

            btn = ctk.CTkButton(
                self.container,
                text=text,
                anchor="w",
                command=lambda r=req: self.on_select_request(r)
            )
            btn.pack(fill="x", padx=5, pady=2)